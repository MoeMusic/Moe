"""This package contains shared functionality for the CLI."""

from . import fmt_changes, prompt
from .fmt_changes import *
from .prompt import *

__all__ = []
__all__.extend(prompt.__all__)
__all__.extend(fmt_changes.__all__)
