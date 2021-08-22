"""Removes music in the library.

Plugin contents:
    ``rm_cli.py``: Adds the ``remove`` command to the cli.
    ``rm_core.py`` : API interface for removing items.

Note:
    This plugin is enabled by default.
"""

import pluggy

import moe
from moe.config import Config

from . import rm_cli, rm_core
from .rm_core import *

__all__ = []
__all__.extend(rm_core.__all__)  # noqa: WPS609


@moe.hookimpl
def plugin_registration(config: Config):
    """Only register the cli sub-plugin if the cli is enabled."""
    config.plugin_manager.register(rm_core, "remove_core")
    if config.plugin_manager.has_plugin("cli"):
        config.plugin_manager.register(rm_cli, "remove_cli")
