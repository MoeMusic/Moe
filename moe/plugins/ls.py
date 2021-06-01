"""Lists music in the library."""

import argparse

import sqlalchemy

import moe
from moe.core import query
from moe.core.config import Config


@moe.hookimpl
def add_command(cmd_parsers: argparse._SubParsersAction):  # noqa: WPS437
    """Adds the ``ls`` command to Moe's CLI."""
    add_parser = cmd_parsers.add_parser(
        "ls",
        aliases=["list"],
        description="Lists music in the library.",
        help="list music in the library",
        parents=[query.query_parser],
    )
    add_parser.set_defaults(func=parse_args)


def parse_args(
    config: Config, session: sqlalchemy.orm.session.Session, args: argparse.Namespace
):
    """Parses the given commandline arguments.

    Args:
        config: Configuration in use.
        session: Current db session.
        args: Commandline arguments to parse.

    Raises:
        SystemExit: Query returned no tracks.
    """
    items = query.query(args.query, session, args.album)

    if not items:
        raise SystemExit(1)

    for item in items:
        print(item)  # noqa: WPS421
