"""Any non-music item attached to an album such as log files are considered extras."""

from pathlib import Path
from typing import TYPE_CHECKING, Optional, Tuple, cast

from sqlalchemy import Column, Integer
from sqlalchemy.orm import joinedload, relationship
from sqlalchemy.schema import ForeignKey

from moe.config import MoeSession
from moe.library import SABase
from moe.library.album import Album
from moe.library.lib_item import LibItem, PathType

# Makes hybrid_property's have the same typing as a normal properties.
# Use until the stubs are improved.
if TYPE_CHECKING:
    typed_hybrid_property = property
else:
    from sqlalchemy.ext.hybrid import hybrid_property as typed_hybrid_property

__all__ = ["Extra"]


class Extra(LibItem, SABase):
    """An Album can have any number of extra files such as logs, cues, etc.

    Attributes:
        album_obj (Album): Album the extra file belongs to.
        filename (str): Base file name of the extra file.
            Read-only. Set ``path`` instead.
        path (Path): Filesystem path of the extra file.
    """

    __tablename__ = "extras"

    _id: int = cast(int, Column(Integer, primary_key=True))
    path: Path = cast(Path, Column(PathType, nullable=False, unique=True))

    _album_id: int = cast(int, Column(Integer, ForeignKey("album._id")))
    album_obj: Album = relationship("Album", back_populates="extras")

    def __init__(self, album: Album, path: Path):
        """Creates an Extra.

        Args:
            album: Album the extra file belongs to.
            path: Filesystem path of the extra file.
        """
        album.extras.append(self)
        self.path = path

    @typed_hybrid_property
    def filename(self) -> str:
        """Gets an Extra's filename."""
        return self.path.name

    def fields(self) -> Tuple[str, ...]:
        """Returns the public fields, or non-method attributes, of an Extra."""
        return "filename", "path"

    def get_existing(self) -> Optional["Extra"]:
        """Gets a matching Extra in the library by its unique attributes.

        Returns:
            Duplicate extra or the same extra if it already exists in the library.
        """
        session = MoeSession()

        existing_extra = (
            session.query(Extra)
            .filter(Extra.path == self.path)
            .options(joinedload("*"))
            .one_or_none()
        )
        if not existing_extra:
            return None

        session.expunge(existing_extra)
        return existing_extra

    def __eq__(self, other):
        """Compares Extras by their 'uniqueness' in the database."""
        if not isinstance(other, Extra):
            return False

        if self.path == other.path:
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
