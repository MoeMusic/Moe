"""Shared functionality between library albums, extras, and tracks."""

import logging
from pathlib import Path
from typing import Any

import pluggy
import sqlalchemy
import sqlalchemy as sa
import sqlalchemy.event
import sqlalchemy.orm
from sqlalchemy.orm import declarative_base

import moe
from moe import config

__all__ = ["LibItem", "LibraryError"]

log = logging.getLogger("moe.lib_item")

SABase = declarative_base()


class LibraryError(Exception):
    """General library error."""


class Hooks:
    """General usage library item hooks."""

    @staticmethod
    @moe.hookspec
    def edit_changed_items(items: list["LibItem"]):
        """Edit items in the library that were changed in some way.

        Args:
            items: Any changed items that existed in the library prior to the current
                session.

        See Also:
            The :meth:`process_changed_items` hook for processing items with finalized
            values.
        """

    @staticmethod
    @moe.hookspec
    def edit_new_items(items: list["LibItem"]):
        """Edit new items in the library.

        Args:
            items: Any items being added to the library for the first time.

        See Also:
            The :meth:`process_new_items` hook for processing items with finalized
            values.
        """

    @staticmethod
    @moe.hookspec
    def process_removed_items(items: list["LibItem"]):
        """Process items that have been removed from the library.

        Args:
            items: Any items that existed in the library prior to the current session,
                but have now been removed from the library.
        """

    @staticmethod
    @moe.hookspec
    def process_changed_items(items: list["LibItem"]):
        """Process items in the library that were changed in some way.

        Args:
            items: Any changed items that existed in the library prior to the current
                session.

        Important:
            Any changes made to the items will be lost.

        See Also:
            The :meth:`edit_changed_items` hook for editing items before their values
            are finalized.
        """

    @staticmethod
    @moe.hookspec
    def process_new_items(items: list["LibItem"]):
        """Process new items in the library.

        Args:
            items: Any items being added to the library for the first time.

        Important:
            Any changes made to the items will be lost.

        See Also:
            The :meth:`edit_new_items` hook for editing items before their values are
            finalized.
        """


@moe.hookimpl
def add_hooks(pm: pluggy.manager.PluginManager):
    """Registers `add` hookspecs to Moe."""
    from moe.library.lib_item import Hooks

    pm.add_hookspecs(Hooks)


@moe.hookimpl
def register_sa_event_listeners(session: sqlalchemy.orm.Session):
    """Registers event listeners for editing and processing new items."""
    sqlalchemy.event.listen(
        session,
        "before_flush",
        _edit_before_flush,
    )
    sqlalchemy.event.listen(
        session,
        "after_flush",
        _process_after_flush,
    )


def _edit_before_flush(
    session: sqlalchemy.orm.Session,
    flush_context: sqlalchemy.orm.UOWTransaction,
    instances,
):
    """Runs the ``edit_*_items`` hook specifications before items are flushed.

    This uses the sqlalchemy ORM event ``before_flush`` in the background to determine
    the time of execution and to provide any new, changed, or deleted items to the hook
    implementations.

    Args:
        session: Current db session.
        flush_context: sqlalchemy obj which handles the details of the flush.
        instances: Objects passed to the `session.flush()` method (deprecated).

    See Also:
        `SQLAlchemy docs on state management <https://docs.sqlalchemy.org/en/14/orm/session_state_management.html>`_
    """  # noqa: E501
    changed_items = []
    for dirty_item in session.dirty:
        if session.is_modified(dirty_item) and isinstance(dirty_item, LibItem):
            changed_items.append(dirty_item)
    if changed_items:
        log.debug(f"Editing changed items. [{changed_items=!r}]")
        config.CONFIG.pm.hook.edit_changed_items(items=changed_items)
        log.debug(f"Edited changed items. [{changed_items=!r}]")

    new_items = []
    for new_item in session.new:
        if isinstance(new_item, LibItem):
            new_items.append(new_item)
    if new_items:
        log.debug(f"Editing new items. [{new_items=!r}]")
        config.CONFIG.pm.hook.edit_new_items(items=new_items)
        log.debug(f"Edited new items. [{new_items=!r}]")


def _process_after_flush(
    session: sqlalchemy.orm.Session,
    flush_context: sqlalchemy.orm.UOWTransaction,
):
    """Runs the ``process_*_items`` hook specifications after items are flushed.

    This uses the sqlalchemy ORM event ``after_flush`` in the background to determine
    the time of execution and to provide any new, changed, or deleted items to the hook
    implementations.

    Args:
        session: Current db session.
        flush_context: sqlalchemy obj which handles the details of the flush.

    See Also:
        `SQLAlchemy docs on state management <https://docs.sqlalchemy.org/en/14/orm/session_state_management.html>`_
    """  # noqa: E501
    changed_items = []
    for dirty_item in session.dirty:
        if session.is_modified(dirty_item) and isinstance(dirty_item, LibItem):
            changed_items.append(dirty_item)
    if changed_items:
        log.debug(f"Processing changed items. [{changed_items=!r}]")
        config.CONFIG.pm.hook.process_changed_items(items=changed_items)
        log.debug(f"Processed changed items. [{changed_items=!r}]")

    new_items = []
    for new_item in session.new:
        if isinstance(new_item, LibItem):
            new_items.append(new_item)
    if new_items:
        log.debug(f"Processing new items. [{new_items=!r}]")
        config.CONFIG.pm.hook.process_new_items(items=new_items)
        log.debug(f"Processed new items. [{new_items=!r}]")

    removed_items = []
    for removed_item in session.deleted:
        if isinstance(removed_item, LibItem):
            removed_items.append(removed_item)
    if removed_items:
        log.debug(f"Processing removed items. [{removed_items=!r}]")
        config.CONFIG.pm.hook.process_removed_items(items=removed_items)
        log.debug(f"Processed removed items. [{removed_items=!r}]")


class LibItem:
    """Base class for library items i.e. Albums, Extras, and Tracks."""

    _custom_fields_set = None

    @property
    def path(self) -> Path:
        """A library item's filesystem path."""
        raise NotImplementedError

    @property
    def custom_fields(self) -> set[str]:
        """Returns the custom fields of an item."""
        if self._custom_fields_set is None:
            object.__setattr__(
                self, "_custom_fields_set", set(self._get_default_custom_fields())
            )

        assert self._custom_fields_set is not None
        return self._custom_fields_set

    def _get_default_custom_fields(self) -> dict[str, Any]:
        """Returns the default custom fields of an item."""
        raise NotImplementedError

    @property
    def fields(self) -> set[str]:
        """Returns the editable fields of an item."""
        raise NotImplementedError

    def is_unique(self, other: "LibItem") -> bool:
        """Returns whether an item is unique in the library from ``other``."""
        raise NotImplementedError

    def __getattr__(self, name: str):
        """See if ``name`` is a custom field."""
        if name in self.custom_fields:
            return self._custom_fields[name]
        else:
            raise AttributeError from None

    def __setattr__(self, name, value):
        """Set custom custom_fields if a valid key."""
        if name in self.custom_fields:
            self._custom_fields[name] = value
        else:
            super().__setattr__(name, value)

    def __lt__(self, other):
        """Library items implement the `lt` magic method to allow sorting."""
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
