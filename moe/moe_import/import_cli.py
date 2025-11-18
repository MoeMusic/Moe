"""Import prompt."""

from __future__ import annotations

import functools
import logging
from typing import TYPE_CHECKING

import dynaconf
import dynaconf.base
from rich import box
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

import moe
from moe import config
from moe.cli import console
from moe.util.cli import PromptChoice, choice_prompt
from moe.util.core import get_matching_tracks
from moe.util.core.match import MatchType, get_field_match_penalty

if TYPE_CHECKING:
    import pluggy

    from moe.library import Album, MetaAlbum, MetaTrack
    from moe.moe_import.import_core import CandidateAlbum

log = logging.getLogger("moe.cli.import")

__all__ = ["candidate_prompt", "import_prompt"]


class AbortImportError(Exception):
    """Used to abort the import process."""


class Hooks:
    """Import plugin cli hook specifications."""

    @staticmethod
    @moe.hookspec
    def add_candidate_prompt_choice(prompt_choices: list[PromptChoice]) -> None:
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
    def add_import_prompt_choice(prompt_choices: list[PromptChoice]) -> None:
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
def add_hooks(pm: pluggy._manager.PluginManager) -> None:
    """Registers `import` cli hookspecs to Moe."""
    from moe.moe_import.import_cli import Hooks  # noqa: PLC0415

    pm.add_hookspecs(Hooks)


@moe.hookimpl
def add_candidate_prompt_choice(prompt_choices: list[PromptChoice]) -> None:
    """Adds the ``abort`` prompt choice to the user prompt."""
    prompt_choices.append(
        PromptChoice(title="Abort", shortcut_key="x", func=_abort_changes)
    )


@moe.hookimpl
def add_import_prompt_choice(prompt_choices: list[PromptChoice]) -> None:
    """Adds the ``apply`` and ``abort`` prompt choices to the user prompt."""
    prompt_choices.append(
        PromptChoice(title="Apply changes", shortcut_key="a", func=_apply_changes)
    )
    prompt_choices.append(
        PromptChoice(title="Abort", shortcut_key="x", func=_abort_changes)
    )


@moe.hookimpl
def add_config_validator(settings: dynaconf.base.LazySettings) -> None:
    """Validates import plugin configuration settings."""
    settings.validators.register(  # type: ignore[reportAttributeAccessIssue] dynaconf doesn't have proper type stubs yet
        dynaconf.Validator("import.max_candidates", default=5, gte=1)
    )


@moe.hookimpl
def process_candidates(new_album: Album, candidates: list[CandidateAlbum]) -> None:
    """Use the import prompt to select and process the imported candidate albums."""
    if candidates:
        max_candidates = config.CONFIG.settings.get("import.max_candidates")
        try:
            candidate_prompt(new_album, candidates[:max_candidates])
        except AbortImportError as err:
            log.debug(err)
            raise SystemExit(0) from err


