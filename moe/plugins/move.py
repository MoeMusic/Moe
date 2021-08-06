"""Alters the location of items in your library.

The ``move`` plugin provides the following features:

* Any items added to your library will be copied to the location set by ``library_path``
  in your configuration file.
* Any items moved or copied will have their paths set to a default format.
  This default format cannot currently be configured, and is as follows:

  * Albums: ``{library_path}/{albumartist} ({album_year})/``
  * Tracks: ``{album_path}/{track_number} - {track_title}.{file_ext}``

    If the album contains more than one disc, tracks will be formatted as:

    ``{album_path}/Disc {disc#}/{track_number} - {track_title}.{file_ext}``
  * Extras: ``{album_path}/{original_file_name}``

API:
    This plugin provides an interface for automatically formatting item paths as
    specified above via ``fmt_item_path()``, moving items with ``move_item()``,
    and copying items with ``copy_item()``.

Note:
    This plugin is enabled by default.
"""

import argparse
import logging
import shutil
from contextlib import suppress
from pathlib import Path
from typing import Union

import dynaconf
import sqlalchemy as sa
from sqlalchemy.orm.session import Session
from unidecode import unidecode

import moe
from moe.core.config import Config
from moe.core.library.album import Album
from moe.core.library.extra import Extra
from moe.core.library.lib_item import LibItem
from moe.core.library.track import Track

__all__ = ["fmt_item_path", "copy_item", "move_item"]

log = logging.getLogger("moe.move")


@moe.hookimpl
def add_config_validator(settings: dynaconf.base.LazySettings):
    """Validate move plugin configuration settings."""
    settings.validators.register(
        dynaconf.Validator("MOVE.ASCIIFY_PATHS", must_exist=True, default=False)
    )
    settings.validators.register(
        dynaconf.Validator("MOVE.LIBRARY_PATH", must_exist=True, default="~/Music")
    )


@moe.hookimpl
def add_command(cmd_parsers: argparse._SubParsersAction):  # noqa: WPS437
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


def _parse_args(
    config: Config, session: sa.orm.session.Session, args: argparse.Namespace
):
    """Parses the given commandline arguments.

    Items will be moved according to the given user configuration.

    Args:
        config: Configuration in use.
        session: Current db session.
        args: Commandline arguments to parse.

    Raises:
        SystemExit: Invalid field or field_value term format.
    """
    albums = session.execute(sa.select(Album)).scalars().all()

    if args.dry_run:
        dry_run_str = ""
        for dry_album in albums:
            album_dest = fmt_item_path(dry_album, config)
            if album_dest != dry_album.path:
                dry_run_str += f"\n{dry_album.path}\n\t-> {album_dest}"

            # temporarily set the album's path so track/extra dests use the right
            # album directory
            sa.orm.attributes.set_committed_value(dry_album, "path", album_dest)

            for dry_track in dry_album.tracks:
                track_dest = fmt_item_path(dry_track, config)
                if track_dest != dry_track.path:
                    dry_run_str += f"\n{dry_track.path}\n\t-> {track_dest}"
            for dry_extra in dry_album.extras:
                extra_dest = fmt_item_path(dry_extra, config)
                if extra_dest != dry_extra.path:
                    dry_run_str += f"\n{dry_extra.path}\n\t-> {extra_dest}"

        if dry_run_str:
            print(dry_run_str.lstrip())  # noqa: WPS421
    else:
        for album in albums:
            move_item(album, config)


@moe.hookimpl
def post_add(config: Config, session: Session, item: LibItem):
    """Copies and formats the path of an item after it has been added to the library."""
    # copy the whole album in case album attributes have changed
    if isinstance(item, Album):
        album = item
    elif isinstance(item, (Extra, Track)):
        album = item.album_obj

    copy_item(album, config)


########################################################################################
# Format paths
########################################################################################
def fmt_item_path(item: LibItem, config: Config) -> Path:
    """Returns a formatted item path according to the user configuration.

    Args:
        item: Library item used to format the directory.
        config: Moe config.

    Returns:
        Formatted item path under the config ``library_path``.
    """
    if isinstance(item, Album):
        new_path = _fmt_album_path(item, config)
    elif isinstance(item, Extra):
        new_path = _fmt_extra_path(item, config)
    elif isinstance(item, Track):
        new_path = _fmt_track_path(item, config)

    if config.settings.move.asciify_paths:
        new_path = Path(unidecode(str(new_path)))

    return new_path


