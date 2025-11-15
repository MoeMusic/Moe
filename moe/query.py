"""Provides functionality to query the library for albums, extras, and tracks."""

from __future__ import annotations

import logging
import re
import shlex
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING

import sqlalchemy as sa

from moe.library import Album, Extra, LibItem, Track
from moe.library.lib_item import SetType

if TYPE_CHECKING:
    from sqlalchemy.orm import InstrumentedAttribute
    from sqlalchemy.orm.session import Session
    from sqlalchemy.sql.elements import KeyedColumnElement

__all__: list[str] = ["QueryError", "QueryType", "query"]

log = logging.getLogger("moe.query")


class QueryError(Exception):
    """Error querying an item from the library."""


class QueryType(str, Enum):
    """The type of library item to query for."""

    ALBUM = "album"
    EXTRA = "extra"
    TRACK = "track"


# each query will be split into these groups
FIELD_TYPE = "field_type"
FIELD = "field"
SEPARATOR = "separator"
VALUE = "value"


def query(
    session: Session, query_str: str, query_type: QueryType
) -> list[Album] | list[Extra] | list[Track]:
    """Queries the database for items matching the given query string.

    Args:
        session: Library db session.
        query_str: Query string to parse. See the query docs for more info.
        query_type: Type of library item to return.

    Returns:
        All items matching the query of type ``query_type``.

    Raises:
        QueryError: Invalid query.

    See Also:
        `The query docs <https://mrmoe.readthedocs.io/en/latest/query.html>`_
    """
    log.debug(f"Querying library for items. [{query_str=}, {query_type=}]")

    terms = shlex.split(query_str)
    if not terms:
        err_msg = "No query given."
        raise QueryError(err_msg)

    if query_type == QueryType.ALBUM:
        library_query = session.query(Album)
        if session.query(Track).first():
            library_query = library_query.join(Track)
    elif query_type == QueryType.EXTRA:
        library_query = session.query(Extra).join(Album).join(Track)
    else:
        library_query = session.query(Track).join(Album)
    if query_type != QueryType.EXTRA and session.query(Extra).first():
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

    log.debug(f"Queried library for items. [{items=}]")
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
        err_msg = f"Invalid query term. [{term=}]"
        raise QueryError(err_msg)

    match_dict = match.groupdict()
    match_dict[FIELD] = match_dict[FIELD].lower()
    if match_dict[FIELD_TYPE] == "a:":
        match_dict[FIELD_TYPE] = "album"
    elif match_dict[FIELD_TYPE] == "e:":
        match_dict[FIELD_TYPE] = "extra"
    else:
        match_dict[FIELD_TYPE] = "track"

    return match_dict


def _create_filter_expression(
    field_type: str, field: str, separator: str, value: str
) -> sa.sql.expression.ColumnExpressionArgument[bool]:
    """Maps a user-given query term to a filter expression for the database query.

    Args:
        field_type: LibItem type of ``field``.
        field: The field to query for.
        separator: Indicates the type of query.
        value: Value of ``field`` to match.

    Returns:
        A filter for the database query.

        A "filter" is anything accepted by a sqlalchemy `Query.filter()`.
        https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.filter

    Raises:
        QueryError: Invalid query given.
    """
    attr = _get_field_attr(field, field_type)

    if separator == ":":
        if num_range := re.fullmatch(r"(?P<min>\d*)..(?P<max>\d*)", value):
            if num_range["min"] and num_range["max"]:
                return sa.and_(attr >= num_range["min"], attr <= num_range["max"])
            if num_range["min"]:
                return attr >= num_range["min"]
            if num_range["max"]:
                return attr <= num_range["max"]

        if str(attr).endswith(".path"):
            return attr == Path(value)

        # normal string match query - should be case insensitive
        return attr.ilike(value, escape="/")
    if separator == "::":
        try:
            re.compile(value)
        except re.error as re_err:
            err_msg = f"Invalid regular expression. [regex={value!r}]"
            raise QueryError(err_msg) from re_err

        return attr.op("regexp")(sa.sql.expression.literal(value))

    err_msg = f"Invalid query type separator. [{separator=}]"
    raise QueryError(err_msg)


def _get_field_attr(
    field: str, field_type: str
) -> sa.sql.expression.ColumnClause | InstrumentedAttribute | KeyedColumnElement:
    """Gets the corresponding attribute for the given field to use in a query filter."""
    # convert singular multi-value fields to their plural equivalents
    if field == "catalog_num" and field_type == "album":
        field = "catalog_nums"
    elif field == "genre" and field_type == "track":
        field = "genres"

    if field_type == "album":
        return _getattr(Album, field)
    if field_type == "extra":
        return _getattr(Extra, field)
    return _getattr(Track, field)


def _getattr(
    item_class: type[LibItem], field: str
) -> sa.sql.expression.ColumnClause | InstrumentedAttribute | KeyedColumnElement:
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
