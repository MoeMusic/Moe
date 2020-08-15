"""Describes all the information available in the library.

A high-level model of the database.

Note:
    The database will be initialized once the user configuration is read.
"""

import pathlib
from contextlib import contextmanager

import sqlalchemy
from sqlalchemy import Column, Integer, String
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
        """Convert to a string of the absolue path on the way in."""
        return str(value.resolve())

    def process_result_value(self, value, dialect):
        """Convert the path back to pathlib.Path on the way out."""
        return pathlib.Path(value)

    def coerce_compared_value(self, op, value):
        """Define path comparisons for different types."""
        if isinstance(value, str):
            return String()


class Track(Base):
    """A single track.

    Attributes:
        id (int): database id
        path (pathlib.Path): path of the track file
        title (str): track title

    Note:
        Can be instantiated as normal using keyword arguments.

    Example:
        >>> track = Track(path=pathlib.Path('mycoolpath'))

    """

    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True)
    path = Column(_PathType, nullable=False, unique=True)
    title = Column(String, nullable=False)

    def __init__(self, path: pathlib.Path, title: str = None):
        """Create a track."""
        if not path.exists():
            raise AttributeError

        self.path = path
        self.title = title if title else "tmp_title"

    def __str__(self):
        """String representation of a track."""
        return str(self.path)


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
