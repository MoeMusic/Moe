"""An Album in the database and any related logic."""

import datetime
from pathlib import Path
from typing import TYPE_CHECKING, List, Optional

import sqlalchemy
from sqlalchemy import Column, Date, Integer, String  # noqa: WPS458
from sqlalchemy.orm import joinedload, relationship
from sqlalchemy.orm.session import Session
from sqlalchemy.schema import UniqueConstraint

from moe.core.library.lib_item import LibItem, PathType
from moe.core.library.session import Base

# This would normally cause a cyclic dependency.
if TYPE_CHECKING:
    from moe.core.library.extra import Extra  # noqa: F401, WPS433
    from moe.core.library.track import Track  # noqa: F401, WPS433

    # Makes hybrid_property's have the same typing as a normal properties.
    # Use until the stubs are improved.
    typed_hybrid_property = property
else:
    from sqlalchemy.ext.hybrid import (  # noqa: WPS440
        hybrid_property as typed_hybrid_property,
    )


class Album(LibItem, Base):
    """An album is a collection of tracks.

    Albums also house any attributes that are shared by tracks e.g. albumartist.

    Attributes:
        artist (str): AKA albumartist.
        date (datetime.date): Album release date.
        extras (List[Extra]): Extra non-track files associated with the album.
        mb_id (str): Musicbrainz album aka release id.
        path (Path): Filesystem path of the album directory.
        title (str)
        tracks (List[Track]): Album's corresponding tracks.
    """

    __tablename__ = "album"

    _id: int = Column(Integer, primary_key=True)
    artist: str = Column(String, nullable=False)
    date: datetime.date = Column(Date, nullable=False)
    mb_id: str = Column(String, nullable=False, default="")
    path: Path = Column(PathType, nullable=False, unique=True)
    title: str = Column(String, nullable=False)

    __table_args__ = (UniqueConstraint("artist", "title", "date"),)

    tracks: "List[Track]" = relationship(
        "Track",
        back_populates="album_obj",
        cascade="all, delete-orphan",
        collection_class=list,
    )
    extras: "List[Extra]" = relationship(
        "Extra",
        back_populates="album",
        cascade="all, delete-orphan",
        collection_class=list,
    )

    def __init__(  # noqa: WPS211
        self, artist: str, title: str, date: datetime.date, path: Path, **kwargs
    ):
        """Creates an album.

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
        self.mb_id = ""

        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_existing(self, session: Session) -> Optional["Album"]:
        """Gets a matching Album in the library."""
        existing_album = (
            session.query(Album)
            .filter_by(artist=self.artist, title=self.title, date=self.date)
            .options(joinedload("*"))
            .one_or_none()
        )
        if not existing_album:
            return None

        session.expunge(existing_album)
        return existing_album

    def get_extra(self, filename: str) -> Optional["Extra"]:
        """Gets an Extra by its filename."""
        return next(
            (extra for extra in self.extras if extra.filename == filename), None
        )

    def get_track(self, track_num: int) -> Optional["Track"]:
        """Gets a Track by its track number."""
        return next(
            (track for track in self.tracks if track.track_num == track_num), None
        )

    def is_unique(self, other: "Album") -> bool:
        """Whether or not the given album is unique (by tags) from the current album."""
        return (
            self.artist != other.artist
            or self.date != other.date
            or self.title != other.title
        )

    def merge(self, other: Optional["Album"], overwrite_album_info=True):
        """Merges the current Album with another, overwriting the other if conflict.

        Changes won't take effect until the album is merged into the session.

        Args:
            other: Other album to be merged into the current album.
            overwrite_album_info: If ``False``, the album metadata of the other album
                will persist onto the current album. Only the tracks and extras will
                be overwritten in this case.
        """
        if not other:
            return

        self._id = other._id

        if not overwrite_album_info:
            self.artist = other.artist
            self.date = other.date
            self.title = other.title
            self.mb_id = other.mb_id

        for other_track in other.tracks:
            conflict_track = self.get_track(other_track.track_num)
            if conflict_track:
                conflict_track._id = other_track._id
            else:
                self.tracks.append(other_track)

        for track in self.tracks:
            track._album_id = self._id

        for other_extra in other.extras:
            conflict_extra = self.get_extra(other_extra.filename)
            if conflict_extra:
                conflict_extra._id = other_extra._id
            else:
                self.extras.append(other_extra)

        for extra in self.extras:
            extra._album_id = self._id

    @typed_hybrid_property
    def year(self) -> int:
        """Gets an Album's year."""
        return self.date.year

    @year.expression  # noqa: WPS440
    def year(cls):  # noqa: B902, N805, WPS440
        """Returns a year at the sql level."""
        return sqlalchemy.extract("year", cls.date)

    def __str__(self):
        """String representation of an Album."""
        return f"{self.artist} - {self.title} ({self.year})"

    def __repr__(self):
        """Represents an Album using it's primary key and unique fields."""
        return (
            f"{self.__class__.__name__}("
            f"id={repr(self._id)}, "
            f"artist={repr(self.artist)}, "
            f"title={repr(self.title)}, "
            f"date={repr(self.date)}, "
            f"path={repr(self.path)})"
        )

    def __eq__(self, other):
        """Compares an Album by it's attributes."""
        if isinstance(other, Album):
            return (
                self.artist == other.artist  # noqa: WPS222
                and self.date == other.date
                and self.mb_id == other.mb_id
                and self.title == other.title
                and self.tracks == other.tracks
                and self.extras == other.extras
            )
        return False
