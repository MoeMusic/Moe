"""Core api for moving items."""

import logging
import re
import shutil
from contextlib import suppress
from pathlib import Path
from typing import Union

import dynaconf
from unidecode import unidecode

import moe
from moe.config import Config
from moe.library.album import Album
from moe.library.extra import Extra
from moe.library.lib_item import LibItem
from moe.library.track import Track

__all__ = ["copy_item", "fmt_item_path", "move_item"]

log = logging.getLogger("moe.move")


@moe.hookimpl
def add_config_validator(settings: dynaconf.base.LazySettings):
    """Validate move plugin configuration settings."""
    default_album_path = "{album.artist}/{album.title} ({album.year})"
    default_extra_path = "{extra.filename}"
    default_track_path = (
        "{f'Disc {track.disc:02}' if track.disc_total > 1 else ''}/"
        "{track.track_num:02} - {track.title}{track.path.suffix}"
    )

    settings.validators.register(
        dynaconf.Validator("MOVE.ASCIIFY_PATHS", default=False)
    )
    settings.validators.register(
        dynaconf.Validator("MOVE.ALBUM_PATH", default=default_album_path)
    )
    settings.validators.register(
        dynaconf.Validator("MOVE.EXTRA_PATH", default=default_extra_path)
    )
    settings.validators.register(
        dynaconf.Validator("MOVE.TRACK_PATH", default=default_track_path)
    )


@moe.hookimpl
def post_add(config: Config, item: LibItem):
    """Copies and formats the path of an item after it has been added to the library."""
    # copy the whole album in case album attributes have changed
    if isinstance(item, Album):
        album = item
    elif isinstance(item, (Extra, Track)):
        album = item.album_obj
    else:
        raise NotImplementedError

    copy_item(config, album)


########################################################################################
# Format paths
########################################################################################
def fmt_item_path(config: Config, item: LibItem) -> Path:
    """Returns a formatted item path according to the user configuration.

    Args:
        config: Moe config.
        item: Library item used to format the directory.

    Returns:
        Formatted item path under the config ``library_path``.

    Raises:
        NotImplementedError: Unknown item.
    """
    if isinstance(item, Album):
        new_path = _fmt_album_path(config, item)
    elif isinstance(item, Extra):
        new_path = _fmt_extra_path(config, item)
    elif isinstance(item, Track):
        new_path = _fmt_track_path(config, item)
    else:
        raise NotImplementedError

    if config.settings.move.asciify_paths:
        new_path = Path(unidecode(str(new_path)))

    return new_path


def _fmt_album_path(config: Config, album: Album) -> Path:
    """Returns a formatted album directory according to the user configuration.

    An album directory should contain, at a minimum, the album artist, title, and year
    to ensure uniqueness.

    Args:
        config: Moe config.
        album: Album used to format the directory.

    Returns:
        Formatted album directory under the config ``library_path``.
    """
    library_path = Path(config.settings.library_path).expanduser()
    album_path = _eval_path_template(config.settings.move.album_path, album)

    return library_path / album_path


def _fmt_extra_path(config: Config, extra: Extra) -> Path:
    """Returns a formatted extra path according to the user configuration."""
    album_path = _fmt_album_path(config, extra.album_obj)
    extra_path = _eval_path_template(config.settings.move.extra_path, extra)

    return album_path / extra_path


def _fmt_track_path(config: Config, track: Track) -> Path:
    """Returns a formatted track path according to the user configuration.

    The track path should contain, at a minimum, the track number and
    disc (if more than one) to ensure uniqueness.

    Args:
        track: Track used to format the path.
        config: Moe config.

    Returns:
        Formatted track path under its album path.
    """
    album_path = _fmt_album_path(config, track.album_obj)
    track_path = _eval_path_template(config.settings.move.track_path, track)

    return album_path / track_path


def _eval_path_template(template, lib_item) -> str:
    """Evaluates and sanitizes a path template.

    Args:
        template: Path template.
            See `_lazy_fstr_item()` for more info on accepted f-string templates.
        lib_item: Library item associated with the template.

    Returns:
        Evaluated path.

    Raises:
        NotImplementedError: You discovered a new library item!
    """
    template_parts = template.split("/")
    sanitized_parts = []
    for template_part in template_parts:
        path_part = _lazy_fstr_item(template_part, lib_item)
        sanitized_part = _sanitize_path_part(path_part)
        if sanitized_part:
            sanitized_parts.append(sanitized_part)

    return "/".join(sanitized_parts)


