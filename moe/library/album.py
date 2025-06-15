"""An Album in the database and any related logic."""

from __future__ import annotations

import datetime  # noqa: TC003 necessary for sqlalchemy
import logging
import sys
from typing import TYPE_CHECKING, Optional, cast

import sqlalchemy as sa
from sqlalchemy import Integer
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.mutable import MutableSet
from sqlalchemy.orm import Mapped, mapped_column, relationship

import moe
from moe import config
from moe.library.lib_item import LibItem, LibraryError, MetaLibItem, SABase, SetType

if sys.version_info < (3, 11):
    from typing_extensions import Self
else:
    from typing import Self

if TYPE_CHECKING:
    from pathlib import Path, PurePath

    import pluggy
    from sqlalchemy.sql import ColumnExpressionArgument

    from moe.library.extra import Extra
    from moe.library.track import MetaTrack, Track

__all__ = ["Album", "AlbumError", "MetaAlbum"]

log = logging.getLogger("moe.album")


class Hooks:
    """Album hook specifications."""

    @staticmethod
    @moe.hookspec
    def is_unique_album(album: Album, other: Album) -> bool:  # type: ignore[reportReturnType]
        """Add new conditions to determine whether two albums are unique.

        "Uniqueness" is meant in terms of whether the two albums should be considered
        duplicates in the library. These additional conditions will be applied inside a
        album's :meth:`is_unique` method.
        """


@moe.hookimpl
def add_hooks(pm: pluggy._manager.PluginManager) -> None:
    """Registers `album` hookspecs to Moe."""
    from moe.library.album import Hooks  # noqa: PLC0415

    pm.add_hookspecs(Hooks)


class AlbumError(LibraryError):
    """Error performing some operation on an Album."""


class MetaAlbum(MetaLibItem):  # noqa: PLW1641 MetaTracks are unhashable
    """A album containing only metadata.

    It does not exist on the filesystem nor in the library. It can be used
    to represent information about a album to later be merged into a full ``Album``
    instance.

    There are no guarantees about information present in a ``MetaAlbum`` object i.e.
    all attributes may be ``None``.

    Attributes:
        artist (str | None): AKA albumartist.
        barcode (str | None): UPC barcode.
        catalog_nums (Optional[set[str]]): Set of all catalog numbers.
        country (str | None): Country the album was released in
            (two character identifier).
        custom (dict[str, Any]): Dictionary of custom fields.
        date (datetime.date | None): Album release date.
        disc_total (int | None): Number of discs in the album.
        label (str | None): Album release label.
        media (str | None): Album release format (e.g. CD, Digital, etc.)
        original_date (datetime.date | None): Date of the original release of the album.
        title (str | None)
        track_total (int | None): Number of tracks that *should* be in the album.
            If an album is missing tracks, then ``len(tracks) < track_total``.
        tracks (list[Track]): Album's corresponding tracks.
    """

    def __init__(  # noqa: PLR0913
        self,
        artist: str | None = None,
        barcode: str | None = None,
        catalog_nums: set[str] | None = None,
        country: str | None = None,
        date: datetime.date | None = None,
        disc_total: int | None = None,
        label: str | None = None,
        media: str | None = None,
        original_date: datetime.date | None = None,
        title: str | None = None,
        track_total: int | None = None,
        tracks: list[MetaTrack] | None = None,
        **kwargs: object,
    ) -> None:
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
    def catalog_num(self) -> str | None:
        """Returns a string of all catalog_nums concatenated with ';'."""
        if self.catalog_nums is None:
            return None

        return ";".join(self.catalog_nums)

    @catalog_num.setter
    def catalog_num(self, catalog_num_str: str | None) -> None:
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

    def get_track(self, track_num: int, disc: int = 1) -> MetaTrack | None:
        """Gets a MetaTrack by its track number."""
        return next(
            (
                track
                for track in self.tracks
                if track.track_num == track_num and track.disc == disc
            ),
            None,
        )

    def merge(self, other: Self, overwrite: bool = False) -> None:  # noqa: FBT001, FBT002
        """Merges another album into this one.

        Args:
            other: Other album to be merged with the current album.
            overwrite: Whether or not to overwrite self if a conflict exists.
        """
        log.debug(f"Merging MetaAlbums. [album_a={self!r}, album_b={other!r}")

        new_tracks: list[MetaTrack] = []
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
            f"MetaAlbums merged. [album_a={self!r}, album_b={other!r}, {overwrite=}]"
        )

    def __eq__(self, other: object) -> bool:
        """Compares MetaAlbums by their fields."""
        if not isinstance(other, MetaAlbum):
            return False

        for field in self.fields:
            if not hasattr(other, field) or (
                getattr(self, field) != getattr(other, field)
            ):
                return False

        return True

    def __lt__(self, other: Self) -> bool:  # noqa: PLR0911
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

    def __str__(self) -> str:
        """String representation of an Album."""
        album_str = f"{self.artist} - {self.title}"

        if self.date:
            album_str += f" ({self.date.year})"

        return album_str

    def __repr__(self) -> str:
        """Represents an Album using its fields."""
        field_reprs = [
            f"{field}={getattr(self, field)!r}"
            for field in self.fields
            if hasattr(self, field)
        ]
        repr_str = "AlbumInfo(" + ", ".join(field_reprs)

        custom_field_reprs = []
        for custom_field, value in self.custom.items():
            custom_field_reprs.append(f"{custom_field}={value}")
        if custom_field_reprs:
            repr_str += ", custom_fields=[" + ", ".join(custom_field_reprs) + "]"

        track_reprs = [
            f"{track.disc}.{track.track_num} - {track.title}"
            for track in sorted(self.tracks)
        ]
        repr_str += ", tracks=[" + ", ".join(track_reprs) + "]"

        repr_str += ")"
        return repr_str


