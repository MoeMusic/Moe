"""Syncs library metadata with external sources."""

import moe
from moe import config

from . import sync_cli, sync_core
from .sync_core import *

__all__ = []
__all__.extend(sync_core.__all__)


@moe.hookimpl
def plugin_registration():
    """Only register the cli sub-plugin if the cli is enabled."""
    config.CONFIG.pm.register(sync_core, "sync_core")
    if config.CONFIG.pm.has_plugin("cli"):
        config.CONFIG.pm.register(sync_cli, "sync_cli")
