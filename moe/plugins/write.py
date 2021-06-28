"""Writes tags to track files."""

import logging

import mediafile
from sqlalchemy.orm.session import Session

import moe
from moe.core.config import Config
from moe.core.library.track import Track

log = logging.getLogger(__name__)


@moe.hookimpl
def post_args(config: Config, session: Session):
    """Writes the tags to any Track that has been altered or added in the session.

    This hook is run after the CLI arguments have been executed.

    Args:
        config: Moe config.
        session: Currrent db session.
    """
    for item in session.new.union(session.dirty):
        if isinstance(item, Track):
            _write_tags(item)


def _write_tags(track: Track):
    """Write tags to a track's file."""
    log.info(f"Writing tags for '{track}'.")

    audio_file = mediafile.MediaFile(track.path)

    audio_file.album = track.album
    audio_file.albumartist = track.albumartist
    audio_file.artist = track.artist
    audio_file.genres = track.genre
    audio_file.title = track.title
    audio_file.track = track.track_num
    audio_file.year = track.year
    audio_file.mb_trackid = track.mb_track_id
    audio_file.mb_albumid = track.mb_album_id

    audio_file.save()
