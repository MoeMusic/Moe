"""Shared functionality between library albums, extras, and tracks."""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any, Generic, TypeVar

import sqlalchemy
import sqlalchemy.event
import sqlalchemy.orm
import sqlalchemy.types
from sqlalchemy import JSON, Integer
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm.session import Session

import moe
from moe import config

if sys.version_info < (3, 11):
    from typing_extensions import Self
else:
    from typing import Self

if TYPE_CHECKING:
    from collections.abc import Iterable

    import pluggy

__all__ = ["LibItem", "LibraryError", "MetaLibItem"]

log = logging.getLogger("moe.lib_item")

T = TypeVar("T", bound="MetaLibItem")


class SABase(DeclarativeBase):
    pass


class LibraryError(Exception):
    """General library error."""


class Hooks:
    """General usage library item hooks."""

    @staticmethod
    @moe.hookspec
    def edit_changed_items(session: Session, items: list[LibItem]) -> None:
        """Edit items in the library that were changed in some way.

        Args:
            session: Library db session.
            items: Any changed items that existed in the library prior to the current
                session.

        See Also:
            The :meth:`process_changed_items` hook for processing items with finalized
            values.
        """

    @staticmethod
    @moe.hookspec
    def edit_new_items(session: Session, items: list[LibItem]) -> None:
        """Edit new items in the library.

        Args:
            session: Library db session.
            items: Any items being added to the library for the first time.

        See Also:
            The :meth:`process_new_items` hook for processing items with finalized
            values.
        """

    @staticmethod
    @moe.hookspec
    def process_removed_items(session: Session, items: list[LibItem]) -> None:
        """Process items that have been removed from the library.

        Args:
            session: Library db session.
            items: Any items that existed in the library prior to the current session,
                but have now been removed from the library.
        """

    @staticmethod
    @moe.hookspec
    def process_changed_items(session: Session, items: list[LibItem]) -> None:
        """Process items in the library that were changed in some way.

        Args:
            session: Library db session.
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
    def process_new_items(session: Session, items: list[LibItem]) -> None:
        """Process new items in the library.

        Args:
            session: Library db session.
            items: Any items being added to the library for the first time.

        Important:
            Any changes made to the items will be lost.

        See Also:
            The :meth:`edit_new_items` hook for editing items before their values are
            finalized.
        """


@moe.hookimpl
def add_hooks(pm: pluggy._manager.PluginManager) -> None:
    """Registers `add` hookspecs to Moe."""
    from moe.library.lib_item import Hooks  # noqa: PLC0415

    pm.add_hookspecs(Hooks)


@moe.hookimpl
def register_sa_event_listeners() -> None:
    """Registers event listeners for editing and processing new items."""
    sqlalchemy.event.listen(
        Session,
        "before_flush",
        _edit_before_flush,
    )
    sqlalchemy.event.listen(
        Session,
        "after_flush",
        _process_after_flush,
    )


def _edit_before_flush(
    session: sqlalchemy.orm.Session,
    flush_context: sqlalchemy.orm.UOWTransaction,  # noqa: ARG001
    instances: Iterable[Any],  # noqa: ARG001
) -> None:
    """Runs the ``edit_*_items`` hook specifications before items are flushed.

    This uses the sqlalchemy ORM event ``before_flush`` in the background to determine
    the time of execution and to provide any new, changed, or deleted items to the hook
    implementations.

    Args:
        session: Current db session.
        flush_context: sqlalchemy obj which handles the details of the flush.
        instances: Objects passed to the `session.flush()` method (deprecated).

    See Also:
        `SQLAlchemy docs on state management <https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#state-management>`_
    """
    changed_items = [
        dirty_item
        for dirty_item in session.dirty
        if session.is_modified(dirty_item) and isinstance(dirty_item, LibItem)
    ]
    if changed_items:
        log.debug(f"Editing changed items. [{changed_items=}]")
        config.CONFIG.pm.hook.edit_changed_items(session=session, items=changed_items)
        log.debug(f"Edited changed items. [{changed_items=}]")

    new_items = [new_item for new_item in session.new if isinstance(new_item, LibItem)]
    if new_items:
        log.debug(f"Editing new items. [{new_items=}]")
        config.CONFIG.pm.hook.edit_new_items(session=session, items=new_items)
        log.debug(f"Edited new items. [{new_items=}]")


def _process_after_flush(
    session: sqlalchemy.orm.Session,
    flush_context: sqlalchemy.orm.UOWTransaction,  # noqa: ARG001
) -> None:
    """Runs the ``process_*_items`` hook specifications after items are flushed.

    This uses the sqlalchemy ORM event ``after_flush`` in the background to determine
    the time of execution and to provide any new, changed, or deleted items to the hook
    implementations.

    Args:
        session: Current db session.
        flush_context: sqlalchemy obj which handles the details of the flush.

    See Also:
        `SQLAlchemy docs on state management <https://docs.sqlalchemy.org/en/20/orm/session_state_management.html#state-management>`_
    """
    changed_items = [
        dirty_item
        for dirty_item in session.dirty
        if session.is_modified(dirty_item) and isinstance(dirty_item, LibItem)
    ]
    if changed_items:
        log.debug(f"Processing changed items. [{changed_items=}]")
        config.CONFIG.pm.hook.process_changed_items(
            session=session, items=changed_items
        )
        log.debug(f"Processed changed items. [{changed_items=}]")

    new_items = [new_item for new_item in session.new if isinstance(new_item, LibItem)]
    if new_items:
        log.debug(f"Processing new items. [{new_items=}]")
        config.CONFIG.pm.hook.process_new_items(session=session, items=new_items)
        log.debug(f"Processed new items. [{new_items=}]")

    removed_items = [
        removed_item
        for removed_item in session.deleted
        if isinstance(removed_item, LibItem)
    ]
    if removed_items:
        log.debug(f"Processing removed items. [{removed_items=}]")
        config.CONFIG.pm.hook.process_removed_items(
            session=session, items=removed_items
        )
        log.debug(f"Processed removed items. [{removed_items=}]")


class PathType(sqlalchemy.types.TypeDecorator):
    """A custom type for paths for database storage.

    Normally, paths are Path type, but we can't store that in the database,
    so we normalize the paths first to strings for database storage. Paths are stored as
    relative paths from ``library_path`` in the config.
    """

    impl = sqlalchemy.types.String  # sql type
    cache_ok = True  # expected to produce same bind/result behavior and sql generation

    library_path: Path  # will be set on config initialization

    def process_bind_param(
        self,
        value: Path | None,
        dialect: sqlalchemy.engine.interfaces.Dialect,  # noqa: ARG002
    ) -> str | None:
        """Normalize pathlib paths as strings for the database.

        Args:
            value: Inbound path to the db.
            dialect: Database in use.

        Returns:
            Relative path from ``library_path`` if possible, otherwise stores the
            absolute path.
        """
        if not value:
            return None

        try:
            return str(value.relative_to(self.library_path))
        except ValueError:
            return str(value.resolve())

    def process_result_value(
        self,
        value: str | None,
        dialect: sqlalchemy.engine.interfaces.Dialect,  # noqa: ARG002
    ) -> Path | None:
        """Convert the path back to a Path object on the way out."""
        path_str = value

        if path_str is None:
            return None

        return Path(self.library_path / path_str)


class SetType(sqlalchemy.types.TypeDecorator):
    """A custom type for storing sets as json in a database."""

    impl = sqlalchemy.types.JSON  # sql type
    cache_ok = True  # expected to produce same bind/result behavior and sql generation

    def process_bind_param(
        self,
        value: set | None,
        dialect: sqlalchemy.engine.interfaces.Dialect,  # noqa: ARG002
    ) -> list | None:
        """Convert the set to a list so it's valid json."""
        json_set = value

        if json_set is not None:
            return list(json_set)
        return None

    def process_result_value(
        self,
        value: list | None,
        dialect: sqlalchemy.engine.interfaces.Dialect,  # noqa: ARG002
    ) -> set | None:
        """Convert the list in the db back to a set."""
        json_list = value

        if json_list is not None:
            return set(json_list)
        return None


