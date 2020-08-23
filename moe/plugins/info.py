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
    config: Config, session: sqlalchemy.orm.session.Session, args: argparse.Namespace,
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

    print(get_infos(items), end="")  # noqa: WPS421


def get_infos(items: List[library.MusicItem]):
    """Get information for a list of items."""
    out_str = ""
    for item in items:
        out_str += get_info(item)

        if item is not items[-1]:
            out_str += "\n"

    return out_str


def get_info(item: library.MusicItem) -> str:
    """Returns information about an item."""
    info_fields = dict(vars(item))  # noqa: WPS421

    if isinstance(item, library.Track):
        info_fields["album"] = item.album.title
        info_fields["albumartist"] = item.album.artist

    info_fields = dict(sorted(info_fields.items()))  # sort by field

    item_info = ""
    for field, value in info_fields.items():  # noqa: WPS421
        # don't print private fields or empty fields
        if value and not field.startswith("_"):
            item_info += f"{field}: {value}\n"

    return item_info
