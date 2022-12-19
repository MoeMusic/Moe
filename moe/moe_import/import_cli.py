"""Import prompt."""

import functools
import logging
from typing import Optional, Union

import pluggy
from rich import box
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

import moe
import moe.cli
from moe import config
from moe.cli import console
from moe.library import Album, MetaAlbum, MetaTrack
from moe.moe_import.import_core import CandidateAlbum
from moe.util.cli import PromptChoice, choice_prompt
from moe.util.core import get_matching_tracks

log = logging.getLogger("moe.cli.import")

__all__ = ["candidate_prompt", "import_prompt"]


class AbortImport(Exception):
    """Used to abort the import process."""


class Hooks:
    """Import plugin cli hook specifications."""

    @staticmethod
    @moe.hookspec
    def add_candidate_prompt_choice(prompt_choices: list[PromptChoice]):
        """Add a user input choice to the candidate prompt.

        ``func`` will be supplied the following keyword arguments:

            * ``new_album``: Album being added to the library.
            * ``candidates``: Candidate albums with all the import changes.

        Args:
            prompt_choices: List of prompt choices. To add a prompt choice, simply
                append it to this list.

        Example:
            .. code:: python

                prompt_choices.append(
                    PromptChoice(
                        title="Abort", shortcut_key="x", func=_abort_changes
                    )
                )
        """

    @staticmethod
    @moe.hookspec
    def add_import_prompt_choice(prompt_choices: list[PromptChoice]):
        """Add a user input choice to the import prompt.

        ``func`` will be supplied the following keyword arguments:

            * ``new_album``: Album being added to the library.
            * ``candidate``: Candidate album with all the import changes.

        Args:
            prompt_choices: List of prompt choices. To add a prompt choice, simply
                append it to this list.

        Example:
            .. code:: python

                prompt_choices.append(
                    PromptChoice(
                        title="Abort", shortcut_key="x", func=_abort_changes
                    )
                )
        """


@moe.hookimpl
def add_hooks(pm: pluggy.manager.PluginManager):
    """Registers `import` cli hookspecs to Moe."""
    from moe.moe_import.import_cli import Hooks

    pm.add_hookspecs(Hooks)


@moe.hookimpl
def add_candidate_prompt_choice(prompt_choices: list[PromptChoice]):
    """Adds the ``abort`` prompt choice to the user prompt."""
    prompt_choices.append(
        PromptChoice(title="Abort", shortcut_key="x", func=_abort_changes)
    )


@moe.hookimpl
def add_import_prompt_choice(prompt_choices: list[PromptChoice]):
    """Adds the ``apply`` and ``abort`` prompt choices to the user prompt."""
    prompt_choices.append(
        PromptChoice(title="Apply changes", shortcut_key="a", func=_apply_changes)
    )
    prompt_choices.append(
        PromptChoice(title="Abort", shortcut_key="x", func=_abort_changes)
    )


@moe.hookimpl
def process_candidates(new_album: Album, candidates: list[CandidateAlbum]):
    """Use the import prompt to select and process the imported candidate albums."""
    if candidates:
        try:
            candidate_prompt(new_album, candidates[:5])
        except AbortImport as err:
            log.debug(err)
            raise SystemExit(0) from err


def candidate_prompt(new_album: Album, candidates: list[CandidateAlbum]):
    """Runs the interactive prompt for a user to select a candidate to import.

    Args:
        new_album: Album being added to the library.
        candidates: List of candidates to choose from.

    Raises:
        AbortImport: Import prompt was aborted by the user.
    """
    prompt_choices: list[PromptChoice] = []

    for num, candidate in enumerate(candidates, start=1):
        prompt_choices.append(
            PromptChoice(
                _fmt_candidate_info(candidate),
                str(num),
                functools.partial(_select_candidate, candidate_num=num - 1),
            )
        )
    config.CONFIG.pm.hook.add_candidate_prompt_choice(prompt_choices=prompt_choices)

    prompt_choice = choice_prompt(
        prompt_choices, question="Which album would you like to import?"
    )
    prompt_choice.func(new_album, candidates)


def _fmt_candidate_info(candidate: CandidateAlbum) -> str:
    """Formats a candidates info for the candidate prompt."""
    sub_header_values = []
    for field in ["media", "country", "label", "catalog_num"]:
        if value := getattr(candidate.album, field):
            sub_header_values.append(value)
    sub_header_values.extend(candidate.disambigs)
    sub_header = " | ".join(sub_header_values)

    return (
        str(candidate)
        + "\n"
        + " " * (9 + len(candidate.match_value_pct))
        + sub_header
        + "\n"
        + " " * (9 + len(candidate.match_value_pct))
        + f"{candidate.plugin_source.capitalize()}: {candidate.source_id}"
        + "\n"
    )


def _select_candidate(
    new_album: Album, candidates: list[CandidateAlbum], candidate_num: int
):
    """Runs the import prompt for a selected candidate."""
    import_prompt(new_album, candidates[candidate_num])


def import_prompt(
    new_album: Album,
    candidate: CandidateAlbum,
):
    """Runs the interactive prompt for the given album changes.

    Args:
        new_album: Album being added to the library. Any changes will be applied to
            this album.
        candidate: New candidate album with all metadata changes. Will be compared
            against ``old_album``.

    Raises:
        AbortImport: Import prompt was aborted by the user.
    """
    log.debug(f"Running import prompt. [{new_album=!r}, {candidate=!r}]")

    console.print(_fmt_import_updates(new_album, candidate))

    prompt_choices: list[PromptChoice] = []
    config.CONFIG.pm.hook.add_import_prompt_choice(prompt_choices=prompt_choices)

    prompt_choice = choice_prompt(prompt_choices)
    prompt_choice.func(new_album, candidate)


