"""Any operations regarding altering the location of files in the library."""

import functools
import logging
import shutil
from contextlib import suppress
from pathlib import Path
from typing import Any, List, Optional

import dynaconf
import sqlalchemy
from sqlalchemy.orm.session import Session

import moe
from moe.core.config import Config
from moe.core.library.album import Album
from moe.core.library.extra import Extra
from moe.core.library.lib_item import LibItem
from moe.core.library.track import Track

__all__: List[str] = []

log = logging.getLogger("moe.move")


@moe.hookimpl
def add_config_validator(settings: dynaconf.base.LazySettings):
    """Validate move plugin configuration settings."""
    settings.validators.register(
        dynaconf.Validator("MOVE.LIBRARY_PATH", must_exist=True, default="~/Music")
    )


@moe.hookimpl
def register_db_listener(config: Config, session: Session):
    """Sets item paths before they are flushed then moves them after a successful flush.

    Args:
        config: Moe config.
        session: Current db session.
    """
    sqlalchemy.event.listen(
        session,
        "before_flush",
        functools.partial(_set_sess_item_paths, config=config),
    )
    sqlalchemy.event.listen(session, "after_flush", _move_flushed_items)


def _set_sess_item_paths(
    session: Session,
    flush_context: sqlalchemy.orm.UOWTransaction,
    instances: Optional[Any],
    config: Config,
):
    """Sets the path of any new or altered items in the session.

    Once the session is successfully flushed, the items will be moved on the filesystem.

    Args:
        session: Current db session.
        flush_context: sqlalchemy obj which handles the details of the flush.
        instances: List of objects passed to the ``flush()`` method.
        config: Moe config.
    """
    library_path = Path(config.settings.move.library_path).expanduser()

    for item in session.dirty.union(session.new):
        if isinstance(item, Album):
            item.path = _get_album_dir(item, library_path)
            for track in item.tracks:
                track.path = _get_track_path(track)
            for extra in item.extras:
                extra.path = _get_extra_path(extra)
        elif isinstance(item, Track):
            item.path = _get_track_path(item)
        elif isinstance(item, Extra):
            item.path = _get_extra_path(item)


def _move_flushed_items(session: Session, flush_context: sqlalchemy.orm.UOWTransaction):
    """Moves altered or new items after they are successfully flushed to the db."""
    # since moving an album involves moving all of its tracks and extras, it's possible
    # to move a track or extra twice if both it and its album exist in ``items_to_move``
    items_to_move = session.new.union(session.dirty)
    albums_to_move = [item for item in items_to_move if isinstance(item, Album)]
    for item in items_to_move:
        if isinstance(item, Album):
            _move_flushed_item(item)
        elif isinstance(item, (Extra, Track)) and item.album_obj not in albums_to_move:
            _move_flushed_item(item)


def _move_flushed_item(item: LibItem):
    """Moves an item that has been flushed to the database."""
    item_path_history = sqlalchemy.inspect(item).attrs.path.history
    assert len(item_path_history.deleted) <= 1  # noqa: S101 # not sure if always True
    try:
        og_path = item_path_history.deleted[0]
    except IndexError:
        return

    new_path = item.path  # the item's path is the path we need to move to

    # Temporarily (will not change in the db) set the item's path to the original
    # path so the move functions know where to find the files on the filesystem.
    sqlalchemy.orm.attributes.set_committed_value(item, "path", og_path)

    if isinstance(item, Album):
        for track_or_extra in item.tracks + item.extras:  # type: ignore
            _move_flushed_item(track_or_extra)
        _move_album(item, new_path)
    elif isinstance(item, Track):
        _move_track(item, new_path)
    elif isinstance(item, Extra):
        _move_extra(item, new_path)


@moe.hookimpl(trylast=True)
def pre_add(config: Config, session: Session, album: Album):
    """Copies and formats the path of an album prior to it being added."""
    library_path = Path(config.settings.move.library_path).expanduser()

    _copy_album(album, _get_album_dir(album, library_path))


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


