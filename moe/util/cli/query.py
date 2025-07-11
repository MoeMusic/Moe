"""CLI-specific query help functionality."""

from __future__ import annotations

import argparse
import logging
from typing import TYPE_CHECKING

from moe.query import QueryError, query

if TYPE_CHECKING:
    from sqlalchemy.orm.session import Session

    from moe.library import Album, Extra, Track

__all__ = ["cli_query", "query_parser"]

log = logging.getLogger("moe.cli")

query_parser = argparse.ArgumentParser(
    add_help=False, formatter_class=argparse.RawTextHelpFormatter
)
"""Argument parser for a query.

Passing this parser as a parent to your command allows your command to accept queries.

Example:
    .. code:: python

        ls_parser = cmd_parsers.add_parser(
            "list",
            description="Lists music in the library.",
            help="list music in the library",
            parents=[query_parser],
        )

Given parsed commandline arguments as ``args``, you can then access the given
query string as ``args.query`` and the query type as ``args.query_type``. Both options
can be passed directly to :meth:`moe.query.query` or :meth:`moe.util.cli.cli_query`.

See Also:
    `argparse parents documentation
    <https://docs.python.org/3/library/argparse.html#parents>`_
"""

query_parser.add_argument("query", help="query the library for matching tracks")

query_type_group = query_parser.add_mutually_exclusive_group()
query_type_group.add_argument(
    "-a",
    "--album",
    action="store_const",
    const="album",
    dest="query_type",
    help="query for matching albums",
)
query_type_group.add_argument(
    "-e",
    "--extra",
    action="store_const",
    const="extra",
    dest="query_type",
    help="query for matching extras",
)
query_parser.set_defaults(query_type="track")


def cli_query(
    session: Session, query_str: str, query_type: str
) -> list[Album] | list[Extra] | list[Track]:
    """Wrapper around the core query call, with some added cli error handling.

    Args:
        session: Library db session.
        query_str: Query string to parse. See the query docs for more info.
        query_type: Type of library item to return: either 'album', 'extra', or 'track'.

    Returns:
        All items matching the given query found in ``args``.

    Raises:
        SystemExit: QueryError or no items returned from the query.

    See Also:
        `The query docs <https://mrmoe.readthedocs.io/en/latest/query.html>`_
    """
    try:
        items = query(session, query_str, query_type)
    except QueryError as err:
        log.exception("Failed query.")
        raise SystemExit(1) from err

    if not items:
        log.error("No items found for given query.")
        raise SystemExit(1)

    return items
