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
    track = library.Track(path=pathlib.Path(args.path))

    log.info("Adding track '%s' to the library.", track)
    session.add(track)