def _lazy_fstr_item(template: str, lib_item: LibItem) -> str:
    """Evalutes the given f-string template for a specific library item.

    Args:
        template: f-string template to evaluate.
            All library items should have their own template and refer to variables as:
                Album: album (e.g. {album.title}, {album.artist})
                Track: track (e.g. {track.title}, {track.artist})
                Extra: extra (e.g. {extra.filename}
        lib_item: Library item referenced in the template.


    Example:
        The default path template for an album is::

            {album.artist}/{album.title} ({album.year})

    Returns:
        Evaluated f-string.

    Raises:
        NotImplementedError: You discovered a new library item!
    """
    # add the appropriate library item to the scope
    if isinstance(lib_item, Album):
        album = lib_item  # noqa: F841
    elif isinstance(lib_item, Track):
        track = lib_item  # noqa: F841
    elif isinstance(lib_item, Extra):
        extra = lib_item  # noqa: F841
    else:
        raise NotImplementedError

    return eval(f'f"""{template}"""')


def _sanitize_path_part(path_part: str) -> str:
    """Sanitizes a part of a path to be compatible with most filesystems.

    Note:
        Only sub-paths of the library path will be affected.

    Args:
        path_part: Path part to sanitize. Must be a single 'part' of a path, i.e. no /
            separators.

    Returns:
        Path part with all the replacements applied.
    """
    PATH_REPLACE_CHARS = {
        r"^\.": "_",  # leading '.' (hidden files on Unix)
        r'[<>:"\?\*\|\\/]': "_",  # <, >, : , ", ?, *, |, \, / (Windows reserved chars)
        r"\.$": "_",  # trailing '.' (Windows restriction)
        r"\s+$": "",  # trailing whitespace (Windows restriction)
    }

    for regex, replacement in PATH_REPLACE_CHARS.items():
        path_part = re.sub(regex, replacement, path_part)

    return path_part


########################################################################################
# Copy
########################################################################################
def copy_item(config: Config, item: LibItem):
    """Copies an item to a destination as determined by the user configuration.

    Overwrites any existing files. Will create the destination if it does not already
    exist.

    Args:
        item: Library item to copy.
        config: Moe config.
    """
    if isinstance(item, Album):
        _copy_album(config, item)
    elif isinstance(item, (Extra, Track)):
        _copy_file_item(config, item)


def _copy_album(config: Config, album: Album):
    """Copies an album to a destination as determined by the user configuration.

    Copying an album will also copy all of it's tracks and extras.

    Args:
        album: Album to copy
        config: Moe config.
    """
    dest = fmt_item_path(config, album)

    log.info(f"Copying album from '{album.path}' to '{dest}'.")
    if album.path != dest:
        dest.mkdir(parents=True, exist_ok=True)
        album.path = dest

    for track in album.tracks:
        _copy_file_item(config, track)

    for extra in album.extras:
        _copy_file_item(config, extra)


def _copy_file_item(config: Config, item: Union[Extra, Track]):
    """Copies an extra or track to a destination as determined by the user config."""
    dest = fmt_item_path(config, item)
    if dest == item.path:
        return

    log.info(f"Copying {type(item).__name__.lower()} from '{item.path}' to '{dest}'.")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(item.path, dest)

    item.path = dest


########################################################################################
# Move
########################################################################################
def move_item(config: Config, item: LibItem):
    """Moves an item to a destination as determined by the user configuration.

    Overwrites any existing files. Will create the destination if it does not already
    exist.

    Args:
        item: Library item to move.
        config: Moe config.
    """
    if isinstance(item, Album):
        _move_album(config, item)
    elif isinstance(item, (Extra, Track)):
        _move_file_item(config, item)


def _move_album(config: Config, album: Album):
    """Moves an album to a given destination.

    - Overwrites any existing files.
    - Creates the destination if it does not already exist.
    - Tracks and extras are also moved.
    - Empty leftover directories will be removed.

    Args:
        album: Album to move.
        config: Moe config.
    """
    dest = fmt_item_path(config, album)
    old_album_dir = album.path

    log.info(f"Moving album from '{album.path}' to '{dest}'.")
    if album.path != dest:
        dest.mkdir(parents=True, exist_ok=True)
        album.path = dest

    for track in album.tracks:
        _move_file_item(config, track)

    for extra in album.extras:
        _move_file_item(config, extra)

    # remove any empty leftover directories
    for old_child in old_album_dir.rglob("*"):
        with suppress(OSError):
            old_child.rmdir()
    with suppress(OSError):
        old_album_dir.rmdir()
    for old_parent in old_album_dir.parents:
        with suppress(OSError):
            old_parent.rmdir()


def _move_file_item(config: Config, item: Union[Extra, Track]):
    """Moves an extra or track to a destination as determined by the user config."""
    dest = fmt_item_path(config, item)
    if dest == item.path:
        return

    log.info(f"Moving {type(item).__name__.lower()} from '{item.path}' to '{dest}'.")
    dest.parent.mkdir(parents=True, exist_ok=True)
    item.path.replace(dest)

    item.path = dest
