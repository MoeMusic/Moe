"""Functionality for formatting the changes between two items in the library.

This module is used in various prompts of the CLI.
"""
from typing import Optional, cast

from moe.library.album import Album
from moe.library.lib_item import LibItem
from moe.library.track import Track
from moe.util.core import get_matching_tracks

__all__ = ["fmt_item_changes"]


def fmt_item_changes(item_a: LibItem, item_b: LibItem) -> str:
    """Formats the changes between two items."""
    if type(item_a) != type(item_b):
        raise ValueError(
            "Cannot format changes of items of different types. "
            f"[{item_a=!r}, {item_b=!r}]"
        )
    if isinstance(item_a, Track) and isinstance(item_b, Track):
        return _fmt_track_changes(item_a, item_b)
    elif isinstance(item_a, Album) and isinstance(item_b, Album):
        return _fmt_album_changes(item_a, item_b)
    else:
        raise NotImplementedError


def _fmt_album_changes(old_album: Album, new_album: Album) -> str:
    """Formats the changes between between two albums."""
    album_info_str = ""
    album_title = f"Album: {old_album.title}"
    if old_album.title != new_album.title:
        album_title += f" -> {new_album.title}"
    album_info_str += album_title

    album_artist = f"Album Artist: {old_album.artist}"
    if old_album.artist != new_album.artist:
        album_artist = album_artist + f" -> {new_album.artist}"
    album_info_str += "\n" + album_artist

    album_year = f"Year: {old_album.year}"
    if old_album.year != new_album.year:
        album_year = album_year + f" -> {new_album.year}"
    album_info_str += "\n" + album_year

    tracklist_str = _fmt_tracklist(old_album, new_album)

    extra_str = ""
    extra_str += "\nExtras:\n"
    extra_str += "\n".join([extra.path.name for extra in old_album.extras])

    album_str = album_info_str + "\n" + tracklist_str
    if old_album.extras:
        album_str += "\n" + extra_str

    return album_str


def _fmt_tracklist(old_album: Album, new_album: Album) -> str:
    """Formats the changes of the tracklists between two albums."""
    tracklist_str = ""

    matches = get_matching_tracks(old_album, new_album)
    matches.sort(
        key=lambda match: (
            getattr(match[1], "disc", 0),
            getattr(match[1], "track_num", 0),
        )
    )  # sort by new track's disc then track number
    unmatched_tracks: list[Track] = []
    for old_track, new_track in matches:
        if not new_track:
            unmatched_tracks.append(cast(Track, old_track))
            continue

        tracklist_str += "\n" + _fmt_track_changes(old_track, new_track)

    if unmatched_tracks:
        tracklist_str += "\n\nUnmatched Tracks:\n"
        tracklist_str += "\n".join([str(track) for track in unmatched_tracks])

    return tracklist_str


def _fmt_track_changes(old_track: Optional[Track], new_track: Track) -> str:
    """Formats the changes between two tracks."""
    track_change = ""
    new_disc = ""
    old_disc = ""
    if new_track.disc_total > 1:
        new_disc = f"{new_track.disc}."
        if old_track:
            old_disc = f"{old_track.disc}."
    if old_track:
        old_track_title = f"{old_disc}{old_track.track_num}: {old_track.title}"
    else:
        old_track_title = "(missing)"
    track_change += old_track_title

    new_track_title = f"{new_disc}{new_track.track_num}: {new_track.title}"

    if old_track_title != new_track_title:
        track_change += f" -> {new_track_title}"

    return track_change
