"""This package contains shared functionality for the CLI."""

from . import prompt, query
from .prompt import *
from .query import *

__all__ = []
__all__.extend(prompt.__all__)
__all__.extend(query.__all__)
