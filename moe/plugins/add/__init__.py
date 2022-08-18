"""Adds music to the library."""

import moe
from moe.config import Config
from moe.plugins.add.add_core import add, match
from moe.plugins.add.add_core.add import *
from moe.plugins.add.add_core.match import *

from . import add_cli

__all__ = []
__all__.extend(add.__all__)
__all__.extend(match.__all__)


@moe.hookimpl
def plugin_registration(config: Config):
    """Only register the cli sub-plugin if the cli is enabled."""
    config.plugin_manager.register(add, "add_core")
    if config.plugin_manager.has_plugin("cli"):
        config.plugin_manager.register(add_cli, "add_cli")
