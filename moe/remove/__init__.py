"""Removes music from the library."""

import moe
from moe import config

from . import rm_cli, rm_core
from .rm_core import *  # noqa: F403

__all__ = []
__all__.extend(rm_core.__all__)


@moe.hookimpl
def plugin_registration() -> None:
    """Only register the cli sub-plugin if the cli is enabled."""
    config.CONFIG.pm.register(rm_core, "remove_core")
    if config.CONFIG.pm.has_plugin("cli"):
        config.CONFIG.pm.register(rm_cli, "remove_cli")
