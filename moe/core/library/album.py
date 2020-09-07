"""An Album in the database and any related logic."""

from collections import OrderedDict
from typing import TYPE_CHECKING, Any, Type, TypeVar

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import Session
from sqlalchemy.schema import UniqueConstraint

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
        tracks (List[Track]): All the album's corresponding tracks.
        year (str)
    """

    __tablename__ = "albums"
    __table_args__ = (UniqueConstraint("artist", "title", "year"),)

    _id = Column(Integer, primary_key=True)
    artist = Column(String, nullable=False)
    title = Column(String, nullable=False)
    year = Column(Integer, nullable=False)

    tracks = relationship("Track", back_populates="_album_obj", cascade="all, delete")

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

    def to_dict(self) -> "OrderedDict[str, Any]":
        """Represents the Album as a dictionary.

        An albums representation is just the merged dictionary of all its tracks.
        If different values are present for any given attribute among tracks, then
        the value becomes "Various".

        Returns:
            Returns a dict representation of an Album.
            It will be in the form { attribute: value } and is sorted by attribute.
        """
        album_dict = self.tracks[0].to_dict()  # type: ignore
        for track in self.tracks[1:]:  # type: ignore
            track_dict = track.to_dict()
            for key in {**track_dict, **album_dict}.keys():
                if album_dict.get(key) != track_dict.get(key):
                    album_dict[key] = "Various"

        return album_dict

    @classmethod
    def get_or_create(
        cls: Type[A],
        session: Session,
        artist: str,
        title: str,
        year: int,
    ) -> A:
        """Fetches the matching album or creates a new one if it doesn't exist."""
        album = (
            session.query(Album)
            .filter(Album.artist == artist)
            .filter(Album.title == title)
            .filter(Album.year == year)
            .scalar()
        )

        if not album:
            album = Album(artist=artist, title=title, year=year)
            session.add(album)

        return album