class Album(LibItem, SABase, MetaAlbum):
    """An album is a collection of tracks and represents a specific album release.

    Albums also house any attributes that are shared by tracks e.g. albumartist.

    Attributes:
        artist (str): AKA albumartist.
        barcode (str | None): UPC barcode.
        catalog_nums (set[str] | None): Set of all catalog numbers.
        country (str | None): Country the album was released in
            (two character identifier).
        custom (dict[str, Any]): Dictionary of custom fields.
        date (datetime.date): Album release date.
        disc_total (int): Number of discs in the album.
        extras (list[Extra]): Extra non-track files associated with the album.
        label (str | None): Album release label.
        media (str | None): Album release format (e.g. CD, Digital, etc.)
        original_date (datetime.date | None): Date of the original release of the
            album.
        path (pathlib.Path): Filesystem path of the album directory.
        title (str)
        track_total (int | None): Number of tracks that *should* be in the album.
            If an album is missing tracks, then ``len(tracks) < track_total``.
        tracks (list[Track]): Album's corresponding tracks.
    """

    __tablename__ = "album"

    artist: Mapped[str]
    barcode: Mapped[Optional[str]]  # noqa: UP045 sqlachemy does not support
    catalog_nums: Mapped[Optional[set[str]]] = mapped_column(  # noqa: UP045 sqlachemy does not support
        MutableSet.as_mutable(SetType()), nullable=True
    )
    country: Mapped[Optional[str]]  # noqa: UP045 sqlachemy does not support
    date: Mapped[datetime.date]
    disc_total: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    label: Mapped[Optional[str]]  # noqa: UP045 sqlachemy does not support
    media: Mapped[Optional[str]]  # noqa: UP045 sqlachemy does not support
    original_date: Mapped[Optional[datetime.date]]  # noqa: UP045 sqlachemy does not support

    title: Mapped[str]
    track_total: Mapped[Optional[int]]  # noqa: UP045 sqlachemy does not support

    tracks: Mapped[list[Track]] = relationship(
        back_populates="album",
        cascade="all, delete-orphan",
        collection_class=list,
    )
    extras: Mapped[list[Extra]] = relationship(
        back_populates="album",
        cascade="all, delete-orphan",
        collection_class=list,
    )

    def __init__(  # noqa: PLR0913
        self,
        path: Path,
        artist: str,
        title: str,
        date: datetime.date,
        barcode: str | None = None,
        catalog_nums: set[str] | None = None,
        country: str | None = None,
        disc_total: int = 1,
        label: str | None = None,
        media: str | None = None,
        original_date: datetime.date | None = None,
        track_total: int | None = None,
        **kwargs: object,
    ) -> None:
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

        if config.CONFIG.settings.original_date and original_date:
            self.date = original_date

        log.debug(f"Album created. [album={self!r}]")

    @classmethod
    def from_dir(cls, album_path: Path) -> Album:
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
        from moe.library.extra import Extra  # noqa: PLC0415 prevents circular import
        from moe.library.track import (  # noqa: PLC0415 prevents circular import
            Track,
            TrackError,
        )

        log.debug(f"Creating album from directory. [dir={album_path}]")

        extra_paths = []
        album_file_paths = [path for path in album_path.rglob("*") if path.is_file()]
        album: Album | None = None
        for file_path in album_file_paths:
            try:
                track = Track.from_file(file_path, album, album_path)
            except TrackError:  # noqa: PERF203
                extra_paths.append(file_path)
            else:
                if not album:
                    album = track.album

        if not album:
            err_msg = f"No tracks found in album directory. [dir={album_path}]"
            raise AlbumError(err_msg)

        for extra_path in extra_paths:
            Extra(album, extra_path)

        log.debug(f"Album created from directory. [dir={album_path}, {album=}]")
        return album

    @property
    def fields(self) -> set[str]:
        """Returns any editable, track-specific fields."""
        return super().fields.union({"path"})

    def get_extra(self, rel_path: PurePath) -> Extra | None:
        """Gets an Extra by its path."""
        return next(
            (extra for extra in self.extras if extra.rel_path == rel_path), None
        )

    def get_track(self, track_num: int, disc: int = 1) -> Track | None:
        """Gets a Track by its track number."""
        return cast("Track", super().get_track(track_num, disc))

    def is_unique(self, other: LibItem) -> bool:
        """Returns whether an album is unique in the library from ``other``."""
        if not isinstance(other, Album):
            return True

        if self.path == other.path:
            return False

        custom_uniqueness = config.CONFIG.pm.hook.is_unique_album(
            album=self, other=other
        )
        return False not in custom_uniqueness

    def merge(self, other: Self | MetaAlbum, overwrite: bool = False) -> None:  # noqa: FBT001, FBT002
        """Merges another album into this one.

        Args:
            other: Other album to be merged with the current album.
            overwrite: Whether or not to overwrite self if a conflict exists.
        """
        log.debug(f"Merging albums. [album_a={self!r}, album_b={other!r}")

        self._merge_tracks(other, overwrite=overwrite)
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

        log.debug(f"Albums merged. [album_a={self!r}, album_b={other!r}, {overwrite=}]")

    def _merge_tracks(
        self, other: Album | MetaAlbum, *, overwrite: bool = False
    ) -> None:
        """Merges the tracks of another album into this one."""
        new_tracks: list[Track] = []
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
        self,
        other: Album | MetaAlbum,
        overwrite: bool = False,  # noqa: FBT001, FBT002
    ) -> None:
        """Merges the extras of another album into this one."""
        if isinstance(other, Album):
            new_extras: list[Extra] = []
            for other_extra in other.extras:
                conflict_extra = self.get_extra(other_extra.rel_path)
                if conflict_extra:
                    conflict_extra.merge(other_extra, overwrite)
                else:
                    new_extras.append(other_extra)
            self.extras.extend(new_extras)

    @hybrid_property
    def original_year(self) -> int | None:
        """Gets an Album's year."""
        if self.original_date is None:
            return None

        return self.original_date.year

    @original_year.inplace.expression  # type: ignore[reportArgumentType]
    @classmethod
    def _original_year_expression(
        cls: type[Album],
    ) -> ColumnExpressionArgument[int | None]:
        """Returns a year at the sql level."""
        return sa.extract("year", cls.original_date)

    @hybrid_property
    def year(self) -> int:
        """Gets an Album's year."""
        return self.date.year

    @year.inplace.expression  # type: ignore[reportArgumentType]
    @classmethod
    def _year_expression(
        cls: type[Album],
    ) -> ColumnExpressionArgument[int]:
        """Returns a year at the sql level."""
        return sa.extract("year", cls.date)

    def __repr__(self) -> str:
        """Represents an Album using its fields."""
        field_reprs = [
            f"{field}={getattr(self, field)!r}"
            for field in self.fields
            if hasattr(self, field)
        ]
        repr_str = "Album(" + ", ".join(field_reprs)

        custom_field_reprs = []
        for custom_field, value in self.custom.items():
            custom_field_reprs.append(f"{custom_field}={value}")
        if custom_field_reprs:
            repr_str += ", custom_fields=[" + ", ".join(custom_field_reprs) + "]"

        track_reprs = [
            f"{track.disc}.{track.track_num} - {track.title}"
            for track in sorted(self.tracks)
        ]
        repr_str += ", tracks=[" + ", ".join(track_reprs) + "]"

        extra_reprs = [f"{extra.path.name}" for extra in sorted(self.extras)]
        repr_str += ", extras=[" + ", ".join(extra_reprs) + "]"

        repr_str += ")"
        return repr_str
