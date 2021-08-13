"""Removes music in the library.

Plugin contents:
    ``rm_cli.py``: Adds the ``remove`` command to the cli.
    ``rm_core.py`` : API interface for removing items.

Note:
    This plugin is enabled by default.
"""

import pluggy

import moe
from moe.core.config import Config

from . import rm_cli, rm_core
from .rm_core import *

__all__ = []
__all__.extend(rm_core.__all__)  # noqa: WPS609
