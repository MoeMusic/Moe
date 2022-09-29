"""Adds the ``add`` command to add music to the library."""

import argparse
import logging
from pathlib import Path

import moe
import moe.cli
from moe.library import Album, AlbumError, Track, TrackError
from moe.plugins import add as moe_add

log = logging.getLogger("moe.cli.add")

__all__: list[str] = []


@moe.hookimpl
def add_command(cmd_parsers: argparse._SubParsersAction):
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


def _parse_args(args: argparse.Namespace):
    """Parses the given commandline arguments.

    Tracks can be added as files or albums as directories.

    Args:
        args: Commandline arguments to parse.

    Raises:
        SystemExit: Path given does not exist.
    """
    paths = [Path(arg_path) for arg_path in args.paths]

    error_count = 0
    for path in paths:
        if path.is_file():
            try:
                track = Track.from_file(path)
            except TrackError as err:
                log.error(err)
                error_count += 1
            else:
                moe_add.add_item(track)
        elif path.is_dir():
            try:
                album = Album.from_dir(path)
            except AlbumError as err:
                log.error(err)
                error_count += 1
            else:
                moe_add.add_item(album)
        else:
            log.error(f"Path not found. [{path=}]")
            error_count += 1

    if error_count:
        raise SystemExit(1)
