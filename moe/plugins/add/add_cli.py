"""Adds the ``add`` command provides duplicate resolution when adding an item."""

import argparse
import logging
from pathlib import Path
from typing import Union, cast

import moe
import moe.cli
from moe.config import Config, MoeSession
from moe.library.album import Album, AlbumError
from moe.library.extra import Extra
from moe.library.lib_item import LibItem
from moe.library.track import Track, TrackError
from moe.plugins import add as moe_add
from moe.plugins.remove import remove_item
from moe.util.cli import PromptChoice, choice_prompt, fmt_album_changes

log = logging.getLogger("moe.cli.add")

__all__: list[str] = []


@moe.hookimpl(hookwrapper=True)
def pre_add(config: Config, item: LibItem):
    """Resolve any library duplicate conflicts after the ``pre_add`` hook has run."""
    yield  # allow all `pre_add` hook implementations to execute

    dup_item = item.get_existing()
    if not dup_item:
        return

    log.debug(
        f"Duplicate item exists in the library. [new_item={item!r}, {dup_item=!r}]"
    )

    if isinstance(item, Album):
        dup_item = cast(Album, dup_item)
        album = item
        dup_album = dup_item
    elif isinstance(item, (Extra, Track)):
        dup_item = cast(Union[Extra, Track], dup_item)
        album = item.album_obj
        dup_album = dup_item.album_obj
    else:
        raise NotImplementedError

    print(fmt_album_changes(album, dup_album))

    # Each PromptChoice `func` should have the following signature:
    # func(config, album, dup_album) # noqa: E800
    prompt_choices = [
        PromptChoice(
            title="Replace the existing album", shortcut_key="r", func=_replace
        ),
        PromptChoice(title="Abort", shortcut_key="x", func=_abort),
        PromptChoice(
            title="Merge without overwriting existing values",
            shortcut_key="m",
            func=_merge,
        ),
        PromptChoice(
            title="Merge, overwriting any existing values",
            shortcut_key="o",
            func=_overwrite,
        ),
    ]
    prompt_choice = choice_prompt(
        prompt_choices,
        "Duplicate item already exists in the library, how would you like to"
        " resolve it?",
    )
    try:
        prompt_choice.func(config, album, dup_album)
    except moe_add.AddAbortError as err:
        log.debug(err)
        raise SystemExit(0) from err


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
        if path.is_file():
            try:
                track = Track.from_file(path)
            except TrackError as err:
                log.error(err)
                error_count += 1
            else:
                moe_add.add_item(config, track)
        elif path.is_dir():
            try:
                album = Album.from_dir(path)
            except AlbumError as err:
                log.error(err)
                error_count += 1
            else:
                moe_add.add_item(config, album)
        else:
            log.error(f"Path not found. [{path=}]")
            error_count += 1

    if error_count:
        raise SystemExit(1)


def _replace(config: Config, album: Album, dup_album: Album):
    """Keeps the new album, removing the existing album from the library."""
    log.debug("Replacing duplicate album.")

    remove_item(config, dup_album)


def _abort(config: Config, album: Album, dup_album: Album):
    """Keeps the existing album i.e. abort adding the new album."""
    raise moe_add.AddAbortError("Duplicate resolution aborted; existing item kept.")


def _merge(config: Config, album: Album, dup_album: Album):
    """Merges the new album into the existing, without overwriting any conflicts."""
    log.debug("Merging duplicate album without overwriting.")

    album.merge(dup_album, overwrite=True)  # persist dup_album values

    session = MoeSession()
    remove_item(config, dup_album)  # remove existing item from the library
    session.expunge(album)  # don't prematurely add the album to the session


def _overwrite(config: Config, album: Album, dup_album: Album):
    """Merges the new album into the existing, overwriting any conflicts."""
    log.debug("Overwriting duplicate album.")

    album.merge(dup_album)

    session = MoeSession()
    remove_item(config, dup_album)  # remove existing item from the library
    session.expunge(album)  # don't prematurely add the album to the session
