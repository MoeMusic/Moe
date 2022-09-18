"""Import prompt."""

import logging

import pluggy

import moe
import moe.cli
from moe import config
from moe.library.album import Album
from moe.util.cli import PromptChoice, choice_prompt, fmt_item_changes
from moe.util.core import get_matching_tracks

log = logging.getLogger("moe.cli.import")

__all__ = ["AbortImport", "import_prompt"]


class AbortImport(Exception):  # noqa: N818
    """Used to abort the import process."""


class Hooks:
    """Import plugin cli hook specifications."""

    @staticmethod
    @moe.hookspec
    def add_import_prompt_choice(prompt_choices: list[PromptChoice]):
        """Add a user input choice to the import prompt.

        ``func`` should return the album to be added to the library (or ``None`` if no
        album should be added) and will be supplied the following keyword arguments:

            * ``old_album``: Old album with no changes applied.
            * ``new_album``: New album consisting of all the new changes.

        Args:
            prompt_choices: List of prompt choices. To add a prompt choice, simply
                append it to this list.

        Example:
            Inside your hook implementation::

                prompt_choices.append(
                    PromptChoice(
                        title="Abort", shortcut_key="x", func=_abort_changes
                    )
                )
        """


@moe.hookimpl
def add_hooks(pm: pluggy.manager.PluginManager):
    """Registers `import` cli hookspecs to Moe."""
    from moe.plugins.moe_import.import_cli import Hooks

    pm.add_hookspecs(Hooks)


@moe.hookimpl
def process_candidates(old_album: Album, candidates):
    """Use the import prompt to select and process the imported candidate albums."""
    if candidates:
        chosen_candidate = candidates[0]
        log.debug(
            "Candidate album chosen for import prompt. "
            f"[candidate={chosen_candidate!r}]"
        )
        try:
            import_prompt(old_album, chosen_candidate)
        except AbortImport as err:
            log.debug(err)
            raise SystemExit(0) from err


@moe.hookimpl
def add_import_prompt_choice(prompt_choices: list[PromptChoice]):
    """Adds the ``apply`` and ``abort`` prompt choices to the user prompt."""
    prompt_choices.append(
        PromptChoice(title="Apply changes", shortcut_key="a", func=_apply_changes)
    )
    prompt_choices.append(
        PromptChoice(title="Abort", shortcut_key="x", func=_abort_changes)
    )


def import_prompt(
    old_album: Album,
    new_album: Album,
):
    """Runs the interactive prompt for the given album changes.

    Args:
        old_album: Album to be added. Any changes will be applied to this album.
        new_album: New album with all metadata changes. Will be compared against
            ``old_album``.

    Raises:
        AbortImport: Import prompt was aborted by the user.
    """
    log.debug("Running import prompt. [{old_album=!r}, {new_album=!r}]")

    print(fmt_item_changes(old_album, new_album))

    prompt_choices: list[PromptChoice] = []
    config.CONFIG.pm.hook.add_import_prompt_choice(prompt_choices=prompt_choices)

    prompt_choice = choice_prompt(prompt_choices)
    prompt_choice.func(old_album, new_album)


def _apply_changes(
    old_album: Album,
    new_album: Album,
):
    """Applies the album changes."""
    log.debug("Applying changes from import prompt.")

    for old_track, new_track in get_matching_tracks(old_album, new_album):
        if not old_track and new_track:
            new_album.tracks.remove(new_track)  # missing track
        elif old_track and not new_track:
            old_album.tracks.remove(old_track)  # unmatched track
        elif (
            old_track
            and new_track
            and old_album.get_track(new_track.track_num, new_track.disc) != old_track
        ):
            # matchup track and disc numbers of matches to ensure they merge properly
            old_track.track_num = new_track.track_num
            old_track.disc = new_track.disc

    old_album.merge(new_album, overwrite=True)


def _abort_changes(
    old_album: Album,
    new_album: Album,
):
    """Aborts the album changes."""
    raise AbortImport("Import prompt aborted; no changes made.")
