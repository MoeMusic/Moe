"""Sync metadata from external sources."""

import logging

import moe
from moe import config
from moe.library import LibItem

log = logging.getLogger("moe.sync")

__all__ = ["sync_item"]


class Hooks:
    """Sync plugin hook specifications."""

    @staticmethod
    @moe.hookspec
    def sync_metadata(item: LibItem):
        """Implement specific metadata syncing for ``item``."""


def sync_item(item: LibItem):
    """Syncs metadata from external sources and merges changes into ``item``."""
    log.debug(f"Syncing metadata. [{item=!r}]")

    config.CONFIG.pm.hook.sync_metadata(item=item)

    log.debug(f"Synced metadata. [{item=!r}]")
