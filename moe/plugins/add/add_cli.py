"""Adds the ``add`` command to add music to the library."""

import argparse
import logging
from pathlib import Path

import moe
import moe.cli
from moe.library import Album, AlbumError, Track, TrackError
from moe.plugins import add as moe_add
from moe.plugins.add.add_core import AddError
from moe.util.cli import PromptChoice

log = logging.getLogger("moe.cli.add")

__all__: list[str] = []


class SkipAdd(Exception):
    """Used to skip adding a single item."""


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


@moe.hookimpl
def add_import_prompt_choice(prompt_choices: list[PromptChoice]):
    """Adds the ``skip`` prompt choice to the import prompt."""
    prompt_choices.append(
        PromptChoice(title="Skip", shortcut_key="s", func=_skip_import)
    )


def _skip_import(
    old_album: Album,
    new_album: Album,
):
    """Skip adding/importing the current item."""
    raise SkipAdd()


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
        try:
            _add_path(path)
        except (AddError, AlbumError, TrackError) as err:
            log.error(err)
            error_count += 1
        except SkipAdd:
            log.debug(f"Skipped adding item. [{path=}]")

    if error_count:
        raise SystemExit(1)


def _add_path(path: Path):
    """Adds an item to the library from a given path.

    Args:
        path: Path to add. Either a directory for an Album or a file for a Track.

    Raises:
        AddError: Path not found or other issue adding the item to the library.
        AlbumError: Could not create an album from the given directory.
        TrackError: Could not create a track from the given file.
        SkipAdd: External program or user elected to skip adding the item.
    """
    if path.is_file():
        moe_add.add_item(Track.from_file(path))
    elif path.is_dir():
        moe_add.add_item(Album.from_dir(path))
    else:
        log.error(f"Path not found. [{path=}]")
        raise AddError("Path not found. [{path=}]")
