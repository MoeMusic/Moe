"""An Album in the database and any related logic."""

from collections import OrderedDict
from typing import TYPE_CHECKING, Any, Set, TypeVar

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from moe.core.library.music_item import MusicItem
from moe.core.library.session import Base

# This would normally cause a cyclic dependency.
if TYPE_CHECKING:
    from moe.core.library.track import Track  # noqa: F401, WPS433

# Album generic, used for typing classmethod
A = TypeVar("A", bound="Album")  # noqa: WPS111


class Album(MusicItem, Base):
    """An album is a collection of tracks.

    Albums also house any attributes that are shared by tracks e.g. albumartist.

    Attributes:
        artist (str): AKA albumartist.
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
    )  # type: Set[Track]  # noqa: WPS400

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

    def to_dict(self) -> "OrderedDict[str, Any]":
        """Represents the Album as a dictionary.

        An albums representation is just the merged dictionary of all its tracks.
        If different values are present for any given attribute among tracks, then
        the value becomes "Various".

        Returns:
            Returns a dict representation of an Album.
            It will be in the form { attribute: value } and is sorted by attribute.
        """
        # access any element to set intial values
        random_track = self.tracks.pop()
        self.tracks.add(random_track)
        album_dict = random_track.to_dict()

        # compare rest of album against initial values
        for track in self.tracks:
            track_dict = track.to_dict()
            for key in {**track_dict, **album_dict}.keys():
                if album_dict.get(key) != track_dict.get(key):
                    album_dict[key] = "Various"

        return album_dict

    def add_to_db(self):
        """Adds an album to the database.

        Raises:
            DbDupTrackPathError: Track's path already exists in the library.
                Note, this will only get raised if the two tracks are not considered
                identical by the DB (same primary keys).
        """
        for track in self.tracks:
            track.add_to_db()
