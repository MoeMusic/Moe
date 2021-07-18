"""Alters the location of files in your library.

The `move` plugin provides the following features:
 * ``move`` command to "consolidate" or move items in the library to reflect changes in
    your configuration.
 * Any items added to the library will be copied to the location set by
    ``library_path`` in your configuration file.
 * Automatically moves any items as their path configurations change due to field
    changes. For example, if you have a track at ``track_title.mp3``, and you change
    the title to ``new_track_title``, the track file will be automatically moved to
    ``new_track_title.mp3``.

This plugin is enabled by default.
"""

import argparse
import logging
import shutil
from contextlib import suppress
from pathlib import Path
from typing import List

import dynaconf
import sqlalchemy as sa
from sqlalchemy.orm.session import Session
from unidecode import unidecode

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
        dynaconf.Validator("MOVE.ASCIIFY_PATHS", must_exist=True, default=False)
    )
    settings.validators.register(
        dynaconf.Validator("MOVE.LIBRARY_PATH", must_exist=True, default="~/Music")
    )


@moe.hookimpl
def add_command(cmd_parsers: argparse._SubParsersAction):  # noqa: WPS437
    """Adds the ``move`` command to Moe's CLI."""
    move_parser = cmd_parsers.add_parser(
        "move",
        aliases=["mv"],
        description="Moves items in the library according to the user configuration.",
        help="move items in the library",
    )
    move_parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="display what will be moved without actually moving the items",
    )
    move_parser.set_defaults(func=_parse_args)


def _parse_args(
    config: Config, session: sa.orm.session.Session, args: argparse.Namespace
):
    """Parses the given commandline arguments.

    Items will be moved according to the given user configuration.

    Args:
        config: Configuration in use.
        session: Current db session.
        args: Commandline arguments to parse.

    Raises:
        SystemExit: Invalid field or field_value term format.
    """
    albums = session.execute(sa.select(Album)).scalars().all()

    if args.dry_run:
        dry_run_str = ""
        for dry_album in albums:
            album_dest = _fmt_album_path(dry_album, config)
            if album_dest != dry_album.path:
                dry_run_str += f"\n{dry_album.path}\n\t-> {album_dest}"

            # temporarily set the album's path so track/extra dests use the right
            # album directory
            sa.orm.attributes.set_committed_value(dry_album, "path", album_dest)

            for dry_track in dry_album.tracks:
                track_dest = _fmt_track_path(dry_track, config)
                if track_dest != dry_track.path:
                    dry_run_str += f"\n{dry_track.path}\n\t-> {track_dest}"
            for dry_extra in dry_album.extras:
                extra_dest = _fmt_extra_path(dry_extra, config)
                if extra_dest != dry_extra.path:
                    dry_run_str += f"\n{dry_extra.path}\n\t-> {extra_dest}"

        if dry_run_str:
            print(dry_run_str.lstrip())  # noqa: WPS421
    else:
        for album in albums:
            _move_album(album, _fmt_album_path(album, config), config)


@moe.hookimpl(trylast=True)
def edit_new_items(config: Config, session: Session, items: List[LibItem]):
    """Sets the path of any new or altered items in the library.

    Once the items are successfully added to the library, they will be moved on the
    filesystem in the ``process_new_items`` hook implementation.

    Args:
        config: Moe config.
        session: Currrent db session.
        items: Any new or changed items that have been committed to the database
            during the current session.

    """
    for item in items:
        if isinstance(item, Album):
            item.path = _fmt_album_path(item, config)
            for track in item.tracks:
                track.path = _fmt_track_path(track, config)
            for extra in item.extras:
                extra.path = _fmt_extra_path(extra, config)
        elif isinstance(item, Extra):
            item.path = _fmt_extra_path(item, config)
        elif isinstance(item, Track):
            item.path = _fmt_track_path(item, config)


@moe.hookimpl
def process_new_items(config: Config, session: Session, items: List[LibItem]):
    """Moves altered or new items after they are added to the library."""
    # since moving an album involves moving all of its tracks and extras, it's possible
    # to move a track or extra twice if both it and its album exist in ``items_to_move``
    albums_to_move = [item for item in items if isinstance(item, Album)]
    for item in items:
        if isinstance(item, Album):
            _process_new_item(item, config)
        elif isinstance(item, (Extra, Track)) and item.album_obj not in albums_to_move:
            _process_new_item(item, config)


def _process_new_item(item: LibItem, config: Config):
    """Moves an item that has been added to the database."""
    item_path_history = sa.inspect(item).attrs.path.history
    assert len(item_path_history.deleted) <= 1  # noqa: S101 # not sure if always True
    try:
        og_path = item_path_history.deleted[0]
    except IndexError:
        return

    # check if the item was already moved
    if not og_path.exists():
        return

    new_path = item.path  # the item's path is the path we need to move to

    # Temporarily (will not change in the db) set the item's path to the original
    # path so the move functions know where to find the files on the filesystem.
    sa.orm.attributes.set_committed_value(item, "path", og_path)

    if isinstance(item, Album):
        for track_or_extra in item.tracks + item.extras:  # type: ignore
            _process_new_item(track_or_extra, config)
        _move_album(item, new_path, config)
    elif isinstance(item, Track):
        _move_track(item, new_path)
    elif isinstance(item, Extra):
        _move_extra(item, new_path)


@moe.hookimpl(trylast=True)
def pre_add(config: Config, session: Session, album: Album):
    """Copies and formats the path of an album prior to it being added."""
    _copy_album(album, _fmt_album_path(album, config), config)


