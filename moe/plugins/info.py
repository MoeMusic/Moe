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
def addcommand(cmd_parsers: argparse._SubParsersAction):
    """Adds a new `add` command to moe."""
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
    """Parse the given commandline arguments."""
    tracks = query.query(args.query, session)

    print_infos(tracks)


def print_infos(tracks: List[library.Track]):
    """Print information for a list of tracks."""
    for track in tracks:
        print_info(track)

        # print()
        # print newline after each track except the last
        if track is not tracks[-1]:
            print()


def print_info(track: library.Track):
    """Print information about a track."""
    BANNED_INFO_FIELDS_RE = re.compile(
        r"""
        ^_.*   # private fields
        |^id$  # id
        """,
        re.VERBOSE,
    )

    for field, value in track.__dict__.items():
        if not re.match(BANNED_INFO_FIELDS_RE, field):
            print("{}: {}".format(field, value))
