"""Adds music to the library.

This module provides the main entry point into the add process via ``add_item()``.
"""

import logging

import pluggy

import moe
from moe.config import Config, MoeSession
from moe.library.album import Album
from moe.library.extra import Extra
from moe.library.lib_item import LibItem
from moe.library.track import Track

__all__ = ["AddAbortError", "AddError", "add_item"]

log = logging.getLogger("moe.add")


class Hooks:
    """Add plugin hook specifications."""

    @staticmethod
    @moe.hookspec
    def pre_add(config: Config, item: LibItem):
        """Provides an item prior to it being added to the library.

        Use this hook if you wish to change the item's metadata. You must also ensure
        there will be no conflicts with existing items in the database if you are
        altering any applicable, i.e. unique, fields.

        Args:
            config: Moe config.
            item: Library item being added.

        Note:
            Any UI application should have a way of detecting and resolving duplicate
            items prior to them being added to the database. You may consider
            implementing a ``hookwrapper`` to run conflict resolution code after the
            ``pre_add`` hook is complete, but before the item has been added to the db.

        See Also:
            * The :meth:`post_add` hook for any post-processing operations.
            * The :meth:`~moe.config.Hooks.edit_new_items` hook.
              The difference between them is that the :meth:`pre_add` hook will only
              operate on an `add` operation, while the
              :meth:`~moe.config.Hooks.edit_new_items` hook will run anytime an item is
              changed or added.
            * `Pluggy hook wrapper documention
              <https://pluggy.readthedocs.io/en/stable/#wrappers>`_
            * :meth:`~moe.library.lib_item.LibItem.get_existing` for detecting duplicate
              items.
        """

    @staticmethod
    @moe.hookspec
    def post_add(config: Config, item: LibItem):
        """Provides an item after it has been added to the library.

        Use this hook if you want to operate on an item after its metadata has been set.

        Args:
            config: Moe config.
            item: Library item added.

        See Also:
            * The :meth:`pre_add` hook if you wish to alter item metadata.
            * The :meth:`~moe.config.Hooks.process_new_items` hook.
              The difference between them is that the :meth:`post_add` hook will only
              operate on an `add` operation, while the
              :meth:`~moe.config.Hooks.process_new_items` hook will run anytime an item
              is changed or added.
        """


@moe.hookimpl
def add_hooks(plugin_manager: pluggy.manager.PluginManager):
    """Registers `add` hookspecs to Moe."""
    from moe.plugins.add.add_core import Hooks

    plugin_manager.add_hookspecs(Hooks)


class AddError(Exception):
    """Error adding an item to the library."""


class AddAbortError(Exception):
    """Add process has been aborted by the user."""


def add_item(config: Config, item: LibItem):
    """Adds a LibItem to the library.

    Args:
        config: Moe config.
        item: Item to be added.

    Raises:
        AddError: Unable to add the item to the library.
    """
    log.debug(f"Adding item to the library. [{item=!r}]")
    session = MoeSession()

    config.plugin_manager.hook.pre_add(config=config, item=item)

    _check_db_dups(item)
    item = session.merge(item)
    log.info(f"Item added to the library. [{item=!r}]")

    config.plugin_manager.hook.post_add(config=config, item=item)


def _check_db_dups(item: LibItem):
    """Checks for any duplicates in the library for the given item and its relatives.

    Args:
        item: Library item to check.

    Raises:
        AddError: Duplicate found.
    """
    if item.get_existing():
        raise AddError(f"Duplicate item cannot be added to the db. [{item=!r}]")
    elif isinstance(item, (Extra, Track)):
        if item.album_obj.get_existing():
            raise AddError(
                f"Item has duplicate album in the db. [album={item.album_obj!r}]"
            )
    elif isinstance(item, Album):
        for track in item.tracks:
            if track.get_existing():
                raise AddError(f"Album has duplicate track in the db. [{track=!r}]")
        for extra in item.extras:
            if extra.get_existing():
                raise AddError(f"Album has duplicate extra in the db. [{extra=!r}]")
