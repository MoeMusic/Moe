"""Remove music from the library."""

import argparse
import logging

import sqlalchemy

import moe
from moe.core import query
from moe.core.config import Config

log = logging.getLogger(__name__)


@moe.hookimpl
def addcommand(cmd_parsers: argparse._SubParsersAction):
    """Adds a new `add` command to moe."""
    add_parser = cmd_parsers.add_parser(
        "rm",
        aliases=["remove"],
        description="Removes music from the library.",
        help="remove music from the library",
        parents=[query.query_parser],
    )
    add_parser.set_defaults(func=parse_args)


def parse_args(
    config: Config, session: sqlalchemy.orm.session.Session, args: argparse.Namespace,
):
    """Parse the given commandline arguments."""
    tracks = query.query(args.query, session)

    for track in tracks:
        log.info("Removing track '%s' from the library.", track)
        session.delete(track)