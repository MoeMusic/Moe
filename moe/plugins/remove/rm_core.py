"""Core api for removing items from the library."""

import logging

import pluggy

import moe
from moe.config import Config, MoeSession
from moe.library.lib_item import LibItem

__all__ = ["remove_item"]

log = logging.getLogger("moe.remove")


class Hooks:
    """Remove plugin hook specifications."""

    @staticmethod
    @moe.hookspec
    def post_remove(config: Config, item: LibItem):
        """Provides an item after it has been removed from the library."""


@moe.hookimpl
def add_hooks(plugin_manager: pluggy.manager.PluginManager):
    """Registers `add` hookspecs to Moe."""
    from moe.plugins.remove.rm_core import Hooks

    plugin_manager.add_hookspecs(Hooks)


def remove_item(config: Config, item: LibItem):
    """Removes an item from the library."""
    session = MoeSession()

    log.info(f"Removing '{item}' from the library.")
    session.delete(item)
    config.plugin_manager.hook.post_remove(config=config, item=item)
