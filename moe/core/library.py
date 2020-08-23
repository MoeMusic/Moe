"""Describes all the information available in the library.

A high-level model of the database.

Note:
    The database will be initialized once the user configuration is read.
"""

import pathlib
from contextlib import contextmanager

import sqlalchemy
from mediafile import MediaFile
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.schema import ForeignKey

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


class MusicItem:
    """An abstract base class for both albums and tracks."""


class Album(MusicItem, Base):
    """An album is a collection of tracks.

    Albums also house any attributes that are shared by tracks e.g. albumartist.

    Attributes:
        artist (str): AKA albumartist.
        title (str)
        tracks (List[Track]): All the album's corresponding tracks.
    """

    __tablename__ = "albums"

    _id = Column(Integer, primary_key=True)
    artist = Column(String, nullable=False, default="")
    title = Column(String, nullable=False, default="")

    tracks = relationship("Track", back_populates="album", cascade="all, delete")

    def __str__(self):
        """String representation of an album."""
        return f"{self.artist} - {self.title}"


class Track(MusicItem, Base):
    """A single track.

    Attributes:
        album (library.Album): Album object.
            Access album-related attributes through the object e.g. `track.album.title`.
        artist (str)
        path (pathlib.Path): Path of the track file.
        title (str)

    Note:
        Can be instantiated as normal using keyword arguments.

    Example:
        >>> track = Track(path=pathlib.Path('mycoolpath'))
    """

    __tablename__ = "tracks"

    _id = Column(Integer, primary_key=True)
    _album_id = Column(Integer, ForeignKey("albums._id"))
    artist = Column(String, nullable=False, default="")
    path = Column(_PathType, nullable=False, unique=True)
    title = Column(String, nullable=False, default="")

    album = relationship("Album", back_populates="tracks")

    def __init__(self, path: pathlib.Path, read_tags: bool = True):
        """Create a track.

        Args:
            path: Path to the track to add.
            read_tags: Whether or not to read tags from the given file.
                If read, the tags will be set to the track.

        Raises:
            FileNotFoundError: Given path doesn't exit.
        """
        if not path.exists():
            raise FileNotFoundError

        self.path = path
        self.title = "tmp_title"

        self.album = Album()

        if read_tags:
            self._set_fields_from_file()

    def __str__(self):
        """String representation of a track."""
        return f"{self.artist} - {self.title}"

    def _set_fields_from_file(self):
        """Reads any tags from the music file and sets them to the Track."""
        self._audio_file = MediaFile(self.path)

        self.artist = self._audio_file.artist
        self.title = self._audio_file.title

        self.album.title = self._audio_file.album
        self.album.artist = self._audio_file.albumartist


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
