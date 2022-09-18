"""Writes tags to track files."""

import logging

import mediafile

import moe
from moe.library.lib_item import LibItem
from moe.library.track import Track

__all__ = ["write_tags"]

log = logging.getLogger("moe.write")


@moe.hookimpl
def process_new_items(items: list[LibItem]):
    """Writes tags to any altered or new tracks in the library."""
    for item in items:
        if isinstance(item, Track):
            write_tags(item)


def write_tags(track: Track):
    """Write tags to a track's file."""
    log.debug(f"Writing tags to track. [{track=!r}]")

    audio_file = mediafile.MediaFile(track.path)

    audio_file.album = track.album
    audio_file.albumartist = track.albumartist
    audio_file.artist = track.artist
    audio_file.date = track.date
    audio_file.disc = track.disc
    audio_file.disctotal = track.disc_total
    audio_file.genres = track.genres
    audio_file.title = track.title
    audio_file.track = track.track_num

    audio_file.save()

    log.info(f"Wrote tags to track. [{track=!r}]")
