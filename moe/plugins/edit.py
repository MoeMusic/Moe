"""Edits music in the library."""

import argparse
import logging

import sqlalchemy

import moe
from moe.core import query
from moe.core.config import Config
from moe.core.library.track import LibItem

log = logging.getLogger(__name__)


class EditError(Exception):
    """Error editing an item in the library."""


@moe.hookimpl
def add_command(cmd_parsers: argparse._SubParsersAction):  # noqa: WPS437
    """Adds the ``edit`` command to Moe's CLI."""
    epilog_help = """
    The FIELD=VALUE argument sets a track's field or an album's field if an album query
    is specified with the `-a` option. If the specified field supports multiple values,
    then you can separate those values with a semicolon. For example,
    `genre=hip hop;pop`.
    """

    add_parser = cmd_parsers.add_parser(
        "edit",
        description="Edits music in the library.",
        help="edit music in the library",
        parents=[query.query_parser],
        epilog=epilog_help,
    )
    add_parser.add_argument(
        "fv_terms", metavar="FIELD=VALUE", nargs="+", help="set FIELD to VALUE"
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
        for item in items:
            try:
                _edit_item(item, term)
            except EditError as exc:
                log.error(exc)
                error_count += 1

    if error_count:
        raise SystemExit(1)


def _edit_item(item: LibItem, term: str):
    """Sets a LibItem's ``field`` to ``value``.

    Args:
        item: LibItem to edit.
        term: FIELD=VALUE format used to set the item's ``field`` to ``value``.

    Raises:
        EditError: ``field`` is not a valid attribute or is not editable.
    """
    try:
        field, value = term.split("=")
    except ValueError:
        raise EditError(f"Invalid FIELD=VALUE format: {term}")

    try:
        attr = getattr(item, field)
    except AttributeError:
        raise EditError(f"'{field}' is not a valid field.")

    non_editable_fields = ["file_ext", "path"]
    if field in non_editable_fields:
        raise EditError(f"'{field}' is not an editable field.")

    if isinstance(attr, str):
        setattr(item, field, value)
    elif isinstance(attr, int):
        setattr(item, field, int(value))
    elif isinstance(
        attr, sqlalchemy.ext.associationproxy._AssociationSet  # noqa: WPS437
    ):
        set_value = {lv.strip() for lv in value.split(";")}
        setattr(item, field, set_value)
