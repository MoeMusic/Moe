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
    config.pm.register(dup_core, "dup_core")
    if config.pm.has_plugin("cli"):
        config.pm.register(dup_cli, "dup_cli")
