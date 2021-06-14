"""Any non-music item attached to an album such as log files are considered extras."""

import pathlib
from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKeyConstraint

from moe.core.library.album import Album
from moe.core.library.lib_item import LibItem, PathType
from moe.core.library.session import Base

# Makes hybrid_property's have the same typing as a normal properties.
# Use until the stubs are improved.
if TYPE_CHECKING:
    typed_hybrid_property = property
else:
    from sqlalchemy.ext.hybrid import (  # noqa: WPS440
        hybrid_property as typed_hybrid_property,
    )


class Extra(LibItem, Base):
    """An Album can have any number of extra files such as logs, cues, etc.

    Attributes:
        album (Album): Album the extra file belongs to.
        path (pathlib.Path): Filesystem path of the extra file.
    """

    __tablename__ = "extras"

    # unique Extra = filename + Album
    _filename = Column(String, primary_key=True)
    _albumartist = Column(String, nullable=False, primary_key=True)
    _album = Column(String, nullable=False, primary_key=True)
    _year = Column(Integer, nullable=False, primary_key=True, autoincrement=False)

    album: Album = relationship("Album", back_populates="extras")
    _path: pathlib.Path = Column(
        PathType, nullable=False, unique=True, primary_key=True
    )

    __table_args__ = (
        ForeignKeyConstraint(
            ["_albumartist", "_album", "_year"],
            ["albums.artist", "albums.title", "albums.year"],
        ),
    )

    def __init__(self, path: pathlib.Path, album: Album):
        """Creates an extra.

        Args:
            path: Filesystem path of the extra file.
            album: Album the extra file belongs to.
        """
        self.path = path
        self.album = album
        self._filename = path.name

    @typed_hybrid_property
    def path(self):
        """Gets an Extra's path."""
        return self._path

    @path.setter
    def path(self, new_path: pathlib.Path):  # noqa: WPS440
        """Sets an Extra's path."""
        self._filename = new_path.name
        self._path = new_path

    def __str__(self):
        """String representation of an Extra."""
        return f"{self.album}: {self._filename}"

    def __repr__(self):
        """Represents an Extra using its primary keys."""
        return (
            f"{self.__class__.__name__}("
            f"{repr(self.album)}, filename={repr(self._filename)})"
        )