def candidate_prompt(new_album: Album, candidates: list[CandidateAlbum]) -> None:
    """Runs the interactive prompt for a user to select a candidate to import.

    Args:
        new_album: Album being added to the library.
        candidates: List of candidates to choose from.

    Raises:
        AbortImportError: Import prompt was aborted by the user.
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
    sub_header_values = [
        value
        for field in ["media", "country", "label", "catalog_num"]
        if (value := getattr(candidate.album, field))
    ]
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
) -> None:
    """Runs the import prompt for a selected candidate."""
    import_prompt(new_album, candidates[candidate_num])


def import_prompt(
    new_album: Album,
    candidate: CandidateAlbum,
) -> None:
    """Runs the interactive prompt for the given album changes.

    Args:
        new_album: Album being added to the library. Any changes will be applied to
            this album.
        candidate: New candidate album with all metadata changes. Will be compared
            against ``old_album``.

    Raises:
        AbortImportError: Import prompt was aborted by the user.
    """
    log.debug(f"Running import prompt. [{new_album=}, {candidate=}]")

    console.print(_fmt_import_updates(new_album, candidate))

    prompt_choices: list[PromptChoice] = []
    config.CONFIG.pm.hook.add_import_prompt_choice(prompt_choices=prompt_choices)

    prompt_choice = choice_prompt(prompt_choices)
    prompt_choice.func(new_album, candidate)


def _apply_changes(
    new_album: Album,
    candidate: CandidateAlbum,
) -> None:
    """Applies the album changes."""
    log.debug("Applying changes from import prompt.")

    for old_track, new_track in get_matching_tracks(new_album, candidate.album):
        if not old_track and new_track:
            candidate.album.tracks.remove(new_track)  # missing track
        elif old_track and not new_track:
            unmatched_track = new_album.get_track(old_track.track_num, old_track.disc)
            if unmatched_track:
                new_album.tracks.remove(unmatched_track)
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
    new_album: Album,  # noqa: ARG001
    candidate: CandidateAlbum,  # noqa: ARG001
) -> None:
    """Aborts the album changes."""
    err_msg = "Import prompt aborted; no changes made."
    raise AbortImportError(err_msg)


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
        if not field_changes and getattr(new_album, sub_header):
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
    track_table.add_column("Duration (external)")

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
                _fmt_duration_with_external(old_track, new_track),
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
            _fmt_duration(missing_track.duration),
        )
    for unmatched_track in sorted(unmatched_tracks):
        track_table.add_row(
            Text("unmatched", style="red"),
            str(unmatched_track.disc),
            str(unmatched_track.track_num),
            unmatched_track.artist,
            unmatched_track.title,
            _fmt_duration(unmatched_track.duration),
        )

    return track_table


def _fmt_field_changes(
    old_item: MetaAlbum | MetaTrack,
    new_item: MetaAlbum | MetaTrack,
    field: str,
) -> Text | None:
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

    old_formatted = str(old_field) if old_field else ""
    new_formatted = str(new_field) if new_field else ""

    if not old_formatted and new_formatted:
        return Text(new_formatted, style="green")
    if old_formatted and not new_formatted:
        return Text(old_formatted, style="red strike")
    if old_formatted != new_formatted and old_formatted and new_formatted:
        return (
            Text(old_formatted)
            .append(Text(" -> ", style="yellow"))
            .append(Text(new_formatted))
        )
    if old_formatted:
        return Text(old_formatted)
    return None


def _fmt_duration_with_external(old_track: MetaTrack, new_track: MetaTrack) -> Text:
    """Formats duration showing file duration with external duration in parentheses.

    Args:
        old_track: Track from the library (file duration).
        new_track: Track from external source (external duration).

    Returns:
        A rich Text object showing "file_duration (external_duration)" with
        color coding based on match quality, or just file_duration if no external
        duration.
    """
    file_duration = old_track.duration
    external_duration = new_track.duration

    file_formatted = _fmt_duration(file_duration)

    if not external_duration or external_duration <= 0:
        return Text(file_formatted) if file_formatted else Text("")

    external_formatted = _fmt_duration(external_duration)

    if not file_duration or file_duration <= 0:
        return Text(external_formatted) if external_formatted else Text("")

    penalty = get_field_match_penalty(
        file_duration, external_duration, MatchType.DURATION
    )

    if penalty == 0.0:
        external_color = "green"
    elif penalty < 1.0:
        external_color = "yellow"
    else:
        external_color = "red"

    result = Text(file_formatted)
    result.append(" (")
    result.append(external_formatted, style=external_color)
    result.append(")")

    return result


def _fmt_duration(duration: float | None) -> str:
    """Formats duration from seconds to a 'MM:SS' string."""
    if duration is None or duration <= 0:
        return ""

    minutes = int(duration // 60)
    seconds = int(duration % 60)
    return f"{minutes}:{seconds:02d}"
