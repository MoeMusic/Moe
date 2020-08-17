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
        match_dict[VALUE_GROUP] = match_dict[VALUE_GROUP].replace(r"\:", ":")

        match_dicts.append(match_dict)

    return match_dicts


def query(
    query_str: str, session: sqlalchemy.orm.session.Session,
) -> List[library.Track]:
    """Queries the database for the given query string.

    Args:
        query_str: Query string to parse. See HELP_STR for more info.
        session: current db session

    Returns:
        empty tracks
        All tracks matching the query.
    """
    expressions = _parse_query(query_str)

    if not expressions:
        log.warning(f"Invalid query '{query_str}'\n{HELP_STR}")
        return []

    filters = []
    for expression in expressions:
        field = sqlalchemy.func.lower(getattr(library.Track, expression[FIELD_GROUP]))
        if expression[SEPARATOR_GROUP] == "::":
            # Regular expression
            # Note, this is a custom sqlite function created in config.py
            value = expression[VALUE_GROUP]

            try:
                re.compile(value)
            except re.error:
                log.warning(f"'{value}' is not a valid regular expression.")
                return []

            filters.append(field.op("regexp")(value))
        else:
            # Normal expression
            value = sqlalchemy.func.lower(expression[VALUE_GROUP])
            filters.append(field == value)

    return session.query(library.Track).filter(*filters).all()
