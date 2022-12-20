"""Removes music from the library.

Note:
    This plugin is enabled by default.
"""

import argparse
import logging
import shutil

from sqlalchemy.orm.session import Session

import moe
import moe.cli
from moe import remove as moe_rm
from moe.util.cli import cli_query, query_parser

__all__: list[str] = []

log = logging.getLogger("moe.cli.remove")


@moe.hookimpl
def add_command(cmd_parsers: argparse._SubParsersAction):
    """Adds the ``remove`` command to Moe's CLI."""
    rm_parser = cmd_parsers.add_parser(
        "remove",
        aliases=["rm"],
        description="Removes music from the library.",
        help="remove music from the library",
        parents=[query_parser],
    )
    rm_parser.add_argument(
        "-d",
        "--delete",
        action="store_true",
        help="delete the items from the filesystem",
    )
    rm_parser.set_defaults(func=_parse_args)


def _parse_args(session: Session, args: argparse.Namespace):
    """Parses the given commandline arguments.

    Args:
        session: Library db session.
        args: Commandline arguments to parse.

    Raises:
        SystemExit: Invalid query given, or no items to remove.
    """
    items = cli_query(session, args.query, query_type=args.query_type)

    for item in items:
        moe_rm.remove_item(session, item)

        if args.delete:
            if item.path.is_file():
                item.path.unlink()
            else:
                shutil.rmtree(item.path)
