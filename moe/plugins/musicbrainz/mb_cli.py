"""Integrates musicbrainz with the import prompt.

The ``musicbrainz`` cli plugin provides the following functionality:

* Ability to search for a specific musicbrainz ID when importing an item.
* `mbcol` command to sync a musicbrainz collection with items in the library.
"""

import argparse
import logging

import questionary
from sqlalchemy.orm.session import Session

import moe
import moe.plugins.musicbrainz as moe_mb
from moe import moe_import
from moe.library import Album, Extra, Track
from moe.util.cli import PromptChoice, cli_query, query_parser

__all__: list[str] = []

log = logging.getLogger("moe.cli.mb")


@moe.hookimpl
def add_command(cmd_parsers: argparse._SubParsersAction) -> None:
    """Adds the ``mbcol`` command to Moe's CLI."""
    mbcol_parser = cmd_parsers.add_parser(
        "mbcol",
        description="Set a musicbrainz collection to a query.",
        help="sync a musicbrainz collection",
        parents=[query_parser],
    )
    col_option_group = mbcol_parser.add_mutually_exclusive_group()
    col_option_group.add_argument(
        "--add",
        action="store_true",
        help="add items to a collection",
    )
    col_option_group.add_argument(
        "--remove",
        action="store_true",
        help="remove items from a collection",
    )
    mbcol_parser.set_defaults(func=_parse_args)


def _parse_args(session: Session, args: argparse.Namespace) -> None:
    """Parses the given commandline arguments.

    Args:
        session: Library db session.
        args: Commandline arguments to parse.

    Raises:
        SystemExit: Invalid query given, or no items to remove.
    """
    items = cli_query(session, args.query, query_type=args.query_type)

    releases = set()
    for item in items:
        release_id: str | None = None
        if isinstance(item, (Extra, Track)):
            release_id = item.album.custom.get("mb_album_id")
        elif isinstance(item, Album):
            release_id = item.custom.get("mb_album_id")

        if release_id:
            releases.add(release_id)

    if not releases:
        log.error("Queried items don't contain any musicbrainz releases to sync.")
        raise SystemExit(1)

    if args.add:
        moe_mb.add_releases_to_collection(releases)
    elif args.remove:
        moe_mb.rm_releases_from_collection(releases)
    else:
        moe_mb.set_collection(releases)


@moe.hookimpl
def add_candidate_prompt_choice(prompt_choices: list[PromptChoice]) -> None:
    """Adds a choice to the import prompt to allow specifying a mb id."""
    prompt_choices.append(
        PromptChoice(title="Enter Musicbrainz ID", shortcut_key="m", func=_enter_id)
    )


def _enter_id(new_album: Album, candidate: moe_import.CandidateAlbum) -> None:
    """Re-run the add prompt with the inputted Musibrainz release."""
    mb_id = questionary.text("Enter Musicbrainz ID: ").ask()

    log.debug(f"Running import prompt for a selected musicbrainz release. [{mb_id=!r}]")

    candidate = moe_mb.get_candidate_by_id(new_album, mb_id)
    moe_import.import_prompt(new_album, candidate)
