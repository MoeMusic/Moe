"""Test the CLI."""

import pytest

from moe import cli


class TestArgParse:
    """Test the argument parser."""

    def test_no_args(self, mocker):
        """Test exit if 0 arguments given."""
        with pytest.raises(SystemExit) as pytest_e:
            cli._parse_args([], mocker.Mock())

        assert pytest_e.value.code != 0
