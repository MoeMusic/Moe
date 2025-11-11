"""Core api for read items from the library."""

import logging

from moe.library import Album, LibItem, MergeStrategy, Track

__all__ = ["read_item"]

log = logging.getLogger("moe.read")


def read_item(item: LibItem) -> None:
    """Reads an item's file and updates the item with any changes.

    Args:
        item: Item to update.

    Raises:
        FileNotFoundError: Item's path doesn't exist.
    """
    log.debug(f"Reading item's file for changes. [{item=}]")

    if not item.path.exists():
        err_msg = f"Item's path does not exist. [path={item.path!r}]"
        raise FileNotFoundError(err_msg)

    if isinstance(item, Track):
        item.merge(Track.from_file(item.path), merge_strategy=MergeStrategy.OVERWRITE)
    elif isinstance(item, Album):
        item.merge(Album.from_dir(item.path), merge_strategy=MergeStrategy.OVERWRITE)

    log.info(f"Updated item from filesystem. [{item=!s}]")
