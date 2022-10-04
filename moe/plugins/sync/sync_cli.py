"""Adds the ``sync`` command to sync library metadata."""

import argparse
import logging

import moe
import moe.cli
from moe.plugins import sync as moe_sync
from moe.util.cli import cli_query, query_parser

log = logging.getLogger("moe.cli.sync")

__all__: list[str] = []


@moe.hookimpl
def add_command(cmd_parsers: argparse._SubParsersAction):
    """Adds the ``add`` command to Moe's CLI."""
    add_parser = cmd_parsers.add_parser(
        "sync",
        description="Sync music metadata.",
        help="sync music metadata",
        parents=[query_parser],
    )
    add_parser.set_defaults(func=_parse_args)


def _parse_args(args: argparse.Namespace):
    """Parses the given commandline arguments.

    Args:
        args: Commandline arguments to parse.

    Raises:
        SystemExit: Invalid query given or query returned no items.
    """
    items = cli_query(args.query, query_type=args.query_type)

    for item in items:
        moe_sync.sync_item(item)
