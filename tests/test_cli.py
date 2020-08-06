"""Test the CLI."""

import pytest

from fili import cli


class TestArgParse:
    """Test the argument parser."""

    def test_no_args(self):
        """Test exit if 0 arguments given."""
        with pytest.raises(SystemExit) as pytest_e:
            cli._parse_args()

        assert pytest_e.value.code != 0
