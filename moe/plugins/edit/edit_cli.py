"""Adds the ``edit`` command to the cli."""

import argparse
import logging

import moe
import moe.cli
from moe.plugins import edit
from moe.query import QueryError, query

log = logging.getLogger("moe.cli.edit")


@moe.hookimpl
def add_command(cmd_parsers: argparse._SubParsersAction):
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
        parents=[moe.cli.query_parser],
        epilog=epilog_help,
    )
    edit_parser.add_argument(
        "fv_terms", metavar="FIELD=VALUE", nargs="+", help="set FIELD to VALUE"
    )
    edit_parser.set_defaults(func=_parse_args)


def _parse_args(args: argparse.Namespace):  # noqa: C901
    """Parses the given commandline arguments.

    Args:
        args: Commandline arguments to parse.

    Raises:
        SystemExit: Invalid query, no items found to edit, or invalid field or
            field_value term format.
    """
    try:
        items = query(args.query, query_type=args.query_type)
    except QueryError as err:
        log.error(err)
        raise SystemExit(1) from err

    if not items:
        log.error("No items found to edit.")
        raise SystemExit(1)

    error_count = 0
    for term in args.fv_terms:
        try:
            field, value = term.split("=")
        except ValueError:
            log.error(f"Invalid FIELD=VALUE format. [{term=!r}]")
            error_count += 1
            continue

        for item in items:
            try:
                edit.edit_item(item, field, value)
            except edit.EditError as err:
                log.error(err)
                error_count += 1

    if error_count:
        raise SystemExit(1)
