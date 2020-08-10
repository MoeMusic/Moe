"""List music in the library."""

import argparse

import sqlalchemy

import moe
from moe.core import library
from moe.core.config import Config


@moe.hookimpl
def addcommand(cmd_parsers: argparse._SubParsersAction):
    """Adds a new `add` command to moe."""
    add_parser = cmd_parsers.add_parser(
        "list", aliases=["ls"], help="list music from the library"
    )
    add_parser.set_defaults(func=parse_args)


def parse_args(
    config: Config, session: sqlalchemy.orm.session.Session, args: argparse.Namespace,
):
    """Parse the given commandline arguments."""
    tracks = session.query(library.Track.path).all()

    for track in tracks:
        print(str(track[0]))
