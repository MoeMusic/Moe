"""Alters the location of items in your library."""

import pluggy

import moe
from moe.config import Config

from . import move_cli, move_core
from .move_core import *

__all__ = []
__all__.extend(move_core.__all__)


@moe.hookimpl
def plugin_registration(config: Config):
    """Only register the cli sub-plugin if the cli is enabled."""
    config.pm.register(move_core, "move_core")
    if config.pm.has_plugin("cli"):
        config.pm.register(move_cli, "move_cli")
