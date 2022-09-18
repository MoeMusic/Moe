"""Handles duplicate detection and resolution in the library."""

import logging

import moe
from moe import config

from . import dup_cli, dup_core
from .dup_core import *

__all__ = []
__all__.extend(dup_core.__all__)

log = logging.getLogger("moe.dup")


@moe.hookimpl
def plugin_registration():
    """Only register the cli sub-plugin if the cli is enabled."""
    config.CONFIG.pm.register(dup_core, "dup_core")
    if config.CONFIG.pm.has_plugin("cli"):
        config.CONFIG.pm.register(dup_cli, "dup_cli")
