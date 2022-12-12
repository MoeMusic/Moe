"""An Album in the database and any related logic."""

import datetime
import logging
from pathlib import Path, PurePath
from typing import TYPE_CHECKING, Any, Optional, TypeVar, Union, cast

import pluggy
import sqlalchemy as sa
from sqlalchemy import JSON, Column, Date, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.mutable import MutableDict, MutableSet
from sqlalchemy.orm import relationship

import moe
from moe import config
from moe.library.lib_item import LibItem, LibraryError, MetaLibItem, SABase, SetType

if TYPE_CHECKING:
    from moe.library.extra import Extra
    from moe.library.track import MetaTrack, Track

__all__ = ["Album", "AlbumError", "MetaAlbum"]

log = logging.getLogger("moe.album")


class Hooks:
    """Album hook specifications."""

    @staticmethod
    @moe.hookspec
    def is_unique_album(album: "Album", other: "Album") -> bool:  # type: ignore
        """Add new conditions to determine whether two albums are unique.

        "Uniqueness" is meant in terms of whether the two albums should be considered
        duplicates in the library. These additional conditions will be applied inside a
        album's :meth:`is_unique` method.
        """


@moe.hookimpl
def add_hooks(pm: pluggy.manager.PluginManager):
    """Registers `album` hookspecs to Moe."""
    from moe.library.album import Hooks

    pm.add_hookspecs(Hooks)


class AlbumError(LibraryError):
    """Error performing some operation on an Album."""


