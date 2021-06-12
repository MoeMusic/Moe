"""An Album in the database and any related logic."""

import pathlib
from collections import OrderedDict
from typing import TYPE_CHECKING, Any, Set, TypeVar

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from moe.core.library.music_item import MusicItem
from moe.core.library.session import Base

# This would normally cause a cyclic dependency.
if TYPE_CHECKING:
    from moe.core.library.extra import Extra  # noqa: F401, WPS433
    from moe.core.library.track import Track  # noqa: F401, WPS433

# Album generic, used for typing classmethod
A = TypeVar("A", bound="Album")  # noqa: WPS111


class Album(MusicItem, Base):
    """An album is a collection of tracks.

    Albums also house any attributes that are shared by tracks e.g. albumartist.

    Attributes:
        artist (str): AKA albumartist.
        path (pathlib.Path)
        title (str)
        tracks (Set[Track]): All the album's corresponding tracks.
        year (str)
    """

    __tablename__ = "albums"

    artist = Column(String, nullable=False, primary_key=True)
    title = Column(String, nullable=False, primary_key=True)
    year = Column(Integer, nullable=False, primary_key=True)

    tracks = relationship(
        "Track",
        back_populates="_album_obj",
        cascade="all, delete-orphan",
        collection_class=set,
    )  # type: Set[Track] # noqa: WPS400

    extras = relationship(
        "Extra",
        back_populates="_album_obj",
        cascade="all, delete-orphan",
        collection_class=set,
    )  # type: Set[Extra] # noqa: WPS400

    def __init__(self, artist: str, title: str, year: int):
        """Creates an album.

        Args:
            artist: Album artist.
            title: Album title.
            year: Album release year.
        """
        self.artist = artist
        self.title = title
        self.year = year

    @hybrid_property
    def path(self) -> pathlib.Path:
        """Returns the directory path of the album."""
        return list(self.tracks)[0].path.parent  # type: ignore

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
        """String representation of an album."""
        return f"{self.artist} - {self.title}"

    def __repr__(self):
        """Represent an album using it's primary keys."""
        return f"{self.artist} - {self.title} ({self.year})"

    def __eq__(self, other):
        """Album equality based on primary key."""
        return (
            self.artist == other.artist
            and self.title == other.title
            and self.year == other.year
        )
