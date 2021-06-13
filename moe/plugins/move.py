"""Any operations regarding altering the location of files in the library."""

import logging
import pathlib
import shutil

import dynaconf
from sqlalchemy.orm.session import Session

import moe
from moe.core.config import Config
from moe.core.library.album import Album
from moe.core.library.extra import Extra
from moe.core.library.music_item import MusicItem
from moe.core.library.track import Track

log = logging.getLogger(__name__)

TRACK_FILE_FMT = "{track_num} - {title}.{file_ext}"  # noqa: FS003


@moe.hookimpl
def add_config_validator(settings: dynaconf.base.LazySettings):
    """Validate move plugin configuration settings."""
    settings.validators.register(
        dynaconf.Validator("MOVE.LIBRARY_PATH", must_exist=True, default="~/Music")
    )


@moe.hookimpl
def post_add(config: Config, session: Session, item: MusicItem):
    """Copies `item` to the library_path specified in the config.

    Also will format the path of the item's copied according to `track_path_fmt`.
    This hook is run after an item is added to the music library.

    Args:
        config: Moe config.
        session: Current db session.
        item: Item to be copied.
    """
    if isinstance(item, Album):
        album_dir = _create_album_dir(config, item)
    if isinstance(item, Track):
        album_dir = _create_album_dir(config, item.album_obj)

    _copy_item(item, album_dir)
    session.merge(item)


def _copy_item(item: MusicItem, album_dir: pathlib.Path):
    """Copies and formats the destination of a MusicItem."""
    if isinstance(item, Album):
        _copy_album(item, album_dir)
    elif isinstance(item, Track):
        # Copy the entire album to ensure there's only a single existing album path.
        _copy_album(item.album_obj, album_dir)


def _create_album_dir(config: Config, album: Album) -> pathlib.Path:
    """Creates and formats an Album directory."""
    album_track = list(album.tracks)[0]

    album_dir_fmt = "{albumartist}/{album} ({year})"  # noqa; FS003
    library_path = pathlib.Path(config.settings.move.library_path)
    album_dir = library_path / album_dir_fmt.format(
        albumartist=album_track.albumartist,
        album=album_track.album,
        year=album_track.year,
    )

    album_dir.mkdir(parents=True, exist_ok=True)
    return album_dir


def _copy_album(album: Album, album_dir: pathlib.Path):
    """Copies an Album to ``album_dir``.

    Overwrites any files at the destination.

    Args:
        album: Album to copy.
        album_dir: Album directory destination.
    """
    log.info(f"Copying album '{album.path}' to '{album_dir}'")
    for track in album.tracks:
        _copy_track(track, album_dir)

    for extra in album.extras:
        _copy_extra(extra, album_dir)

    album.path = album_dir


def _copy_track(track: Track, album_dir: pathlib.Path):
    """Copies and formats the destination of a single track.

    Overwrites any file at the destination.

    Note:
        The track path should contain, at a minimum, the album artist, album title,
        year, and track number to ensure uniqueness.

    Args:
        track: Track to copy.
        album_dir: Album directory destination.
    """
    track_filename = TRACK_FILE_FMT.format(
        track_num=track.track_num, title=track.title, file_ext=track.file_ext
    )
    track_dest = album_dir / track_filename
    log.info(f"Copying track '{track.path}' to '{track_dest}'")

    shutil.copyfile(track.path, track_dest)

    track.filename = track_filename


def _copy_extra(extra: Extra, album_dir: pathlib.Path):
    """Copies and formats the destination of an album extra file.

    Overwrites any file at the destination.

    Args:
        extra: Extra to copy.
        album_dir: Album directory to copy the extra to.
    """
    extra_dest = album_dir / extra.filename
    log.info(f"Copying extra '{extra}' to '{extra_dest}'")

    shutil.copyfile(extra.path, extra_dest)
