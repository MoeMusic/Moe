"""Reads item files and updates moe with any changes."""

import moe
from moe import config

from . import read_cli, read_core
from .read_core import *

__all__ = []
__all__.extend(read_core.__all__)


@moe.hookimpl
def plugin_registration():
    """Only register the cli sub-plugin if the cli is enabled."""
    config.CONFIG.pm.register(read_core, "read_core")
    if config.CONFIG.pm.has_plugin("cli"):
        config.CONFIG.pm.register(read_cli, "read_cli")
