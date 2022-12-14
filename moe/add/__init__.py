"""Adds music to the library."""

import moe
from moe import config

from . import add_cli, add_core
from .add_core import *

__all__ = []
__all__.extend(add_core.__all__)


@moe.hookimpl
def plugin_registration():
    """Only register the cli sub-plugin if the cli is enabled."""
    config.CONFIG.pm.register(add_core, "add_core")
    if config.CONFIG.pm.has_plugin("cli"):
        config.CONFIG.pm.register(add_cli, "add_cli")
