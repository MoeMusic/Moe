"""A Track in the database and any related logic."""

import logging
from pathlib import Path
from typing import Any, Optional, TypeVar, cast

import mediafile
import pluggy
from sqlalchemy import JSON, Column, Integer, String
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey, UniqueConstraint

import moe
from moe import config
from moe.library.album import Album
from moe.library.lib_item import LibItem, LibraryError, PathType, SABase

__all__ = ["Track", "TrackError"]

log = logging.getLogger("moe.track")


class Hooks:
    """Track hook specifications."""

    @staticmethod
    @moe.hookspec
    def create_custom_track_fields() -> dict[str, Any]:  # type: ignore
        """Creates new custom fields for a Track.

        Returns:
            Dict of the field names to their default values or ``None`` for no default.

        Example:
            Inside your hook implementation::

                return {"my_new_field": "default value", "other_field": None}

            You can then access your new field as if it were a normal field::

                track.my_new_field = "awesome new value"

        Important:
            Your custom field should follow the same naming rules as any other python
            variable i.e. no spaces, starts with a letter, and consists solely of
            alpha-numeric and underscore characters.
        """  # noqa: DAR202

    @staticmethod
    @moe.hookspec
    def is_unique_track(track: "Track", other: "Track") -> bool:  # type: ignore
        """Add new conditions to determine whether two tracks are unique.

        "Uniqueness" is meant in terms of whether the two tracks should be considered
        duplicates in the library. These additional conditions will be applied inside a
        track's :meth:`is_unique` method.
        """

    @staticmethod
    @moe.hookspec
    def read_custom_tags(
        track_path: Path, album_fields: dict[str, Any], track_fields: dict[str, Any]
    ) -> None:
        """Read and set any fields from a track_path.

        How you read the file and assign tags is up to each individual plugin.
        Internally, Moe uses the `mediafile <https://github.com/beetbox/mediafile>`_
        library to read tags.

        Args:
            track_path: Path of the track file to read.
            album_fields: Dictionary of album fields to read from the given track file's
                tags. The dictionary may contain existing fields and values, and you
                can choose to either override the existing fields, or to provide new
                fields.
            track_fields: Dictionary of track fields to read from the given track file's
                tags. The dictionary may contain existing fields and values, and you
                can choose to either override the existing fields, or to provide new
                fields.

        Example:
            .. code:: python

                audio_file = mediafile.MediaFile(track_path)
                album_fields["title"] = audio_file.album
                track_fields["title"] = audio_file.title

        See Also:
            * :ref:`Album and track fields <fields:Fields>`
            * `Mediafile docs <https://mediafile.readthedocs.io/en/latest/>`_
            * The :meth:`~moe.plugins.write.Hooks.write_custom_tags` hook for writing
              tags.
        """


@moe.hookimpl
def add_hooks(pm: pluggy.manager.PluginManager):
    """Registers `track` hookspecs to Moe."""
    from moe.library.track import Hooks

    pm.add_hookspecs(Hooks)


@moe.hookimpl(tryfirst=True)
def read_custom_tags(
    track_path: Path, album_fields: dict[str, Any], track_fields: dict[str, Any]
) -> None:
    """Read and set internally tracked fields."""
    audio_file = mediafile.MediaFile(track_path)

    album_fields["artist"] = audio_file.albumartist or audio_file.artist
    album_fields["country"] = audio_file.country
    album_fields["date"] = audio_file.date
    album_fields["disc_total"] = audio_file.disctotal
    album_fields["label"] = audio_file.label
    album_fields["media"] = audio_file.media
    album_fields["original_date"] = audio_file.original_date
    album_fields["path"] = track_path.parent
    album_fields["title"] = audio_file.album

    track_fields["artist"] = audio_file.artist
    track_fields["artists"] = set(audio_file.artists)
    track_fields["disc"] = audio_file.disc
    track_fields["genres"] = set(audio_file.genres)
    track_fields["path"] = track_path
    track_fields["title"] = audio_file.title
    track_fields["track_num"] = audio_file.track


class TrackError(LibraryError):
    """Error performing some operation on a Track."""


class _Artist(SABase):
    """A track can have multiple artists."""

    __tablename__ = "artist"

    _id: int = cast(int, Column(Integer, primary_key=True))
    _track_id: int = cast(int, Column(Integer, ForeignKey("track._id")))
    name: str = cast(str, Column(String, nullable=False))

    def __init__(self, name: str):
        self.name = name


class _Genre(SABase):
    """A track can have multiple genres."""

    __tablename__ = "genre"

    _id: int = cast(int, Column(Integer, primary_key=True))
    _track_id: int = cast(int, Column(Integer, ForeignKey("track._id")))
    name: str = cast(str, Column(String, nullable=False))

    def __init__(self, name: str):
        self.name = name


# Track generic, used for typing classmethod
T = TypeVar("T", bound="Track")


