"""Adds music to the library.

This module provides the main entry point into the add process via ``add_item()``.
"""

import logging
from pathlib import Path
from typing import List, Optional

import mediafile
import pluggy

import moe
from moe.config import Config, MoeSession
from moe.library.album import Album
from moe.library.extra import Extra
from moe.library.lib_item import LibItem
from moe.library.track import Track, TrackError

__all__ = ["AddAbortError", "AddError", "add_item"]

log = logging.getLogger("moe.add")


class Hooks:
    """Add plugin hook specifications."""

    @staticmethod
    @moe.hookspec
    def pre_add(config: Config, item: LibItem):
        """Provides an item prior to it being added to the library.

        Use this hook if you wish to change the item's metadata. You must also ensure
        there will be no conflicts with existing items in the database if you are
        altering any applicable, i.e. unique, fields.

        Args:
            config: Moe config.
            item: Library item being added.

        Note:
            Any UI application should have a way of detecting and resolving duplicate
            items prior to them being added to the database. You may consider
            implementing a ``hookwrapper`` to run conflict resolution code after the
            ``pre_add`` hook is complete, but before the item has been added to the db.

        See Also:
            * The :meth:`post_add` hook for any post-processing operations.
            * The :meth:`~moe.config.Hooks.edit_new_items` hook.
              The difference between them is that the :meth:`pre_add` hook will only
              operate on an `add` operation, while the
              :meth:`~moe.config.Hooks.edit_new_items` hook will run anytime an item is
              changed or added.
            * `Pluggy hook wrapper documention
              <https://pluggy.readthedocs.io/en/stable/#wrappers>`_
            * :meth:`~moe.library.lib_item.LibItem.get_existing` for detecting duplicate
              items.
        """

    @staticmethod
    @moe.hookspec
    def post_add(config: Config, item: LibItem):
        """Provides an item after it has been added to the library.

        Use this hook if you want to operate on an item after its metadata has been set.

        Args:
            config: Moe config.
            item: Library item added.

        See Also:
            * The :meth:`pre_add` hook if you wish to alter item metadata.
            * The :meth:`~moe.config.Hooks.process_new_items` hook.
              The difference between them is that the :meth:`post_add` hook will only
              operate on an `add` operation, while the
              :meth:`~moe.config.Hooks.process_new_items` hook will run anytime an item
              is changed or added.
        """


@moe.hookimpl
def add_hooks(plugin_manager: pluggy.manager.PluginManager):
    """Registers `add` hookspecs to Moe."""
    from moe.plugins.add.add_core.add import Hooks

    plugin_manager.add_hookspecs(Hooks)


class AddError(Exception):
    """Error adding an item to the library."""


class AddAbortError(Exception):
    """Add process has been aborted by the user."""


def add_item(config: Config, item_path: Path):
    """Adds a LibItem to the library from a given path.

    Args:
        config: Moe config.
        item_path: Filesystem path of the item.

    Raises:
        AddError: Unable to add the item to the library.
        NotImplementedError: Attempting to add an Extra.
    """
    session = MoeSession()

    item: LibItem
    if item_path.is_file():
        item = _add_track(item_path)
    elif item_path.is_dir():
        item = _add_album(item_path)
    else:
        raise AddError(f"Path not found: {item_path}")

    config.plugin_manager.hook.pre_add(config=config, item=item)

    _check_db_dups(item)
    item = session.merge(item)

    config.plugin_manager.hook.post_add(config=config, item=item)


def _add_track(track_path: Path) -> Track:
    """Add a track to the library from a given file.

    The Track's attributes are populated from the tags read at `track_path`.

    Args:
        track_path: Filesystem path of the track file to add.

    Returns:
        Track added.

    Raises:
        AddError: Unable to add the track to the library.
    """
    log.info(f"Adding track to the library: {track_path}")

    try:
        track = Track.from_path(path=track_path)
    except (TrackError, mediafile.UnreadableFileError) as init_exc:
        raise AddError(init_exc) from init_exc

    return track


def _add_album(album_path: Path) -> Album:
    """Add an album to the library from a given directory.

    Args:
        album_path: Filesystem path of the album directory to add.

    Returns:
        Album added.

    Raises:
        AddError: Unable to add the album to the library.
    """
    log.info(f"Adding album to the library: {album_path}")

    extra_paths = []
    album_file_paths = [path for path in album_path.rglob("*") if path.is_file()]
    album: Optional[Album] = None
    for file_path in album_file_paths:
        try:
            track = Track.from_path(path=file_path, album_path=album_path)
        except mediafile.UnreadableFileError:
            extra_paths.append(file_path)
        except TrackError as err:
            log.error(err)
        else:
            log.info(f"Adding track file to the library: {track.path}")
            if not album:
                album = track.album_obj
            else:
                album.tracks.append(track)

    if not album:
        raise AddError(f"No tracks found in album: {album_path}")

    try:
        _resolve_dup_tracks(album)
    except AddError as err:
        # Only log here as other plugins may still resolve the issue before the album
        # is added to the database. There is another check in case it wasn't resolved.
        log.warning(err)

    for extra_path in extra_paths:
        log.info(f"Adding extra file to the library: {extra_path}")
        Extra(album, extra_path)

    return album


def _resolve_dup_tracks(album: Album):
    """Tries to resolve any duplicate tracks due to incorrect or missing disc numbers.

    Args:
        album: Album to check.

    Raises:
        AddError: Unable to resolve the duplicates.
    """
    for track in album.tracks:
        if album.tracks.count(track) > 1:
            # Duplicate track found, potentially due to an incorrect disc tag.
            track.disc = _guess_disc(track)

    for track in album.tracks:
        if album.tracks.count(track) > 1:
            # Either we couldn't guess the disc or there's some other issue.
            raise AddError(f"Duplicate track found in album: {track}")


def _guess_disc(track: Track) -> int:
    """Attempts to guess the disc of a track based on it's path."""
    album = track.album_obj
    if track.path.parent == album.path:
        return 1

    # The track is in a subdirectory of the album, which are hopefully split by disc.
    disc_dirs: List[Path] = []
    for path in album.path.iterdir():
        if not path.is_dir():
            continue

        contains_tracks = False
        for album_track in album.tracks:
            if path in album_track.path.parents:
                contains_tracks = True

        if contains_tracks:
            disc_dirs.append(path)

    # Guess the disc by the order of the disc directory it appears in.
    for disc_num, disc_dir in enumerate(sorted(disc_dirs), start=1):
        if disc_dir in track.path.parents:
            return disc_num

    return 1


def _check_db_dups(item: LibItem):
    """Checks for any duplicates in the library for the given item and its relatives.

    Args:
        item: Library item to check.

    Raises:
        AddError: Duplicate found.
    """
    if item.get_existing():
        raise AddError(f"Duplicate item cannot be added to the db: {item}")
    elif isinstance(item, (Extra, Track)):
        if item.album_obj.get_existing():
            raise AddError(f"Item has duplicate album in the db: {item.album_obj}")
    elif isinstance(item, Album):
        for track in item.tracks:
            if track.get_existing():
                raise AddError(f"Album has duplicate track in the db: {track}")
        for extra in item.extras:
            if extra.get_existing():
                raise AddError(f"Album has duplicate extra in the db: {extra}")
