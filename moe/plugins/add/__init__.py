"""Add plugin."""

from .add import *
from .hooks import *
from .match import *
from .prompt import *

__all__ = []
submodules = [add, match, prompt, hooks]  # type: ignore # noqa: F405
for submodule in submodules:
    __all__.extend(submodule.__all__)  # noqa: WPS609
