"""Shared functionality between library albums, extras, and tracks."""

from pathlib import Path
from typing import Tuple

import sqlalchemy as sa

__all__ = ["LibItem"]


class LibItem:
    """Abstract base class for library items i.e. Albums, Extras, and Tracks."""

    @property
    def path(self):
        """A library item's filesystem path."""
        raise NotImplementedError

    def fields(self) -> Tuple[str, ...]:
        """Returns the public attributes of an item."""
        raise NotImplementedError

    def get_existing(self) -> "LibItem":
        """Returns a matching item in the library by its unique attributes."""
        raise NotImplementedError


class PathType(sa.types.TypeDecorator):
    """A custom type for paths for database storage.

    Normally, paths are Path type, but we can't store that in the database,
    so we normalize the paths first to strings for database storage. Paths are stored as
    relative paths from ``library_path`` in the config.
    """

    impl = sa.types.String  # sql type
    cache_ok = True  # expected to produce same bind/result behavior and sql generation

    library_path: Path  # will be set on config initialization

    def process_bind_param(self, pathlib_path, dialect):
        """Normalize pathlib paths as strings for the database.

        Args:
            pathlib_path: Inbound path to the db.
            dialect: Database in use.

        Returns:
            Relative path from ``library_path`` if possible, otherwise stores the
            absolute path.
        """
        try:
            return str(pathlib_path.relative_to(self.library_path))
        except ValueError:
            return str(pathlib_path.resolve())

    def process_result_value(self, path_str, dialect):
        """Convert the path back to a Path object on the way out."""
        if path_str is None:
            return None

        return Path(self.library_path / path_str)
