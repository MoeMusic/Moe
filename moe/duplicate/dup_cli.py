"""Adds a duplicate resolution prompt to the CLI."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, cast

from rich.columns import Columns
from rich.console import Group, RenderableType
from rich.padding import Padding
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

import moe
from moe.cli import console
from moe.library import Album, Extra, LibItem, Track
from moe.remove import remove_item
from moe.util.cli import PromptChoice, choice_prompt

if TYPE_CHECKING:
    from sqlalchemy.orm.session import Session

log = logging.getLogger("moe.cli.dup")


__all__: list[str] = []


@moe.hookimpl(trylast=True)
def resolve_dup_items(session: Session, item_a: LibItem, item_b: LibItem) -> None:
    """Resolve any library duplicate conflicts using a user prompt."""
    console.print(_fmt_item_vs(item_a, item_b))

    # Each PromptChoice `func` should have the following signature:
    # func(session, item_a, item_b) # noqa: ERA001
    prompt_choices = [
        PromptChoice(title="Keep item A", shortcut_key="a", func=_keep_a),
        PromptChoice(title="Keep item B", shortcut_key="b", func=_keep_b),
        PromptChoice(
            title="Merge A -> B without overwriting conflicts",
            shortcut_key="m",
            func=_merge,
        ),
        PromptChoice(
            title="Merge A -> B, overwriting any conflicts",
            shortcut_key="o",
            func=_overwrite,
        ),
    ]
    prompt_choice = choice_prompt(
        prompt_choices,
        "Duplicate items found in the library, how would you like to resolve it?",
    )
    prompt_choice.func(session, item_a, item_b)


def _keep_a(session: Session, item_a: LibItem, item_b: LibItem) -> None:  # noqa: ARG001
    """Keeps `item_a`, removing `item_b` from the library."""
    log.debug("Keeping item A.")

    remove_item(session, item_b)


def _keep_b(session: Session, item_a: LibItem, item_b: LibItem) -> None:  # noqa: ARG001
    """Keeps `item_a`, removing `item_b` from the library."""
    log.debug("Keeping item B.")

    remove_item(session, item_a)


def _merge(session: Session, item_a: LibItem, item_b: LibItem) -> None:
    """Merges `item_a` into `item_b` without overwriting any conflicts."""
    log.debug("Merging A -> B without overwriting any conflicts.")

    item_b.merge(item_a)
    remove_item(session, item_a)


def _overwrite(session: Session, item_a: LibItem, item_b: LibItem) -> None:
    """Merges `item_a` into `item_b`, overwriting any conflicts."""
    log.debug("Merging A -> B, overwriting B on conflict.")

    item_b.merge(item_a, overwrite=True)
    remove_item(session, item_b)


def _fmt_item_vs(item_a: LibItem, item_b: LibItem) -> Columns:
    """Formats the differences between two items for output."""
    panel_a_style = "spring_green4"
    panel_b_style = "dark_red"

    if isinstance(item_a, Album):
        panel_a_title = "Album A"
        panel_b_title = "Album B"
    elif isinstance(item_a, Extra):
        panel_a_title = "Extra A"
        panel_b_title = "Extra B"
    else:
        panel_a_title = "Track A"
        panel_b_title = "Track B"

    panel_a = Panel(
        _fmt_item_text(item_a, item_b), title=panel_a_title, border_style=panel_a_style
    )
    panel_b = Panel(
        _fmt_item_text(item_b, item_a), title=panel_b_title, border_style=panel_b_style
    )
    return Columns((panel_a, panel_b))


def _fmt_item_text(
    item: LibItem, other: LibItem, *, include_header: bool = True
) -> RenderableType:
    """Formats a library item highlighting any differences from `other`."""
    if isinstance(item, Album):
        header = Text(f"{item}", justify="center")
        omit_fields = {"extras", "tracks", "year"}
    elif isinstance(item, Extra):
        header = Text(f"{item.rel_path}\n{item.album}", justify="center")
        omit_fields = {"album", "rel_path", "path"}
    else:
        item = cast("Track", item)
        header = Text(f"{item.title}\n{item.album}", justify="center")
        omit_fields = {
            "album",
            "date",
            "disc_total",
            "genre",
            "year",
        }

    item_diff = Table.grid("field value", padding=(0, 1))
    item_has_diff = False
    for field in sorted(item.fields - omit_fields):
        field_diff = _fmt_value_vs(
            getattr(item, field, None), getattr(other, field, None)
        )
        if field_diff:
            item_has_diff = True
            item_diff.add_row(Text(field, style="italic grey69"), field_diff)

    for custom_field in sorted(set(item.custom).union(set(other.custom))):
        field_diff = _fmt_value_vs(
            item.custom.get(custom_field), other.custom.get(custom_field)
        )
        if field_diff:
            item_has_diff = True
            item_diff.add_row(Text(custom_field, style="italic grey69"), field_diff)

    if isinstance(item, Album) and isinstance(other, Album):
        item_diff = Group(item_diff, "", _fmt_album_lists(item, other))
        item_has_diff = True

    if include_header and item_has_diff:
        return Group(header, "", item_diff)
    if include_header and not item_has_diff:
        return header
    return item_diff


def _fmt_album_lists(album: Album, other: Album) -> Group | Table:
    """Formats the track and extra lists for an album highlighting diffs from other."""
    tracklist = Table.grid("track", padding=(0, 1))
    for track in sorted(album.tracks):
        tracklist.add_row(f"{track.disc}.{track.track_num} - {track.title}")

        other_track = other.get_track(track.track_num, track.disc)
        if other_track:
            track_diff = cast(
                "Table", _fmt_item_text(track, other_track, include_header=False)
            )
            if len(track_diff.rows):
                tracklist.add_row(Padding(track_diff, (0, 4)))

    extralist = Table.grid("extra", padding=(0, 1))
    for extra in sorted(album.extras):
        extralist.add_row(f"{extra.rel_path}")

        other_extra = other.get_extra(extra.rel_path)
        if other_extra:
            extra_diff = cast(
                "Table", _fmt_item_text(extra, other_extra, include_header=False)
            )
            if len(extra_diff.rows):
                extralist.add_row(Padding(extra_diff, (0, 4)))

    if album.extras:
        return Group(tracklist, "", extralist)
    return tracklist


def _fmt_value_vs(value_a: object, value_b: object) -> Text | None:
    """Highlights differences between two values.

    Args:
        value_a: Value to base comparisons off of.
        value_b: Other value to compare against.

    Returns:
        A rich 'Text' based on the following cases:

        1. `item.field` DNE:
           return `None`
        2. `item.field` == `other.field`:
           return `None`
        3. `item.field` != `other.field`:
           `item.field` will be returned in yellow
        4. `item.field` exists and `other.field` DNE:
           `item.field` will be returned in green
    """
    if not value_a or (value_a == value_b):
        return None
    if value_a != value_b:
        return Text(str(value_a), style="yellow")
    if value_a and not value_b:
        return Text(str(value_a), style="green")
