"""Lists music in the library.

Note:
    This plugin is enabled by default.
"""

import argparse
import logging

import moe
import moe.cli
from moe import config
from moe.query import QueryError, query

__all__: list[str] = []

log = logging.getLogger("moe.cli.list")


@moe.hookimpl
def plugin_registration():
    """Depend on the cli plugin."""
    if not config.CONFIG.pm.has_plugin("cli"):
        config.CONFIG.pm.set_blocked("list")
        log.warning("The 'list' plugin requires the 'cli' plugin to be enabled.")


@moe.hookimpl
def add_command(cmd_parsers: argparse._SubParsersAction):
    """Adds the ``list`` command to Moe's CLI."""
    ls_parser = cmd_parsers.add_parser(
        "list",
        aliases=["ls"],
        description="Lists music in the library.",
        help="list music in the library",
        parents=[moe.cli.query_parser],
    )
    ls_parser.add_argument(
        "-p",
        "--paths",
        action="store_true",
        help="list paths",
    )
    ls_parser.set_defaults(func=_parse_args)


def _parse_args(args: argparse.Namespace):
    """Parses the given commandline arguments.

    Args:
        args: Commandline arguments to parse.

    Raises:
        SystemExit: Invalid query or no items found.
    """
    try:
        items = query(args.query, query_type=args.query_type)
    except QueryError as err:
        log.error(err)
        raise SystemExit(1) from err

    if not items:
        log.error("No items found to list.")
        raise SystemExit(1)

    for item in items:
        if args.paths:
            print(item.path)
        else:
            print(item)
