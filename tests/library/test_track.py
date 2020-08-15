"""Test a Track object."""

import pytest

from moe.core.library import Track


class TestInit:
    """Test Track initialization."""

    def test_path_dne(self):
        """Raise an error if the path used to create the Track does not exist."""
        with pytest.raises(AttributeError):
            Track(path="this_doesnt_exist")
