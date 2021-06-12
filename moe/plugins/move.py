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

ALBUM_DIR_FMT = "{albumartist}/{album} ({year})"  # noqa; FS003
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
    _copy_item(session, item, pathlib.Path(config.settings.move.library_path))


def _copy_item(session, item: MusicItem, root: pathlib.Path):
    """Copies and formats the destination of a MusicItem."""
    if isinstance(item, Album):
        _copy_album(session, item, root)
    elif isinstance(item, Track):
        _copy_track(session, item, root)


def _copy_album(session: Session, album: Album, root: pathlib.Path):
    """Copies and formats the destination of an album.

    Args:
        session: Current db session.
        album: Album to copy.
        root: Root folder to copy the album to.
    """
    for track in album.tracks:
        _copy_track(session, track, root)

    for extra in album.extras:
        _copy_extra(session, extra, root)

    session.merge(album)


def _copy_track(session: Session, track: Track, root: pathlib.Path):
    """Copies and formats the destination of a single track.

    The track will overwrite any conflicting filenames.

    Note:
        The track path should contain, at a minimum, the album artist, album title,
        year, and track number to ensure uniqueness.

    Args:
        session: Current db session.
        track: Track to copy.
        root: Root folder to copy the track to.
    """
    track_dest = (
        root
        / ALBUM_DIR_FMT.format(
            albumartist=track.albumartist, album=track.album, year=track.year
        )
        / TRACK_FILE_FMT.format(
            track_num=track.track_num, title=track.title, file_ext=track.file_ext
        )
    )
    log.info(f"Copying track '{track.path}' to '{track_dest}'")

    if track_dest.is_file():
        track_dest.unlink()
    track_dest.parents[0].mkdir(parents=True, exist_ok=True)
    shutil.copyfile(track.path, track_dest)  # type: ignore

    track.path = track_dest
    session.merge(track)


def _copy_extra(session: Session, extra: Extra, album_dir: pathlib.Path):
    """Copies and formats the destination of an album extra file.

    The extra will overwrite any conflicting filenames.

    Args:
        session: Current db session.
        extra: Extra to copy.
        album_dir: Album directory to copy the extra to.
    """
    extra_dest = album_dir / extra.path.name  # type: ignore
    log.info(f"Copying extra '{extra}' to '{extra_dest}'")

    if extra_dest.is_file():
        extra_dest.unlink()
    extra_dest.parents[0].mkdir(parents=True, exist_ok=True)
    shutil.copyfile(extra.path, extra_dest)

    extra.path = extra_dest
    session.merge(extra)
