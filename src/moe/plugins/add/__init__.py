"""Add plugin.

CLI:
    This plugin provides an ``add`` command that adds music to your library and corrects
    tags by importing metadata from external sources.

API:
    The ``add_item()`` function is the entry point into the add process. The entire
    functionality is split into separate modules within the ``add`` package.

Note:
    This plugin is enabled by default.
"""
# The add module is "split" into a package, but the following code ensures that the
# interface for interacting with the add plugin is consistent with other plugins
# i.e. any functionality can be reached with a ``moe.plugins.add`` import.
#
# Included modules:
#    * `add`: Main module and entry point for the `add` plugin.
#    * `hooks`: Hook specifications for the `add` plugin.
#    * `match`: Logic for matching tracks and albums against each other. This is used
#       in the import process.
#    * `prompt`: CLI user prompts to interact with the adding process.

from moe.plugins.add.add_core import add, match
from moe.plugins.add.add_core.add import *
from moe.plugins.add.add_core.match import *

__all__ = []
__all__.extend(add.__all__)  # noqa: WPS609
__all__.extend(match.__all__)  # noqa: WPS609
