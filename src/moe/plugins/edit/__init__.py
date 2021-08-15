"""Edits music in the library.

Plugin contents:
    ``edit_cli.py``: Adds the ``edit`` command to the cli.
    ``edit_core.py`` : API interface for editing the library.

Note:
    This plugin is enabled by default.
"""

import pluggy

import moe
from moe.config import Config

from . import edit_cli, edit_core
from .edit_core import *

__all__ = []
__all__.extend(edit_core.__all__)  # noqa: WPS609
