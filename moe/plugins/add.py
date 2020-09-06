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
    add_parser.add_argument("path", help="path to the music you want to add")
    add_parser.set_defaults(func=parse_args)


def parse_args(config: Config, session: Session, args: argparse.Namespace):
    """Parses the given commandline arguments.

    Args:
        config: Configuration in use.
        session: Current session.
        args: Commandline arguments to parse.

    Raises:
        SystemExit: Could not add the given track to the library.
    """
    path = pathlib.Path(args.path)

    try:
        with session_scope() as add_session:
            track = Track.from_tags(path=path, session=add_session)

            log.info(f"Adding '{path}' to the library.")
            add_session.add(track)
    except mediafile.UnreadableFileError:
        log.error(f"Could not read '{path}'.")
        raise SystemExit(1)
    except DbDupTrackError:
        log.error(f"Track already exists in library: {track}")
        raise SystemExit(1)
