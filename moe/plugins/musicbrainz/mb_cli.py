"""Integrates musicbrainz with the import prompt.

The ``musicbrainz`` cli plugin provides the following functionality:

* Ability to search for a specific musicbrainz ID when importing an item.
"""


import logging

import questionary

import moe
import moe.cli
from moe.library import Album
from moe.plugins import moe_import
from moe.plugins import musicbrainz as moe_mb
from moe.util.cli import PromptChoice

log = logging.getLogger("moe.cli.mb")


@moe.hookimpl
def add_import_prompt_choice(prompt_choices: list[PromptChoice]):
    """Adds the ``apply`` and ``abort`` prompt choices to the user prompt."""
    prompt_choices.append(
        PromptChoice(title="Enter Musicbrainz ID", shortcut_key="m", func=_enter_id)
    )


def _enter_id(
    old_album: Album,
    new_album: Album,
):
    """Re-run the add prompt with the inputted Musibrainz release."""
    mb_id = questionary.text("Enter Musicbrainz ID: ").ask()

    log.debug(
        f"Re-running import prompt for different musicbrainz release. [{mb_id=!r}]"
    )

    album = moe_mb.get_album_by_id(mb_id)

    moe_import.import_prompt(old_album, album)
