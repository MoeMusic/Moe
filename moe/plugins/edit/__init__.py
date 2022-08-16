"""Edits music in the library."""

import pluggy

import moe
from moe.config import Config

from . import edit_cli, edit_core
from .edit_core import *

__all__ = []
__all__.extend(edit_core.__all__)


@moe.hookimpl
def plugin_registration(config: Config):
    """Only register the cli sub-plugin if the cli is enabled."""
    config.plugin_manager.register(edit_core, "edit_core")
    if config.plugin_manager.has_plugin("cli"):
        config.plugin_manager.register(edit_cli, "edit_cli")
