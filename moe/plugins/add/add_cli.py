"""Adds the ``add`` command and various user prompts to the cli."""

import argparse
import logging
from pathlib import Path
from typing import List

import moe
from moe.config import Config
from moe.plugins import add as moe_add

log = logging.getLogger("moe.add")

__all__: List[str] = []


@moe.hookimpl
def add_command(cmd_parsers: argparse._SubParsersAction):  # noqa: WPS437
    """Adds the ``add`` command to Moe's CLI."""
    add_parser = cmd_parsers.add_parser(
        "add", description="Adds music to the library.", help="add music to the library"
    )
    add_parser.add_argument(
        "paths",
        metavar="path",
        nargs="+",
        help="dir to add an album or file to add a track",
    )
    add_parser.set_defaults(func=_parse_args)


def _parse_args(config: Config, args: argparse.Namespace):
    """Parses the given commandline arguments.

    Tracks can be added as files or albums as directories.

    Args:
        config: Moe config.
        args: Commandline arguments to parse.

    Raises:
        SystemExit: Path given does not exist.
    """
    paths = [Path(arg_path) for arg_path in args.paths]

    error_count = 0
    for path in paths:
        try:
            moe_add.add_item(config, path)
        except moe_add.AddError as exc:
            log.error(exc)
            error_count += 1

    if error_count:
        raise SystemExit(1)
