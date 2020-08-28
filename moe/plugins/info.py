"""Prints information about music in the library.

All fields and their values should be printed to stdout for any music queried.
"""

import argparse
from typing import List

import sqlalchemy

import moe
from moe.core import library, query
from moe.core.config import Config


@moe.hookimpl
def addcommand(cmd_parsers: argparse._SubParsersAction):  # noqa: WPS437
    """Adds a new `info` command to moe."""
    add_parser = cmd_parsers.add_parser(
        "info",
        description="Prints information about music in the library.",
        help="print info for music in the library",
        parents=[query.query_parser],
    )
    add_parser.set_defaults(func=parse_args)


def parse_args(
    config: Config, session: sqlalchemy.orm.session.Session, args: argparse.Namespace
):
    """Parses the given commandline arguments.

    Args:
        config: configuration in use
        session: current session
        args: commandline arguments to parse

    Raises:
        SystemExit: Query returned no tracks.
    """
    items = query.query(args.query, session, args.album)

    if not items:
        raise SystemExit(1)

    print(fmt_infos(items), end="")  # noqa: WPS421


def fmt_infos(items: List[library.MusicItem]):
    """Formats information for multiple items together."""
    out_str = ""
    for item in items:
        out_str += fmt_info(item)

        if item is not items[-1]:
            out_str += "\n"

    return out_str


def fmt_info(item: library.MusicItem) -> str:
    """Formats the attribute/value pairs of an item into a str."""
    return "".join(f"{field}: {value}\n" for field, value in item.to_dict().items())
