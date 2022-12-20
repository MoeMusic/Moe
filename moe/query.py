"""Provides functionality to query the library for albums, extras, and tracks."""

import logging
import re
import shlex
from pathlib import Path
from typing import Type

import sqlalchemy as sa
import sqlalchemy.orm
import sqlalchemy.sql.elements
from sqlalchemy.orm.session import Session

from moe.library import Album, Extra, LibItem, Track
from moe.library.lib_item import SetType

__all__: list[str] = ["QueryError", "query"]

log = logging.getLogger("moe.query")


class QueryError(Exception):
    """Error querying an item from the library."""


# each query will be split into these groups
FIELD_TYPE = "field_type"
FIELD = "field"
SEPARATOR = "separator"
VALUE = "value"


def query(session: Session, query_str: str, query_type: str) -> list[LibItem]:
    """Queries the database for items matching the given query string.

    Args:
        session: Library db session.
        query_str: Query string to parse. See the query docs for more info.
        query_type: Type of library item to return: either 'album', 'extra', or 'track'.

    Returns:
        All items matching the query of type ``query_type``.

    Raises:
        QueryError: Invalid query.

    See Also:
        `The query docs <https://mrmoe.readthedocs.io/en/latest/query.html>`_
    """
    log.debug(f"Querying library for items. [{query_str=!r}, {query_type=!r}]")

    terms = shlex.split(query_str)
    if not terms:
        raise QueryError("No query given.")

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
        raise QueryError(f"Invalid query term. [{term=!r}]")

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
        if match := re.fullmatch(r"(?P<low>\d*)..(?P<high>\d*)", value):
            if match["low"] and match["high"]:
                return sa.and_(attr >= match["low"], attr <= match["high"])
            if match["low"]:
                return attr >= match["low"]
            if match["high"]:
                return attr <= match["high"]

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
    # convert singular multi-value fields to their plural equivalents
    if field == "catalog_num" and field_type == "album":
        field = "catalog_nums"
    elif field == "genre" and field_type == "track":
        field = "genres"

    if field_type == "album":
        return _getattr(Album, field)
    elif field_type == "extra":
        return _getattr(Extra, field)
    else:
        return _getattr(Track, field)


def _getattr(item_class: Type[LibItem], field: str):
    """Get an attribute for the given class type."""
    try:
        attr = getattr(item_class, field)
    except AttributeError:
        # assume custom field
        custom_func = sa.func.json_each(item_class.custom, f"$.{field}").table_valued(
            "value", joins_implicitly=True
        )

        return custom_func.c.value

    try:
        column_type = attr.property.columns[0].type
    except AttributeError:
        # hybrid_property
        pass
    else:
        if isinstance(column_type, SetType):
            multi_func = sa.func.json_each(
                getattr(item_class, field), "$"
            ).table_valued("value", joins_implicitly=True)
            return multi_func.c.value

    return attr
