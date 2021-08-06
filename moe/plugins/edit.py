"""Edits music in the library.

Editing items is done through the ``edit_item()`` function.

Note:
    This plugin is enabled by default.
"""

import argparse
import datetime
import logging
import re
import sys

import sqlalchemy

import moe
from moe.core import query
from moe.core.config import Config
from moe.core.library.lib_item import LibItem

__all__ = ["edit_item", "EditError"]

log = logging.getLogger("moe.edit")


class EditError(Exception):
    """Error editing an item in the library."""


@moe.hookimpl
def add_command(cmd_parsers: argparse._SubParsersAction):  # noqa: WPS437
    """Adds the ``edit`` command to Moe's CLI."""
    epilog_help = """
    The FIELD=VALUE argument sets a track's field, an album's field if an album query is
    specified with `-a`, or an extra's field if an extra query is specified with `-e`.
    If the specified field supports multiple values, then you can separate those values
    with a semicolon. For example, `genre=hip hop;pop`.

    For more information on editing, see the documentation
    https://mrmoe.readthedocs.io/en/latest/plugins/edit.html
    """

    edit_parser = cmd_parsers.add_parser(
        "edit",
        description="Edits music in the library.",
        help="edit music in the library",
        parents=[query.query_parser],
        epilog=epilog_help,
    )
    edit_parser.add_argument(
        "fv_terms", metavar="FIELD=VALUE", nargs="+", help="set FIELD to VALUE"
    )
    edit_parser.set_defaults(func=_parse_args)


def _parse_args(
    config: Config, session: sqlalchemy.orm.session.Session, args: argparse.Namespace
):
    """Parses the given commandline arguments.

    Args:
        config: Configuration in use.
        session: Current db session.
        args: Commandline arguments to parse.

    Raises:
        SystemExit: Invalid field or field_value term format.
    """
    if args.album:
        query_type = "album"
    elif args.extra:
        query_type = "extra"
    else:
        query_type = "track"
    items = query.query(args.query, session, query_type=query_type)

    error_count = 0
    for term in args.fv_terms:
        # term: FIELD=VALUE format used to set the item's `field` to `value`
        try:
            field, value = term.split("=")
        except ValueError:
            log.error(f"Invalid FIELD=VALUE format: {term}")
            error_count += 1
            continue

        for item in items:
            try:
                edit_item(item, field, value)
            except EditError as exc:
                log.error(exc)
                error_count += 1

    if error_count:
        raise SystemExit(1)


def edit_item(item: LibItem, field: str, value: str):
    """Sets a LibItem's ``field`` to ``value``.

    Args:
        item: Library item to edit.
        field: Item field to edit.
        value: Value to set the item's field to.

    Raises:
        EditError: ``field`` is not a valid attribute or is not editable.
    """
    try:
        attr = getattr(item, field)
    except AttributeError:
        raise EditError(
            f"'{field}' is not a valid {type(item).__name__.lower()} field."
        )

    non_editable_fields = ["path"]
    if field in non_editable_fields:
        raise EditError(f"'{field}' is not an editable field.")

    log.debug(f"Editing '{field}' to '{value}' for '{item}'.")
    if isinstance(attr, str):
        setattr(item, field, value)
    elif isinstance(attr, int):
        setattr(item, field, int(value))
    elif isinstance(attr, datetime.date):
        if (sys.version_info.major, sys.version_info.minor) < (3, 7):
            if not re.match(
                r"^\d{4}-([0]\d|1[0-2])-([0-2]\d|3[01])$", value  # noqa: FS003
            ):
                raise EditError("Date must be in format YYYY-MM-DD")
            date = value.split("-")
            setattr(
                item, field, datetime.date(int(date[0]), int(date[1]), int(date[2]))
            )
        else:
            try:
                setattr(item, field, datetime.date.fromisoformat(value))
            except ValueError:
                raise EditError("Date must be in format YYYY-MM-DD")
    else:
        raise EditError(f"Editing field of type '{type(attr)}' not supported.")
