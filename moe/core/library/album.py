"""An Album in the database and any related logic."""

import pathlib
from typing import TYPE_CHECKING, List, Optional, TypeVar

from sqlalchemy import Column, Integer, String  # noqa: WPS458
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import Session
from sqlalchemy.schema import UniqueConstraint

from moe.core.library.lib_item import LibItem, PathType
from moe.core.library.session import Base

# This would normally cause a cyclic dependency.
if TYPE_CHECKING:
    from moe.core.library.extra import Extra  # noqa: F401, WPS433
    from moe.core.library.track import Track  # noqa: F401, WPS433

# Album generic, used for typing classmethod
A = TypeVar("A", bound="Album")  # noqa: WPS111


class Album(LibItem, Base):
    """An album is a collection of tracks.

    Albums also house any attributes that are shared by tracks e.g. albumartist.

    Attributes:
        artist (str): AKA albumartist.
        extras (List[Extra]): Extra non-track files associated with the album.
        path (pathlib.Path): Filesystem path of the album directory.
        title (str)
        tracks (List[Track]): Album's corresponding tracks.
        year (str)
    """

    __tablename__ = "album"

    _id: int = Column(Integer, primary_key=True)
    artist: str = Column(String, nullable=False)
    path: pathlib.Path = Column(PathType, nullable=False, unique=True)
    title: str = Column(String, nullable=False)
    year: int = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("artist", "title", "year", sqlite_on_conflict="IGNORE"),
    )

    tracks = relationship(
        "Track",
        back_populates="album_obj",
        cascade="all, delete-orphan",
        collection_class=list,
    )  # type: List[Track] # noqa: WPS400
    extras = relationship(
        "Extra",
        back_populates="album",
        cascade="all, delete-orphan",
        collection_class=list,
    )  # type: List[Extra] # noqa: WPS400

    def __init__(
        self,
        artist: str,
        title: str,
        year: int,
        path: pathlib.Path,
    ):
        """Creates an album.

        Args:
            artist: Album artist.
            title: Album title.
            year: Album release year.
            path: Filesystem path of the album directory.

        Raises:
            ValueError: No path given and the move plugin is disabled.
        """
        self.artist = artist
        self.title = title
        self.year = year
        self.path = path

    def has_eq_keys(self, other: "Album") -> bool:
        """Compares an Album by its primary keys."""
        return (
            self.artist == other.artist
            and self.title == other.title
            and self.year == other.year
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
                .filter_by(artist=self.artist, title=self.title, year=self.year)
                .options(query_opts)
                .one_or_none()
            )
        return (
            session.query(Album)
            .filter_by(artist=self.artist, title=self.title, year=self.year)
            .one_or_none()
        )

    def merge_existing(self, session: Session):
        """Merges the current Album with an existing Album in the library."""
        existing_album = self.get_existing(session)
        if existing_album:
            self._id = existing_album._id  # noqa: WPS437

        for track in self.tracks:
            track._album_id = self._id  # noqa: WPS437
            existing_track = track.get_existing(session)
            if existing_track:
                track._id = existing_track._id  # noqa: WPS437

        for extra in self.extras:
            extra._album_id = self._id  # noqa: WPS437
            existing_extra = extra.get_existing(session)
            if existing_extra:
                extra._id = existing_extra._id  # noqa: WPS437

        session.merge(self)

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
            f"year={repr(self.year)}, "
            f"path={repr(self.path)})"
        )

    def __eq__(self, other):
        """Compares an Album by it's attributes."""
        if isinstance(other, Album):
            return (
                self.artist == other.artist  # noqa: WPS222
                and self.title == other.title
                and self.year == other.year
                and self.tracks == other.tracks
                and self.extras == other.extras
            )
        return False
