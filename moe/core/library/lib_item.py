"""A LibItem in the database and any related logic."""

import pathlib

import sqlalchemy


class LibItem:
    """Abstract base class for library items i.e. Albums, Extras, and Tracks."""


class PathType(sqlalchemy.types.TypeDecorator):
    """A custom type for paths for database storage.

    Normally, paths are pathlib.Path type, but we can't store that in the database,
    so we normalize the paths first for database storage.
    """

    impl = sqlalchemy.types.String  # sql type
    cache_ok = True  # expected to produce same bind/result behavior and sql generation

    def process_bind_param(self, pathlib_path, dialect):
        """Convert the absolute path to a string prior to enterting in the database."""
        return str(pathlib_path.resolve())

    def process_result_value(self, path_str, dialect):
        """Convert the path back to pathlib.Path on the way out."""
        return pathlib.Path(path_str)
