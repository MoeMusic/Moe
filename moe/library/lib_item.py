"""Shared functionality between library albums, extras, and tracks."""

import functools
from pathlib import Path
from typing import Any

import pluggy
import sqlalchemy
import sqlalchemy as sa
import sqlalchemy.event
import sqlalchemy.orm

import moe
from moe.config import Config

__all__ = ["LibItem", "LibraryError"]


class LibraryError(Exception):
    """General library error."""


class Hooks:
    """General usage library item hooks."""

    @staticmethod
    @moe.hookspec
    def process_new_items(config: Config, items: list["LibItem"]):
        """Process any new or changed items after they have been added to the library.

        Args:
            config: Moe config.
            items: Any new or changed items that have been successfully added to the
                library during the current session.
        """


@moe.hookimpl
def add_hooks(plugin_manager: pluggy.manager.PluginManager):
    """Registers `add` hookspecs to Moe."""
    from moe.library.lib_item import Hooks

    plugin_manager.add_hookspecs(Hooks)


@moe.hookimpl
def register_sa_event_listeners(config: Config, session: sqlalchemy.orm.Session):
    """Registers event listeners for editing and processing new items."""
    sqlalchemy.event.listen(
        session,
        "after_flush",
        functools.partial(_process_new_items, config=config),
    )


def _process_new_items(
    session: sqlalchemy.orm.Session,
    flush_context: sqlalchemy.orm.UOWTransaction,
    config: Config,
):
    """Runs the ``process_new_items`` hook specification.

    This uses the sqlalchemy ORM event ``after_flush`` in the background to determine
    the time of execution and to provide any new or changed items to the hook
    implementations.

    Args:
        session: Current db session.
        flush_context: sqlalchemy obj which handles the details of the flush.
        config: Moe config.
    """
    config.plugin_manager.hook.process_new_items(
        config=config, items=session.new.union(session.dirty)
    )


class LibItem:
    """Abstract base class for library items i.e. Albums, Extras, and Tracks."""

    @property
    def path(self):
        """A library item's filesystem path."""
        raise NotImplementedError

    def fields(self) -> tuple[str, ...]:
        """Returns the public attributes of an item."""
        raise NotImplementedError

    def __getattr__(self, name: str) -> Any:
        """See if ``name`` is a custom field."""
        try:
            return self.__dict__["_custom_fields"][name]
        except KeyError:
            raise AttributeError from None

    def __setattr__(self, name: str, value: Any) -> None:
        """Set custom fields if a valid key."""
        if (
            "_custom_fields" in self.__dict__
            and name in self.__dict__["_custom_fields"]
        ):
            self._custom_fields[name] = value
        else:
            super().__setattr__(name, value)


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