def _apply_changes(
    new_album: Album,
    candidate: CandidateAlbum,
):
    """Applies the album changes."""
    log.debug("Applying changes from import prompt.")

    for old_track, new_track in get_matching_tracks(new_album, candidate.album):
        if not old_track and new_track:
            candidate.album.tracks.remove(new_track)  # missing track
        elif old_track and not new_track:
            new_album.tracks.remove(
                new_album.get_track(old_track.track_num, old_track.disc)
            )  # unmatched track
        elif (
            old_track
            and new_track
            and new_album.get_track(new_track.track_num, new_track.disc) != old_track
        ):
            # matchup track and disc numbers of matches to ensure they merge properly
            old_track.track_num = new_track.track_num
            old_track.disc = new_track.disc

    new_album.merge(candidate.album, overwrite=True)


def _abort_changes(
    new_album: Album,
    candidate: CandidateAlbum,
):
    """Aborts the album changes."""
    raise AbortImport("Import prompt aborted; no changes made.")


def _fmt_import_updates(new_album: Album, candidate: CandidateAlbum) -> Panel:
    """Formats import updates between `new_album` and the `candidate`."""
    album_text = _fmt_album(new_album, candidate)
    track_text = _fmt_tracks(new_album, candidate)

    return Panel(
        Group(album_text, track_text),
        title="Import Updates",
        border_style="light_cyan1",
    )


def _fmt_album(new_album: Album, candidate: CandidateAlbum) -> Text:
    """Formats the header for the import panel."""
    header_text = Text(justify="center", style="bold")

    for header_field in ("title", "artist"):
        field_changes = _fmt_field_changes(new_album, candidate.album, header_field)
        if not field_changes:
            field_changes = Text(getattr(new_album, header_field))

        header_text.append_text(field_changes).append("\n")

    sub_header_text = Text()
    for sub_header in ("media", "country", "label", "catalog_num"):
        field_changes = _fmt_field_changes(new_album, candidate.album, sub_header)
        if not field_changes:
            if getattr(new_album, sub_header):
                field_changes = Text(getattr(new_album, sub_header))

        if sub_header_text and field_changes:
            sub_header_text.append(" | ")
        if field_changes:
            sub_header_text.append_text(field_changes)

    return (
        header_text.append_text(sub_header_text)
        .append("\n")
        .append(f"{candidate.plugin_source.capitalize()}: {candidate.source_id}")
        .append("\n")
    )


def _fmt_tracks(new_album: Album, candidate: CandidateAlbum) -> Table:
    """Formats the tracklist for the import panel."""
    track_table = Table(box=box.SIMPLE)
    track_table.add_column("status")
    track_table.add_column("disc")
    track_table.add_column("#")
    track_table.add_column("Artist")
    track_table.add_column("Title")

    matches = get_matching_tracks(new_album, candidate.album)
    matches.sort(
        key=lambda match: (
            getattr(match[1], "disc", 0),
            getattr(match[1], "track_num", 0),
        )
    )  # sort by new track's disc then track number

    unmatched_tracks: list[MetaTrack] = []
    missing_tracks: list[MetaTrack] = []
    for old_track, new_track in matches:
        if old_track and new_track:
            track_table.add_row(
                Text("matched", style="green"),
                _fmt_field_changes(old_track, new_track, "disc"),
                _fmt_field_changes(old_track, new_track, "track_num"),
                _fmt_field_changes(old_track, new_track, "artist"),
                _fmt_field_changes(old_track, new_track, "title"),
            )
        elif old_track and not new_track:
            unmatched_tracks.append(old_track)
        elif not old_track and new_track:
            missing_tracks.append(new_track)
    if track_table.rows:
        track_table.rows[-1].end_section = True

    for missing_track in sorted(missing_tracks):
        track_table.add_row(
            Text("missing", style="red"),
            str(missing_track.disc),
            str(missing_track.track_num),
            missing_track.artist,
            missing_track.title,
        )
    for unmatched_track in sorted(unmatched_tracks):
        track_table.add_row(
            Text("unmatched", style="red"),
            str(unmatched_track.disc),
            str(unmatched_track.track_num),
            unmatched_track.artist,
            unmatched_track.title,
        )

    return track_table


def _fmt_field_changes(
    old_item: Union[MetaAlbum, MetaTrack],
    new_item: Union[MetaAlbum, MetaTrack],
    field: str,
) -> Optional[Text]:
    """Formats changes of a single field.

    Args:
        old_item: Old track or album to compare.
        new_item: New track or album to compare.
        field: Field to compare.

    Returns:
        A rich 'Text' based on the following cases:

        1. `old_item.field` DNE and `new_item.field` exists:
        `new_item.field` will be returned in green
        2. `old_item.field` exists and `new_item.field` DNE:
        `old_item.field`  will be striketroughed and in red
        3. `old_item.field` differs from `new_item.field`:
            "{old_item.field} -> {new_item.field}" and the arrow is yellow
        4. `old_item.field` is equal to `new_item.field`:
           `old_item.field` returned
        5. None if `old_item.field` and `new_item.field` DNE
    """
    old_field = getattr(old_item, field)
    new_field = getattr(new_item, field)

    if not old_field and new_field:
        return Text(str(new_field), style="green")
    if old_field and not new_field:
        return Text(str(old_field), style="red strike")
    if old_field != new_field:
        return (
            Text(str(old_field))
            .append(Text(" -> ", style="yellow"))
            .append(Text(str(new_field)))
        )

    if old_field:
        return Text(str(old_field))
    else:
        return None
