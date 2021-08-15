"""Core api for removing items from the library."""

import logging

from sqlalchemy.orm.session import Session

from moe.library.lib_item import LibItem

__all__ = ["remove_item"]

log = logging.getLogger("moe.remove")


def remove_item(item: LibItem, session: Session):
    """Removes an item from the library."""
    log.info(f"Removing '{item}' from the library.")
    session.delete(item)
