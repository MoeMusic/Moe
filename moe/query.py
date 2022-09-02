"""Provides a positional commandline argument for querying the database.

Plugins wishing to use the query argument should define query as a parent parser
when using the add_command() hook.

Example:
    Inside your `add_command` hook implemention::

        my_parser = cmd_parser.add_parser("my_plugin", parents=[query.query_parser])

Then, in your argument parsing function, call `query.query(args.query)`
to get a list of Tracks matching the query from the library.
"""

import logging
import re
import shlex
from pathlib import Path
from typing import Any, Dict, List

import sqlalchemy as sa
import sqlalchemy.orm
import sqlalchemy.sql.elements

from moe.config import MoeSession
from moe.library.album import Album
from moe.library.extra import Extra
from moe.library.lib_item import LibItem
from moe.library.track import Track

__all__: List[str] = ["QueryError", "query"]

log = logging.getLogger("moe.query")


class QueryError(Exception):
    """Error querying an item from the library."""


HELP_STR = r"""
The query must be in the format 'field:value' where field is a track's field to
match and value is that field's value. Internally, this 'field:value' pair is referred
to as a single term. The match is case-insensitive.

Album queries, specified with the `-a, --album` option, will return albums that contain
any tracks matching the given query. Similarly, extra queries, specified with the
`-e, --extra` option, will return extras that are attached to albums that contain any
tracks matching the given query.

If you would like to specify a value with whitespace or multiple words, enclose the
term in quotes.

SQL LIKE query syntax is used for normal queries, which means
the '_'  and '%' characters have special meaning:
% - The percent sign represents zero, one, or multiple characters.
_ - The underscore represents a single character.

To match these special characters as normal, use '/' as an escape character.

The value can also be a regular expression. To enforce this, use two colons
e.g. 'field::value.*'

As a shortcut to matching all entries, use '*' as the term.

Finally, you can also specify any number of terms.
For example, to match all Wu-Tang Clan tracks that start with the letter 'A', use:
'"artist:wu-tang clan" title:a%'

Note that when using multiple terms, they are joined together using AND logic, meaning
all terms must be true to return a match.

For more information on queries, see the docs.
https://mrmoe.readthedocs.io/en/latest/query.html
"""

# each query will be split into these groups
FIELD_GROUP = "field"
SEPARATOR_GROUP = "separator"
VALUE_GROUP = "value"


def query(query_str: str, query_type: str = "track") -> List[LibItem]:
    """Queries the database for the given query string.

    Args:
        query_str: Query string to parse. See HELP_STR for more info.
        query_type: Type of query. Should be one of "album", "extra", or "track"

    Returns:
        All tracks matching the query.
    """
    terms = shlex.split(query_str)
    if not terms:
        log.error(f"No query given.\n{HELP_STR}")
        return []

    try:
        items = _create_query(terms, query_type).all()
    except QueryError as exc:
        log.error(exc)
        return []

    if not items:
        log.warning(f"No items found for the query '{query_str}'.")

    items_str = "".join(f"\n    {str(item)}" for item in items)
    log.debug(f"Query '{query_str}' returned: {items_str}")
    return items


def _create_query(terms: List[str], query_type: str) -> sqlalchemy.orm.query.Query:
    """Creates a query statement.

    Args:
        terms: Query terms to parse.
        query_type: Type of query. Should be one of "album", "extra", or "track"

    Returns:
        Sqlalchemy query statement.

    Raises:
        QueryError: Invalid query terms or type.
    """
    session = MoeSession()

    if query_type == "track":
        library_query = session.query(Track).join(Album, Extra, isouter=True)
    elif query_type == "album":
        library_query = session.query(Album).join(Track, Extra, isouter=True)
    elif query_type == "extra":
        library_query = session.query(Extra).join(Album, Track, isouter=True)
    else:
        raise QueryError(f"Invalid query type: {query_type}")

    for term in terms:
        library_query = library_query.filter(_create_expression(_parse_term(term)))

    return library_query


def _parse_term(term: str) -> Dict[str, str]:
    """Parse the given database query term.

    A term is a single field:value declaration.

    Args:
        term: Query term to parse.

    Returns:
        A dictionary containing each named group and its value.
        The named groups are field, separator, and value.

    Example:
        >>> parse_term('artist:name')
        {"field": "artist", "separator": ":", "value": "name"}

    Note:
        The fields are meant to be programatically accessed with the respective
        group constant e.g. `expression[FIELD_GROUP] == "artist"`

    Raises:
        QueryError: Invalid query term.
    """
    # '*' is used as a shortcut to return all entries.
    # We use track_num as all tracks are guaranteed to have a track number.
    # '%' is an SQL LIKE query special character.
    if term == "*":
        return {FIELD_GROUP: "_id", SEPARATOR_GROUP: ":", VALUE_GROUP: "%"}

    query_re = re.compile(
        rf"""
        (?P<{FIELD_GROUP}>\S+?)
        (?P<{SEPARATOR_GROUP}>::?)
        (?P<{VALUE_GROUP}>\S.*)
        """,
        re.VERBOSE,
    )

    match = re.match(query_re, term)
    if not match:
        raise QueryError(f"Invalid query term: {term}\n{HELP_STR}")

    match_dict = match.groupdict()
    match_dict[FIELD_GROUP] = match_dict[FIELD_GROUP].lower()

    return match_dict


def _create_expression(term: Dict[str, str]) -> sqlalchemy.sql.elements.ClauseElement:
    """Maps a user-given query term to a filter expression for the database query.

    Args:
        term: A parsed query term defined by `_parse_term()`.

    Returns:
        A filter for the database query.

        A "filter" is anything accepted by a sqlalchemy `Query.filter()`.
        https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.filter

    Raises:
        QueryError: Invalid query given.
    """
    field = term[FIELD_GROUP].lower()
    separator = term[SEPARATOR_GROUP]
    value = term[VALUE_GROUP]

    attr = _get_item_attr(field)

    if separator == ":":
        # path matching
        if str(attr) == "Track.path":
            return Track.path == Path(value)  # type: ignore
        elif str(attr) == "Extra.path":
            return Extra.path == Path(value)  # type: ignore
        elif str(attr) == "Album.path":
            return Album.path == Path(value)  # type: ignore

        # normal string match query - should be case insensitive
        return attr.ilike(value, escape="/")

    elif separator == "::":
        # Regular expression query.
        # Note, this is a custom sqlite function created in config.py
        try:
            re.compile(value)
        except re.error as re_err:
            raise QueryError(f"Invalid regular expression: {value}") from re_err

        return attr.op("regexp")(sa.sql.expression.literal(value))

    raise QueryError(f"Invalid query type: {separator}")


def _get_item_attr(query_field: str) -> Any:
    """Gets the matching attribute for a given query field.

    Args:
        query_field: Library item field to query.

    Returns:
        Matching library item attribute for the given query field.

    Raises:
        QueryError: Invalid query field.
    """
    attr: Any
    if query_field == "extra_path":
        attr = Extra.path
    elif query_field == "album_path":
        attr = Album.path
    elif query_field == "genre":
        attr = Track.genres
    else:
        # match track query_fields (all album fields should also be exposed)
        try:
            attr = getattr(Track, query_field)
        except AttributeError as track_err:
            raise QueryError(f"Invalid Track query_field: {query_field}") from track_err

    return attr
