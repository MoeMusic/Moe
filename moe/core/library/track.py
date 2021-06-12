"""A Track in the database and any related logic."""

import errno
import logging
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
from moe.core.library.music_item import MusicItem, PathType
from moe.core.library.session import Base

log = logging.getLogger(__name__)


class _Genre(Base):
    """A track can have multiple genres."""

    __tablename__ = "genres"

    name = Column(String, nullable=False, primary_key=True)

    def __init__(self, name: str):
        self.name = name


track_genres = Table(
    "track_genres",
    Base.metadata,
    Column("genre", String, ForeignKey("genres.name")),
    Column("track_path", PathType, ForeignKey("tracks.path")),
)


# Track generic, used for typing classmethod
T = TypeVar("T", bound="Track")  # noqa: WPS111


class Track(MusicItem, Base):  # noqa: WPS230, WPS214
    """A single track.

    Attributes:
        album (str)
        albumartist (str)
        album_path (pathlib.Path): Path of the album directory.
        artist (str)
        file_ext (str): Audio format extension e.g. mp3, flac, wav, etc.
        genre (Set[str])
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
    file_ext = Column(String, nullable=False, default="")
    path = Column(PathType, nullable=False, unique=True)
    title = Column(String, nullable=False, default="")

    genre = association_proxy("_genre_obj", "name")

    _album_obj: Album = relationship("Album", back_populates="tracks")
    _genre_obj: _Genre = relationship(
        "_Genre", secondary=track_genres, collection_class=set
    )

    __table_args__ = (
        ForeignKeyConstraint(
            [_albumartist, _album, _year],
            [Album.artist, Album.title, Album.year],  # type: ignore
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
        """Setting a new album title assigns the track to a different album."""
        self._album_obj = Album(
            artist=self.albumartist, title=new_album_title, year=self.year
        )

    @hybrid_property
    def albumartist(self) -> str:
        """Allow the album's artist to be accessible by the track."""
        return self._album_obj.artist

    @albumartist.setter  # type: ignore
    def albumartist(self, new_albumartist: str):  # noqa: WPS440
        """Setting a new album artist assigns the track to a different album."""
        self._album_obj = Album(
            artist=new_albumartist, title=self.album, year=self.year
        )

    @hybrid_property
    def album_path(self) -> pathlib.Path:
        """Returns the directory path of the album."""
        return self._album_obj.path

    @hybrid_property
    def year(self) -> int:
        """Allow the album's year to be accessible by the track."""
        return self._album_obj.year

    @year.setter  # type: ignore
    def year(self, new_album_year: int):  # noqa: WPS440
        """Setting a new album year assigns the track to a different album."""
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
            file_ext=audio_file.type,
            genre=audio_file.genres,
            title=audio_file.title,
        )

    @staticmethod
    def get_attr(field: str) -> sqlalchemy.orm.attributes.InstrumentedAttribute:
        """Gets a Track's attribute for the given field.

        This is essentially a custom ``getattr()`` because the builtin one doesn't work
        with hybrid properties.

        Args:
            field: Track attribute to retrieve.

        Returns:
            The associated Track attribute for a given field.

        Raises:
            ValueError: Invalid Track field given.
        """
        # hybrid attributes
        if field == "album":
            return Album.title
        elif field == "albumartist":
            return Album.artist
        elif field == "album_path":
            return Album.path
        elif field == "year":
            return Album.year

        # normal Track field
        try:
            return getattr(Track, field)
        except AttributeError:
            log.error(f"Invalid Track field: {field}")
            raise ValueError

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
                if (
                    value
                    and not isinstance(value, types.MethodType)
                    and not isinstance(value, types.FunctionType)
                ):
                    track_dict[attr] = value

        return track_dict

    def write_tags(self):
        """Write tags to the file."""
        audio_file = mediafile.MediaFile(self.path)

        audio_file.album = self.album
        audio_file.albumartist = self.albumartist
        audio_file.artist = self.artist
        audio_file.genres = self.genre
        audio_file.title = self.title
        audio_file.track = self.track_num
        audio_file.year = self.year

        audio_file.save()

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
