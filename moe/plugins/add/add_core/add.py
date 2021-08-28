"""Adds music to the library.

This module provides the main entry point into the add process via ``add_item()``.
"""

import logging
from pathlib import Path

import mediafile
import pluggy

import moe
from moe.config import Config, MoeSession
from moe.library.album import Album
from moe.library.extra import Extra
from moe.library.lib_item import LibItem
from moe.library.track import Track, TrackError

__all__ = ["add_item", "AddError"]

log = logging.getLogger("moe.add")


class Hooks:
    """Add plugin hook specifications."""

    @staticmethod
    @moe.hookspec
    def pre_add(config: Config, item: LibItem):
        """Provides an item prior to it being added to the library.

        Use this hook if you wish to change the item's metadata.

        Args:
            config: Moe config.
            item: Library item being added.

        See Also:
            * The :meth:`post_add` hook for any post-processing operations.
            * The :meth:`~moe.config.Hooks.edit_new_items` hook.
              The difference between them is that the :meth:`pre_add` hook will only
              operate on an `add` operation, while the
              :meth:`~moe.config.Hooks.edit_new_items` hook will run anytime an item is
              changed or added.
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
    from moe.plugins.add.add_core.add import Hooks  # noqa: WPS433, WPS442

    plugin_manager.add_hookspecs(Hooks)


class AddError(Exception):
    """Error adding an item to the library."""


def add_item(config: Config, item_path: Path):
    """Adds a LibItem to the library from a given path.

    Args:
        config: Moe config.
        item_path: Filesystem path of the item.

    Raises:
        AddError: Unable to add the item to the library.
    """
    session = MoeSession()

    item: LibItem
    if item_path.is_file():
        item = _add_track(item_path)
        album = item.album_obj
    elif item_path.is_dir():
        item = _add_album(item_path)
        album = item
    else:
        raise AddError(f"Path not found: {item_path}")

    album.merge(album.get_existing(), overwrite_album_info=False)
    config.plugin_manager.hook.pre_add(config=config, item=item)
    item = session.merge(item)
    config.plugin_manager.hook.post_add(config=config, item=item)


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

    album_tracks = []
    extra_paths = []
    album_file_paths = [path for path in album_path.rglob("*") if path.is_file()]
    for file_path in album_file_paths:
        try:
            album_tracks.append(Track.from_tags(path=file_path, album_path=album_path))
        except mediafile.UnreadableFileError:
            extra_paths.append(file_path)
        except TrackError as err:
            log.error(err)

    if not album_tracks:
        raise AddError(f"No tracks found in album: {album_path}")

    albums = [track.album_obj for track in album_tracks]

    # ensure each track belongs to the same album
    for discovered_album in albums:
        if albums[0].is_unique(discovered_album):
            raise AddError(
                f"Not all tracks in '{album_path}' share the same album attributes."
            )

    album = albums[0]
    for track in album_tracks:
        log.info(f"Adding track file to the library: {track.path}")
        album.tracks.append(track)

    for extra_path in extra_paths:
        log.info(f"Adding extra file to the library: {extra_path}")
        Extra(extra_path, album)

    return album


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
        track = Track.from_tags(path=track_path)
    except (TrackError, mediafile.UnreadableFileError) as init_exc:
        raise AddError(init_exc) from init_exc

    return track
