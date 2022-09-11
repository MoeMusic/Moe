"""An Album in the database and any related logic."""

import datetime
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Optional, TypeVar, cast

import pluggy
import sqlalchemy as sa
from sqlalchemy import JSON, Column, Date, Integer, String, and_, or_
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import joinedload, relationship

import moe
from moe.config import Config, MoeSession
from moe.library import SABase
from moe.library.lib_item import LibItem, PathType

# This would normally cause a cyclic dependency.
if TYPE_CHECKING:
    from moe.library.extra import Extra
    from moe.library.track import Track

    # Makes hybrid_property's have the same typing as a normal properties.
    # Use until the stubs are improved.
    typed_hybrid_property = property
else:
    from sqlalchemy.ext.hybrid import hybrid_property as typed_hybrid_property

__all__ = ["Album"]

log = logging.getLogger("moe.album")


class Hooks:
    """Album hook specifications."""

    @staticmethod
    @moe.hookspec
    def create_custom_album_fields(config: Config) -> list[str]:  # type: ignore
        """Creates new custom fields for an Album.

        Args:
            config: Moe config.

        Returns:
            A list of any new fields you wish to create.

        Example:
            Inside your hook implementation::

                return "my_new_field"

            You can then access your new field as if it were a normal field::

                album.my_new_field = "awesome new value"

        Important:
            Your custom field should follow the same naming rules as any other python
            variable i.e. no spaces, starts with a letter, and consists solely of
            alpha-numeric and underscore characters.
        """  # noqa: DAR202


@moe.hookimpl
def add_hooks(plugin_manager: pluggy.manager.PluginManager):
    """Registers `album` hookspecs to Moe."""
    from moe.library.album import Hooks

    plugin_manager.add_hookspecs(Hooks)


class AlbumError(Exception):
    """Error creating an Album."""


# Album generic, used for typing classmethod
A = TypeVar("A", bound="Album")


