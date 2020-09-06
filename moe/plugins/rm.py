"""Remove music from the library."""

import argparse
import logging

import sqlalchemy

import moe
from moe.core import query
from moe.core.config import Config

log = logging.getLogger(__name__)


@moe.hookimpl
def addcommand(cmd_parsers: argparse._SubParsersAction):  # noqa: WPS437
    """Adds a new `rm` command to moe.

    Args:
        cmd_parsers: contains all the sub-command parsers
    """
    add_parser = cmd_parsers.add_parser(
        "rm",
        aliases=["remove"],
        description="Removes music from the library.",
        help="remove music from the library",
        parents=[query.query_parser],
    )
    add_parser.set_defaults(func=parse_args)


def parse_args(
    config: Config, session: sqlalchemy.orm.session.Session, args: argparse.Namespace
):
    """Parses the given commandline arguments.

    Args:
        config: Configuration in use.
        session: Current session.
        args: Commandline arguments to parse.

    Raises:
        SystemExit: Query returned no tracks.
    """
    items = query.query(args.query, session, args.album)

    if not items:
        raise SystemExit(1)

    for item in items:
        log.info(f"Removing '{item}' from the library.")
        session.delete(item)
