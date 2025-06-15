"""This package contains shared functionality for the core API."""

from . import match
from .match import *  # noqa: F403

__all__ = []
__all__.extend(match.__all__)
