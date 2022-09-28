"""Provides functionality to query the library for albums, extras, and tracks."""

import logging
import re
import shlex
from pathlib import Path

import sqlalchemy as sa
import sqlalchemy.orm
import sqlalchemy.sql.elements

from moe.config import MoeSession
from moe.library import Album, Extra, LibItem, Track

__all__: list[str] = ["QueryError", "query"]

log = logging.getLogger("moe.query")


class QueryError(Exception):
    """Error querying an item from the library."""


HELP_STR = r"""
The query must be in the format 'field:value' where field is, by default, a track's
field to match and value is that field's value (case-insensitive). To match an album's
field or an extra's field, prepend the field with `a:` or `e:` respectively.
Internally, this 'field:value' pair is referred to as a single term.

By default, tracks will be returned by the query, but you can choose to return albums
by using the ``-a, --album`` option, or you can return extras using the ``-e, --extra``
option.

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
FIELD_TYPE = "field_type"
FIELD = "field"
SEPARATOR = "separator"
VALUE = "value"


def query(query_str: str, query_type: str) -> list[LibItem]:
    """Queries the database for items matching the given query string.

    Args:
        query_str: Query string to parse. See HELP_STR for more info.
        query_type: Type of library item to return: either 'album', 'extra', or 'track'.

    Returns:
        All items matching the query of type ``query_type``.

    Raises:
        QueryError: Invalid query.

    See Also:
        `The query docs <https://mrmoe.readthedocs.io/en/latest/query.html>`_
    """
    log.debug(f"Querying library for items. [{query_str=!r}, {query_type=!r}]")
    session = MoeSession()

    terms = shlex.split(query_str)
    if not terms:
        raise QueryError(f"No query given.\n{HELP_STR}")

    if query_type == "album":
        library_query = session.query(Album)
        if session.query(Track).first():
            library_query = library_query.join(Track)
    elif query_type == "extra":
        library_query = session.query(Extra).join(Album).join(Track)
    else:
        library_query = session.query(Track).join(Album)
    if query_type != "extra" and session.query(Extra).first():
        library_query = library_query.join(Extra)

    for term in terms:
        parsed_term = _parse_term(term)
        library_query = library_query.filter(
            _create_filter_expression(
                parsed_term[FIELD_TYPE],
                parsed_term[FIELD],
                parsed_term[SEPARATOR],
                parsed_term[VALUE],
            )
        )
    items = library_query.all()

    log.debug(f"Queried library for items. [{items=!r}]")
    return items


def _parse_term(term: str) -> dict[str, str]:
    """Parse the given database query term.

    A term is a single field:value declaration.

    Args:
        term: Query term to parse.

    Returns:
        A dictionary containing each named group and its value.
        The named groups are field_type, field, separator, and value.

    Example:
        >>> parse_term('a:artist:name')
        {"field_type": "album", "field": "artist", "separator": ":", "value": "name"}

    Note:
        * The fields are meant to be programatically accessed with the respective
        group constant e.g. `expression[FIELD] == "artist"`
        * All `field` values are automatically converted to lowercase.

    Raises:
        QueryError: Invalid query term.
    """
    # '*' is used as a shortcut to return all entries.
    # We use track_num as all tracks are guaranteed to have a track number.
    # '%' is an SQL LIKE query special character.
    if term == "*":
        return {FIELD_TYPE: "album", FIELD: "_id", SEPARATOR: ":", VALUE: "%"}

    query_re = re.compile(
        rf"""
        (?P<{FIELD_TYPE}>[aet]:)?
        (?P<{FIELD}>\S+?)
        (?P<{SEPARATOR}>::?)
        (?P<{VALUE}>.*)
        """,
        re.VERBOSE,
    )

    match = re.match(query_re, term)
    if not match:
        raise QueryError(f"Invalid query term. [{term=!r}]\n{HELP_STR}")

    match_dict = match.groupdict()
    match_dict[FIELD] = match_dict[FIELD].lower()
    if match_dict[FIELD_TYPE] == "a:":
        match_dict[FIELD_TYPE] = "album"
    elif match_dict[FIELD_TYPE] == "e:":
        match_dict[FIELD_TYPE] = "extra"
    else:
        match_dict[FIELD_TYPE] = "track"

    return match_dict


def _create_filter_expression(field_type: str, field: str, separator: str, value: str):
    """Maps a user-given query term to a filter expression for the database query.

    Args:
        field_type: LibItem type of ``field``.
        field: The field to query for.
        separator: Indicates the type of query.
        value: Value of ``field`` to match.

    Returns:
        A filter for the database query.

        A "filter" is anything accepted by a sqlalchemy `Query.filter()`.
        https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.filter

    Raises:
        QueryError: Invalid query given.
    """
    attr = _get_field_attr(field, field_type)

    if separator == ":":
        if str(attr).endswith(".path"):
            return attr == Path(value)

        # normal string match query - should be case insensitive
        return attr.ilike(value, escape="/")

    elif separator == "::":
        try:
            re.compile(value)
        except re.error as re_err:
            raise QueryError(
                f"Invalid regular expression. [regex={value!r}]"
            ) from re_err

        return attr.op("regexp")(sa.sql.expression.literal(value))

    raise QueryError(f"Invalid query type separator. [{separator=!r}]")


def _get_field_attr(field: str, field_type: str):
    """Gets the corresponding attribute for the given field to use in a query filter."""
    if field == "genre":
        field = "genres"

    if field_type == "album":
        try:
            return getattr(Album, field)
        except AttributeError:
            # assume custom field
            custom_func = sa.func.json_each(
                Album._custom_fields, f"$.{field}"
            ).table_valued("value", joins_implicitly=True)
            return custom_func.c.value
    elif field_type == "extra":
        try:
            return getattr(Extra, field)
        except AttributeError:
            # assume custom field
            custom_func = sa.func.json_each(
                Extra._custom_fields, f"$.{field}"
            ).table_valued("value", joins_implicitly=True)
            return custom_func.c.value
    else:
        try:
            return getattr(Track, field)
        except AttributeError:
            # assume custom field
            custom_func = sa.func.json_each(
                Track._custom_fields, f"$.{field}"
            ).table_valued("value", joins_implicitly=True)
            return custom_func.c.value
