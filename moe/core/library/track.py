"""A Track in the database and any related logic."""

import logging
import pathlib
import types
from collections import OrderedDict
from typing import TYPE_CHECKING, Any, List, Set, Type, TypeVar

import mediafile
import sqlalchemy
from sqlalchemy import Column, Integer, String  # noqa: WPS458
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey, ForeignKeyConstraint, Table

from moe.core.library.album import Album
from moe.core.library.lib_item import LibItem, PathType
from moe.core.library.session import Base

# Makes hybrid_property's have the same typing as a normal properties.
# Use until the stubs are improved.
if TYPE_CHECKING:
    typed_hybrid_property = property
else:
    from sqlalchemy.ext.hybrid import (  # noqa: WPS440
        hybrid_property as typed_hybrid_property,
    )

log = logging.getLogger(__name__)


class _Genre(Base):
    """A track can have multiple genres."""

    __tablename__ = "genres"

    name: str = Column(String, nullable=False, primary_key=True)

    def __init__(self, name: str):
        self.name = name


track_genres = Table(
    "track_genres",
    Base.metadata,
    Column("genre", String, ForeignKey("genres.name")),
    Column("track_path", PathType, ForeignKey("tracks.path")),
)
__table_args__ = ()


# Track generic, used for typing classmethod
T = TypeVar("T", bound="Track")  # noqa: WPS111


class Track(LibItem, Base):  # noqa: WPS230, WPS214
    """A single track.

    Attributes:
        album (str)
        albumartist (str)
        album_obj (Album): Corresponding Album object.
        album_path (pathlib.Path): Path of the album directory.
        artist (str)
        file_ext (str): Audio format extension e.g. mp3, flac, wav, etc.
        genre (Set[str])
        path (pathlib.Path): Filesystem path of the track file.
        title (str)
        track_num (int)
        year (int): Album release year.

    Note:
        Altering any album-related property attributes, will result in changing the
        album field and thus all other tracks in the album as well.
    """

    __tablename__ = "tracks"

    # unqiue track = track_num + Album
    track_num: int = Column(
        Integer, nullable=False, primary_key=True, autoincrement=False
    )
    _albumartist = Column(String, nullable=False, primary_key=True)
    _album = Column(String, nullable=False, primary_key=True)
    _year = Column(Integer, nullable=False, primary_key=True, autoincrement=False)

    artist: str = Column(String, nullable=False, default="")
    file_ext: str = Column(String, nullable=False, default="")
    path: pathlib.Path = Column(PathType, nullable=False, unique=True)
    title: str = Column(String, nullable=False, default="")

    genre: Set[str] = association_proxy("_genre_obj", "name")

    album_obj: Album = relationship("Album", back_populates="tracks")
    _genre_obj: _Genre = relationship(
        "_Genre", secondary=track_genres, collection_class=set
    )
    __table_args__ = (
        ForeignKeyConstraint(
            ["_albumartist", "_album", "_year"],
            ["albums.artist", "albums.title", "albums.year"],
        ),
    )

    def __init__(
        self,
        album: Album,
        path: pathlib.Path,
        track_num: int,
        **kwargs,
    ):
        """Create a track.

        Args:
            album: Album the track belongs to.
            path: Filesystem path of the track file.
            track_num: Track number.
            **kwargs: Any other fields to assign to the Track.

        Note:
            If you wish to add several tracks to the same album, ensure the album
            already exists in the database, or use `session.merge()`.
        """
        self.album_obj = album
        self._album = album.title
        self._albumartist = album.artist
        self._year = album.year
        self.path = path
        self.track_num = track_num

        for key, value in kwargs.items():
            setattr(self, key, value)

    @typed_hybrid_property
    def album(self) -> str:
        """Returns the album's title."""
        return self.album_obj.title

    @album.setter
    def album(self, new_album_title: str):  # noqa: WPS440
        """Changes the title of the Album this Track belongs to."""
        self.album_obj.title = new_album_title

    @typed_hybrid_property
    def albumartist(self) -> str:
        """Returns the album's artist."""
        return self.album_obj.artist

    @albumartist.setter
    def albumartist(self, new_albumartist: str):  # noqa: WPS440
        """Changes the artist of the Album this Track belongs to."""
        self.album_obj.artist = new_albumartist

    @typed_hybrid_property
    def album_path(self) -> pathlib.Path:
        """Returns the directory path of the album."""
        return self.album_obj.path

    @album_path.setter
    def album_path(self, new_album_path: pathlib.Path):  # noqa: WPS440
        """Changes the path of the Album this Track belongs to.

        Be careful changing this that you ensure each item in the Album physically
        resides under this path.

        Args:
            new_album_path: New album path.
        """
        self.album_obj.path = new_album_path

    @typed_hybrid_property
    def year(self) -> int:
        """Returns the album's artist."""
        return self.album_obj.year

    @year.setter
    def year(self, new_year: int):  # noqa: WPS440
        """Changes the year of the Album this Track belongs to."""
        self.album_obj.year = new_year

    @classmethod
    def from_tags(cls: Type[T], path: pathlib.Path) -> T:
        """Alternate initializer that creates a Track from its tags.

        Will read any tags from the given path and save them to the Track.

        Args:
            path: Filesystem path of the track to add.

        Returns:
            Track instance.

        Raises:
            TypeError: Missing required tags.
        """
        audio_file = mediafile.MediaFile(path)

        missing_tags: List[str] = []
        if not audio_file.album:
            missing_tags.append("album")
        if not audio_file.albumartist:
            missing_tags.append("albumartist")
        if not audio_file.track:
            missing_tags.append("track_num")
        if not audio_file.year:
            missing_tags.append("year")
        if missing_tags:
            raise TypeError(
                f"'{path}' is missing required tag(s): {', '.join(missing_tags)}"
            )

        album = Album(
            artist=audio_file.albumartist,
            title=audio_file.album,
            year=audio_file.year,
            path=path.parent,
        )
        return cls(
            album=album,
            path=path,
            track_num=audio_file.track,
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

    def __str__(self):
        """String representation of a track."""
        return f"{self.artist} - {self.title}"

    def __repr__(self):
        """Represents a Track using its primary and other common keys."""
        return (
            f"{self.__class__.__name__}("
            f"{repr(self.album_obj)}, "
            f"artist={repr(self.artist)}, "
            f"title={repr(self.title)}, "
            f"track_num={repr(self.track_num)}, "
            f"filename={repr(self.filename)})"
        )
