"""An Album in the database and any related logic."""

import pathlib
from typing import TYPE_CHECKING, Set, TypeVar

from sqlalchemy import Column, Integer, String  # noqa: WPS458
from sqlalchemy.orm import relationship

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
        extras (Set(Extra)): Extra non-track files associated with the album.
        path (pathlib.Path): Filesystem path of the album directory.
        title (str)
        tracks (Set[Track]): Album's corresponding tracks.
        year (str)
    """

    __tablename__ = "albums"

    # unique Album = artist + title + year
    artist: str = Column(String, nullable=False, primary_key=True)
    title: str = Column(String, nullable=False, primary_key=True)
    year: int = Column(Integer, nullable=False, primary_key=True)

    path: pathlib.Path = Column(PathType, nullable=False, unique=True)

    tracks = relationship(
        "Track",
        back_populates="album_obj",
        cascade="all, delete-orphan",
        collection_class=set,
    )  # type: Set[Track] # noqa: WPS400
    extras = relationship(
        "Extra",
        back_populates="album",
        cascade="all, delete-orphan",
        collection_class=set,
    )  # type: Set[Extra] # noqa: WPS400

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

    def __str__(self):
        """String representation of an Album."""
        return f"{self.artist} - {self.title} ({self.year})"

    def __repr__(self):
        """Represents an Album using it's primary keys."""
        return (
            f"{self.__class__.__name__}("
            f"artist={repr(self.artist)}, "
            f"title={repr(self.title)}, "
            f"year={repr(self.year)}, "
            f"path={repr(self.path)})"
        )

    def __eq__(self, other):
        """Compares an Album using its primary keys."""
        if isinstance(other, Album):
            return (
                self.artist == other.artist
                and self.title == other.title
                and self.year == other.year
            )
        return False
