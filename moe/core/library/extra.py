"""Any non-music item attached to an album such as log files are considered extras."""

import os
from pathlib import Path
from typing import TYPE_CHECKING, cast

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey, UniqueConstraint

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


class Extra(LibItem, Base):  # noqa: WPS214
    """An Album can have any number of extra files such as logs, cues, etc.

    Attributes:
        album (Album): Album the extra file belongs to.
        filename (str): Base file name of the extra file.
        path (Path): Filesystem path of the extra file.
    """

    __tablename__ = "extras"

    _id: int = Column(Integer, primary_key=True)
    _filename: str = Column(String, nullable=False)
    _path: Path = Column(PathType, nullable=False, unique=True)

    _album_id: int = Column(Integer, ForeignKey("album._id"))
    album: Album = relationship("Album", back_populates="extras")

    __table_args__ = (UniqueConstraint("_filename", "_album_id"),)

    def __init__(self, path: Path, album: Album):
        """Creates an extra.

        Args:
            path: Filesystem path of the extra file.
            album: Album the extra file belongs to.
        """
        self.path = path
        self.album = album

    @typed_hybrid_property
    def filename(self) -> str:
        """Gets an Extra's filename."""
        return cast(str, self._filename)

    @filename.setter  # noqa: WPS440
    def filename(self, new_name: str):  # noqa: WPS440
        """Sets an Extra's filename and renames it on the filesystem."""
        self._filename = new_name
        new_path = self.path.parent / new_name
        os.rename(self.path, new_path)
        self.path = new_path

    @typed_hybrid_property
    def path(self) -> Path:
        """Gets an Extra's path."""
        return self._path

    @path.setter  # noqa: WPS440
    def path(self, new_path: Path):  # noqa: WPS440
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

    def __eq__(self, other):
        """Compares an Extra by it's attributes."""
        if isinstance(other, Extra):
            return (
                self.album.artist == other.album.artist
                and self.album.title == other.album.title
                and self.album.year == other.album.year
                and self.filename == other.filename
            )
        return False
