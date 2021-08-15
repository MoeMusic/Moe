"""Edits music in the library.

Plugin contents:
    ``edit_cli.py``: Adds the ``edit`` command to the cli.
    ``edit_core.py`` : API interface for editing the library.

Note:
    This plugin is enabled by default.
"""

import pluggy

import moe
from moe.config import Config

from . import edit_cli, edit_core
from .edit_core import *

__all__ = []
__all__.extend(edit_core.__all__)  # noqa: WPS609


@moe.hookimpl
def plugin_registration(config: Config, plugin_manager: pluggy.manager.PluginManager):
    """Only register the cli sub-plugin if the cli is enabled."""
    plugin_manager.register(edit_core, "edit_core")
    if "cli" in config.plugins:
        plugin_manager.register(edit_cli, "edit_cli")
