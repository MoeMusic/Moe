"""Main moe package."""

import logging

import pluggy

hookspec = pluggy.HookspecMarker("moe")
hookimpl = pluggy.HookimplMarker("moe")

log = logging.getLogger(__name__)
"""Root logger.

Each module should define their own logger instead of using this one. The log level
is set to WARNING by default and should not be adjusted outside of the cli arguments.
"""
