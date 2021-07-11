"""Provides a positional commandline argument for querying the database.

Plugins wishing to use the query argument should define query as a parent parser
when using the add_command() hook.

Example:
    Inside your `add_command` hook implemention::

        my_parser = cmd_parser.add_parser("my_plugin", parents=[query.query_parser])

Then, in your argument parsing function, call `query.query(args.query)`
to get a list of Tracks matching the query from the library.
"""

import argparse
import logging
import re
import shlex
from pathlib import Path
from typing import Any, Dict, List

import sqlalchemy
from sqlalchemy.ext.associationproxy import ColumnAssociationProxyInstance
from sqlalchemy.orm.attributes import InstrumentedAttribute

from moe.core.library.album import Album
from moe.core.library.extra import Extra
from moe.core.library.lib_item import LibItem
from moe.core.library.track import Track

__all__: List[str] = ["QueryError", "query", "query_parser"]

log = logging.getLogger("moe.query")


class QueryError(Exception):
    """Error querying an item from the library."""


# Argument parser for a query. This should be passed as a parent parser for a command.
query_parser = argparse.ArgumentParser(
    add_help=False, formatter_class=argparse.RawTextHelpFormatter
)
query_parser.add_argument("query", help="query the library for matching tracks")

query_type_group = query_parser.add_mutually_exclusive_group()
query_type_group.add_argument(
    "-a", "--album", action="store_true", help="query for matching albums"
)
query_type_group.add_argument(
    "-e", "--extra", action="store_true", help="query for matching extras"
)


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
"""  # noqa: WPS360

# each query will be split into these groups
FIELD_GROUP = "field"
SEPARATOR_GROUP = "separator"
VALUE_GROUP = "value"


def query(
    query_str: str, session: sqlalchemy.orm.session.Session, query_type: str = "track"
) -> List[LibItem]:
    """Queries the database for the given query string.

    Args:
        query_str: Query string to parse. See HELP_STR for more info.
        session: Current db session.
        query_type: Type of query. Should be one of "album", "extra", or "track"

    Returns:
        All tracks matching the query.
    """
    terms = shlex.split(query_str)

    if not terms:
        log.error(f"No query given.\n{HELP_STR}")
        return []

    try:
        items = _create_query(session, terms, query_type).all()
    except QueryError as exc:
        log.error(exc)
        return []

    if not items:
        log.warning(f"No items found for the query '{query_str}'.")

    items_str = "".join(f"\n    {str(item)}" for item in items)
    log.debug(f"Query '{query_str}' returned: {items_str}")
    return items


def _create_query(
    session: sqlalchemy.orm.session.Session, terms: List[str], query_type: str
) -> sqlalchemy.orm.query.Query:
    """Creates a query statement.

    Args:
        session: Current db session.
        terms: Query terms to parse.
        query_type: Type of query. Should be one of "album", "extra", or "track"

    Returns:
        Sqlalchemy query statement.

    Raises:
        QueryError: Invalid query terms or type.
    """
    if query_type == "track":
        library_query = session.query(Track).join(Album)
    elif query_type == "album":
        library_query = session.query(Album).join(Track)
    elif query_type == "extra":
        library_query = session.query(Extra).join(Album).join(Track)
    else:
        raise QueryError(f"Invalid query type: {query_type}")

    # only join Extras if the table is not empty
    if session.query(Extra).all() and query_type in {"album", "track"}:
        library_query = library_query.join(Extra)

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
        return {FIELD_GROUP: "track_num", SEPARATOR_GROUP: ":", VALUE_GROUP: "%"}

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

    attr: Any
    if field == "extra_path":
        attr = Extra.path
    elif field == "album_path":
        attr = Album.path
    elif field == "genre":
        attr = Track.genres
    else:
        # match track fields (all album fields should also be exposed by the Track)
        try:
            attr = getattr(Track, field)
        except AttributeError:
            raise QueryError(f"Invalid Track field: {field}")

    if separator == ":":
        # path matching
        if isinstance(attr, InstrumentedAttribute) and attr == Track.path:
            return Track.path == Path(value)
        elif (
            isinstance(attr, ColumnAssociationProxyInstance)
            and attr.attr[1] == Album.path
        ):
            return Album.path == Path(value)
        elif str(attr) == "Extra.path":
            return Extra.path == Path(value)  # type: ignore
        elif str(attr) == "Album.path":
            return Album.path == Path(value)  # type: ignore

        # normal string match query - should be case insensitive
        return attr.ilike(value, escape="/")  # type: ignore

    elif separator == "::":
        # Regular expression query.
        # Note, this is a custom sqlite function created in config.py
        try:
            re.compile(value)
        except re.error:
            raise QueryError(f"Invalid regular expression: {value}")

        return attr.op("regexp")(sqlalchemy.sql.expression.literal(value))

    raise QueryError(f"Invalid query type: {separator}")
