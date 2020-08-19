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

    def process_bind_param(self, pathlib_path, dialect):
        """Convert the path to a string prior to enterting in the database."""
        return str(pathlib_path.resolve())

    def process_result_value(self, path_str, dialect):
        """Convert the path back to pathlib.Path on the way out."""
        return pathlib.Path(path_str)


class Track(Base):
    """A single track.

    Attributes:
        path (pathlib.Path): path of the track file
        title (str): track title

    Note:
        Can be instantiated as normal using keyword arguments.

    Example:
        >>> track = Track(path=pathlib.Path('mycoolpath'))
    """

    __tablename__ = "tracks"

    _id = Column(Integer, primary_key=True)
    path = Column(_PathType, nullable=False, unique=True)
    title = Column(String, nullable=False)

    def __init__(self, path: pathlib.Path):
        """Create a track.

        Populates the tags by reading the file.

        Args:
            path: Path to the track to add.

        Raises:
            FileNotFoundError: Given path doesn't exit.
        """
        if not path.exists():
            raise FileNotFoundError

        self.path = path
        self.title = "tmp_title"

    def __str__(self):
        """A track is represented by its path.

        Returns:
            string represenation of the path
        """
        return str(self.path)


@contextmanager
def session_scope():
    """Provides a transactional scope around a series of operations.

    Yields:
        A database session to use.

    Raises:
        BaseException: Any exceptions occured during while committing to
            the database will be re-raised.
    """
    session = Session()
    yield session
    try:
        session.commit()
    except BaseException:  # noqa: WPS424
        session.rollback()
        raise
    finally:
        session.close()
