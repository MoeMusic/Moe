"""Functionality for dealing with sessions that connect to the library.

Note:
    The database will be initialized once the user configuration is read.
"""

from contextlib import contextmanager

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Session = sessionmaker()
Base = declarative_base()


class DbDupMusicItemError(Exception):
    """Attempt to add a duplicate MusicItem to the database."""


class DbDupTrackPathError(DbDupMusicItemError):
    """Attempt to add a duplicate Track path to the database."""


class DbDupAlbumError(DbDupMusicItemError):
    """Attempt to add a duplicate Album to the database."""


def _parse_integrity_error(error: sqlalchemy.exc.IntegrityError):
    """Parses a general IntegrityError and raises a more specific one.

    Args:
        error: IntegrityError to parse.

    Raises:
        DbDupTrackTagsError: Track's unique tags already exist in the database.
        DbDupTrackPathError: Track's path already exists in the database.
        DbDupAlbumError: Album already exists in the database.
    """
    error_msg = str(error.orig)
    track_path_dup_msg = "UNIQUE constraint failed: tracks.path"
    album_dup_msg = "UNIQUE constraint failed: albums.artist, albums.title, albums.year"

    if error_msg == track_path_dup_msg:
        raise DbDupTrackPathError from error
    elif error_msg == album_dup_msg:
        raise DbDupAlbumError from error


@contextmanager
def session_scope():
    """Yields a transactional scope around a series of operations."""
    session = Session()
    yield session
    try:
        session.commit()
    except sqlalchemy.exc.IntegrityError as exc:
        session.rollback()
        _parse_integrity_error(exc)
        raise
    except:  # noqa: B001, E722
        session.rollback()
        raise
    finally:
        session.close()
