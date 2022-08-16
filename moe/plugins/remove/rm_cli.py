"""Removes music from the library.

Note:
    This plugin is enabled by default.
"""

import argparse
from typing import List

import moe
import moe.cli
from moe import query
from moe.config import Config
from moe.plugins import remove as moe_rm

__all__: List[str] = []


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
        moe_rm.remove_item(item)
