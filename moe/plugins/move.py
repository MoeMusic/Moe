"""Any operations regarding altering the location of files in the library."""

import logging
import shutil
from pathlib import Path
from typing import List

import dynaconf
from sqlalchemy.orm.session import Session

import moe
from moe.core.config import Config
from moe.core.library.album import Album
from moe.core.library.extra import Extra
from moe.core.library.track import Track

__all__: List[str] = []

log = logging.getLogger(__name__)


@moe.hookimpl
def add_config_validator(settings: dynaconf.base.LazySettings):
    """Validate move plugin configuration settings."""
    settings.validators.register(
        dynaconf.Validator("MOVE.LIBRARY_PATH", must_exist=True, default="~/Music")
    )


@moe.hookimpl(trylast=True)
def post_args(config: Config, session: Session):
    """Moves altered or new items in the session after the CLI args have executed."""
    library_path = Path(config.settings.move.library_path).expanduser()

    for item in session.new.union(session.dirty):
        if isinstance(item, Album):
            album = item
        elif isinstance(item, Track):
            album = item.album_obj
        elif isinstance(item, Extra):
            album = item.album
        else:
            return

        _move_album(album, library_path)


@moe.hookimpl
def pre_add(config: Config, session: Session, album: Album):
    """Copies and formats the path of an album prior to it being added."""
    library_path = Path(config.settings.move.library_path).expanduser()

    _copy_album(album, library_path)


########################################################################################
# Format paths
########################################################################################
def _get_album_dir(album: Album, root_dir: Path) -> Path:
    """Returns a formatted album directory under ``root_dir``.

    An album directory should contain, at a minimum, the album artist, title, and year
    to ensure uniqueness.

    Args:
        album: Album used to format the directory.
        root_dir: Directory to place the album directory under.

    Returns:
        Formatted album directory under ``root_dir``.
    """
    album_dir_name = f"{album.artist}/{album.title} ({album.year})"
    return root_dir / album_dir_name


def _get_extra_path(extra: Extra, album_dir: Path) -> Path:
    """Returns a formatted track path under ``album_dir``."""
    return album_dir / extra.path.name


def _get_track_path(track: Track, album_dir: Path) -> Path:
    """Returns a formatted track path under ``album_dir``.

    The track path should contain, at a minimum, the track number and
    disc (if more than one) to ensure uniqueness.

    Args:
        track: Track used to format the path.
        album_dir: Directory to place the album directory under.

    Returns:
        Formatted album directory under ``root_dir``.
    """
    disc_dir_name = ""
    if track.disc_total > 1:
        disc_dir_name = f"Disc {track.disc:02}"
    disc_dir = album_dir / disc_dir_name

    track_filename = f"{track.track_num:02} - {track.title}.{track.file_ext}"
    return disc_dir / track_filename


########################################################################################
# Copy
# ####
#
# When copying an item, operate at the album-level with `_copy_album()`.
########################################################################################
def _copy_album(album: Album, root_dir: Path):
    """Copies an album to a formatted dir under ``root_dir``.

    Overwrites any existing files.

    Args:
        album: Album to copy
        root_dir: Root directory to copy the album to.
    """
    album_dir = _get_album_dir(album, root_dir)

    album_dir.mkdir(parents=True, exist_ok=True)

    for track in album.tracks:
        _copy_track(track, album_dir)

    for extra in album.extras:
        _copy_extra(extra, album_dir)

    album.path = album_dir


def _copy_track(track: Track, album_dir: Path):
    """Copies a track to a formatted destination under ``album_dir``.

    Overwrites any existing files.

    Args:
        track: Track to copy.
        album_dir: Album directory destination.
    """
    track_dest = _get_track_path(track, album_dir)

    if track_dest == track.path:
        return

    log.info(f"Copying track '{track.path}' to '{track_dest}'.")
    track_dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(track.path, track_dest)

    track.path = track_dest


def _copy_extra(extra: Extra, album_dir: Path):
    """Copies an extra to a formatted destination under ``album_dir``.

    Overwrites any existing files.

    Args:
        extra: Extra to copy.
        album_dir: Album directory to copy the extra to.
    """
    extra_dest = _get_extra_path(extra, album_dir)

    if extra_dest == extra.path:
        return

    log.info(f"Copying extra '{extra}' to '{extra_dest}'.")
    extra_dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(extra.path, extra_dest)

    extra.path = extra_dest


########################################################################################
# Move
# ####
#
# When moving an item, operate at the album-level with `_move_album()`.
########################################################################################
def _move_album(album: Album, root_dir: Path):
    """Moves an album to a formatted dir under ``root_dir``.

    Overwrites any existing files.

    Args:
        album: Album to copy
        root_dir: Root directory to copy the album to.
    """
    album_dir = _get_album_dir(album, root_dir)

    album_dir.mkdir(parents=True, exist_ok=True)

    for track in album.tracks:
        _move_track(track, album_dir)

    for extra in album.extras:
        _move_extra(extra, album_dir)

    # remove any empty leftover directories
    for old_path in album.path.rglob("*"):
        try:
            old_path.rmdir()
        except OSError:
            pass  # noqa: WPS420
    try:
        album.path.rmdir()
    except OSError:
        pass  # noqa: WPS420

    album.path = album_dir


def _move_track(track: Track, album_dir: Path):
    """Moves a track to a formatted destination under ``album_dir``.

    Overwrites any existing files.

    Args:
        track: Track to copy.
        album_dir: Album directory destination.
    """
    track_dest = _get_track_path(track, album_dir)

    if track_dest == track.path:
        return

    log.info(f"Moving track '{track.path}' to '{track_dest}'.")
    track_dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(track.path, track_dest)

    track.path = track_dest


def _move_extra(extra: Extra, album_dir: Path):
    """Moves an extra to a formatted destination under ``album_dir``.

    Overwrites any existing files.

    Args:
        extra: Extra to copy.
        album_dir: Album directory to copy the extra to.
    """
    extra_dest = _get_extra_path(extra, album_dir)

    if extra_dest == extra.path:
        return

    log.info(f"Copying extra '{extra}' to '{extra_dest}'.")
    extra_dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(extra.path, extra_dest)

    extra.path = extra_dest
