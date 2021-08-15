"""Musicbrainz integration plugin.

Plugin contents:
    ``mb_cli.py``: Integrates musicbrainz with the import prompt.
    ``mb_core.py`` : API interface for getting metadata from musicbrainz.

Note:
    This plugin is enabled by default.

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
__all__.extend(mb_core.__all__)  # noqa: WPS609


@moe.hookimpl
def plugin_registration(config: Config):
    """Only register the cli sub-plugin if the cli is enabled."""
    config.plugin_manager.register(mb_core, "mb_core")
    if config.plugin_manager.has_plugin("cli"):
        config.plugin_manager.register(mb_cli, "mb_cli")
