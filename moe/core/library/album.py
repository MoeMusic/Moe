"""An Album in the database and any related logic."""

import datetime
import pathlib
from typing import TYPE_CHECKING, List, Optional

import sqlalchemy
from sqlalchemy import Column, Date, Integer, String  # noqa: WPS458
from sqlalchemy.orm import relationship
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
        path (pathlib.Path): Filesystem path of the album directory.
        title (str)
        tracks (List[Track]): Album's corresponding tracks.
    """

    __tablename__ = "album"

    _id: int = Column(Integer, primary_key=True)
    artist: str = Column(String, nullable=False)
    date: datetime.date = Column(Date, nullable=False)
    path: pathlib.Path = Column(PathType, nullable=False, unique=True)
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
        self, artist: str, title: str, date: datetime.date, path: pathlib.Path, **kwargs
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

        for key, value in kwargs.items():
            setattr(self, key, value)

    def has_eq_keys(self, other: "Album") -> bool:
        """Compares an Album by its primary keys."""
        return (
            self.artist == other.artist
            and self.date == other.date
            and self.title == other.title
        )

    def get_existing(self, session: Session, query_opts=None) -> Optional["Album"]:
        """Gets a matching Album in the library.

        Args:
            session: Current db session.
            query_opts: Optional query options to provide. See
                https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query.options
                for more info.

        Returns:
             Matching existing album in the library.
        """
        if query_opts:
            return (
                session.query(Album)
                .filter_by(artist=self.artist, title=self.title, date=self.date)
                .options(query_opts)
                .one_or_none()
            )
        return (
            session.query(Album)
            .filter_by(artist=self.artist, title=self.title, date=self.date)
            .one_or_none()
        )

    def merge_existing(self, session: Session):
        """Merges the current Album with an existing Album in the library."""
        existing_album = self.get_existing(session)
        if existing_album:
            self._id = existing_album._id

        for track in self.tracks:
            track._album_id = self._id
            existing_track = track.get_existing(session)
            if existing_track:
                track._id = existing_track._id

        for extra in self.extras:
            extra._album_id = self._id
            existing_extra = extra.get_existing(session)
            if existing_extra:
                extra._id = existing_extra._id

        session.merge(self)

    @typed_hybrid_property
    def year(self) -> int:
        """Gets an Album's year."""
        return self.date.year

    @year.expression
    def year(cls):  # noqa: B902, N805, WPS440
        """Returns a year at the sql level."""
        return sqlalchemy.extract("year", cls.date)

    def __str__(self):
        """String representation of an Album."""
        return f"{self.artist} - {self.title} ({self.year})"

    def __repr__(self):
        """Represents an Album using it's primary keys."""
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
                and self.title == other.title
                and self.tracks == other.tracks
                and self.extras == other.extras
            )
        return False
