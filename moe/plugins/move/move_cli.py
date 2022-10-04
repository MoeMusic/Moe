"""Adds the ``move`` command to the cli."""

import argparse
import logging
from typing import cast

import sqlalchemy.orm

import moe
from moe.library import Album
from moe.plugins import move as moe_move
from moe.util.cli import cli_query

log = logging.getLogger("moe.cli.move")


@moe.hookimpl
def add_command(cmd_parsers: argparse._SubParsersAction):
    """Adds the ``move`` command to Moe's CLI."""
    move_parser = cmd_parsers.add_parser(
        "move",
        aliases=["mv"],
        description="Moves items in the library according to the user configuration.",
        help="move items in the library",
    )
    move_parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="display what will be moved without actually moving the items",
    )
    move_parser.set_defaults(func=_parse_args)


def _parse_args(args: argparse.Namespace):
    """Parses the given commandline arguments.

    Items will be moved according to the given user configuration.

    Args:
        args: Commandline arguments to parse.

    Raises:
        SystemExit: Invalid query or no items found to move.
    """
    albums = cast(list[Album], cli_query("*", query_type="album"))

    if args.dry_run:
        dry_run_str = _dry_run(albums)
        if dry_run_str:
            print(dry_run_str.lstrip())
    else:
        for album in albums:
            moe_move.move_item(album)


def _dry_run(albums: list[Album]) -> str:
    """Returns a string of output representing a 'dry-run' of moving albums."""
    dry_run_str = ""

    for dry_album in albums:
        album_dest = moe_move.fmt_item_path(dry_album)
        if album_dest != dry_album.path:
            dry_run_str += f"\n{dry_album.path}\n\t-> {album_dest}"

        # temporarily set the album's path so track/extra dests use the right
        # album directory
        sqlalchemy.orm.attributes.set_committed_value(dry_album, "path", album_dest)

        for dry_track in dry_album.tracks:
            track_dest = moe_move.fmt_item_path(dry_track)
            if track_dest != dry_track.path:
                dry_run_str += f"\n{dry_track.path}\n\t-> {track_dest}"
        for dry_extra in dry_album.extras:
            extra_dest = moe_move.fmt_item_path(dry_extra)
            if extra_dest != dry_extra.path:
                dry_run_str += f"\n{dry_extra.path}\n\t-> {extra_dest}"

    return dry_run_str
