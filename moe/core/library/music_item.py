"""A MusicItem in the database and any related logic."""

from collections import OrderedDict
from typing import Any


class MusicItem:
    """Abstract base class for albums, extras, and tracks."""

    def to_dict(self) -> "OrderedDict[str, Any]":
        """Represents the MusicItem as an alphabetically-sorted dictionary."""
        raise NotImplementedError
