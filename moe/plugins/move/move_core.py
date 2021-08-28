"""Core api for moving items."""

import logging
import shutil
from contextlib import suppress
from pathlib import Path
from typing import Union

import dynaconf
from unidecode import unidecode

import moe
from moe.config import Config
from moe.library.album import Album
from moe.library.extra import Extra
from moe.library.lib_item import LibItem
from moe.library.track import Track

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
def post_add(config: Config, item: LibItem):
    """Copies and formats the path of an item after it has been added to the library."""
    # copy the whole album in case album attributes have changed
    if isinstance(item, Album):
        album = item
    elif isinstance(item, (Extra, Track)):
        album = item.album_obj

    copy_item(config, album)


########################################################################################
# Format paths
########################################################################################
def fmt_item_path(config: Config, item: LibItem) -> Path:
    """Returns a formatted item path according to the user configuration.

    Args:
        item: Library item used to format the directory.
        config: Moe config.

    Returns:
        Formatted item path under the config ``library_path``.
    """
    if isinstance(item, Album):
        new_path = _fmt_album_path(config, item)
    elif isinstance(item, Extra):
        new_path = _fmt_extra_path(config, item)
    elif isinstance(item, Track):
        new_path = _fmt_track_path(config, item)

    if config.settings.move.asciify_paths:
        new_path = Path(unidecode(str(new_path)))

    return new_path


def _fmt_album_path(config: Config, album: Album) -> Path:
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


def _fmt_extra_path(config: Config, extra: Extra) -> Path:
    """Returns a formatted extra path according to the user configuration."""
    return extra.album_obj.path / extra.path.name


def _fmt_track_path(config: Config, track: Track) -> Path:
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
def copy_item(config: Config, item: LibItem):
    """Copies an item to a destination as determined by the user configuration.

    Overwrites any existing files. Will create the destination if it does not already
    exist.

    Args:
        item: Library item to copy.
        config: Moe config.
    """
    if isinstance(item, Album):
        _copy_album(config, item)
    elif isinstance(item, (Extra, Track)):
        _copy_file_item(config, item)


def _copy_album(config: Config, album: Album):
    """Copies an album to a destination as determined by the user configuration.

    Copying an album will also copy all of it's tracks and extras.

    Args:
        album: Album to copy
        config: Moe config.
    """
    dest = fmt_item_path(config, album)

    log.info(f"Copying album from '{album.path}' to '{dest}'.")
    if album.path != dest:
        dest.mkdir(parents=True, exist_ok=True)
        album.path = dest

    for track in album.tracks:
        _copy_file_item(config, track)

    for extra in album.extras:
        _copy_file_item(config, extra)


def _copy_file_item(config: Config, item: Union[Extra, Track]):
    """Copies an extra or track to a destination as determined by the user config."""
    dest = fmt_item_path(config, item)
    if dest == item.path:
        return

    log.info(f"Copying {type(item).__name__.lower()} from '{item.path}' to '{dest}'.")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(item.path, dest)

    item.path = dest


########################################################################################
# Move
########################################################################################
def move_item(config: Config, item: LibItem):
    """Moves an item to a destination as determined by the user configuration.

    Overwrites any existing files. Will create the destination if it does not already
    exist.

    Args:
        item: Library item to move.
        config: Moe config.
    """
    if isinstance(item, Album):
        _move_album(config, item)
    elif isinstance(item, (Extra, Track)):
        _move_file_item(config, item)


def _move_album(config: Config, album: Album):
    """Moves an album to a given destination.

    - Overwrites any existing files.
    - Creates the destination if it does not already exist.
    - Tracks and extras are also moved.
    - Empty leftover directories will be removed.

    Args:
        album: Album to move.
        config: Moe config.
    """
    dest = fmt_item_path(config, album)
    old_album_dir = album.path

    log.info(f"Moving album from '{album.path}' to '{dest}'.")
    if album.path != dest:
        dest.mkdir(parents=True, exist_ok=True)
        album.path = dest

    for track in album.tracks:
        _move_file_item(config, track)

    for extra in album.extras:
        _move_file_item(config, extra)

    # remove any empty leftover directories
    for old_child in old_album_dir.rglob("*"):
        with suppress(OSError):
            old_child.rmdir()
    with suppress(OSError):
        old_album_dir.rmdir()
    for old_parent in old_album_dir.parents:
        with suppress(OSError):
            old_parent.rmdir()


def _move_file_item(config: Config, item: Union[Extra, Track]):
    """Moves an extra or track to a destination as determined by the user config."""
    dest = fmt_item_path(config, item)
    if dest == item.path:
        return

    log.info(f"Moving {type(item).__name__.lower()} from '{item.path}' to '{dest}'.")
    dest.parent.mkdir(parents=True, exist_ok=True)
    item.path.replace(dest)

    item.path = dest
