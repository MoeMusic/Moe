"""Shared functionality between library albums, extras, and tracks."""

from pathlib import Path

import sqlalchemy

__all__ = ["LibItem"]


class LibItem:
    """Abstract base class for library items i.e. Albums, Extras, and Tracks."""

    @property
    def path(self):
        """A library item's filesystem path."""
        raise NotImplementedError


class PathType(sqlalchemy.types.TypeDecorator):
    """A custom type for paths for database storage.

    Normally, paths are Path type, but we can't store that in the database,
    so we normalize the paths first for database storage.
    """

    impl = sqlalchemy.types.String  # sql type
    cache_ok = True  # expected to produce same bind/result behavior and sql generation

    def process_bind_param(self, pathlib_path, dialect):
        """Convert the absolute path to a string prior to entering in the database."""
        return str(pathlib_path.resolve())

    def process_result_value(self, path_str, dialect):
        """Convert the path back to Path on the way out."""
        if path_str is None:
            return None

        return Path(path_str)