class MetaAlbum(MetaLibItem):
    """A album containing only metadata.

    It does not exist on the filesystem nor in the library. It can be used
    to represent information about a album to later be merged into a full ``Album``
    instance.

    There are no guarantees about information present in a ``MetaAlbum`` object i.e.
    all attributes may be ``None``.

    Attributes:
        artist (Optional[str]): AKA albumartist.
        barcode (Optional[str]): UPC barcode.
        catalog_nums (Optional[set[str]]): Set of all catalog numbers.
        country (Optional[str]): Country the album was released in
            (two character identifier).
        custom (dict[str, Any]): Dictionary of custom fields.
        date (Optional[datetime.date]): Album release date.
        disc_total (Optional[int]): Number of discs in the album.
        label (Optional[str]): Album release label.
        media (Optional[str]): Album release format (e.g. CD, Digital, etc.)
        original_date (Optional[datetime.date]): Date of the original release of the
            album.
        title (Optional[str])
        track_total (Optional[int]): Number of tracks that *should* be in the album.
            If an album is missing tracks, then ``len(tracks) < track_total``.
        tracks (list[Track]): Album's corresponding tracks.
    """

    def __init__(
        self,
        artist: Optional[str] = None,
        barcode: Optional[str] = None,
        catalog_nums: Optional[set[str]] = None,
        country: Optional[str] = None,
        date: Optional[datetime.date] = None,
        disc_total: Optional[int] = None,
        label: Optional[str] = None,
        media: Optional[str] = None,
        original_date: Optional[datetime.date] = None,
        title: Optional[str] = None,
        track_total: Optional[int] = None,
        tracks: Optional[list["MetaTrack"]] = None,
        **kwargs,
    ):
        """Creates a MetaAlbum object with any additional custom fields as kwargs."""
        self.custom = kwargs

        self.artist = artist
        self.barcode = barcode
        self.catalog_nums = catalog_nums
        self.country = country
        self.date = date
        self.disc_total = disc_total
        self.label = label
        self.media = media
        self.original_date = original_date
        self.title = title
        self.track_total = track_total

        if not tracks:
            self.tracks = []

        if config.CONFIG.settings.original_date and self.original_date:
            self.date = self.original_date

        log.debug(f"MetaAlbum created. [album={self!r}]")

    @property
    def catalog_num(self) -> Optional[str]:
        """Returns a string of all catalog_nums concatenated with ';'."""
        if self.catalog_nums is None:
            return None

        return ";".join(self.catalog_nums)

    @catalog_num.setter
    def catalog_num(self, catalog_num_str: Optional[str]):
        """Sets a track's catalog_num from a string.

        Args:
            catalog_num_str: For more than one catalog_num, they should be split with
                ';'.
        """
        if catalog_num_str is None:
            self.catalog_nums = None
        else:
            self.catalog_nums = {
                catalog_num.strip() for catalog_num in catalog_num_str.split(";")
            }

    @property
    def fields(self) -> set[str]:
        """Returns any editable album fields."""
        return {
            "artist",
            "barcode",
            "catalog_nums",
            "country",
            "date",
            "disc_total",
            "label",
            "media",
            "original_date",
            "title",
            "track_total",
        }

    def get_track(self, track_num: int, disc: int = 1) -> Optional["MetaTrack"]:
        """Gets a MetaTrack by its track number."""
        return next(
            (
                track
                for track in self.tracks
                if track.track_num == track_num and track.disc == disc
            ),
            None,
        )

    def merge(self, other: "MetaAlbum", overwrite: bool = False) -> None:
        """Merges another album into this one.

        Args:
            other: Other album to be merged with the current album.
            overwrite: Whether or not to overwrite self if a conflict exists.
        """
        log.debug(f"Merging MetaAlbums. [album_a={self!r}, album_b={other!r}")

        new_tracks: list["MetaTrack"] = []
        for other_track in other.tracks:
            conflict_track = None
            if other_track.track_num and other_track.disc:
                conflict_track = self.get_track(other_track.track_num, other_track.disc)
            if conflict_track:
                conflict_track.merge(other_track, overwrite)
            else:
                new_tracks.append(other_track)
        self.tracks.extend(new_tracks)

        for field in self.fields:
            other_value = getattr(other, field)
            self_value = getattr(self, field)
            if other_value and (overwrite or (not overwrite and not self_value)):
                setattr(self, field, other_value)

        for custom_field in self.custom:
            other_value = other.custom.get(custom_field)
            if other_value and (
                overwrite or (not overwrite and not self.custom[custom_field])
            ):
                self.custom[custom_field] = other_value

        log.debug(
            f"MetaAlbums merged. [album_a={self!r}, album_b={other!r}, {overwrite=!r}]"
        )

    def __eq__(self, other: "MetaAlbum") -> bool:
        """Compares MetaAlbums by their fields."""
        if type(self) != type(other):
            return False

        for field in self.fields:
            if not hasattr(other, field) or (
                getattr(self, field) != getattr(other, field)
            ):
                return False

        return True

    def __lt__(self, other: "MetaAlbum") -> bool:
        """Sort an album based on its title, then artist, then date."""
        if self.title == other.title:
            if self.artist == other.artist:
                if self.date is None:
                    return False
                if other.date is None:
                    return True
                return self.date < other.date

            if self.artist is None:
                return False
            if other.artist is None:
                return True
            return self.artist < other.artist

        if self.title is None:
            return False
        if other.title is None:
            return True
        return self.title < other.title

    def __str__(self):
        """String representation of an Album."""
        album_str = f"{self.artist} - {self.title}"

        if self.date:
            album_str += f" ({self.date.year})"

        return album_str

    def __repr__(self):
        """Represents an Album using its fields."""
        field_reprs = []
        for field in self.fields:
            if hasattr(self, field):
                field_reprs.append(f"{field}={getattr(self, field)!r}")
        repr_str = "AlbumInfo(" + ", ".join(field_reprs)

        custom_field_reprs = []
        for custom_field, value in self.custom.items():
            custom_field_reprs.append(f"{custom_field}={value}")
        if custom_field_reprs:
            repr_str += ", custom_fields=[" + ", ".join(custom_field_reprs) + "]"

        track_reprs = []
        for track in sorted(self.tracks):
            track_reprs.append(f"{track.disc}.{track.track_num} - {track.title}")
        repr_str += ", tracks=[" + ", ".join(track_reprs) + "]"

        repr_str += ")"
        return repr_str


# Album generic, used for typing classmethod
A = TypeVar("A", bound="Album")


