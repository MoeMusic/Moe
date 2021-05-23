"""Any operations regarding altering the location of files in the library."""

import logging
import pathlib
import shutil

import dynaconf
from sqlalchemy.orm.session import Session

import moe
from moe.core.config import Config
from moe.core.library.album import Album
from moe.core.library.music_item import MusicItem
from moe.core.library.track import Track

log = logging.getLogger(__name__)


@moe.hookimpl
def add_config_validator(settings: dynaconf.base.LazySettings):
    """Validate move plugin configuration settings."""
    settings.validators.register(
        dynaconf.Validator("LIBRARY_PATH", must_exist=True, default="~/Music")
    )


@moe.hookimpl
def post_add(config: Config, session: Session, item: MusicItem):
    """Copies `item` to the library_path specified in the config.

    Also will format the path of the item's copied according to `track_path_fmt`.
    This hook is run after an item is added to the music library.

    Args:
        config: moe config
        session: Current db session.
        item: Item to be copied.
    """
    root_dest = pathlib.Path(config.settings.library_path).expanduser()
    if isinstance(item, Track):
        _copy_track(session, item, root_dest)
    elif isinstance(item, Album):
        _copy_album(session, item, root_dest)


def _copy_track(session, track: Track, root: pathlib.Path):
    """Copies and formats the destination of a single track.

    The track will overwrite anything that currently exists at the destination path.

    Note:
        The track path should contain, at a minimum, the album artist, album title,
        year, and track number to ensure uniqueness.

    Args:
        session: Current db session.
        track: track to copy
        root: root folder to copy the track to
    """
    track_path_fmt = (
        f"{track.albumartist}/{track.album} ({track.year})/"
        f"{track.track_num} - {track.title}.{track.file_ext}"
    )
    track_dest = root / track_path_fmt

    log.info(f"Copying track '{track.path}' to '{track_dest}'")
    if track_dest.is_file():
        track_dest.unlink()
    track_dest.parents[0].mkdir(parents=True, exist_ok=True)
    shutil.copyfile(track.path, track_dest)  # type: ignore

    track.path = track_dest
    session.merge(track)


def _copy_album(session: Session, album: Album, root: pathlib.Path):
    """Copies and formats the destination of an album.

    Args:
        session: Current db session.
        album: Album to copy.
        root: Root folder to copy the album to.
    """
    for track in album.tracks:
        _copy_track(session, track, root)
