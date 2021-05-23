"""A Track in the database and any related logic."""

import errno
import os
import pathlib
import types
from collections import OrderedDict
from typing import Any, List, Type, TypeVar

import mediafile
import sqlalchemy
from sqlalchemy import Column, Integer, String  # noqa: WPS458
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import events, relationship
from sqlalchemy.schema import ForeignKey, ForeignKeyConstraint, Table

from moe.core.library.album import Album
from moe.core.library.music_item import MusicItem
from moe.core.library.session import Base


class _PathType(sqlalchemy.types.TypeDecorator):
    """A custom type for paths for database storage.

    Normally, paths are pathlib.Path type, but we can't store that in the database,
    so we normalize the paths first for database storage.
    """

    impl = sqlalchemy.types.String  # sql type
    cache_ok = True  # expected to produce same bind/result behavior and sql generation

    def process_bind_param(self, pathlib_path, dialect):
        """Convert the absolute path to a string prior to enterting in the database."""
        return str(pathlib_path.resolve())

    def process_result_value(self, path_str, dialect):
        """Convert the path back to pathlib.Path on the way out."""
        return pathlib.Path(path_str)


class _Genre(Base):
    """A track can have multiple genres."""

    __tablename__ = "genres"

    name = Column(String, nullable=False, primary_key=True)

    def __init__(self, name):
        self.name = name


track_genres = Table(
    "association",
    Base.metadata,
    Column("genre", String, ForeignKey("genres.name")),
    Column("track_path", _PathType, ForeignKey("tracks.path")),
)


# Track generic, used for typing classmethod
T = TypeVar("T", bound="Track")  # noqa: WPS111


class Track(MusicItem, Base):  # noqa: WPS230, WPS214
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
        Altering any album-related property attributes, will result in changing the
        album field and thus all other tracks in the album as well.
    """

    __tablename__ = "tracks"

    # unqiue track = track_num + Album
    track_num = Column(Integer, nullable=False, primary_key=True, autoincrement=False)
    _albumartist = Column(String, nullable=False, primary_key=True)
    _album = Column(String, nullable=False, primary_key=True)
    _year = Column(Integer, nullable=False, primary_key=True, autoincrement=False)

    artist = Column(String, nullable=False, default="")
    path = Column(_PathType, nullable=False, unique=True)
    title = Column(String, nullable=False, default="")

    genre = association_proxy("_genre_obj", "name")

    _album_obj: Album = relationship("Album", back_populates="tracks")
    _genre_obj: _Genre = relationship("_Genre", secondary=track_genres)

    __table_args__ = (
        ForeignKeyConstraint(
            [_albumartist, _album, _year],
            [Album.artist, Album.title, Album.year],
        ),
    )

    def __init__(  # noqa: WPS211
        self,
        path: pathlib.Path,
        album: str,
        albumartist: str,
        track_num: int,
        year: int,
        **kwargs,
    ):
        """Create a track.

        Args:
            path: Filesystem path of the track to add.
            album: Album title.
            albumartist: Album artist.
            track_num: Track number.
            year: Album release year.
            **kwargs: Any other fields to assign to the Track.

        Note:
            If you wish to add several tracks to the same album, ensure the album
            already exists in the database, or use `session.merge()`.

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

        self._album_obj = Album(artist=albumartist, title=album, year=year)
        self._album = album
        self._albumartist = albumartist
        self._year = year

        self.path = path
        self.track_num = track_num

        for key, value in kwargs.items():
            setattr(self, key, value)

    @hybrid_property
    def album(self) -> str:
        """Allow the album's title to be accessible by the track."""
        return self._album_obj.title

    @album.setter  # type: ignore
    def album(self, new_album_title: str):  # noqa: WPS440
        """Setting a new album title should assign the track to a different album."""
        self._album_obj = Album(
            artist=self.albumartist, title=new_album_title, year=self.year
        )

    @hybrid_property
    def albumartist(self) -> str:
        """Allow the album's artist to be accessible by the track."""
        return self._album_obj.artist

    @albumartist.setter  # type: ignore
    def albumartist(self, new_albumartist: str):  # noqa: WPS440
        """Setting a new album artist should assign the track to a different album."""
        self._album_obj = Album(
            artist=new_albumartist, title=self.album, year=self.year
        )

    @hybrid_property
    def year(self) -> int:
        """Allow the album's year to be accessible by the track."""
        return self._album_obj.year

    @year.setter  # type: ignore
    def year(self, new_album_year: str):  # noqa: WPS440
        """Setting a new album year should assign the track to a different album."""
        self._album_obj = Album(
            artist=self.albumartist, title=self.album, year=new_album_year
        )

    @classmethod
    def from_tags(cls: Type[T], path: pathlib.Path) -> T:
        """Alternate initializer that creates a Track from its tags.

        Will read any tags from the given path and save them to the Track.

        Args:
            path: Filesystem path of the track to add.

        Returns:
            Track instance.
        """
        audio_file = mediafile.MediaFile(path)

        return cls(
            path=path,
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

        Only public attributes that are not empty will be included. We also remove any
        attributes that are not relevant to the music file e.g. sqlalchemy specific
        attributes.

        Returns:
            Returns a dict representation of a Track.
            It will be in the form { attribute: value } and is sorted by attribute.
        """
        track_dict = OrderedDict()
        for attr in dir(self):  # noqa: WPS421
            if not attr.startswith("_") and attr != "metadata" and attr != "registry":
                value = getattr(self, attr)
                if value and not isinstance(value, types.MethodType):
                    track_dict[attr] = value

        return track_dict

    def __str__(self):
        """String representation of a track."""
        return f"{self.artist} - {self.title}"

    def __repr__(self):
        """Track representation using the primary keys."""
        return f"{self.albumartist} - {self.album} ({self.year}): {self.track_num}"


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
