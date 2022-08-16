"""Musicbrainz integration plugin.

See Also:
    * https://musicbrainz.org/doc/MusicBrainz_API/
    * https://python-musicbrainzngs.readthedocs.io/en/latest/api/
"""

import pluggy

import moe
from moe.config import Config

from . import mb_cli, mb_core
from .mb_core import *

__all__ = []
__all__.extend(mb_core.__all__)


@moe.hookimpl
def plugin_registration(config: Config):
    """Only register the cli sub-plugin if the cli is enabled."""
    config.plugin_manager.register(mb_core, "musicbrainz_core")
    if config.plugin_manager.has_plugin("cli"):
        config.plugin_manager.register(mb_cli, "musicbrainz_cli")
