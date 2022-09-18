"""Adds music to the library."""

import moe
from moe.config import Config

from . import add_cli, add_core
from .add_core import *

__all__ = []
__all__.extend(add_core.__all__)


@moe.hookimpl
def plugin_registration(config: Config):
    """Only register the cli sub-plugin if the cli is enabled."""
    config.pm.register(add_core, "add_core")
    if config.pm.has_plugin("cli"):
        config.pm.register(add_cli, "add_cli")
