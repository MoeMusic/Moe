"""Prints information about music in the library.

All fields and their values should be printed to stdout for any music queried.
"""

import argparse
import re
from typing import List

import sqlalchemy

import moe
from moe.core import library, query
from moe.core.config import Config


@moe.hookimpl
def addcommand(cmd_parsers: argparse._SubParsersAction):  # noqa: WPS437
    """Adds a new `info` command to moe."""
    add_parser = cmd_parsers.add_parser(
        "info",
        description="Prints information about music in the library.",
        help="print info for music in the library",
        parents=[query.query_parser],
    )
    add_parser.set_defaults(func=parse_args)


def parse_args(
    config: Config, session: sqlalchemy.orm.session.Session, args: argparse.Namespace,
):
    """Parse the given commandline arguments.

    Args:
        config: configuration in use
        session: current session
        args: commandline arguments to parse
    """
    tracks = query.query(args.query, session)

    print(get_infos(tracks), end="")  # noqa: WPS421


def get_infos(tracks: List[library.Track]):
    """Get information for a list of tracks."""
    out_str = ""
    for track in tracks:
        out_str += get_info(track)

        if track is not tracks[-1]:
            out_str += "\n"

    return out_str


def get_info(track: library.Track) -> str:
    """Returns information about a track."""
    track_info = ""
    private_field_re = "^_.*"
    for field, value in vars(track).items():  # noqa: WPS421
        if not re.match(private_field_re, field):
            track_info += f"{field}: {value}\n"

    return track_info
