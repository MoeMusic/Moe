"""Describes all the information available in the library.

A high-level model of the database.

Note:
    The database will be initialized once the user configuration is read.
"""

import logging
import pathlib
import types
from collections import OrderedDict
from contextlib import contextmanager
from typing import Any, Type, TypeVar

import sqlalchemy
from mediafile import MediaFile
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.schema import ForeignKey, UniqueConstraint

log = logging.getLogger(__name__)

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

    def to_dict(self) -> "OrderedDict[str, Any]":
        """Represents the MusicItem as a dictionary.

        The dictionary should be sorted alphabetically.

        Raises:
            NotImplementedError: Not implemented by subclasses.
        """
        raise NotImplementedError


# Album generic, used for typing classmethod
A = TypeVar("A", bound="Album")  # noqa: WPS111


class Album(MusicItem, Base):
    """An album is a collection of tracks.

    Albums also house any attributes that are shared by tracks e.g. albumartist.

    Attributes:
        artist (str): AKA albumartist.
        title (str)
        tracks (List[Track]): All the album's corresponding tracks.
        year (str)
    """

    __tablename__ = "albums"
    __table_args__ = (UniqueConstraint("artist", "title", "year"),)

    _id = Column(Integer, primary_key=True)
    artist = Column(String, nullable=False)
    title = Column(String, nullable=False)
    year = Column(Integer, nullable=False)

    tracks = relationship("Track", back_populates="_album_obj", cascade="all, delete")

    def __init__(self, artist: str, title: str, year: int):
        """Creates an album.

        Args:
            artist: Album artist.
            title: Album title.
            year: Album release year.
        """
        self.artist = artist
        self.title = title
        self.year = year

    def __str__(self):
        """String representation of an album."""
        return f"{self.artist} - {self.title}"

    def to_dict(self) -> "OrderedDict[str, Any]":
        """Represents the Album as a dictionary.

        An albums representation is just the merged dictionary of all its tracks.
        If different values are present for any given attribute among tracks, then
        the value becomes "Various".

        Returns:
            Returns a dict representation of an Album.
            It will be in the form { attribute: value } and is sorted by attribute.
        """
        album_dict = self.tracks[0].to_dict()  # type: ignore
        for track in self.tracks[1:]:  # type: ignore
            for key, value in track.to_dict().items():
                if key not in album_dict or album_dict[key] != value:
                    album_dict[key] = "Various"

        return album_dict

    @classmethod
    def get_or_create(
        cls: Type[A],
        session: sqlalchemy.orm.session.Session,
        artist: str,
        title: str,
        year: int,
    ) -> A:
        """Fetches the matching album or creates a new one if it doesn't exist."""
        album = (
            session.query(Album)
            .filter(Album.artist == artist)
            .filter(Album.title == title)
            .filter(Album.year == year)
            .scalar()
        )

        return album if album else Album(artist=artist, title=title, year=year)


# Track generic, used for typing classmethod
T = TypeVar("T", bound="Track")  # noqa: WPS111


class Track(MusicItem, Base):  # noqa: WPS230
    """A single track.

    Attributes:
        album (str)
        albumartist (str)
        artist (str)
        path (pathlib.Path): Path of the track file.
        title (str)
        track_num (int)
        year (int): Album release year.

    Note:
        Alterting any album-related properties (all association_proxy) attributes,
        will result in changing the album field and thus all other tracks in the
        album as well.
    """

    __tablename__ = "tracks"
    __table_args__ = (UniqueConstraint("_album_id", "track_num"),)

    _id = Column(Integer, primary_key=True)
    _album_id = Column(Integer, ForeignKey("albums._id"))
    artist = Column(String, nullable=False, default="")
    path = Column(_PathType, nullable=False, unique=True)
    title = Column(String, nullable=False, default="")
    track_num = Column(Integer, nullable=False)

    _album_obj = relationship("Album", back_populates="tracks")

    album = association_proxy("_album_obj", "title")
    albumartist = association_proxy("_album_obj", "artist")
    year = association_proxy("_album_obj", "year")

    def __init__(  # noqa: WPS211
        self,
        path: pathlib.Path,
        session: sqlalchemy.orm.session.Session,
        album: str,
        albumartist: str,
        track_num: int,
        year: int,
        **kwargs,
    ):
        """Create a track.

        If `read_tags` is `False`, then `album`, `albumartist`, `track_num`,
        and `year` must be set.

        Args:
            path: Path to the track to add.
            session: sqlalchemy session to use to query for a matching album.
            album: Album title.
            albumartist: Album artist.
            track_num: Track number.
            year: Album release year.
            **kwargs: Any other fields to assign to the Track.

        Note:
           If you wish to add several tracks to the same album,
            ensure the album already exists in the database.

        Raises:
            FileNotFoundError: Given path doesn't exit.
            ValueError: Given path already exists in the library.
        """
        if not path.exists():
            log.error(f"{path}' does not exist.")
            raise FileNotFoundError
        self.path = path

        existing_track = (
            session.query(Track.path).filter(Track.path == self.path).first()
        )
        if existing_track:
            log.error(f"{path}' already exists in the library.")
            raise ValueError

        self._album_obj = Album.get_or_create(
            session, artist=albumartist, title=album, year=year
        )

        self.track_num = track_num
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def from_tags(
        cls: Type[T], path: pathlib.Path, session: sqlalchemy.orm.session.Session
    ) -> T:
        """Alternate initializer that creates a Track from it's tags.

        Will read any tags from the file at path and save them to the Track.

        Args:
            path: Path to the track to add.
            session: sqlalchemy session to use to query for a matching album.

        Returns:
            Track instance.

        Raises:
            FileNotFoundError: Given path doesn't exit.
        """
        if not path.exists():
            log.error(f"{path}' does not exist.")
            raise FileNotFoundError

        audio_file = MediaFile(path)

        return cls(
            path=path,
            session=session,
            album=audio_file.album,
            albumartist=audio_file.albumartist,
            track_num=audio_file.track,
            year=audio_file.year,
            artist=audio_file.artist,
            title=audio_file.title,
        )

    def to_dict(self) -> "OrderedDict[str, Any]":
        """Represents the Track as a dictionary.

        Only public attributes that are not empty will be included.

        Returns:
            Returns a dict representation of a Track.
            It will be in the form { attribute: value } and is sorted by attribute.
        """
        track_dict = OrderedDict()
        for attr in dir(self):  # noqa: WPS421
            if not attr.startswith("_") and attr != "metadata":
                value = getattr(self, attr)
                if value and not isinstance(value, types.MethodType):
                    track_dict[attr] = value

        return track_dict

    def __str__(self):
        """String representation of a track."""
        return f"{self.artist} - {self.title}"


@contextmanager
def session_scope():
    """Provides a transactional scope around a series of operations.

    Yields:
        A database session to use.
    """
    session = Session()
    yield session
    try:
        session.commit()
    except:  # noqa: E722
        session.rollback()
        raise
    finally:
        session.close()
