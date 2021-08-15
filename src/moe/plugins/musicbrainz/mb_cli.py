"""Integrates musicbrainz with the import prompt."""


from typing import List, Optional

import questionary
from sqlalchemy.orm.session import Session

import moe
import moe.cli
from moe.config import Config
from moe.library.album import Album
from moe.plugins import moe_import
from moe.plugins import musicbrainz as moe_mb


@moe.hookimpl
def add_import_prompt_choice(prompt_choices: List[moe.cli.PromptChoice]):
    """Adds the ``apply`` and ``abort`` prompt choices to the user prompt."""
    prompt_choices.append(
        moe.cli.PromptChoice(
            title="Enter Musicbrainz ID",
            shortcut_key="m",
            func=_enter_id,
        )
    )


def _enter_id(
    config: Config,
    session: Session,
    old_album: Album,
    new_album: Album,
) -> Optional[Album]:
    """Re-run the add prompt with the inputted Musibrainz release."""
    mb_id = questionary.text("Enter Musicbrainz ID: ").ask()

    album = moe_mb.get_album_by_id(mb_id)

    return moe_import.import_prompt(config, session, old_album, album)
