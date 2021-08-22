"""Writes tags to track files."""

import logging
from typing import List

import mediafile

import moe
from moe.config import Config
from moe.library.lib_item import LibItem
from moe.library.track import Track

__all__ = ["write_tags"]

log = logging.getLogger("moe.write")


@moe.hookimpl
def process_new_items(config: Config, items: List[LibItem]):
    """Writes tags to any altered or new tracks in the library.

    Args:
        config: Moe config.
        items: Any new or changed items that have been committed to the database
            during the current session.
    """
    for item in items:
        if isinstance(item, Track):
            write_tags(item)


def write_tags(track: Track):
    """Write tags to a track's file."""
    log.info(f"Writing tags for '{track}'.")

    audio_file = mediafile.MediaFile(track.path)

    audio_file.album = track.album
    audio_file.albumartist = track.albumartist
    audio_file.artist = track.artist
    audio_file.date = track.date
    audio_file.disc = track.disc
    audio_file.disctotal = track.disc_total
    audio_file.genres = track.genres
    audio_file.mb_releasetrackid = track.mb_track_id
    audio_file.mb_albumid = track.mb_album_id
    audio_file.title = track.title
    audio_file.track = track.track_num

    audio_file.save()
