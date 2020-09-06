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
from typing import Dict, List, Type, Union

import sqlalchemy

from moe.core.library.album import Album
from moe.core.library.music_item import MusicItem
from moe.core.library.track import Track

log = logging.getLogger(__name__)

query_parser = argparse.ArgumentParser(
    add_help=False, formatter_class=argparse.RawTextHelpFormatter
)
query_parser.add_argument("query", help="query the library for matching tracks")
query_parser.add_argument(
    "-a", "--album", action="store_true", help="match albums instead of tracks"
)


HELP_STR = r"""
The query must be in the format 'field:value' where field is a track or album's field to
match and value is that field's value. The match is case-insensitive.

SQL LIKE query syntax is used for normal queries, which means
the '_'  and '%' characters have special meaning:
% - The percent sign represents zero, one, or multiple characters.
_ - The underscore represents a single character.

The value can also be a regular expression. To enforce this, use two colons
e.g. 'field::value.*'

Finally, you can specify any number of field/value pairs.
For example, to match all Wu-Tang Clan tracks that start with the letter 'A', use:
'artist:wu-tang clan title:a%'

There are a few special meaning characters that need to be escaped if you would like
to match them normally. These include '%', '_', and ':'. To escape any of these
characters, prepend it with a '\'. Note that ':' is only disallowed if it would
otherwise cause the query to look like another field:value pair.
e.g. 'album:Vol 1: Wow' is fine, but 'album: Vol 1\:Wow' needs the escape character.

Multiple field:value expressions are joined together using AND logic.

If doing an album query, you still specify track fields, but it will match albums
instead of tracks.

Tip: Normal queries may be faster when compared to regex queries. If you
are experiencing performance issues with regex queries, see if you can make an
equivalent normal query using the LIKE wildcard characters.
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
    expression: Dict[str, str], query_cls: Union[Type[Album], Type[Track]]
) -> sqlalchemy.sql.elements.BinaryExpression:
    """Maps a user-given query expression to a filter for the database query.

    Args:
        expression: A single query expression defined by `_parse_query()`.
        query_cls: Library class to query for. Should be either `Album`
            or `Track`

    Returns:
        A list of the filters to filter the database query against.

        A "filter" is anything accepted by a sqlalchemy `Query.filter()`.
        https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.filter

    Raises:
        ValueError: Invalid query given.
    """
    field = expression[FIELD_GROUP].lower()
    separator = expression[SEPARATOR_GROUP]
    value = expression[VALUE_GROUP]
    try:
        attr = getattr(Track, field)
    except AttributeError:
        log.error(f"Invalid Track field: {field}")
        raise ValueError

    if separator == ":":
        # Normal string match query - should be case insensitive.
        return attr.ilike(value)

    elif separator == "::":
        # Regular expression query.
        # Note, this is a custom sqlite function created in config.py
        try:
            re.compile(value)
        except re.error:
            log.error(f"Invalid regular expression: {value}")
            raise ValueError

        return attr.op("regexp")(value)

    log.error(f"Invalid query type: {separator}")
    raise ValueError


def query(
    query_str: str, session: sqlalchemy.orm.session.Session, album_query: bool = False
) -> List[MusicItem]:
    """Queries the database for the given query string.

    Args:
        query_str: Query string to parse. See HELP_STR for more info.
        album_query: Whether or not to match albums instead of tracks.
        session: current db session

    Returns:
        All tracks matching the query.
    """
    expressions = _parse_query(query_str)

    if not expressions:
        log.error(f"Invalid query '{query_str}'\n{HELP_STR}")
        return []

    query_cls = Album if album_query else Track
    query_filters = []
    for expression in expressions:
        try:
            query_filters.append(_create_filter(expression, query_cls))
        except ValueError:
            return []

    items = session.query(query_cls).filter(*query_filters).all()

    if not items:
        log.warning(f"No items found for the query '{query_str}'.")

    return items
