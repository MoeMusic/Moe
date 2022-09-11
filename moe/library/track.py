"""A Track in the database and any related logic."""

import datetime
import logging
from pathlib import Path
from typing import Optional, TypeVar, cast

import mediafile
import pluggy
import sqlalchemy.orm as sa_orm
from sqlalchemy import JSON, Column, Integer, String, and_, or_
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import joinedload, relationship
from sqlalchemy.schema import ForeignKey, Table, UniqueConstraint

import moe
from moe.config import Config, MoeSession
from moe.library import SABase
from moe.library.album import Album
from moe.library.lib_item import LibItem, PathType

__all__ = ["Track", "TrackError"]

log = logging.getLogger("moe.track")


class Hooks:
    """Track hook specifications."""

    @staticmethod
    @moe.hookspec
    def create_custom_track_fields(config: Config) -> list[str]:  # type: ignore
        """Creates new custom fields for a Track.

        Args:
            config: Moe config.

        Returns:
            A list of any new fields you wish to create.

        Example:
            Inside your hook implementation::

                return "my_new_field"

            You can then access your new field as if it were a normal field::

                track.my_new_field = "awesome new value"

        Important:
            Your custom field should follow the same naming rules as any other python
            variable i.e. no spaces, starts with a letter, and consists solely of
            alpha-numeric and underscore characters.
        """  # noqa: DAR202


@moe.hookimpl
def add_hooks(plugin_manager: pluggy.manager.PluginManager):
    """Registers `track` hookspecs to Moe."""
    from moe.library.track import Hooks

    plugin_manager.add_hookspecs(Hooks)


class TrackError(Exception):
    """Error creating a Track."""


class _Genre(SABase):
    """A track can have multiple genres."""

    __tablename__ = "genre"

    name: str = cast(str, Column(String, nullable=False, primary_key=True))

    def __init__(self, name: str):
        self.name = name


track_genre = Table(
    "track_genre",
    SABase.metadata,
    Column("genre", String, ForeignKey("genre.name")),
    Column("track_id", Integer, ForeignKey("track._id")),
)
__table_args__ = ()


# Track generic, used for typing classmethod
T = TypeVar("T", bound="Track")


