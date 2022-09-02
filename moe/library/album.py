"""An Album in the database and any related logic."""

import datetime
from pathlib import Path
from typing import TYPE_CHECKING, List, Optional, Tuple, cast

import sqlalchemy as sa
from sqlalchemy import Column, Date, Integer, String, and_, or_
from sqlalchemy.orm import joinedload, relationship

from moe.config import MoeSession
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


class Album(LibItem, SABase):
    """An album is a collection of tracks and represents a specific album release.

    Albums also house any attributes that are shared by tracks e.g. albumartist.

    Attributes:
        artist (str): AKA albumartist.
        date (datetime.date): Album release date.
        disc_total (int): Number of discs in the album.
        extras (List[Extra]): Extra non-track files associated with the album.
        mb_album_id (str): Musicbrainz album aka release id.
        path (Path): Filesystem path of the album directory.
        title (str)
        tracks (List[Track]): Album's corresponding tracks.
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

    tracks: "List[Track]" = relationship(
        "Track",
        back_populates="album_obj",
        cascade="all, delete-orphan",
        collection_class=list,
    )
    extras: "List[Extra]" = relationship(
        "Extra",
        back_populates="album_obj",
        cascade="all, delete-orphan",
        collection_class=list,
    )

    def __init__(
        self, artist: str, title: str, date: datetime.date, path: Path, **kwargs
    ):
        """Creates an Album.

        Args:
            artist: Album artist.
            title: Album title.
            date: Album release date.
            path: Filesystem path of the album directory.
            **kwargs: Any other fields to assign to the Album.

        Note that a path must be present prior to the album being added to the db.

        Raises:
            ValueError: No path given and the move plugin is disabled.
        """
        self.artist = artist
        self.date = date
        self.path = path
        self.title = title

        # set default values
        self.disc_total = 1

        for key, value in kwargs.items():
            if value:
                setattr(self, key, value)

    def fields(self) -> Tuple[str, ...]:
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
            return None

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

    def is_unique(self, other: Optional["Album"]) -> bool:
        """Whether or not the given album is unique (by tags) from the current album."""
        if not other:
            return True
        return self.mb_album_id != other.mb_album_id

    def merge(self, other: "Album", overwrite: bool = False) -> None:
        """Merges another album into this one.

        Args:
            other: Other album to be merged with the current album.
            overwrite: Whether or not to overwrite self if a conflict exists.
        """
        for field in self.fields():
            if field not in {"path", "year", "tracks", "extras"}:
                other_value = getattr(other, field)
                self_value = getattr(self, field)
                if other_value and (overwrite or (not overwrite and not self_value)):
                    setattr(self, field, other_value)

        new_tracks: List["Track"] = []
        for other_track in other.tracks:
            conflict_track = self.get_track(other_track.track_num, other_track.disc)
            if conflict_track:
                conflict_track.merge(other_track, overwrite)
            else:
                new_tracks.append(other_track)
        self.tracks.extend(new_tracks)

        new_extras: List["Extra"] = []
        for other_extra in other.extras:
            conflict_extra = self.get_extra(other_extra.filename)
            if conflict_extra and overwrite:
                self.extras.remove(conflict_extra)
                new_extras.append(other_extra)
            elif not conflict_extra:
                new_extras.append(other_extra)
        self.extras.extend(new_extras)

    @typed_hybrid_property
    def year(self) -> int:  # type: ignore
        """Gets an Album's year."""
        return self.date.year

    @year.expression  # type: ignore
    def year(cls):  # noqa: B902
        """Returns a year at the sql level."""
        return sa.extract("year", cls.date)

    def __eq__(self, other) -> bool:
        """Compares an Album by its attributes."""
        if isinstance(other, Album):
            for attr in self.fields():
                if getattr(self, attr) != getattr(other, attr):
                    return False
            return True
        return False

    def __lt__(self, other: "Album") -> bool:
        """Sort an album based on its title, then artist, then date."""
        if self.title == other.title:
            if self.artist == other.artist:
                return self.date < other.date

            return self.artist < other.artist

        return self.title < other.title

    def __str__(self):
        """String representation of an Album."""
        return f"{self.artist} - {self.title} ({self.year})"

    def __repr__(self):
        """Represents an Album using its primary key and unique fields."""
        return (
            f"{self.__class__.__name__}("
            f"id={repr(self._id)}, "
            f"artist={repr(self.artist)}, "
            f"title={repr(self.title)}, "
            f"date={repr(self.date)}, "
            f"path={repr(self.path)})"
        )
