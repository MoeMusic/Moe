"""Test the CLI."""

from unittest.mock import Mock

import pytest

from moe import cli


class TestArgParse:
    """Test the argument parser."""

    def test_no_args(self):
        """Test exit if 0 subcommands given."""
        with pytest.raises(SystemExit):
            cli._parse_args(["moe"], Mock(), Mock())
