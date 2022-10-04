"""Prints information about music in the library.

All fields and their values should be printed to stdout for any music queried.

Note:
    This plugin is enabled by default.
"""

import argparse
import logging
from collections import OrderedDict
from typing import Any

import moe
import moe.cli
from moe import config
from moe.library import Album, Extra, LibItem, Track
from moe.util.cli import cli_query, query_parser

__all__: list[str] = []

log = logging.getLogger("moe.cli.info")


@moe.hookimpl
def plugin_registration():
    """Depend on the cli plugin."""
    if not config.CONFIG.pm.has_plugin("cli"):
        config.CONFIG.pm.set_blocked("info")
        log.warning("The 'info' plugin requires the 'cli' plugin to be enabled.")


@moe.hookimpl
def add_command(cmd_parsers: argparse._SubParsersAction):
    """Adds the ``info`` command to Moe's CLI."""
    info_parser = cmd_parsers.add_parser(
        "info",
        description="Prints information about music in the library.",
        help="print info for music in the library",
        parents=[query_parser],
    )
    info_parser.set_defaults(func=_parse_args)


def _parse_args(args: argparse.Namespace):
    """Parses the given commandline arguments.

    Args:
        args: Commandline arguments to parse.

    Raises:
        SystemExit: Invalid query given, or no items found.
    """
    items = cli_query(args.query, query_type=args.query_type)

    print(_fmt_infos(items), end="")


def _fmt_infos(items: list[LibItem]):
    """Formats information for multiple items together."""
    out_str = ""
    for item in items:
        out_str += _fmt_info(item) + "\n"

        if item is not items[-1]:
            out_str += "\n"

    return out_str


def _fmt_info(item: LibItem) -> str:
    """Formats the attribute/value pairs of an item into a str."""
    if isinstance(item, Track):
        return _fmt_track_info(item)
    elif isinstance(item, Album):
        return _fmt_album_info(item)
    elif isinstance(item, Extra):
        return _fmt_extra_info(item)

    raise NotImplementedError


def _fmt_album_info(album: Album) -> str:
    """Formats an album's information for display."""
    base_dict = _get_base_dict(album)
    base_dict.pop("extras", None)
    base_dict.pop("tracks", None)
    base_info = "\n".join(
        f"{field}: {value}"
        for field, value in OrderedDict(sorted(base_dict.items())).items()
    )

    tracks = "\nTracks\n"
    tracks += "\n".join(track.title for track in sorted(album.tracks))

    extras = "\nExtras\n"
    extras += "\n".join(extra.path.name for extra in sorted(album.extras))

    return base_info + "\n" + tracks + "\n" + extras


def _fmt_extra_info(extra: Extra) -> str:
    """Formats a extra's information for display."""
    base_dict = _get_base_dict(extra)

    return "\n".join(
        f"{field}: {value}"
        for field, value in OrderedDict(sorted(base_dict.items())).items()
    )


def _fmt_track_info(track: Track) -> str:
    """Formats a track's information for display."""
    base_dict = OrderedDict(sorted(_get_base_dict(track).items()))
    base_dict.pop("album_obj", None)

    return "\n".join(
        f"{field}: {value}"
        for field, value in OrderedDict(sorted(base_dict.items())).items()
    )


def _get_base_dict(item: LibItem) -> dict[str, Any]:
    """Represents an item as a dictionary.

    Only public attributes that are not empty will be included. Also, any attributes
    that are not relevant to the user e.g. sqlalchemy specific attributes will
    be removed.

    Args:
        item: Library item.

    Returns:
        Returns a dict representation of an Item in the form { attribute: value }.
    """
    item_dict = {}
    for attr in sorted(item.fields):
        value = getattr(item, attr)
        if value:
            item_dict[attr] = value

    return item_dict