def _get_extra_path(extra: Extra) -> Path:
    """Returns a formatted extra path."""
    return extra.album_obj.path / extra.path.name


def _get_track_path(track: Track) -> Path:
    """Returns a formatted track path.

    The track path should contain, at a minimum, the track number and
    disc (if more than one) to ensure uniqueness.

    Args:
        track: Track used to format the path.

    Returns:
        Formatted track path.
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
def _copy_album(album: Album, dest: Path):
    """Copies an album to a given destination.

    Overwrites any existing files. Will create ``dest`` if it does not already exist.
    Copying an album will also copy all of it's tracks and extras.

    Args:
        album: Album to copy
        dest: Destination to copy the album to.
    """
    if album.path == dest:
        return

    log.info(f"Copying album from '{album.path}' to '{dest}'.")
    album.path = dest

    album.path.mkdir(parents=True, exist_ok=True)

    for track in album.tracks:
        _copy_track(track)

    for extra in album.extras:
        _copy_extra(extra)


def _copy_track(track: Track, dest: Path = None):
    """Copies a track to a given or generated destination.

    Overwrites any existing files.

    Args:
        track: Track to copy.
        dest: Destination to copy the extra to. If not given, the destination will be
            generated by the track's attributes.
    """
    if not dest:
        dest = _get_track_path(track)

    if dest == track.path:
        return

    log.info(f"Copying track from '{track.path}' to '{dest}'.")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(track.path, dest)

    track.path = dest


def _copy_extra(extra: Extra, dest: Path = None):
    """Copies an extra to a given or generated destination.

    Overwrites any existing files.

    Args:
        extra: Extra to copy.
        dest: Destination to copy the extra to. If not given, the destination will be
            generated by the extra's attributes.
    """
    if not dest:
        dest = _get_extra_path(extra)

    if dest == extra.path:
        return

    log.info(f"Copying extra from '{extra.path}' to '{dest}'.")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(extra.path, dest)

    extra.path = dest


########################################################################################
# Move
########################################################################################
def _move_album(album: Album, dest: Path):
    """Moves an album to a given destination.

    Overwrites any existing files. Will create ``dest`` if it does not already exist.
    Moving an album will also move all of it's tracks and extras.

    Args:
        album: Album to move.
        dest: Destination to move the album to.
    """
    if album.path == dest:
        return

    log.info(f"Moving album from '{album.path}' to '{dest}'.")
    old_album_dir = album.path
    album.path = dest
    album.path.mkdir(parents=True, exist_ok=True)

    for track in album.tracks:
        _move_track(track)

    for extra in album.extras:
        _move_extra(extra)

    # remove any empty leftover directories
    for old_path in old_album_dir.rglob("*"):
        with suppress(OSError):
            old_path.rmdir()
    with suppress(OSError):
        old_album_dir.rmdir()


def _move_track(track: Track, dest: Path = None):
    """Moves a track to a given or generated destination.

    Overwrites any existing files.

    Args:
        track: Track to move.
        dest: Destination to move the track to. If not given, the destination will be
            generated by the track's attributes.
    """
    if not dest:
        dest = _get_track_path(track)

    if dest == track.path:
        return

    log.info(f"Moving track from '{track.path}' to '{dest}'.")
    dest.parent.mkdir(parents=True, exist_ok=True)

    track.path.replace(dest)

    track.path = dest


def _move_extra(extra: Extra, dest: Path = None):
    """Moves an extra to a given or generated destination.

    Overwrites any existing files.

    Args:
        extra: Extra to move.
        dest: Destination to move the extra to. If not given, the destination will be
            generated by the extra's attributes.
    """
    if not dest:
        dest = _get_extra_path(extra)

    if dest == extra.path:
        log.debug(f"dest: {dest}")
        return

    log.info(f"Moving extra from '{extra.path}' to '{dest}'.")
    dest.parent.mkdir(parents=True, exist_ok=True)
    extra.path.replace(dest)
    extra.path = dest
