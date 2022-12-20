"""Adds the ``read`` command to moe."""

import argparse
import logging

from sqlalchemy.orm.session import Session

import moe
import moe.cli
from moe import read, remove
from moe.util.cli import cli_query, query_parser

log = logging.getLogger("moe.cli.read")

__all__: list[str] = []


@moe.hookimpl
def add_command(cmd_parsers: argparse._SubParsersAction):
    """Adds the ``read`` command to Moe's CLI."""
    read_parser = cmd_parsers.add_parser(
        "read",
        description="Read item files and update moe with any changes.",
        help="read item files and update moe with any changes",
        parents=[query_parser],
    )
    read_parser.add_argument(
        "-r",
        "--remove",
        action="store_true",
        help="remove items that no longer exist on the filesystem",
    )
    read_parser.set_defaults(func=_parse_args)


def _parse_args(session: Session, args: argparse.Namespace):
    """Parses the given commandline arguments.

    Tracks can be added as files or albums as directories.

    Args:
        session: Library db session.
        args: Commandline arguments to parse.

    Raises:
        SystemExit: Path given does not exist.
    """
    items = cli_query(session, args.query, args.query_type)

    error_count = 0
    for item in items:
        try:
            read.read_item(item)
        except FileNotFoundError:
            if args.remove:
                remove.remove_item(session, item)
            else:
                log.error(f"Could not find item's path. [{item=!r}]")
                error_count += 1

    if error_count:
        raise SystemExit(1)
