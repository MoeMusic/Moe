"""Import prompt."""

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
from moe.library import Album, Track
from moe.util.cli import PromptChoice, choice_prompt
from moe.util.core import get_matching_tracks

log = logging.getLogger("moe.cli.import")

__all__ = ["AbortImport", "import_prompt"]


class AbortImport(Exception):
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
    log.debug(f"Running import prompt. [{old_album=!r}, {new_album=!r}]")

    console.print(_fmt_import_updates(old_album, new_album))

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


def _fmt_import_updates(old_album: Album, new_album: Album) -> Panel:
    """Formats import updates from `old_album` to `new_album`."""
    album_text = _fmt_album(old_album, new_album)
    track_text = _fmt_tracks(old_album, new_album)

    return Panel(
        Group(album_text, track_text),
        title="Import Updates",
        border_style="light_cyan1",
    )


def _fmt_album(old_album: Album, new_album: Album) -> Text:
    """Formats the header for the album changes panel."""
    header_text = Text(justify="center", style="bold")

    for header_field in ("title", "artist"):
        field_changes = _fmt_field_changes(old_album, new_album, header_field)
        if not field_changes:
            field_changes = Text(getattr(old_album, header_field))

        header_text.append_text(field_changes).append("\n")

    sub_header_text = Text()
    for sub_header in ("media", "year", "country", "label"):
        field_changes = _fmt_field_changes(old_album, new_album, sub_header)
        if not field_changes:
            if getattr(old_album, sub_header):
                field_changes = Text(getattr(old_album, sub_header))

        if sub_header_text and field_changes:
            sub_header_text.append(" | ")
        if field_changes:
            sub_header_text.append_text(field_changes)

    return header_text.append_text(sub_header_text).append("\n")


def _fmt_tracks(old_album: Album, new_album: Album) -> Table:
    """Formats the tracklist differences between two albums."""
    track_table = Table(box=box.SIMPLE)
    track_table.add_column("status")
    track_table.add_column("disc")
    track_table.add_column("#")
    track_table.add_column("Artist")
    track_table.add_column("Title")

    matches = get_matching_tracks(old_album, new_album)
    matches.sort(
        key=lambda match: (
            getattr(match[1], "disc", 0),
            getattr(match[1], "track_num", 0),
        )
    )  # sort by new track's disc then track number

    unmatched_tracks: list[Track] = []
    missing_tracks: list[Track] = []
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
    old_item: Union[Album, Track], new_item: Union[Album, Track], field: str
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
