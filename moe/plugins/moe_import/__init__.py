"""Imports metadata for music in your library."""

import sys

import moe
from moe.config import Config

from . import import_cli, import_core
from .import_cli import *
from .import_core import *

__all__ = []
__all__.extend(import_cli.__all__)
__all__.extend(import_core.__all__)


@moe.hookimpl
def plugin_registration(config: Config):
    """Only register the cli sub-plugin if the cli is enabled."""
    config.plugin_manager.register(import_core, "import_core")
    if config.plugin_manager.has_plugin("cli"):
        config.plugin_manager.register(import_cli, "import_cli")

    # re-register under the "import" name instead of "moe_import"
    config.plugin_manager.unregister(name="moe_import")
    config.plugin_manager.register(sys.modules[__name__], "import")
