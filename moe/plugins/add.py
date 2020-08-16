"""Adds music to the library."""

import argparse
import logging
import pathlib

import sqlalchemy

import moe
from moe.core import library
from moe.core.config import Config

log = logging.getLogger(__name__)


@moe.hookimpl
def addcommand(cmd_parsers: argparse._SubParsersAction):
    """Adds a new `add` command to moe."""
    add_parser = cmd_parsers.add_parser(
        "add", description="Adds music to the library.", help="add music to the library"
    )
    add_parser.add_argument("path", help="path to the music you want to add")
    add_parser.set_defaults(func=parse_args)


def parse_args(
    config: Config, session: sqlalchemy.orm.session.Session, args: argparse.Namespace,
):
    """Parse the given commandline arguments."""
    try:
        track = library.Track(path=pathlib.Path(args.path))
    except FileNotFoundError:
        log.error("Unable to add '%s' to the library; file does not exist.", args.path)
    else:
        # create our own session so we can do proper error handling
        session.close()
        try:
            with library.session_scope() as session:
                log.info("Adding track '%s' to the library.", track)
                session.add(track)
        except sqlalchemy.exc.IntegrityError:
            log.error(
                "Unable to add '%s'; file already exists in the library.", args.path
            )
