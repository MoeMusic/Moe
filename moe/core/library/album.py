"""An Album in the database and any related logic."""

import errno
import os
import pathlib
from collections import OrderedDict
from typing import TYPE_CHECKING, Any, Set, TypeVar

import sqlalchemy
from sqlalchemy import Column, Integer, String  # noqa: WPS458
from sqlalchemy.orm import events, relationship

from moe.core.library.lib_item import LibItem
from moe.core.library.session import Base

# This would normally cause a cyclic dependency.
if TYPE_CHECKING:
    from moe.core.library.extra import Extra  # noqa: F401, WPS433
    from moe.core.library.track import Track  # noqa: F401, WPS433

# Album generic, used for typing classmethod
A = TypeVar("A", bound="Album")  # noqa: WPS111


class _PathType(sqlalchemy.types.TypeDecorator):
    """A custom type for paths for database storage.

    Normally, paths are pathlib.Path type, but we can't store that in the database,
    so we normalize the paths first for database storage.
    """

    impl = sqlalchemy.types.String  # sql type
    cache_ok = True  # expected to produce same bind/result behavior and sql generation

    def process_bind_param(self, pathlib_path, dialect):
        """Convert the absolute path to a string prior to enterting in the database."""
        return str(pathlib_path.resolve())

    def process_result_value(self, path_str, dialect):
        """Convert the path back to pathlib.Path on the way out."""
        return pathlib.Path(path_str)


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

    path: pathlib.Path = Column(_PathType, nullable=False, unique=True)

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

    def to_dict(self) -> "OrderedDict[str, Any]":
        """Represents the Album as a dictionary.

        The basis of an album's representation is the merged dictionary of its tracks.
        If different values are present for any given attribute among tracks, then
        the value becomes "Various". It also includes any extras, and removes any
        values that are guaranteed to be unique between tracks, such as track number.

        Returns:
            A dict representation of an Album.
            It will be in the form { attribute: value } and is sorted by attribute.
        """
        # access any element to set intial values
        track_list = list(self.tracks)  # easier to deal with a list for this func
        album_dict = track_list[0].to_dict()

        # compare rest of album against initial values
        for track in track_list[1:]:
            track_dict = track.to_dict()
            for key in {**track_dict, **album_dict}.keys():
                if album_dict.get(key) != track_dict.get(key):
                    album_dict[key] = "Various"

        album_dict["extras"] = {str(extra.path) for extra in self.extras}

        # remove values that are always unique between tracks
        album_dict.pop("path")
        album_dict.pop("title")
        album_dict.pop("track_num")

        return album_dict

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


@sqlalchemy.event.listens_for(Album.path, "set")
def album_path_set(
    target: Album,
    value: pathlib.Path,
    oldvalue: pathlib.Path,
    initiator: events.AttributeEvents,
):
    """Only allow paths that exist."""
    if not value.is_dir():
        raise NotADirectoryError(
            errno.ENOENT, os.strerror(errno.ENOENT), str(value.resolve())
        )
