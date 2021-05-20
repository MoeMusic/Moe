"""List music in the library."""

import argparse

import sqlalchemy

import moe
from moe.core import query


@moe.hookimpl
def addcommand(cmd_parsers: argparse._SubParsersAction):  # noqa: WPS437
    """Adds a new `ls` command to moe.

    Args:
        cmd_parsers: contains all the sub-command parsers
    """
    add_parser = cmd_parsers.add_parser(
        "ls",
        aliases=["list"],
        description="Lists music from the library.",
        help="list music from the library",
        parents=[query.query_parser],
    )
    add_parser.set_defaults(func=parse_args)


def parse_args(session: sqlalchemy.orm.session.Session, args: argparse.Namespace):
    """Parses the given commandline arguments.

    Args:
        session: Current session.
        args: Commandline arguments to parse.

    Raises:
        SystemExit: Query returned no tracks.
    """
    items = query.query(args.query, session, args.album)

    if not items:
        raise SystemExit(1)

    for item in items:
        print(item)  # noqa: WPS421
