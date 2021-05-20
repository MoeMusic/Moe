"""Test the CLI."""

import pytest

from moe import cli


class TestArgParse:
    """Test the argument parser."""

    def test_no_args(self):
        """Test exit if 0 subcommands given."""
        with pytest.raises(SystemExit) as error:
            cli._parse_args([])

        assert error.value.code != 0