class Album(LibItem, SABase, MetaAlbum):
    """An album is a collection of tracks and represents a specific album release.

    Albums also house any attributes that are shared by tracks e.g. albumartist.

    Attributes:
        artist (str): AKA albumartist.
        barcode (Optional[str]): UPC barcode.
        catalog_nums (Optional[set[str]]): Set of all catalog numbers.
        country (Optional[str]): Country the album was released in
            (two character identifier).
        custom (dict[str, Any]): Dictionary of custom fields.
        date (datetime.date): Album release date.
        disc_total (int): Number of discs in the album.
        extras (list[Extra]): Extra non-track files associated with the album.
        label (Optional[str]): Album release label.
        media (Optional[str]): Album release format (e.g. CD, Digital, etc.)
        original_date (Optional[datetime.date]): Date of the original release of the
            album.
        path (pathlib.Path): Filesystem path of the album directory.
        title (str)
        track_total (Optional[int]): Number of tracks that *should* be in the album.
            If an album is missing tracks, then ``len(tracks) < track_total``.
        tracks (list[Track]): Album's corresponding tracks.
    """

    __tablename__ = "album"

    artist: str = cast(str, Column(String, nullable=False))
    barcode: Optional[str] = cast(Optional[str], Column(String, nullable=True))
    catalog_nums: Optional[set[str]] = cast(
        Optional[set[str]], MutableSet.as_mutable(Column(SetType, nullable=True))
    )
    country: Optional[str] = cast(Optional[str], Column(String, nullable=True))
    date: datetime.date = cast(datetime.date, Column(Date, nullable=False))
    disc_total: int = cast(int, Column(Integer, nullable=False, default=1))
    label: Optional[str] = cast(Optional[str], Column(String, nullable=True))
    media: Optional[str] = cast(Optional[str], Column(String, nullable=True))
    original_date: Optional[datetime.date] = cast(
        Optional[datetime.date], Column(Date, nullable=True)
    )
    title: str = cast(str, Column(String, nullable=False))
    track_total: Optional[int] = cast(Optional[int], Column(Integer, nullable=True))
    custom: dict[str, Any] = cast(
        dict[str, Any],
        Column(
            MutableDict.as_mutable(JSON(none_as_null=True)),
            default="{}",
            nullable=False,
        ),
    )

    tracks: list["Track"] = relationship(
        "Track",
        back_populates="album",
        cascade="all, delete-orphan",
        collection_class=list,
    )
    extras: list["Extra"] = relationship(
        "Extra",
        back_populates="album",
        cascade="all, delete-orphan",
        collection_class=list,
    )

    def __init__(
        self,
        path: Path,
        artist: str,
        title: str,
        date: datetime.date,
        barcode: Optional[str] = None,
        catalog_nums: Optional[set[str]] = None,
        country: Optional[str] = None,
        disc_total=1,
        label: Optional[str] = None,
        media: Optional[str] = None,
        original_date: Optional[datetime.date] = None,
        track_total: Optional[int] = None,
        **kwargs,
    ):
        """Creates an Album object with any additional custom fields as kwargs."""
        self.custom = kwargs

        self.path = path
        self.artist = artist
        self.barcode = barcode
        self.catalog_nums = catalog_nums
        self.country = country
        self.date = date
        self.disc_total = disc_total
        self.label = label
        self.media = media
        self.original_date = original_date
        self.track_total = track_total
        self.title = title

        if config.CONFIG.settings.original_date and self.original_date:
            self.date = self.original_date

        log.debug(f"Album created. [album={self!r}]")

    @classmethod
    def from_dir(cls: type[A], album_path: Path) -> A:
        """Creates an album from a directory.

        Args:
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
                track = Track.from_file(file_path, album)
            except TrackError:
                extra_paths.append(file_path)
            else:
                if not album:
                    album = track.album

        if not album:
            raise AlbumError(f"No tracks found in album directory. [dir={album_path}]")

        for extra_path in extra_paths:
            Extra(album, extra_path)

        log.debug(f"Album created from directory. [dir={album_path}, {album=!r}]")
        return album

    @property
    def fields(self) -> set[str]:
        """Returns any editable, track-specific fields."""
        return super().fields.union({"path"})

    def get_extra(self, rel_path: PurePath) -> Optional["Extra"]:
        """Gets an Extra by its path."""
        return next(
            (extra for extra in self.extras if extra.rel_path == rel_path), None
        )

    def get_track(self, track_num: int, disc: int = 1) -> Optional["Track"]:
        """Gets a Track by its track number."""
        return cast("Track", super().get_track(track_num, disc))

    def is_unique(self, other: "Album") -> bool:
        """Returns whether an album is unique in the library from ``other``."""
        if self.path == other.path:
            return False

        custom_uniqueness = config.CONFIG.pm.hook.is_unique_album(
            album=self, other=other
        )
        if False in custom_uniqueness:
            return False

        return True

    def merge(self, other: Union["Album", MetaAlbum], overwrite: bool = False) -> None:
        """Merges another album into this one.

        Args:
            other: Other album to be merged with the current album.
            overwrite: Whether or not to overwrite self if a conflict exists.
        """
        log.debug(f"Merging albums. [album_a={self!r}, album_b={other!r}")

        self._merge_tracks(other, overwrite)
        self._merge_extras(other, overwrite)

        for field in self.fields:
            other_value = getattr(other, field, None)
            self_value = getattr(self, field, None)
            if other_value and (overwrite or (not overwrite and not self_value)):
                setattr(self, field, other_value)

        for custom_field in self.custom:
            other_value = other.custom.get(custom_field)
            if other_value and (
                overwrite or (not overwrite and not self.custom[custom_field])
            ):
                self.custom[custom_field] = other_value

        log.debug(
            f"Albums merged. [album_a={self!r}, album_b={other!r}, {overwrite=!r}]"
        )

    def _merge_tracks(
        self, other: Union["Album", MetaAlbum], overwrite: bool = False
    ) -> None:
        """Merges the tracks of another album into this one."""
        new_tracks: list["Track"] = []
        for other_track in other.tracks:
            conflict_track = None
            if other_track.track_num and other_track.disc:
                conflict_track = self.get_track(other_track.track_num, other_track.disc)
            if conflict_track:
                conflict_track.merge(other_track, overwrite)
            else:
                new_tracks.append(other_track)
        self.tracks.extend(new_tracks)

    def _merge_extras(
        self, other: Union["Album", MetaAlbum], overwrite: bool = False
    ) -> None:
        """Merges the extras of another album into this one."""
        if isinstance(other, Album):
            new_extras: list["Extra"] = []
            for other_extra in other.extras:
                conflict_extra = self.get_extra(other_extra.rel_path)
                if conflict_extra:
                    conflict_extra.merge(other_extra, overwrite)
                else:
                    new_extras.append(other_extra)
            self.extras.extend(new_extras)

    @hybrid_property
    def original_year(self) -> Optional[int]:  # type: ignore
        """Gets an Album's year."""
        if self.original_date is None:
            return None

        return self.original_date.year

    @original_year.expression  # type: ignore
    def original_year(cls):  # noqa: B902
        """Returns a year at the sql level."""
        return sa.extract("year", cls.original_date)

    @hybrid_property
    def year(self) -> int:  # type: ignore
        """Gets an Album's year."""
        return self.date.year

    @year.expression  # type: ignore
    def year(cls):  # noqa: B902
        """Returns a year at the sql level."""
        return sa.extract("year", cls.date)

    def __repr__(self):
        """Represents an Album using its fields."""
        field_reprs = []
        for field in self.fields:
            if hasattr(self, field):
                field_reprs.append(f"{field}={getattr(self, field)!r}")
        repr_str = "Album(" + ", ".join(field_reprs)

        custom_field_reprs = []
        for custom_field, value in self.custom.items():
            custom_field_reprs.append(f"{custom_field}={value}")
        if custom_field_reprs:
            repr_str += ", custom_fields=[" + ", ".join(custom_field_reprs) + "]"

        track_reprs = []
        for track in sorted(self.tracks):
            track_reprs.append(f"{track.disc}.{track.track_num} - {track.title}")
        repr_str += ", tracks=[" + ", ".join(track_reprs) + "]"

        extra_reprs = []
        for extra in sorted(self.extras):
            extra_reprs.append(f"{extra.path.name}")
        repr_str += ", extras=[" + ", ".join(extra_reprs) + "]"

        repr_str += ")"
        return repr_str
