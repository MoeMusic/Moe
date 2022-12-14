"""Edits music in the library."""

import pluggy

import moe
from moe import config

from . import edit_cli, edit_core
from .edit_core import *

__all__ = []
__all__.extend(edit_core.__all__)


@moe.hookimpl
def plugin_registration():
    """Only register the cli sub-plugin if the cli is enabled."""
    config.CONFIG.pm.register(edit_core, "edit_core")
    if config.CONFIG.pm.has_plugin("cli"):
        config.CONFIG.pm.register(edit_cli, "edit_cli")
