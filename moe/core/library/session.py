"""Functionality for dealing with sessions that connect to the library.

Note:
    The database will be initialized once the user configuration is read.
"""

from contextlib import contextmanager
from typing import Generator

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Session = sessionmaker()
Base: sqlalchemy.orm.decl_api.DeclarativeMeta = declarative_base()


class DbDupLibItemError(Exception):
    """Attempt to add a duplicate LibItem to the database."""


class DbDupAlbumPathError(DbDupLibItemError):
    """Attempt to add a duplicate Album path to the database."""


class DbDupAlbumError(DbDupLibItemError):
    """Attempt to add a duplicate Album to the database."""


@contextmanager
def session_scope() -> Generator[sqlalchemy.orm.session.Session, None, None]:
    """Yields a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
    except SystemExit:
        # assumes session has already been cleaned if SystemExit intentionally raised
        _commit_session(session)
        raise
    else:
        _commit_session(session)


def _commit_session(session: sqlalchemy.orm.session.Session):
    """Commits the changes in the sqlalchemy db session."""
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


def _parse_integrity_error(error: sqlalchemy.exc.IntegrityError):
    """Parses a general IntegrityError and raises a more specific one.

    Args:
        error: IntegrityError to parse.

    Raises:
        DbDupAlbumPathError: Album's path already exists in the database.
        DbDupAlbumError: Album already exists in the database.
    """
    error_msg = str(error.orig)
    album_path_dup_msg = "UNIQUE constraint failed: albums.path"
    album_dup_msg = "UNIQUE constraint failed: albums.artist, albums.title, albums.year"

    if error_msg == album_path_dup_msg:
        raise DbDupAlbumPathError from error
    elif error_msg == album_dup_msg:
        raise DbDupAlbumError from error
