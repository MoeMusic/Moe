"""Handles duplicate detection and resolution in the library."""

import logging

import moe
from moe.config import Config

from . import dup_cli, dup_core
from .dup_core import *

__all__ = []
__all__.extend(dup_core.__all__)

log = logging.getLogger("moe.dup")


@moe.hookimpl
def plugin_registration(config: Config):
    """Only register the cli sub-plugin if the cli is enabled."""
    config.plugin_manager.register(dup_core, "dup_core")
    if config.plugin_manager.has_plugin("cli"):
        config.plugin_manager.register(dup_cli, "dup_cli")
