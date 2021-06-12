"""Any non-music item attached to an album such as log files are considered extras."""

import pathlib

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKeyConstraint

from moe.core.library.album import Album
from moe.core.library.music_item import MusicItem, PathType
from moe.core.library.session import Base


class Extra(MusicItem, Base):
    """An Album can have any number of extra files such as logs, cues, etc.

    Attributes:
        path (pathlib.Path): Path of the extra file.
    """

    __tablename__ = "extras"

    path: pathlib.Path = Column(PathType, nullable=False, primary_key=True)

    _albumartist: str = Column(String, nullable=False)
    _album: str = Column(String, nullable=False)
    _year: int = Column(Integer, nullable=False, autoincrement=False)

    _album_obj: Album = relationship("Album", back_populates="extras")

    __table_args__ = (
        ForeignKeyConstraint(
            [_albumartist, _album, _year],
            [Album.artist, Album.title, Album.year],  # type: ignore
        ),
    )

    def __init__(self, path: pathlib.Path):
        """Creates an extra."""
        self.path = path
