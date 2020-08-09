"""Adds music to the library."""

import argparse
import pathlib

import moe
from moe.lib import library


@moe.hookimpl
def addcommand(cmd_parsers: argparse._SubParsersAction):
    """Adds a new `add` command to moe."""
    add_parser = cmd_parsers.add_parser("add", help="add music to the library")
    add_parser.add_argument("path", help="path to the music you want to add")
    add_parser.set_defaults(func=parse_args)


def parse_args(config, session, args):
    """Parse the given commandline arguments."""
    track = library.Track(path=pathlib.Path(args.path))

    session.add(track)
