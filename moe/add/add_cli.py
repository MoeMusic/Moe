"""Adds the ``add`` command to add music to the library."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING, cast

import moe
import moe.add
from moe.add.add_core import AddError
from moe.library import Album, AlbumError, Extra, Track, TrackError
from moe.util.cli import PromptChoice
from moe.util.cli.query import cli_query

if TYPE_CHECKING:
    import argparse

    from sqlalchemy.orm.session import Session

log = logging.getLogger("moe.cli.add")

__all__: list[str] = []


class SkipAdd(Exception):  # noqa: N818 breaking change
    """Used to skip adding a single item."""


@moe.hookimpl
def add_command(cmd_parsers: argparse._SubParsersAction) -> None:
    """Adds the ``add`` command to Moe's CLI."""
    add_parser = cmd_parsers.add_parser(
        "add", description="Adds music to the library.", help="add music to the library"
    )
    add_parser.add_argument(
        "paths",
        metavar="path",
        nargs="+",
        help="dir to add an album or file to add a track or extra",
    )
    add_parser.add_argument(
        "-a",
        "--album_query",
        help="album to add an extra or track to (required if adding an extra)",
    )
    add_parser.set_defaults(func=_parse_args)


@moe.hookimpl
def add_import_prompt_choice(prompt_choices: list[PromptChoice]) -> None:
    """Adds the ``skip`` prompt choice to the import prompt."""
    prompt_choices.append(
        PromptChoice(title="Skip", shortcut_key="s", func=_skip_import)
    )


def _skip_import(
    old_album: Album,  # noqa: ARG001
    new_album: Album,  # noqa: ARG001
) -> None:
    """Skip adding/importing the current item."""
    raise SkipAdd


def _parse_args(session: Session, args: argparse.Namespace) -> None:
    """Parses the given commandline arguments.

    Tracks can be added as files or albums as directories.

    Args:
        session: Library db session.
        args: Commandline arguments to parse.

    Raises:
        SystemExit: Path given does not exist.
    """
    paths = [Path(arg_path) for arg_path in args.paths]

    album: Album | None = None
    if args.album_query:
        albums = cast("list[Album]", cli_query(session, args.album_query, "album"))

        if len(albums) > 1:
            log.error("Query returned more than one album.")
            raise SystemExit(1)
        album = albums[0]

    error_count = 0
    for path in paths:
        try:
            _add_path(session, path, album)
        except (AddError, AlbumError):  # noqa: PERF203
            log.exception("Error adding item.")
            error_count += 1
        except SkipAdd:
            log.debug(f"Skipped adding item. [{path=}]")

    if error_count:
        raise SystemExit(1)


def _add_path(session: Session, path: Path, album: Album | None) -> None:
    """Adds an item to the library from a given path.

    Args:
        session: Library db session.
        path: Path to add. Either a directory for an Album or a file for a Track.
        album: If ``path`` is a file, add it to ``album`` if given. Note, this
            argument is required if adding an Extra.

    Raises:
        AddError: Path not found or other issue adding the item to the library.
        AlbumError: Could not create an album from the given directory.
        SkipAdd: External program or user elected to skip adding the item.
    """
    if path.is_file():
        try:
            moe.add.add_item(session, Track.from_file(path, album=album))
        except TrackError:
            if not album:
                err_msg = f"An album query is required to add an extra. [{path=}]"
                raise AddError(err_msg) from None

            moe.add.add_item(session, Extra(album, path))
    elif path.is_dir():
        moe.add.add_item(session, Album.from_dir(path))
    else:
        err_msg = f"Path not found. [{path=}]"
        raise AddError(err_msg)
