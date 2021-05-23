"""Adds music to the library."""

import argparse
import logging
import pathlib
from typing import List, Optional

import mediafile
import pluggy
from sqlalchemy.orm.session import Session

import moe
from moe.core.config import Config
from moe.core.library.album import Album
from moe.core.library.music_item import MusicItem
from moe.core.library.track import Track

log = logging.getLogger(__name__)


class AddError(Exception):
    """Error adding an item to the library."""


class Hooks:
    """Add hooks."""

    @staticmethod
    @moe.hookspec
    def post_add(config: Config, item: MusicItem):
        """Provides the MusicItem that was added to the library."""


@moe.hookimpl
def moe_addhooks(pluginmanager: pluggy.manager.PluginManager):
    """Register add hooks to be used by other plugins."""
    from moe.plugins.add import Hooks  # noqa: WPS433, WPS442

    pluginmanager.add_hookspecs(Hooks)


@moe.hookimpl
def addcommand(cmd_parsers: argparse._SubParsersAction):  # noqa: WPS437
    """Adds a new `add` command to moe."""
    add_parser = cmd_parsers.add_parser(
        "add", description="Adds music to the library.", help="add music to the library"
    )
    add_parser.add_argument(
        "paths", nargs="+", help="dir to add an album or file to add a track"
    )
    add_parser.set_defaults(func=parse_args)


def parse_args(config: Config, session: Session, args: argparse.Namespace):
    """Parses the given commandline arguments.

    This is the plugin entry point from the commandline. Tracks can be added as files
    or albums as directories. Assumes a given directory is a single album.

    Args:
        config: Configuration in use.
        session: Current session.
        args: Commandline arguments to parse.

    Raises:
        SystemExit: Path given does not exist.
    """
    paths = [pathlib.Path(arg_path) for arg_path in args.paths]

    error_count = 0
    for path in paths:
        if path.exists():
            item_added = _add_item(path)
            if item_added:
                config.pluginmanager.hook.post_add(config=config, item=item_added)
            else:
                error_count += 1
        else:
            log.error(f"Path not found: {path}")
            error_count += 1

    if error_count:
        raise SystemExit(1)


def _add_item(item_path: pathlib.Path) -> Optional[MusicItem]:
    """Adds an item to the library.

    Args:
        item_path: Filesystem path of the item.

    Returns:
        The MusicItem added.
    """
    item_added: MusicItem
    try:
        if item_path.is_file():
            item_added = _add_track(item_path)
        elif item_path.is_dir():
            item_added = _add_album(item_path)
    except AddError as exc:
        log.error(exc)
        return None

    return item_added


def _add_album(album_path: pathlib.Path) -> Album:
    """Add an album to the library from a given directory.

    Args:
        album_path: Filesystem path of the album directory to add.

    Returns:
        Album added.

    Raises:
        AddError: Unable to add the album to the library.
    """
    log.info(f"Adding album to the library: {album_path}")
    album_tracks: List[Track] = []
    for file_path in album_path.rglob("*"):
        log.info(f"Adding track to the library: {file_path}")
        try:
            album_tracks.append(Track.from_tags(path=file_path))
        except (TypeError, mediafile.UnreadableFileError) as exc:
            log.warning(f"Could not add track to album: {str(exc)}")

    if not album_tracks:
        raise AddError(f"No tracks found in album: {album_path}")

    albums = [track._album_obj for track in album_tracks]  # noqa: WPS437

    # ensure every track belongs to the same album
    if albums.count(albums[0]) != len(albums):  # checks if each album is the same
        raise AddError(
            f"Not all tracks in '{album_path}' share the same album attributes."
        )

    # merge tracks into a single album
    album = albums[0]  # we already ensured this list is just multiple of the same album
    for track in album_tracks:
        album.tracks.add(track)

    album.add_to_db()
    return album


def _add_track(track_path: pathlib.Path) -> Track:
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
    except (TypeError, mediafile.UnreadableFileError) as init_exc:
        raise AddError(init_exc) from init_exc

    track.add_to_db()
    return track
