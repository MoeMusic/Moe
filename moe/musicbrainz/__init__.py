"""Musicbrainz integration plugin.

See Also:
    * https://musicbrainz.org/doc/MusicBrainz_API/
    * https://python-musicbrainzngs.readthedocs.io/en/latest/api/
"""

import pluggy

import moe
from moe import config

from . import mb_cli, mb_core
from .mb_core import *

__all__ = []
__all__.extend(mb_core.__all__)


@moe.hookimpl
def plugin_registration():
    """Only register the cli sub-plugin if the cli is enabled."""
    config.CONFIG.pm.register(mb_core, "musicbrainz_core")
    if config.CONFIG.pm.has_plugin("cli"):
        config.CONFIG.pm.register(mb_cli, "musicbrainz_cli")
