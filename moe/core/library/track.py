"""A Track in the database and any related logic."""

import errno
import os
import pathlib
import types
from collections import OrderedDict
from typing import Any, List, Type, TypeVar

import mediafile
import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import events, relationship
from sqlalchemy.schema import ForeignKey, Table, UniqueConstraint

from moe.core.library.album import Album
from moe.core.library.music_item import MusicItem
from moe.core.library.session import Base


class _PathType(sqlalchemy.types.TypeDecorator):
    """A custom type for paths for database storage.

    Normally, paths are pathlib.Path type, but we can't store that in the database,
    so we normalize the paths first for database storage.
    """

    impl = sqlalchemy.types.String  # sql type

    def process_bind_param(self, pathlib_path, dialect):
        """Convert the absolute path to a string prior to enterting in the database."""
        return str(pathlib_path.resolve())

    def process_result_value(self, path_str, dialect):
        """Convert the path back to pathlib.Path on the way out."""
        return pathlib.Path(path_str)


class _Genre(Base):
    """A track can have multiple genres."""

    __tablename__ = "genres"

    _id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __init__(self, name):
        self.name = name


track_genres = Table(
    "association",
    Base.metadata,
    Column("genre_id", Integer, ForeignKey("genres._id")),
    Column("track_id", Integer, ForeignKey("tracks._id")),
)


# Track generic, used for typing classmethod
T = TypeVar("T", bound="Track")  # noqa: WPS111


class Track(MusicItem, Base):  # noqa: WPS230
    """A single track.

    Attributes:
        album (str)
        albumartist (str)
        artist (str)
        genre (List[str])
        path (pathlib.Path): Path of the track file.
        title (str)
        track_num (int)
        year (int): Album release year.

    Note:
        Altering any album-related properties (all association_proxy) attributes,
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

    _genre_obj = relationship("_Genre", secondary=track_genres)
    genre = association_proxy("_genre_obj", "name")

    def __init__(  # noqa: WPS211
        self,
        path: pathlib.Path,
        album: str,
        albumartist: str,
        track_num: int,
        year: int,
        session: sqlalchemy.orm.session.Session,
        **kwargs,
    ):
        """Create a track.

        Args:
            path: Path to the track to add.
            album: Album title.
            albumartist: Album artist.
            track_num: Track number.
            year: Album release year.
            session: sqlalchemy session to use to query for a matching album.
            **kwargs: Any other fields to assign to the Track.

        Note:
           If you wish to add several tracks to the same album,
            ensure the album already exists in the database.

        Raises:
            TypeError: None value found in arguments.
        """
        missing_tags: List[str] = []
        if album is None:
            missing_tags.append("album")
        if albumartist is None:
            missing_tags.append("albumartist")
        if track_num is None:
            missing_tags.append("track_num")
        if year is None:
            missing_tags.append("year")
        if missing_tags:
            raise TypeError(
                f"'{path}' is missing required tag(s): {', '.join(missing_tags)}"
            )

        self._album_obj = Album.get_or_create(
            session, artist=albumartist, title=album, year=year
        )

        self.path = path
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
        """
        audio_file = mediafile.MediaFile(path)

        return cls(
            path=path,
            session=session,
            album=audio_file.album,
            albumartist=audio_file.albumartist,
            track_num=audio_file.track,
            year=audio_file.year,
            artist=audio_file.artist,
            title=audio_file.title,
            genre=audio_file.genres,
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


@sqlalchemy.event.listens_for(Track.path, "set")
def track_path_set(
    target: Track,
    value: pathlib.Path,
    oldvalue: pathlib.Path,
    initiator: events.AttributeEvents,
):
    """Only allow paths that exist."""
    if not value.is_file():
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), str(value.resolve())
        )
