"""Alters the location of items in your library.

The ``move`` plugin provides the following features:

* Any items added to your library will be copied to the location set by ``library_path``
  in your configuration file.
* Any items moved or copied will have their paths set to a default format.
  This default format cannot currently be configured, and is as follows:

  * Albums: ``{library_path}/{albumartist} ({album_year})/``
  * Tracks: ``{album_path}/{track_number} - {track_title}.{file_ext}``

    If the album contains more than one disc, tracks will be formatted as:

    ``{album_path}/Disc {disc#}/{track_number} - {track_title}.{file_ext}``
  * Extras: ``{album_path}/{original_file_name}``

Plugin contents:
    ``move_cli.py``: Adds the ``move`` command to the cli.
    ``move_core.py`` : Core api for moving items.

Note:
    This plugin is enabled by default.
"""

import pluggy

import moe
from moe.core.config import Config

from . import move_cli, move_core
from .move_core import *

__all__ = []
__all__.extend(move_core.__all__)  # noqa: WPS609
