"""Imports metadata for music in your library."""

import moe
from moe import config

from . import import_cli, import_core
from .import_cli import *  # noqa: F403
from .import_core import *  # noqa: F403

__all__ = []
__all__.extend(import_cli.__all__)
__all__.extend(import_core.__all__)


@moe.hookimpl
def plugin_registration() -> None:
    """Only register the cli sub-plugin if the cli is enabled."""
    config.CONFIG.pm.register(import_core, "import_core")
    if config.CONFIG.pm.has_plugin("cli"):
        config.CONFIG.pm.register(import_cli, "import_cli")
