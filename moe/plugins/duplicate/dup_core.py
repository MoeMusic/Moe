"""Detect and handle duplicates in the library."""

import logging
from typing import Optional, cast

import sqlalchemy

import moe
from moe import config
from moe.library.album import Album
from moe.library.lib_item import LibItem
from moe.query import query

__all__ = ["get_duplicates"]

log = logging.getLogger("moe.dup")


class DuplicateError(Exception):
    """Duplicate items could not be resolved."""


class Hooks:
    """Duplicate plugin hook specifications."""

    @staticmethod
    @moe.hookspec
    def resolve_dup_items(item_a: LibItem, item_b: LibItem):
        """Resolve two duplicate items.

        A resolution should come in one of two forms:
        1. The field(s) triggering the duplicate detection is altered on one or both
           of the items so that they are no longer duplicates.
        2. One of the items is removed from the library entirely using
           :meth:`~moe.plugins.remove.remove_item`.

        Important:
            Duplicates are determined by each item's
            :meth:`~moe.library.lib_item.LibItem.is_unique` method. This behavior can be
            extended by the various ``is_unique_*`` hooks.

        Note:
            As a plugin that may have introduced new ``unique`` constraints via one of
            the ``is_unique_*`` hooks, you only need to be concerned about resolving
            that particular constraint. You may also just rely on the default duplicate
            resolution method of Moe, which depending on the UI in use, may be
            sufficient for your plugin's needs. For example, the CLI will offer a
            'duplicate resolution' prompt to the user anytime a duplicate is detected.
            This hook allows you to implement your own duplicate resolution methods in
            addition to what's offered by default.

        Args:
            item_a: First item.
            item_b: Second item.

        See Also:
            * The :meth:`~moe.library.album.Hooks.is_unique_album` hook.
            * The :meth:`~moe.library.extra.Hooks.is_unique_extra` hook.
            * The :meth:`~moe.library.track.Hooks.is_unique_track` hook.
        """


@moe.hookimpl(hookwrapper=True)
def edit_changed_items(items: list[LibItem]):
    """Check for and resolve duplicates when items are edited."""
    yield  # run all `edit_changed_items` hook implementations
    resolve_duplicates(items)


@moe.hookimpl(hookwrapper=True)
def edit_new_items(items: list[LibItem]):
    """Check for and resolve duplicates when items are added to the library."""
    yield  # run all `edit_new_items` hook implementations
    resolve_duplicates(items)


def resolve_duplicates(items: list[LibItem]):
    """Search for and resolve any duplicates of items in ``items``."""
    log.debug(f"Checking for duplicate items. [{items=!r}]")

    albums = [item for item in items if isinstance(item, Album)]
    items = cast(list[LibItem], albums + items)  # resolve albums first
    resolved_items = []
    for item in items:
        dup_items = get_duplicates(item, items)
        dup_items += get_duplicates(item)

        for dup_item in dup_items:
            if dup_item in resolved_items:
                continue

            log.debug(
                f"Resolving duplicate items. [item_a={item!r}, item_b={dup_item!r}]"
            )
            config.CONFIG.pm.hook.resolve_dup_items(item_a=item, item_b=dup_item)
            if (
                not item.is_unique(dup_item)
                and not _is_removed(item)
                and not _is_removed(dup_item)
            ):
                raise DuplicateError(
                    "Duplicate items could not be resolved. "
                    f"[item_a={item!r}, item_b={dup_item!r}]"
                )

        if dup_items:
            resolved_items.append(item)

    if resolved_items:
        log.debug(f"Resolved duplicate items. [{resolved_items=!r}]")
    else:
        log.debug("No duplicate items found.")


def _is_removed(item):
    """Check whether or not an item is removed from the library."""
    insp = sqlalchemy.inspect(item)

    if insp.deleted or insp.transient:
        return True

    print(f"{item!r}")
    print(f"pending? {insp.pending}")
    print(f"persistent? {insp.persistent}")
    print(f"detached? {insp.detached}")
    return False


def get_duplicates(
    item: LibItem, others: Optional[list[LibItem]] = None
) -> list[LibItem]:
    """Returns items considered duplicates of ``item``.

    Args:
        item: Library item to get duplicates of.
        others: Items to compare against. If not given, will query the database
            and compare against all items in the library.

    Returns:
        Any items considered a duplicate as defined by
        :meth:`~moe.library.lib_item.LibItem.is_unique`.
    """
    dup_items = []
    if not others:
        others = query("*", type(item).__name__.lower())

    for other in others:
        if (
            item is not other
            and type(item) == type(other)
            and not item.is_unique(other)
        ):
            dup_items.append(other)

    return dup_items
