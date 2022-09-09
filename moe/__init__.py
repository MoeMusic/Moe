"""Main moe package."""

import logging

import pluggy

hookspec = pluggy.HookspecMarker("moe")
hookimpl = pluggy.HookimplMarker("moe")

log = logging.getLogger("moe")
log_fmt = "{levelname}: {message}"
logging.basicConfig(level=logging.WARNING, format=log_fmt, style="{")

# always set external loggers to warning
for key in logging.Logger.manager.loggerDict:
    if "moe" not in key:
        logging.getLogger(key).setLevel(logging.WARNING)
