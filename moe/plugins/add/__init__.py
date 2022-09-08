"""Adds music to the library."""

import logging

import moe
from moe.config import Config

from . import add_cli, add_core
from .add_core import *

__all__ = []
__all__.extend(add_core.__all__)

log = logging.getLogger("moe.add")


@moe.hookimpl
def plugin_registration(config: Config):
    """Only register the cli sub-plugin if the cli is enabled."""
    config.plugin_manager.register(add_core, "add_core")
    if config.plugin_manager.has_plugin("cli"):
        config.plugin_manager.register(add_cli, "add_cli")

        if not config.plugin_manager.has_plugin("remove"):
            log.warning(
                "Duplicate resolution when adding an item to the library requires the"
                " 'remove' plugin to work properly."
            )
