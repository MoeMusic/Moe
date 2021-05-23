"""Any operations regarding altering the location of files in the library."""

import logging
import pathlib
import shutil

import dynaconf

import moe
from moe.core.config import Config
from moe.core.library.album import Album
from moe.core.library.music_item import MusicItem
from moe.core.library.track import Track

log = logging.getLogger(__name__)


class MoveError(Exception):
    """Error moving an item."""


# TODO: add file extension to track and include in path format
@moe.hookimpl
def add_config_validator(settings: dynaconf.base.LazySettings):
    """Validate move plugin configuration settings."""
    settings.validators.register(
        dynaconf.Validator("LIBRARY_PATH", must_exist=True, default="~/Music")
    )


@moe.hookimpl
def post_add(config: Config, item: MusicItem):
    """Copies `item` to the library_path specified in the config.

    Also will format the path of the item's copied according to `track_path_fmt`.
    This hook is run after an item is added to the music library.

    Args:
        config: moe config
        item: Item to be copied.
    """
    root_dest = pathlib.Path(config.settings.library_path).expanduser()
    if isinstance(item, Track):
        _move_track(item, root_dest)
    elif isinstance(item, Album):
        _move_album(item, root_dest)


def _move_track(track: Track, root: pathlib.Path):
    """Copies and formats the destination of a single track.

    The track will overwrite anything that currently exists at the destination path.

    Note:
        The track path should contain, at a minimum, the album artist, album title,
        year, and track number to ensure uniqueness.

    Args:
        track: track to copy
        root: root folder to copy the track to
    """
    track_path_fmt = (
        f"{track.albumartist}/{track.album} ({track.year})/"
        f"{track.track_num} - {track.title}"
    )
    track_dest = root / track_path_fmt

    if track_dest.is_file():
        track_dest.unlink()
    track_dest.parents[0].mkdir(parents=True, exist_ok=True)
    shutil.copyfile(track.path, track_dest)  # type: ignore

    track.path = track_dest
    track.add_to_db()


def _move_album(album: Album, root: pathlib.Path):
    """Copies and formats the destination of an album.

    Args:
        album: Album to copy.
        root: Root folder to copy the album to.
    """
    for track in album.tracks:
        _move_track(track, root)
