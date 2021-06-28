"""Any operations regarding altering the location of files in the library."""

import logging
import shutil
from pathlib import Path

import dynaconf
from sqlalchemy.orm.session import Session

import moe
from moe.core.config import Config
from moe.core.library.album import Album
from moe.core.library.extra import Extra
from moe.core.library.lib_item import LibItem
from moe.core.library.track import Track

log = logging.getLogger(__name__)

TRACK_FILE_FMT = "{track_num} - {title}.{file_ext}"  # noqa: FS003


@moe.hookimpl
def add_config_validator(settings: dynaconf.base.LazySettings):
    """Validate move plugin configuration settings."""
    settings.validators.register(
        dynaconf.Validator("MOVE.LIBRARY_PATH", must_exist=True, default="~/Music")
    )


@moe.hookimpl(trylast=True)
def post_args(config: Config, session: Session):
    """Alters the location of any changed or new items in the session.

    This hook is run after the CLI arguments have been executed.

    Args:
        config: Moe config.
        session: Currrent db session.
    """
    for item in session.new.union(session.dirty):
        if isinstance(item, LibItem):
            _alter_item_loc(config, item)


def _alter_item_loc(config: Config, item: LibItem):
    """Alters the location of an item according to the given configuration.

    By default, the item will be copied, overwriting any existing files.

    Args:
        config: Moe config.
        item: Item to be moved.
    """
    if isinstance(item, Album):
        album_dir = _create_album_dir(config, item)
    elif isinstance(item, Track):
        album_dir = _create_album_dir(config, item.album_obj)
    else:
        return

    _copy_item(item, album_dir)


def _copy_item(item: LibItem, album_dir: Path):
    """Copies and formats the destination of a LibItem."""
    if isinstance(item, Album):
        _copy_album(item, album_dir)
    elif isinstance(item, Track):
        # copy the entire album to ensure there's only a single existing album path
        _copy_album(item.album_obj, album_dir)


def _create_album_dir(config: Config, album: Album) -> Path:
    """Creates and formats an Album directory."""
    album_track = album.tracks[0]

    album_dir_fmt = "{albumartist}/{album} ({year})"  # noqa; FS003
    library_path = Path(config.settings.move.library_path).expanduser()
    album_dir = library_path / album_dir_fmt.format(
        albumartist=album_track.albumartist,
        album=album_track.album,
        year=album_track.year,
    )

    album_dir.mkdir(parents=True, exist_ok=True)
    return album_dir


def _copy_album(album: Album, album_dir: Path):
    """Copies an Album to ``album_dir``.

    Overwrites any files at the destination.

    Args:
        album: Album to copy.
        album_dir: Album directory destination.
    """
    for track in album.tracks:
        _copy_track(track, album_dir)

    for extra in album.extras:
        _copy_extra(extra, album_dir)

    album.path = album_dir


def _copy_track(track: Track, album_dir: Path):
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

    if track_dest == track.path:
        return

    log.info(f"Copying track '{track.path}' to '{track_dest}'")
    shutil.copyfile(track.path, track_dest)

    track.path = track_dest


def _copy_extra(extra: Extra, album_dir: Path):
    """Copies and formats the destination of an album extra file.

    Overwrites any file at the destination.

    Args:
        extra: Extra to copy.
        album_dir: Album directory to copy the extra to.
    """
    extra_dest = album_dir / extra.path.name

    if extra_dest == extra.path:
        return

    log.info(f"Copying extra '{extra}' to '{extra_dest}'")
    shutil.copyfile(extra.path, extra_dest)

    extra.path = extra_dest
