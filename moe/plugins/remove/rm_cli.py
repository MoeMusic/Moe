"""Removes music from the library.

Note:
    This plugin is enabled by default.
"""

import argparse
import logging

import moe
import moe.cli
from moe.plugins import remove as moe_rm
from moe.query import QueryError, query

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
        parents=[moe.cli.query_parser],
    )
    rm_parser.set_defaults(func=_parse_args)


def _parse_args(args: argparse.Namespace):
    """Parses the given commandline arguments.

    Args:
        args: Commandline arguments to parse.

    Raises:
        SystemExit: Invalid query given, or no items to remove.
    """
    try:
        items = query(args.query, query_type=args.query_type)
    except QueryError as err:
        log.error(err)
        raise SystemExit(1) from err

    if not items:
        log.error("No items found to remove.")
        raise SystemExit(1)

    for item in items:
        moe_rm.remove_item(item)
