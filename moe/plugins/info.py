"""Prints information about music in the library.

All fields and their values should be printed to stdout for any music queried.
"""

import argparse
import types
from typing import Any, List, OrderedDict, Union

import sqlalchemy

import moe
from moe.core import query
from moe.core.config import Config
from moe.core.library.album import Album
from moe.core.library.extra import Extra
from moe.core.library.lib_item import LibItem
from moe.core.library.track import Track


@moe.hookimpl
def add_command(cmd_parsers: argparse._SubParsersAction):  # noqa: WPS437
    """Adds the ``info`` command to Moe's CLI."""
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
        config: Configuration in use.
        session: Current db session.
        args: Commandline arguments to parse.

    Raises:
        SystemExit: Query returned no tracks.
    """
    if args.album:
        query_type = "album"
    elif args.extra:
        query_type = "extra"
    else:
        query_type = "track"
    items = query.query(args.query, session, query_type=query_type)

    if not items:
        raise SystemExit(1)

    print(_fmt_infos(items), end="")  # noqa: WPS421


def _fmt_infos(items: List[LibItem]):
    """Formats information for multiple items together."""
    out_str = ""
    for item in items:
        out_str += _fmt_info(item)

        if item is not items[-1]:
            out_str += "\n"

    return out_str


def _fmt_info(item: LibItem) -> str:
    """Formats the attribute/value pairs of an item into a str."""
    return "".join(f"{field}: {value}\n" for field, value in _item_dict(item).items())


def _item_dict(item: LibItem) -> "OrderedDict[str, Any]":
    """Represents a LibItem as a dictionary.

    Only relevant, non-empty attributes will be included in the dictionary.

    Args:
        item: Library item to represent

    Returns:
        Returns a dict representation of an Extra.
        It will be in the form { attribute: value } and is sorted by attribute.

    Raises:
        NotImplementedError: No ``dict()`` method has been implemented for the item.
    """
    if isinstance(item, (Track, Extra)):
        return _track_extra_dict(item)
    elif isinstance(item, Album):
        return _album_dict(item)

    raise NotImplementedError(f"``_item_dict()`` not yet implemented for {type(item)}")


def _album_dict(album: Album) -> "OrderedDict[str, Any]":
    """Represents an Album as a dictionary.

    The basis of an album's representation is the merged dictionary of its tracks.
    If different values are present for any given attribute among tracks, then
    the value becomes "Various". It also includes any extras, and removes any
    values that are guaranteed to be unique between tracks, such as track number.

    Args:
        album: Album.

    Returns:
        A dict representation of an Album.
        It will be in the form { attribute: value } and is sorted by attribute.
    """
    # access any element to set intial values
    track_list = list(album.tracks)  # easier to deal with a list for this func
    album_dict = _track_extra_dict(track_list[0])

    # compare rest of album against initial values
    for track in track_list[1:]:
        track_dict = _track_extra_dict(track)
        for key in {**track_dict, **album_dict}.keys():
            if album_dict.get(key) != track_dict.get(key):
                album_dict[key] = "Various"

    album_dict["extras"] = {str(extra.path) for extra in album.extras}

    # remove values that are always unique between tracks
    album_dict.pop("path")
    album_dict.pop("title")
    album_dict.pop("track_num")

    return album_dict


def _track_extra_dict(item: Union[Extra, Track]) -> "OrderedDict[str, Any]":
    """Represents a Item or an Extra as a dictionary.

    Only public attributes that are not empty will be included. We also remove any
    attributes that are not relevant to the music file e.g. sqlalchemy specific
    attributes.

    Args:
        item: Track or Extra.

    Returns:
        Returns a dict representation of a Item.
        It will be in the form { attribute: value } and is sorted by attribute.
    """
    item_dict = OrderedDict()
    for attr in dir(item):  # noqa: WPS421
        if not attr.startswith("_") and attr != "metadata" and attr != "registry":
            value = getattr(item, attr)
            if (
                value
                and not isinstance(value, types.MethodType)
                and not isinstance(value, types.FunctionType)
            ):
                item_dict[attr] = value

    return item_dict
