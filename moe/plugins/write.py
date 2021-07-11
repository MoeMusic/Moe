"""Writes tags to track files."""

import logging
from typing import List

import mediafile
import sqlalchemy
from sqlalchemy.orm.session import Session

import moe
from moe.core.config import Config
from moe.core.library.track import Track

__all__: List[str] = []

log = logging.getLogger("moe.write")


def write_session_tracks(
    session: Session, flush_context: sqlalchemy.orm.UOWTransaction
):
    """Writes tags to any altered or new Track in a session.

    Args:
        session: Current db session.
        flush_context: sqlalchemy obj which handles the details of the flush.
    """
    for item in session.new.union(session.dirty):
        if isinstance(item, Track):
            _write_tags(item)


@moe.hookimpl
def register_db_listener(config: Config, session: Session):
    """Write tags to any tracks being committed to the database."""
    sqlalchemy.event.listen(session, "after_flush", write_session_tracks)


def _write_tags(track: Track):
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