class Album(LibItem, SABase):
    """An album is a collection of tracks and represents a specific album release.

    Albums also house any attributes that are shared by tracks e.g. albumartist.

    Attributes:
        artist (str): AKA albumartist.
        date (datetime.date): Album release date.
        disc_total (int): Number of discs in the album.
        extras (list[Extra]): Extra non-track files associated with the album.
        mb_album_id (str): Musicbrainz album aka release id.
        path (Path): Filesystem path of the album directory.
        title (str)
        tracks (list[Track]): Album's corresponding tracks.
        year (int): Album release year.
    """

    __tablename__ = "album"

    _id: int = cast(int, Column(Integer, primary_key=True))
    artist: str = cast(str, Column(String, nullable=False))
    date: datetime.date = cast(datetime.date, Column(Date, nullable=False))
    disc_total: int = cast(int, Column(Integer, nullable=False, default=1))
    mb_album_id: str = cast(str, Column(String, nullable=True, unique=True))
    path: Path = cast(Path, Column(PathType, nullable=False, unique=True))
    title: str = cast(str, Column(String, nullable=False))
    _custom_fields: dict[str, Optional[str]] = cast(
        dict[str, Optional[str]],
        Column(MutableDict.as_mutable(JSON(none_as_null=True))),
    )

    tracks: list["Track"] = relationship(
        "Track",
        back_populates="album_obj",
        cascade="all, delete-orphan",
        collection_class=list,
    )
    extras: list["Extra"] = relationship(
        "Extra",
        back_populates="album_obj",
        cascade="all, delete-orphan",
        collection_class=list,
    )

    def __init__(
        self,
        config: Config,
        path: Path,
        artist: str,
        title: str,
        date: datetime.date,
        disc_total=1,
        **kwargs,
    ):
        """Creates an Album.

        Args:
            config: Moe config.
            path: Filesystem path of the album directory.
            artist: Album artist.
            title: Album title.
            date: Album release date.
            disc_total: Number of discs in the album.
            **kwargs: Any other fields to assign to the album.
        """
        self.config = config
        self.__dict__["_custom_fields"] = {}
        custom_fields = config.plugin_manager.hook.create_custom_album_fields(
            config=config
        )
        for plugin_fields in custom_fields:
            for plugin_field in plugin_fields:
                self._custom_fields[plugin_field] = None

        self.path = path
        self.artist = artist
        self.title = title
        self.date = date
        self.disc_total = disc_total

        for key, value in kwargs.items():
            if value:
                setattr(self, key, value)

        log.debug(f"Album created. [album={self!r}]")

    @classmethod
    def from_dir(cls: type[A], config: Config, album_path: Path) -> A:
        """Creates an album from a directory.

        Args:
            config: Moe config.
            album_path: Album directory path. The directory will be scanned for any
                files to be added to the album. Any non-track files will be added as
                extras.

        Returns:
            Created album.

        Raises:
            AlbumError: No tracks found in the given directory.
        """
        from moe.library.extra import Extra
        from moe.library.track import Track, TrackError

        log.debug(f"Creating album from directory. [dir={album_path}]")

        extra_paths = []
        album_file_paths = [path for path in album_path.rglob("*") if path.is_file()]
        album: Optional[Album] = None
        for file_path in album_file_paths:
            try:
                track = Track.from_file(config, file_path, album)
            except TrackError:
                extra_paths.append(file_path)
            else:
                if not album:
                    album = track.album_obj

        if not album:
            raise AlbumError(f"No tracks found in album directory. [dir={album_path}]")

        for extra_path in extra_paths:
            Extra(config, album, extra_path)

        log.debug(f"Album created from directory. [dir={album_path}, {album=!r}]")
        return album

    def fields(self) -> tuple[str, ...]:
        """Returns the public fields, or non-method attributes, of an Album."""
        return (
            "artist",
            "date",
            "disc_total",
            "extras",
            "mb_album_id",
            "path",
            "title",
            "tracks",
            "year",
        )

    def get_existing(self) -> Optional["Album"]:
        """Gets a matching Album in the library by its unique attributes.

        Returns:
            Duplicate album or the same album if it already exists in the library.
        """
        log.debug(f"Searching library for existing album. [album={self!r}]")

        session = MoeSession()
        existing_album = (
            session.query(Album)
            .filter(
                or_(
                    Album.path == self.path,
                    and_(
                        Album.mb_album_id == self.mb_album_id,
                        Album.mb_album_id != None,  # noqa: E711
                    ),
                )
            )
            .options(joinedload("*"))
            .one_or_none()
        )
        if not existing_album:
            log.debug("No matching album found.")
            return None

        log.debug(f"Matching album found. [match={existing_album!r}]")
        return existing_album

    def get_extra(self, filename: str) -> Optional["Extra"]:
        """Gets an Extra by its filename."""
        return next(
            (extra for extra in self.extras if extra.filename == filename), None
        )

    def get_track(self, track_num: int, disc: int = 1) -> Optional["Track"]:
        """Gets a Track by its track number."""
        return next(
            (
                track
                for track in self.tracks
                if track.track_num == track_num and track.disc == disc
            ),
            None,
        )

    def merge(self, other: "Album", overwrite: bool = False) -> None:
        """Merges another album into this one.

        Args:
            other: Other album to be merged with the current album.
            overwrite: Whether or not to overwrite self if a conflict exists.
        """
        log.debug(
            f"Merging albums. [album_a={self!r}, album_b={other!r}, {overwrite=!r}]"
        )

        for field in self.fields():
            if field not in {"path", "year", "tracks", "extras"}:
                other_value = getattr(other, field)
                self_value = getattr(self, field)
                if other_value and (overwrite or (not overwrite and not self_value)):
                    setattr(self, field, other_value)

        new_tracks: list[Track] = []
        for other_track in other.tracks:
            conflict_track = self.get_track(other_track.track_num, other_track.disc)
            if conflict_track:
                conflict_track.merge(other_track, overwrite)
            else:
                new_tracks.append(other_track)
        self.tracks.extend(new_tracks)

        new_extras: list[Extra] = []
        for other_extra in other.extras:
            conflict_extra = self.get_extra(other_extra.filename)
            if conflict_extra and overwrite:
                self.extras.remove(conflict_extra)
                new_extras.append(other_extra)
            elif not conflict_extra:
                new_extras.append(other_extra)
        self.extras.extend(new_extras)

        log.debug(
            f"Albums merged. [album_a={self!r}, album_b={other!r}, {overwrite=!r}]"
        )

    @typed_hybrid_property
    def year(self) -> int:  # type: ignore
        """Gets an Album's year."""
        return self.date.year

    @year.expression  # type: ignore
    def year(cls):  # noqa: B902
        """Returns a year at the sql level."""
        return sa.extract("year", cls.date)

    def __eq__(self, other) -> bool:
        """Compares Albums by their 'uniqueness' in the database."""
        if not isinstance(other, Album):
            return False

        if self.mb_album_id and self.mb_album_id == other.mb_album_id:
            return True
        if self.path == other.path:
            return True

        return False

    def __lt__(self, other: "Album") -> bool:
        """Sort an album based on its title, then artist, then date."""
        if self.title == other.title:
            if self.artist == other.artist:
                return self.date < other.date

            return self.artist < other.artist

        return self.title < other.title

    def __repr__(self):
        """Represents an Album using its fields."""
        repr_fields = [
            "artist",
            "title",
            "date",
            "mb_album_id",
            "path",
        ]
        field_reprs = []
        for field in repr_fields:
            if hasattr(self, field):
                field_reprs.append(f"{field}={getattr(self, field)!r}")
        repr_str = "Album(" + ", ".join(field_reprs)

        custom_field_reprs = []
        for custom_field, value in self._custom_fields.items():
            custom_field_reprs.append(f"{custom_field}={value}")
        if custom_field_reprs:
            repr_str += ", custom_fields=[" + ", ".join(custom_field_reprs) + "]"

        track_reprs = []
        for track in sorted(self.tracks):
            track_reprs.append(f"{track.disc}.{track.track_num} - {track.title}")
        repr_str += ", tracks=[" + ", ".join(track_reprs) + "]"

        extra_reprs = []
        for extra in sorted(self.extras):
            extra_reprs.append(f"{extra.filename}")
        repr_str += ", extras=[" + ", ".join(extra_reprs) + "]"

        repr_str += ")"
        return repr_str

    def __str__(self):
        """String representation of an Album."""
        return f"{self.artist} - {self.title} ({self.year})"
