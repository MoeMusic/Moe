"""This package contains shared functionality for the CLI."""

from . import prompt, query
from .prompt import *  # noqa: F403
from .query import *  # noqa: F403

__all__ = []
__all__.extend(prompt.__all__)
__all__.extend(query.__all__)
