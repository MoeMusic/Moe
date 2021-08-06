"""Any non-music item attached to an album such as log files are considered extras."""

from pathlib import Path
from typing import TYPE_CHECKING, Tuple

from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey

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

__all__ = ["Extra"]


class Extra(LibItem, Base):
    """An Album can have any number of extra files such as logs, cues, etc.

    Attributes:
        album_obj (Album): Album the extra file belongs to.
        filename (str): Base file name of the extra file.
            Read-only. Set ``path`` instead.
        path (Path): Filesystem path of the extra file.
    """

    __tablename__ = "extras"

    _id: int = Column(Integer, primary_key=True)
    path: Path = Column(PathType, nullable=False, unique=True)

    _album_id: int = Column(Integer, ForeignKey("album._id"))
    album_obj: Album = relationship("Album", back_populates="extras")

    def __init__(self, path: Path, album: Album):
        """Creates an extra.

        Args:
            path: Filesystem path of the extra file.
            album: Album the extra file belongs to.
        """
        self.path = path
        self.album_obj = album

    @typed_hybrid_property
    def filename(self) -> str:
        """Gets an Extra's filename."""
        return self.path.name

    def fields(self) -> Tuple[str, ...]:
        """Returns the public fields, or non-method attributes, of an Extra."""
        return "filename", "path"

    def __eq__(self, other):
        """Compares an Extra by it's attributes."""
        if isinstance(other, Extra):
            if self.album_obj.is_unique(other.album_obj):
                return False

            for attr in self.fields():
                if attr == "album_obj":  # prevent cyclic comparison
                    continue
                if getattr(self, attr) != getattr(other, attr):
                    return False
            return True
        return False

    def __lt__(self, other: "Extra") -> bool:
        """Sort based on album then path."""
        if self.album_obj == other.album_obj:
            return self.path < other.path

        return self.album_obj < other.album_obj

    def __str__(self):
        """String representation of an Extra."""
        return f"{self.album_obj}: {self.filename}"

    def __repr__(self):
        """Represents an Extra using its primary keys."""
        return (
            f"{self.__class__.__name__}("
            f"{repr(self.album_obj)}, filename={repr(self.filename)})"
        )
