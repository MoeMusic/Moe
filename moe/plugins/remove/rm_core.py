"""Core api for removing items from the library."""

import logging

from moe.config import MoeSession
from moe.library.lib_item import LibItem

__all__ = ["remove_item"]

log = logging.getLogger("moe.remove")


def remove_item(item: LibItem):
    """Removes an item from the library."""
    session = MoeSession()

    log.info(f"Removing '{item}' from the library.")
    session.delete(item)