########################################################################################
# Format paths
########################################################################################
def _fmt_album_path(album: Album, config: Config) -> Path:
    """Returns a formatted album directory according to the user configuration.

    An album directory should contain, at a minimum, the album artist, title, and year
    to ensure uniqueness.

    Args:
        album: Album used to format the directory.
        config: Moe config.

    Returns:
        Formatted album directory under the config ``library_path``.
    """
    library_path = Path(config.settings.move.library_path).expanduser()
    album_dir_name = f"{album.artist}/{album.title} ({album.year})"

    album_path = library_path / album_dir_name

    if config.settings.move.asciify_paths:
        album_path = Path(unidecode(str(album_path)))

    return album_path


def _fmt_extra_path(extra: Extra, config: Config) -> Path:
    """Returns a formatted extra path according to the user configuration.

    Args:
        extra: Extra used to format the path.
        config: Moe config.

    Returns:
        Formatted extra path under its album path.
    """
    extra_path = extra.album_obj.path / extra.path.name

    if config.settings.move.asciify_paths:
        extra_path = Path(unidecode(str(extra_path)))

    return extra_path


def _fmt_track_path(track: Track, config: Config) -> Path:
    """Returns a formatted track path according to the user configuration.

    The track path should contain, at a minimum, the track number and
    disc (if more than one) to ensure uniqueness.

    Args:
        track: Track used to format the path.
        config: Moe config.

    Returns:
        Formatted track path under its album path.
    """
    disc_dir_name = ""
    if track.disc_total > 1:
        disc_dir_name = f"Disc {track.disc:02}"
    disc_dir = track.album_obj.path / disc_dir_name

    track_filename = f"{track.track_num:02} - {track.title}{track.path.suffix}"

    track_path = disc_dir / track_filename

    if config.settings.move.asciify_paths:
        track_path = Path(unidecode(str(track_path)))

    return track_path


########################################################################################
# Copy
########################################################################################
def _copy_album(album: Album, dest: Path, config: Config):
    """Copies an album to a given destination.

    Overwrites any existing files. Will create ``dest`` if it does not already exist.
    Copying an album will also copy all of it's tracks and extras.

    Args:
        album: Album to copy
        dest: Destination to copy the album to.
        config: Moe config.
    """
    log.info(f"Copying album from '{album.path}' to '{dest}'.")
    if album.path != dest:
        dest.mkdir(parents=True, exist_ok=True)
        album.path = dest

    for track in album.tracks:
        _copy_track(track, _fmt_track_path(track, config))

    for extra in album.extras:
        _copy_extra(extra, _fmt_extra_path(extra, config))


def _copy_track(track: Track, dest: Path):
    """Copies a track to a given destination.

    Overwrites any existing file at ``dest`` and creates any missing parent directories.

    Args:
        track: Track to copy.
        dest: Destination file path to copy the track to.
    """
    if dest == track.path:
        return

    log.info(f"Copying track from '{track.path}' to '{dest}'.")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(track.path, dest)

    track.path = dest


def _copy_extra(extra: Extra, dest: Path):
    """Copies an extra to a given destination.

    Overwrites any existing file at ``dest`` and creates any missing parent directories.

    Args:
        extra: Extra to copy.
        dest: Destination file path to copy the extra to.
    """
    if dest == extra.path:
        return

    log.info(f"Copying extra from '{extra.path}' to '{dest}'.")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(extra.path, dest)

    extra.path = dest


########################################################################################
# Move
########################################################################################
def _move_album(album: Album, dest: Path, config: Config):
    """Moves an album to a given destination.

    Overwrites any existing files. Will create ``dest`` if it does not already exist.
    Moving an album will also move all of it's tracks and extras.

    Args:
        album: Album to move.
        dest: Destination to move the album to.
        config: Moe config.
    """
    log.info(f"Moving album from '{album.path}' to '{dest}'.")
    old_album_dir = album.path
    if album.path != dest:
        dest.mkdir(parents=True, exist_ok=True)
        album.path = dest

    for track in album.tracks:
        _move_track(track, _fmt_track_path(track, config))

    for extra in album.extras:
        _move_extra(extra, _fmt_extra_path(extra, config))

    # remove any empty leftover directories
    for old_child in old_album_dir.rglob("*"):
        with suppress(OSError):
            old_child.rmdir()
    with suppress(OSError):
        old_album_dir.rmdir()
    for old_parent in old_album_dir.parents:
        with suppress(OSError):
            old_parent.rmdir()


def _move_track(track: Track, dest: Path):
    """Moves a track to a given destination.

    Overwrites any existing file at ``dest`` and creates any missing parent directories.

    Args:
        track: Track to move.
        dest: Destination file path to move the track to.
    """
    if dest == track.path:
        return

    log.info(f"Moving track from '{track.path}' to '{dest}'.")
    dest.parent.mkdir(parents=True, exist_ok=True)
    track.path.replace(dest)

    track.path = dest


def _move_extra(extra: Extra, dest: Path):
    """Moves an extra to a given destination.

    Overwrites any existing file at ``dest`` and creates any missing parent directories.

    Args:
        extra: Extra to move.
        dest: Destination file path to move the extra to.
    """
    if dest == extra.path:
        return

    log.info(f"Moving extra from '{extra.path}' to '{dest}'.")
    dest.parent.mkdir(parents=True, exist_ok=True)
    extra.path.replace(dest)

    extra.path = dest
