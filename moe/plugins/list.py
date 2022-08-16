"""Lists music in the library.

Note:
    This plugin is enabled by default.
"""

import argparse
import logging
from typing import List

import moe
import moe.cli
from moe import query
from moe.config import Config

__all__: List[str] = []

log = logging.getLogger("moe.list")


@moe.hookimpl
def plugin_registration(config: Config):
    """Depend on the cli plugin."""
    if not config.plugin_manager.has_plugin("cli"):
        config.plugin_manager.set_blocked("list")
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


def _parse_args(config: Config, args: argparse.Namespace):
    """Parses the given commandline arguments.

    Args:
        config: Configuration in use.
        args: Commandline arguments to parse.

    Raises:
        SystemExit: Query returned no tracks.
    """
    items = query.query(args.query, query_type=args.query_type)

    if not items:
        raise SystemExit(1)

    for item in items:
        if args.paths:
            print(item.path)
        else:
            print(item)
