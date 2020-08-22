"""Provides a positional commandline argument for querying the database.

Plugins wishing to use the query argument should define query as a parent parser
when using the addcommand() hook.

Example:
    Inside of your `addcommand` hook implemention::

        my_parser = cmd_parser.add_parser("my_plugin", parents=[query.query_parser])

Then, in your argument parsing function, call `query.query(args.query)`
to get a list of Tracks matching the query from the library.
"""

import argparse
import logging
import re
from typing import Dict, List

import sqlalchemy

from moe.core import library

log = logging.getLogger(__name__)

query_parser = argparse.ArgumentParser(
    add_help=False, formatter_class=argparse.RawTextHelpFormatter,
)
query_parser.add_argument("query", help="query the library")


HELP_STR = r"""
The query must be in the format 'field:value' where field is a track's field to
match and value is that field's value. The match is case-insensitive.

The value can also be a regular expression. To enforce this, use two colons
e.g. 'field::value.*'

If you need to use the ':' character in a value, that would otherwise look like another
field:value reference, you can escape it with '\'.
e.g. 'album:Vol 1: Wow' is fine, but 'album: Vol 1\:Wow' needs the escape character.

Finally, you can specify any number of field/value pairs.
For example, to match all Wu-Tang Clan tracks that start with the letter 'A', use:
'artist:wu-tang clan title::A.*'

Note that multiple field:value expressions are joined together using AND logic.
"""

# each query will be split into these groups
FIELD_GROUP = "field"
SEPARATOR_GROUP = "separator"
VALUE_GROUP = "value"


def _parse_query(query_str: str) -> List[Dict[str, str]]:
    """Parse the given database query string.

    Args:
        query_str: Query string to parse.

    Returns:
        A list of dictionaries containing each named group and its value.
        The named groups are field, separator, and value.

        Each dictionary can be referred to as an "expression".
        E.g. for the query `artist:name title:my_title`, `artist:name` and
        `title:my_title` are two distinct expressions.

    Example:
        >>> parse_query('artist:name')
        [{"field": "artist", "separator": ":", "value": "name"}]

    Note:
        The fields are meant to be programatically accessed with the respective
        group constant e.g. `expression[FIELD_GROUP] == "artist"`
    """
    query_re = re.compile(
        rf"""
        (?P<{FIELD_GROUP}>\S+?)
        (?P<{SEPARATOR_GROUP}>::?)
        (?P<{VALUE_GROUP}>\S.*?)
        (?=\s\S+(?<!\\):\S|$)  # don't match next field if it exists
        """,
        re.VERBOSE,
    )

    matches = re.finditer(query_re, query_str)

    match_dicts = []
    for match in matches:
        match_dict = match.groupdict()
        match_dict[FIELD_GROUP] = match_dict[FIELD_GROUP].lower()
        match_dict[VALUE_GROUP] = match_dict[VALUE_GROUP].replace(r"\:", ":")

        match_dicts.append(match_dict)

    return match_dicts


def _create_filter(
    expression: Dict[str, str]
) -> sqlalchemy.sql.elements.BinaryExpression:
    """Maps a user-given query expression to a filter for the database query.

    Args:
        expression: A single query expression defined by `_parse_query()`.

    Returns:
        A list of the filters to filter the database query against.

        A "filter" is anything accepted by a sqlalchemy `Query.filter()`.
        https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.filter

    Raises:
        ValueError: Invalid query value given.
    """
    field = sqlalchemy.func.lower(getattr(library.Track, expression[FIELD_GROUP]))

    if expression[SEPARATOR_GROUP] == "::":
        # Regular expression
        # Note, this is a custom sqlite function created in config.py
        value = expression[VALUE_GROUP]

        try:
            re.compile(value)
        except re.error:
            log.error(f"'{value}' is not a valid regular expression.")
            raise ValueError

        return field.op("regexp")(value)

    # Normal expression
    value = sqlalchemy.func.lower(expression[VALUE_GROUP])
    return field == value


def query(
    query_str: str, session: sqlalchemy.orm.session.Session,
) -> List[library.Track]:
    """Queries the database for the given query string.

    Args:
        query_str: Query string to parse. See HELP_STR for more info.
        session: current db session

    Returns:
        All tracks matching the query.
    """
    expressions = _parse_query(query_str)

    if not expressions:
        log.error(f"Invalid query '{query_str}'\n{HELP_STR}")
        return []

    query_filters = []
    for expression in expressions:
        try:
            query_filter = _create_filter(expression)
        except ValueError:
            return []

        query_filters.append(query_filter)

    tracks = session.query(library.Track).filter(*query_filters).all()

    if not tracks:
        log.warning(f"No tracks found for the query '{query_str}'.")

    return tracks
