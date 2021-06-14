"""Any non-music item attached to an album such as log files are considered extras."""

import pathlib
from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKeyConstraint

from moe.core.library.album import Album
from moe.core.library.lib_item import LibItem
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
        filename (str): Base filename of the extra file.
        path (pathlib.Path): Filesystem path of the extra file. Read-only, but you can
            alter the ``filename``.
    """

    __tablename__ = "extras"

    # unique Extra = filename + Album
    filename: str = Column(String, nullable=False, primary_key=True)
    _albumartist = Column(String, nullable=False, primary_key=True)
    _album = Column(String, nullable=False, primary_key=True)
    _year = Column(Integer, nullable=False, primary_key=True, autoincrement=False)

    album: Album = relationship("Album", back_populates="extras")

    __table_args__ = (
        ForeignKeyConstraint(
            ["_albumartist", "_album", "_year"],
            ["albums.artist", "albums.title", "albums.year"],
        ),
    )

    def __init__(self, filename: str, album: Album):
        """Creates an extra.

        Args:
            album: Album the extra file belongs to.
            filename: Base filename of the extra file.
        """
        self.filename = filename
        self.album = album

    @typed_hybrid_property
    def path(self) -> pathlib.Path:
        """Returns the filesystem path of the extra file."""
        return self.album.path / self.filename

    @path.expression  # type: ignore
    def path(cls):  # noqa: WPS440, N805, B902
        """Creates a sql expression so we can query for a path."""
        return Album.path + cls.filename

    def __str__(self):
        """String representation of an Extra."""
        return f"{self.album}: {self.filename}"

    def __repr__(self):
        """Represents an Extra using its primary keys."""
        return (
            f"{self.__class__.__name__}("
            f"{repr(self.album)}, filename={repr(self.filename)})"
        )
