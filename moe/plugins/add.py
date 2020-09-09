"""Adds music to the library."""

import argparse
import logging
import pathlib

import mediafile
from sqlalchemy.orm.session import Session

import moe
from moe.core.config import Config
from moe.core.library.session import DbDupTrackError, session_scope
from moe.core.library.track import Track

log = logging.getLogger(__name__)


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

    Args:
        config: Configuration in use.
        session: Current session.
        args: Commandline arguments to parse.

    Raises:
        SystemExit: Path given does not exist.
    """
    paths = [pathlib.Path(arg_path) for arg_path in args.paths]

    for path in paths:
        if not path.exists():
            log.error(f"Path not found: {path}")
            raise SystemExit(1)

        _add_path(path)


def _add_path(path: pathlib.Path):
    """Add a given path to the library.

    Args:
        path: Path of the music to add. If a file, add as a track,
            if a directory, add as an album.

    Raises:
        SystemExit: Unable to add the given path to the library.
    """
    if path.is_file():
        try:
            _add_track(path)
        except (TypeError, mediafile.UnreadableFileError, DbDupTrackError):
            log.error(f"Unable to add track: {path}")
            raise SystemExit(1)


def _add_track(track_path: pathlib.Path):
    """Add a track to the library.

    The Track's attributes are populated from the tags read at `track_path`.

    Args:
        track_path: Path of track to add.

    Raises:
        TypeError: Required tags missing.
        mediafile.UnreadableFileError: `track_path` is not a valid track.
        DbDupTrackError: Duplicate track found in library.
    """
    log.info(f"Adding '{track_path}' to the library.")
    try:
        with session_scope() as add_session:
            track = Track.from_tags(path=track_path, session=add_session)

            add_session.add(track)
    except (TypeError, mediafile.UnreadableFileError) as exc:
        log.error(exc)
        raise
    except DbDupTrackError:
        log.error(f"Track already exists in library: {track}")
        raise
