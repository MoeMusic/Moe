"""Imports metadata."""

from . import import_cli, import_core
from .import_cli import *
from .import_core import *

__all__ = []
__all__.extend(import_cli.__all__)  # noqa: WPS609
__all__.extend(import_core.__all__)  # noqa: WPS609