def _fmt_album_path(album: Album, config: Config) -> Path:
    """Returns a formatted album directory according to the user configuration.

    An album directory should contain, at a minimum, the album artist, title, and year
    to ensure uniqueness.

    Args:
        album: Album used to format the directory.
        config: Moe config.

    Returns:
        Formatted album directory under the config ``library_path``.
    """
    library_path = Path(config.settings.move.library_path).expanduser()
    album_dir_name = f"{album.artist}/{album.title} ({album.year})"

    return library_path / album_dir_name


def _fmt_extra_path(extra: Extra, config: Config) -> Path:
    """Returns a formatted extra path according to the user configuration."""
    return extra.album_obj.path / extra.path.name


def _fmt_track_path(track: Track, config: Config) -> Path:
    """Returns a formatted track path according to the user configuration.

    The track path should contain, at a minimum, the track number and
    disc (if more than one) to ensure uniqueness.

    Args:
        track: Track used to format the path.
        config: Moe config.

    Returns:
        Formatted track path under its album path.
    """
    disc_dir_name = ""
    if track.disc_total > 1:
        disc_dir_name = f"Disc {track.disc:02}"
    disc_dir = track.album_obj.path / disc_dir_name

    track_filename = f"{track.track_num:02} - {track.title}{track.path.suffix}"

    return disc_dir / track_filename


########################################################################################
# Copy
########################################################################################
def copy_item(item: LibItem, config: Config):
    """Copies an item to a destination as determined by the user configuration.

    Overwrites any existing files. Will create the destination if it does not already
    exist.

    Args:
        item: Library item to copy.
        config: Moe config.
    """
    if isinstance(item, Album):
        _copy_album(item, config)
    elif isinstance(item, (Extra, Track)):
        _copy_file_item(item, config)


def _copy_album(album: Album, config: Config):
    """Copies an album to a destination as determined by the user configuration.

    Copying an album will also copy all of it's tracks and extras.

    Args:
        album: Album to copy
        config: Moe config.
    """
    dest = fmt_item_path(album, config)

    log.info(f"Copying album from '{album.path}' to '{dest}'.")
    if album.path != dest:
        dest.mkdir(parents=True, exist_ok=True)
        album.path = dest

    for track in album.tracks:
        _copy_file_item(track, config)

    for extra in album.extras:
        _copy_file_item(extra, config)


def _copy_file_item(item: Union[Extra, Track], config: Config):
    """Copies an extra or track to a destination as determined by the user config."""
    dest = fmt_item_path(item, config)
    if dest == item.path:
        return

    log.info(f"Copying {type(item).__name__.lower()} from '{item.path}' to '{dest}'.")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(item.path, dest)

    item.path = dest


########################################################################################
# Move
########################################################################################
def move_item(item: LibItem, config: Config):
    """Moves an item to a destination as determined by the user configuration.

    Overwrites any existing files. Will create the destination if it does not already
    exist.

    Args:
        item: Library item to move.
        config: Moe config.
    """
    if isinstance(item, Album):
        _move_album(item, config)
    elif isinstance(item, (Extra, Track)):
        _move_file_item(item, config)


def _move_album(album: Album, config: Config):
    """Moves an album to a given destination.

    - Overwrites any existing files.
    - Creates the destination if it does not already exist.
    - Tracks and extras are also moved.
    - Empty leftover directories will be removed.

    Args:
        album: Album to move.
        config: Moe config.
    """
    dest = fmt_item_path(album, config)
    old_album_dir = album.path

    log.info(f"Moving album from '{album.path}' to '{dest}'.")
    if album.path != dest:
        dest.mkdir(parents=True, exist_ok=True)
        album.path = dest

    for track in album.tracks:
        _move_file_item(track, config)

    for extra in album.extras:
        _move_file_item(extra, config)

    # remove any empty leftover directories
    for old_child in old_album_dir.rglob("*"):
        with suppress(OSError):
            old_child.rmdir()
    with suppress(OSError):
        old_album_dir.rmdir()
    for old_parent in old_album_dir.parents:
        with suppress(OSError):
            old_parent.rmdir()


def _move_file_item(item: Union[Extra, Track], config: Config):
    """Moves an extra or track to a destination as determined by the user config."""
    dest = fmt_item_path(item, config)
    if dest == item.path:
        return

    log.info(f"Moving {type(item).__name__.lower()} from '{item.path}' to '{dest}'.")
    dest.parent.mkdir(parents=True, exist_ok=True)
    item.path.replace(dest)

    item.path = dest