class MetaLibItem(Generic[T]):
    """Base class for MetaTrack and MetaAlbum objects representing metadata-only.

    These objects do not exist on the filesystem nor in the library.
    """

    custom: dict[str, Any]

    def _get_default_custom_fields(self) -> dict[str, Any]:
        """Returns the default custom fields of an item."""
        raise NotImplementedError

    @property
    def fields(self) -> set[str]:
        """Returns the editable fields of an item."""
        raise NotImplementedError

    def merge(self: T, other: T, overwrite: bool = False) -> None:  # noqa: FBT001, FBT002, PYI019
        """Merges another item into this one."""
        raise NotImplementedError

    def __lt__(self: T, other: T) -> bool:  # noqa: PYI019
        """Library items implement the `lt` magic method to allow sorting."""
        raise NotImplementedError


class LibItem(MetaLibItem):
    """Base class for library items i.e. Albums, Extras, and Tracks."""

    _id: Mapped[int] = mapped_column(Integer, primary_key=True)
    path: Mapped[Path] = mapped_column(PathType, nullable=False, unique=True)
    custom: Mapped[dict[str, Any]] = mapped_column(  # type: ignore[reportIncompatibleVariableOverride]
        MutableDict.as_mutable(JSON(none_as_null=True)), default="{}", nullable=False
    )

    def is_unique(self, other: Self) -> bool:
        """Returns whether an item is unique in the library from ``other``."""
        raise NotImplementedError
