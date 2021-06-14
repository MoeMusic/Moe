"""A LibItem in the database and any related logic."""

from collections import OrderedDict
from typing import Any


class LibItem:
    """Abstract base class for library items i.e. Albums, Extras, and Tracks."""

    def to_dict(self) -> "OrderedDict[str, Any]":
        """Represents the LibItem as an alphabetically-sorted dictionary."""
        raise NotImplementedError
