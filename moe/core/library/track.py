"""A Track in the database and any related logic."""

import datetime
import logging
from pathlib import Path
from typing import List, Tuple, Type, TypeVar

import mediafile
import sqlalchemy
from sqlalchemy import Column, Integer, String  # noqa: WPS458
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey, Table, UniqueConstraint

from moe.core.library.album import Album
from moe.core.library.lib_item import LibItem, PathType
from moe.core.library.session import Base

__all__ = ["Track", "TrackError"]

log = logging.getLogger("moe.track")


class TrackError(Exception):
    """Error creating a Track."""


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


class Track(LibItem, Base):
    """A single track.

    Attributes:
        album (str)
        albumartist (str)
        album_obj (Album): Corresponding Album object.
        artist (str)
        date (datetime.date): Album release date.
        disc (int): Disc number the track is on.
        disc_total (int): Number of discs in the album.
        genre (str): String of all genres concatenated with ';'.
        genres (List[str]): List of all genres.
        mb_album_id (str): Musicbrainz album aka release ID.
        mb_track_id (str): Musicbrainz track ID.
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
    disc: int = Column(Integer, nullable=False, default=1)
    mb_track_id: str = Column(String, nullable=False, default="")
    path: Path = Column(PathType, nullable=False, unique=True)
    title: str = Column(String, nullable=False, default="")
    track_num: int = Column(Integer, nullable=False)

    _album_id: int = Column(Integer, ForeignKey("album._id"))
    album_obj: Album = relationship("Album", back_populates="tracks")
    album: str = association_proxy("album_obj", "title")
    albumartist: str = association_proxy("album_obj", "artist")
    date: datetime.date = association_proxy("album_obj", "date")
    disc_total: int = association_proxy("album_obj", "disc_total")
    mb_album_id: str = association_proxy("album_obj", "mb_album_id")
    year: int = association_proxy("album_obj", "year")

    _genres: List[_Genre] = relationship(
        "_Genre", secondary=track_genre, collection_class=list
    )
    genres: List[str] = association_proxy("_genres", "name")

    __table_args__ = (UniqueConstraint("disc", "track_num", "_album_id"),)

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
        self.disc = 1
        self.mb_track_id = ""
        self.title = ""

        for key, value in kwargs.items():
            if value:
                setattr(self, key, value)

    @classmethod
    def from_tags(cls: Type[T], path: Path, album_path: Path = None) -> T:
        """Alternate initializer that creates a Track from its tags.

        Will read any tags from the given path and save them to the Track.

        Args:
            path: Filesystem path of the track to add.
            album_path: Filesystem path of the track's album. Defaults to using the
                parent of the track path.

        Returns:
            Track instance.

        Raises:
            TrackError: Missing required tags.
        """
        audio_file = mediafile.MediaFile(path)

        missing_tags: List[str] = []
        if not audio_file.album:
            missing_tags.append("album")
        if not audio_file.albumartist and not audio_file.artist:
            missing_tags.append("albumartist")
        if not audio_file.track:
            missing_tags.append("track_num")
        if not audio_file.date:
            missing_tags.append("date")
        if missing_tags:
            raise TrackError(
                f"'{path}' is missing required tag(s): {', '.join(missing_tags)}"
            )

        # use artist as the backup for the albumartist if missing
        if audio_file.albumartist:
            albumartist = audio_file.albumartist
        else:
            log.debug(
                f"'{path}' is missing an albumartist, using the artist"
                f" '{audio_file.artist}' as a backup."
            )
            albumartist = audio_file.artist

        if not album_path:
            album_path = path.parent
        album = Album(
            artist=albumartist,
            title=audio_file.album,
            date=audio_file.date,
            disc_total=audio_file.disctotal,
            mb_album_id=audio_file.mb_albumid,
            path=album_path,
        )
        return cls(
            album=album,
            path=path,
            track_num=audio_file.track,
            artist=audio_file.artist,
            disc=audio_file.disc,
            genres=audio_file.genres,
            mb_track_id=audio_file.mb_releasetrackid,
            title=audio_file.title,
        )

    @property
    def genre(self) -> str:
        """Returns a string of all genres concatenated with ';'."""
        return ";".join(self.genres)

    @genre.setter
    def genre(self, genre_str: str):
        """Sets a track's genre from a string.

        Args:
            genre_str: For more than one genre, they should be split with ';'.
        """
        self.genres = [genre.strip() for genre in genre_str.split(";")]

    def fields(self) -> Tuple[str, ...]:
        """Returns the public fields, or non-method attributes, of a Track."""
        return (
            "album",
            "albumartist",
            "album_obj",
            "artist",
            "date",
            "disc",
            "disc_total",
            "genre",
            "genres",
            "mb_album_id",
            "mb_track_id",
            "path",
            "title",
            "track_num",
            "year",
        )

    def __eq__(self, other) -> bool:
        """Compares a Track by it's attributes."""
        if isinstance(other, Track):
            if self.album_obj.is_unique(other.album_obj):
                return False

            for attr in self.fields():
                if attr == "album_obj":  # prevent cyclic comparison
                    continue
                if getattr(self, attr) != getattr(other, attr):
                    return False
            return True
        return False

    def __lt__(self, other) -> bool:
        """Sort based on album, then disc, then track number."""
        if self.album_obj == other.album_obj:
            if self.disc == other.disc:
                return self.track_num < other.track_num

            return self.disc < other.disc

        return self.album_obj < other.album_obj

    def __str__(self):
        """String representation of a track."""
        return f"{self.artist} - {self.title}"

    def __repr__(self):
        """Represents a Track using its primary key, unique fields, title and artist."""
        return (
            f"{self.__class__.__name__}("
            f"id={repr(self._id)}, "
            f"disc={repr(self.disc)}, "
            f"track_num={repr(self.track_num)}, "
            f"{repr(self.album_obj)}, "
            f"artist={repr(self.artist)}, "
            f"title={repr(self.title)}, "
            f"path={repr(self.path)})"
        )

    @sqlalchemy.orm.validates("_genres")
    def _append_genre(self, key: str, genre: _Genre) -> _Genre:
        """Prevents duplicate genres in the database by returning any existing ones."""
        genre_session = sqlalchemy.orm.sessionmaker.object_session(self)
        if not genre_session:
            return genre

        persistent_genre = genre_session.get(_Genre, genre.name)
        if persistent_genre:
            return persistent_genre

        return genre
