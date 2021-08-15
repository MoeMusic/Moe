"""Imports metadata."""

import sys

import pluggy

import moe
from moe.config import Config

from . import import_cli, import_core
from .import_cli import *
from .import_core import *

__all__ = []
__all__.extend(import_cli.__all__)  # noqa: WPS609
__all__.extend(import_core.__all__)  # noqa: WPS609


@moe.hookimpl
def plugin_registration(config: Config, plugin_manager: pluggy.manager.PluginManager):
    """Only register the cli sub-plugin if the cli is enabled."""
    plugin_manager.register(import_core, "import_core")
    if "cli" in config.plugins:
        plugin_manager.register(import_cli, "import_cli")

    # re-register under the "import" name instead of "moe_import"
    plugin_manager.unregister(name="moe_import")
    plugin_manager.register(sys.modules[__name__], "import")
