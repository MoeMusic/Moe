"""Describes all the information available in the library.

A high-level model of the database.

Note:
    The database will be initialized once the user configuration is read.
"""

import pathlib
from contextlib import contextmanager

import sqlalchemy
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Session = sessionmaker()
Base = declarative_base()


class _PathType(sqlalchemy.types.TypeDecorator):
    """A custom type for paths for database storage.

    Normally, paths are pathlib.Path type, but we can't store that in the database,
    so we normalize the paths first for database storage.
    """

    impl = sqlalchemy.types.String  # sql type

    def process_bind_param(self, value, dialect):
        """Convert the path to a string on the way in."""
        return str(value)

    def process_result_value(self, value, dialect):
        """Convert the path back to pathlib.Path on the way out."""
        return pathlib.Path(value)


class Track(Base):
    """A single track.

    Attributes:
        id (int): database id
        path (pathlib.Path): path of the track file
    """

    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True)
    path = Column(_PathType)


@contextmanager
def session_scope():
    """Provides a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except BaseException:
        session.rollback()
        raise
    finally:
        session.close()
