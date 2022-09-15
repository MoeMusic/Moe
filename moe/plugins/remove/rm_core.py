"""Core api for removing items from the library."""

import logging

from moe.config import Config, MoeSession
from moe.library.lib_item import LibItem

__all__ = ["remove_item"]

log = logging.getLogger("moe.remove")


def remove_item(config: Config, item: LibItem):
    """Removes an item from the library."""
    log.debug(f"Removing item from the library. [{item=!r}]")

    session = MoeSession()
    session.delete(item)

    log.info(f"Removed item from the library. [{item=!r}]")
