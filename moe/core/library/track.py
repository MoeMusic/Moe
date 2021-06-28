"""A Track in the database and any related logic."""

import datetime
import logging
from pathlib import Path
from typing import List, Type, TypeVar

import mediafile
from sqlalchemy import Column, Integer, String  # noqa: WPS458
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey, Table, UniqueConstraint

from moe.core.library.album import Album
from moe.core.library.lib_item import LibItem, PathType
from moe.core.library.session import Base

log = logging.getLogger(__name__)


class _Genre(Base):
    """A track can have multiple genres."""

    __tablename__ = "genre"

    name: str = Column(String, nullable=False, primary_key=True)

    def __init__(self, name: str):
        self.name = name


track_genre = Table(
    "track_genre",
    Base.metadata,
    Column("genre", String, ForeignKey("genre.name")),
    Column("track_id", Integer, ForeignKey("track._id")),
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
        album_path (Path): Path of the album directory.
        artist (str)
        date (datetime.date): Album release date.
        file_ext (str): Audio format extension e.g. mp3, flac, wav, etc.
        genre (List[str])
        mb_album_id (str): Musicbrainz album aka release id.
        mb_id (str): Musicbrainz track aka recording id.
        path (Path): Filesystem path of the track file.
        title (str)
        track_num (int)
        year (int): Album release year.

    Note:
        Altering any album-related property attributes, will result in changing the
        album field and thus all other tracks in the album as well.
    """

    __tablename__ = "track"

    _id: int = Column(Integer, primary_key=True)
    artist: str = Column(String, nullable=False, default="")
    file_ext: str = Column(String, nullable=False, default="")
    mb_id: str = Column(String, nullable=False, default="")
    path: Path = Column(PathType, nullable=False, unique=True)
    title: str = Column(String, nullable=False, default="")
    track_num: int = Column(Integer, nullable=False)

    _album_id: int = Column(Integer, ForeignKey("album._id"))
    album_obj: Album = relationship("Album", back_populates="tracks")
    album: str = association_proxy("album_obj", "title")
    album_path: Path = association_proxy("album_obj", "path")
    albumartist: str = association_proxy("album_obj", "artist")
    date: datetime.date = association_proxy("album_obj", "date")
    mb_album_id: str = association_proxy("album_obj", "mb_id")
    year: int = association_proxy("album_obj", "year")

    _genres: List[_Genre] = relationship(
        "_Genre", secondary=track_genre, collection_class=list
    )
    genre: List[str] = association_proxy("_genres", "name")

    __table_args__ = (UniqueConstraint("track_num", "_album_id"),)

    def __init__(self, album: Album, track_num: int, path: Path, **kwargs):
        """Create a track.

        Args:
            album: Album the track belongs to.
            track_num: Track number.
            path: Filesystem path of the track file.
            **kwargs: Any other fields to assign to the Track.

        Note:
            If you wish to add several tracks to the same album, ensure the album
            already exists in the database, or use `session.merge()`.
        """
        self.album_obj = album
        self.path = path
        self.track_num = track_num

        # set default values
        self.artist = ""
        self.file_ext = ""
        self.mb_id = ""
        self.title = ""

        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def from_tags(cls: Type[T], path: Path) -> T:
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
        if not audio_file.date:
            missing_tags.append("date")
        if missing_tags:
            raise TypeError(
                f"'{path}' is missing required tag(s): {', '.join(missing_tags)}"
            )

        album = Album(
            artist=audio_file.albumartist,
            title=audio_file.album,
            date=audio_file.date,
            mb_id=audio_file.mb_albumid,
            path=path.parent,
        )
        return cls(
            album=album,
            path=path,
            track_num=audio_file.track,
            artist=audio_file.artist,
            file_ext=audio_file.type,
            genre=audio_file.genres,
            mb_id=audio_file.mb_trackid,
            title=audio_file.title,
        )

    def __str__(self):
        """String representation of a track."""
        return f"{self.artist} - {self.title}"

    def __repr__(self):
        """Represents a Track using its primary key, unique fields, title and artist."""
        return (
            f"{self.__class__.__name__}("
            f"id={repr(self._id)}, "
            f"track_num={repr(self.track_num)}, "
            f"{repr(self.album_obj)}, "
            f"artist={repr(self.artist)}, "
            f"title={repr(self.title)}, "
            f"path={repr(self.path)})"
        )

    def __eq__(self, other):
        """Compares a Track by it's attributes."""
        if isinstance(other, Track):
            return (
                self.album_obj.artist == other.album_obj.artist  # noqa: WPS222
                and self.album_obj.date == other.album_obj.date
                and self.album_obj.title == other.album_obj.title
                and self.artist == other.artist
                and self.file_ext == other.file_ext
                and set(self.genre) == set(other.genre)
                and self.mb_id == other.mb_id
                and self.path == other.path
                and self.title == other.title
                and self.track_num == other.track_num
            )
        return False