class Track(LibItem, SABase):
    """A single track.

    Attributes:
        album (str)
        albumartist (str)
        album_obj (Album): Corresponding Album object.
        artist (str)
        artists (set[str]): Set of all artists.
        disc (int): Disc number the track is on.
        genre (str): String of all genres concatenated with ';'.
        genres (set[str]): Set of all genres.
        path (Path): Filesystem path of the track file.
        title (str)
        track_num (int)

    Note:
        Altering any album-related property attributes, will result in changing the
        album field and thus all other tracks in the album as well.
    """

    __tablename__ = "track"

    _id: int = cast(int, Column(Integer, primary_key=True))
    artist: str = cast(str, Column(String, nullable=False))
    disc: int = cast(int, Column(Integer, nullable=False, default=1))
    path: Path = cast(Path, Column(PathType, nullable=False, unique=True))
    title: str = cast(str, Column(String, nullable=False))
    track_num: int = cast(int, Column(Integer, nullable=False))
    _custom_fields: dict[str, Any] = cast(
        dict[str, Any],
        Column(
            MutableDict.as_mutable(JSON(none_as_null=True)),
            default="{}",
            nullable=False,
        ),
    )

    _album_id: int = cast(int, Column(Integer, ForeignKey("album._id")))
    album_obj: Album = relationship("Album", back_populates="tracks")
    album: str = association_proxy("album_obj", "title")
    albumartist: str = association_proxy("album_obj", "artist")

    _artists: set[_Artist] = relationship(
        "_Artist", collection_class=set, cascade="save-update, merge, expunge"
    )
    artists: set[str] = association_proxy("_artists", "name")
    _genres: set[_Genre] = relationship(
        "_Genre", collection_class=set, cascade="save-update, merge, expunge"
    )
    genres: set[str] = association_proxy("_genres", "name")

    __table_args__ = (UniqueConstraint("disc", "track_num", "_album_id"),)

    def __init__(
        self,
        album: Album,
        path: Path,
        title: str,
        track_num: int,
        **kwargs,
    ):
        """Creates a Track.

        Args:
            album: Album the track belongs to.
            path: Filesystem path of the track file.
            title: Title of the track.
            track_num: Track number.
            **kwargs: Any other fields to assign to the track.
        """
        self._custom_fields = self._get_default_custom_fields()
        self._custom_fields_set = set(self._custom_fields)

        album.tracks.append(self)
        self.path = path
        self.title = title
        self.track_num = track_num

        self.artist = self.albumartist  # default value

        for key, value in kwargs.items():
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
    def from_file(cls: type[T], track_path: Path, album: Optional[Album] = None) -> T:
        """Alternate initializer that creates a Track from a track file.

        Will read any tags from the given path and save them to the Track.

        Args:
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
            mediafile.MediaFile(track_path)
        except mediafile.UnreadableFileError as err:
            raise TrackError(
                "Unable to create track; given path is not a track file. "
                f"[path={track_path}]"
            ) from err

        album_fields: dict[str, Any] = {}
        track_fields: dict[str, Any] = {}
        config.CONFIG.pm.hook.read_custom_tags(
            track_path=track_path, album_fields=album_fields, track_fields=track_fields
        )
        if not album:
            album = Album(
                path=album_fields.pop("path"),
                artist=album_fields.pop("artist"),
                title=album_fields.pop("title"),
                date=album_fields.pop("date"),
                disc_total=album_fields.pop("disc_total"),
                **album_fields,
            )

        return cls(
            album=album,
            path=track_fields.pop("path"),
            title=track_fields.pop("title"),
            track_num=track_fields.pop("track_num"),
            **track_fields,
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
        self.genres = {genre.strip() for genre in genre_str.split(";")}

    @property
    def fields(self) -> set[str]:
        """Returns any editable, track-specific fields."""
        return {
            "album_obj",
            "artist",
            "artists",
            "disc",
            "genres",
            "path",
            "title",
            "track_num",
        }.union(set(self._custom_fields))

    def is_unique(self, other: "Track") -> bool:
        """Returns whether a track is unique in the library from ``other``."""
        if self.path == other.path:
            return False
        if (
            self.track_num == other.track_num
            and self.disc == other.disc
            and self.album_obj == other.album_obj
        ):
            return False

        custom_uniqueness = config.CONFIG.pm.hook.is_unique_track(
            track=self, other=other
        )
        if False in custom_uniqueness:
            return False

        return True

    def merge(self, other: "Track", overwrite: bool = False):
        """Merges another track into this one.

        Args:
            other: Other track to be merged with the current track.
            overwrite: Whether or not to overwrite self if a conflict exists.
        """
        log.debug(
            f"Merging tracks. [track_a={self!r}, track_b={other!r}, {overwrite=!r}]"
        )

        omit_fields = {"album_obj", "year"}
        for field in self.fields - omit_fields:
            other_value = getattr(other, field)
            self_value = getattr(self, field)
            if other_value and (overwrite or (not overwrite and not self_value)):
                setattr(self, field, other_value)

        log.debug(
            f"Tracks merged. [track_a={self!r}, track_b={other!r}, {overwrite=!r}]"
        )

    def __eq__(self, other) -> bool:
        """Compares Tracks by their fields."""
        if not isinstance(other, Track):
            return False

        for field in self.fields:
            if not hasattr(other, field) or (
                getattr(self, field) != getattr(other, field)
            ):
                return False

        return True

    def __lt__(self, other) -> bool:
        """Sort based on album, then disc, then track number."""
        if self.album_obj == other.album_obj:
            if self.disc == other.disc:
                return self.track_num < other.track_num

            return self.disc < other.disc

        return self.album_obj < other.album_obj

    def __repr__(self):
        """Represents a Track using track-specific and relevant album fields."""
        field_reprs = []
        omit_fields = {"album_obj"}
        for field in self.fields - omit_fields:
            if hasattr(self, field):
                field_reprs.append(f"{field}={getattr(self, field)!r}")
        repr_str = "Track(" + ", ".join(field_reprs) + f", album='{self.album_obj}'"

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

    def _get_default_custom_fields(self) -> dict[str, Any]:
        """Returns the default custom track fields."""
        return {
            field: default_val
            for plugin_fields in config.CONFIG.pm.hook.create_custom_track_fields()
            for field, default_val in plugin_fields.items()
        }