class Track(LibItem, SABase):
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
        genres (list[str]): List of all genres.
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

    _id: int = cast(int, Column(Integer, primary_key=True))
    artist: str = cast(str, Column(String, nullable=False))
    disc: int = cast(int, Column(Integer, nullable=False, default=1))
    mb_track_id: str = cast(str, Column(String, nullable=True, unique=True))
    path: Path = cast(Path, Column(PathType, nullable=False, unique=True))
    title: str = cast(str, Column(String, nullable=False))
    track_num: int = cast(int, Column(Integer, nullable=False))
    _custom_fields: dict[str, Optional[str]] = cast(
        dict[str, Optional[str]],
        Column(MutableDict.as_mutable(JSON(none_as_null=True))),
    )

    _album_id: int = cast(int, Column(Integer, ForeignKey("album._id")))
    album_obj: Album = relationship("Album", back_populates="tracks")
    album: str = association_proxy("album_obj", "title")
    albumartist: str = association_proxy("album_obj", "artist")
    date: datetime.date = association_proxy("album_obj", "date")
    disc_total: int = association_proxy("album_obj", "disc_total")
    mb_album_id: str = association_proxy("album_obj", "mb_album_id")
    year: int = association_proxy("album_obj", "year")

    _genres: list[_Genre] = relationship(
        "_Genre",
        secondary=track_genre,
        collection_class=list,
        cascade="save-update, merge, expunge",
    )
    genres: list[str] = association_proxy("_genres", "name")

    __table_args__ = (UniqueConstraint("disc", "track_num", "_album_id"),)

    def __init__(
        self,
        config: Config,
        album: Album,
        path: Path,
        title: str,
        track_num: int,
        **kwargs,
    ):
        """Creates a Track.

        Args:
            config: Moe config.
            album: Album the track belongs to.
            path: Filesystem path of the track file.
            title: Title of the track.
            track_num: Track number.
            **kwargs: Any other fields to assign to the track.
        """
        self.config = config
        self.__dict__["_custom_fields"] = {}
        custom_fields = config.plugin_manager.hook.create_custom_track_fields(
            config=config
        )
        for plugin_fields in custom_fields:
            for plugin_field in plugin_fields:
                self._custom_fields[plugin_field] = None

        album.tracks.append(self)
        self.path = path
        self.title = title
        self.track_num = track_num

        self.artist = self.albumartist  # default value

        for key, value in kwargs.items():
            if value:
                setattr(self, key, value)

        if not self.disc:
            self.disc = self._guess_disc()

        log.debug(f"Track created. [track={self!r}]")

    def _guess_disc(self) -> int:
        """Attempts to guess the disc of a track based on it's path."""
        log.debug(f"Guessing track disc number. [track={self!r}]")

        if self.path.parent == self.album_obj.path:
            return 1

        # The track is in a subdirectory of the album - most likely disc directories.
        disc_dirs: list[Path] = []
        for path in self.album_obj.path.iterdir():
            if not path.is_dir():
                continue

            contains_tracks = False
            for album_track in self.album_obj.tracks:
                if album_track.path.is_relative_to(path):
                    contains_tracks = True

            if contains_tracks:
                disc_dirs.append(path)

        # Guess the disc by the order of the disc directory it appears in.
        for disc_num, disc_dir in enumerate(sorted(disc_dirs), start=1):
            if self.path.is_relative_to(disc_dir):
                return disc_num

        return 1

    @classmethod
    def from_file(
        cls: type[T], config: Config, track_path: Path, album: Optional[Album] = None
    ) -> T:
        """Alternate initializer that creates a Track from a track file.

        Will read any tags from the given path and save them to the Track.

        Args:
            config: Moe config.
            track_path: Filesystem path of the track.
            album: Corresponding album for the track. If not given, the album will be
                created.

        Returns:
            Track instance.

        Raises:
            TrackError: Given ``path`` does not correspond to a track file.
        """
        log.debug(f"Creating track from path. [path={track_path}, {album=}]")

        try:
            audio_file = mediafile.MediaFile(track_path)
        except mediafile.UnreadableFileError as err:
            raise TrackError(
                "Unable to create track; given path is not a track file. "
                f"[path={track_path}]"
            ) from err

        if not album:
            albumartist = audio_file.albumartist or audio_file.artist

            album = Album(
                config=config,
                artist=albumartist,
                title=audio_file.album,
                date=audio_file.date,
                disc_total=audio_file.disctotal,
                mb_album_id=audio_file.mb_albumid,
                path=track_path.parent,
            )

        return cls(
            config=config,
            album=album,
            path=track_path,
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

    def fields(self) -> tuple[str, ...]:
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

    def get_existing(self) -> Optional["Track"]:
        """Gets a matching Track in the library by its unique attributes.

        Returns:
            Duplicate track or the same track if it already exists in the library.
        """
        log.debug(f"Searching library for existing track. [track={self!r}]")

        session = MoeSession()
        existing_track = (
            session.query(Track)
            .filter(
                or_(
                    Track.path == self.path,
                    and_(
                        Track.mb_track_id == self.mb_track_id,
                        Track.mb_track_id != None,  # noqa: E711
                    ),
                    and_(
                        Track.track_num == self.track_num,
                        Track.disc == self.disc,
                        Track._album_id == self._album_id,
                    ),
                )
            )
            .options(joinedload("*"))
            .one_or_none()
        )
        if not existing_track:
            log.debug("No matching track found.")
            return None

        log.debug(f"Matching track found. [match={existing_track!r}]")
        return existing_track

    def merge(self, other: "Track", overwrite: bool = False):
        """Merges another track into this one.

        Args:
            other: Other track to be merged with the current track.
            overwrite: Whether or not to overwrite self if a conflict exists.
        """
        log.debug(
            f"Merging tracks. [track_a={self!r}, track_b={other!r}, {overwrite=!r}]"
        )

        for field in self.fields():
            if field not in {"album_obj", "path", "year"}:
                other_value = getattr(other, field)
                self_value = getattr(self, field)
                if other_value and (overwrite or (not overwrite and not self_value)):
                    setattr(self, field, other_value)

        log.debug(
            f"Tracks merged. [track_a={self!r}, track_b={other!r}, {overwrite=!r}]"
        )

    def __eq__(self, other) -> bool:
        """Compares Tracks by their 'uniqueness' in the database."""
        if not isinstance(other, Track):
            return False

        if self.mb_track_id and self.mb_track_id == other.mb_track_id:
            return True
        if self.path == other.path:
            return True
        if (
            self.track_num == other.track_num
            and self.disc == other.disc
            and self.album_obj == other.album_obj
        ):
            return True

        return False

    def __lt__(self, other) -> bool:
        """Sort based on album, then disc, then track number."""
        if self.album_obj == other.album_obj:
            if self.disc == other.disc:
                return self.track_num < other.track_num

            return self.disc < other.disc

        return self.album_obj < other.album_obj

    def __repr__(self):
        """Represents a Track using track-specific and relevant album fields."""
        repr_fields = [
            "track_num",
            "disc",
            "title",
            "artist",
            "genre",
            "mb_track_id",
            "album",
            "path",
        ]
        field_reprs = []
        for field in repr_fields:
            if hasattr(self, field):
                field_reprs.append(f"{field}={getattr(self, field)!r}")
        repr_str = "Track(" + ", ".join(field_reprs)

        custom_field_reprs = []
        for custom_field, value in self._custom_fields.items():
            custom_field_reprs.append(f"{custom_field}={value}")
        if custom_field_reprs:
            repr_str += ", custom_fields=[" + ", ".join(custom_field_reprs) + "]"

        repr_str += ")"
        return repr_str

    def __str__(self):
        """String representation of a track."""
        return f"{self.artist} - {self.title}"

    @sa_orm.validates("_genres")
    def _append_genre(self, key: str, genre: _Genre) -> _Genre:
        """Prevents duplicate genres in the database by returning any existing ones."""
        genre_session = sa_orm.sessionmaker.object_session(self)
        if not genre_session:
            return genre

        persistent_genre = genre_session.get(_Genre, genre.name)
        if persistent_genre:
            return persistent_genre

        return genre
