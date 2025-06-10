"""Imports metadata for music in your library."""

import sys

import dynaconf
import dynaconf.base

import moe
from moe import config

from . import import_cli, import_core
from .import_cli import *
from .import_core import *

__all__ = []
__all__.extend(import_cli.__all__)
__all__.extend(import_core.__all__)


@moe.hookimpl
def add_config_validator(settings: dynaconf.base.LazySettings):
    """Add configuration validators for the import plugin."""
    settings.validators.register(  # type: ignore
        dynaconf.Validator("import.max_candidates", default=5, gte=1)
    )


@moe.hookimpl
def plugin_registration():
    """Only register the cli sub-plugin if the cli is enabled."""
    config.CONFIG.pm.register(import_core, "import_core")
    if config.CONFIG.pm.has_plugin("cli"):
        config.CONFIG.pm.register(import_cli, "import_cli")
