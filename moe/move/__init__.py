"""Alters the location of items in your library."""

import moe
from moe import config

from . import move_cli, move_core
from .move_core import *  # noqa: F403

__all__ = []
__all__.extend(move_core.__all__)


@moe.hookimpl
def plugin_registration() -> None:
    """Only register the cli sub-plugin if the cli is enabled."""
    config.CONFIG.pm.register(move_core, "move_core")
    if config.CONFIG.pm.has_plugin("cli"):
        config.CONFIG.pm.register(move_cli, "move_cli")
