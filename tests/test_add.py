"""Test the add plugin."""

import argparse
import pathlib
from unittest.mock import Mock, patch

import pytest

from moe import cli
from moe.core import library
from moe.plugins import add


class TestParseArgs:
    """Test the plugin argument parser."""

    def test_track(self, tmp_path, tmp_session):
        """Tracks are added to the database."""
        args = argparse.Namespace(path=tmp_path)

        add.parse_args(Mock(), tmp_session, args)

        test_path = tmp_session.query(library.Track.path).scalar()

        assert test_path == pathlib.Path(tmp_path).resolve()

    def test_file_not_found(self, tmp_session):
        """We should raise SystemExit if we can't find the file to add."""
        args = argparse.Namespace(path="does not exist")

        with pytest.raises(SystemExit):
            add.parse_args(Mock(), Mock(), args)

    def test_duplicate_file(self, tmp_path, tmp_session):
        """We should raise SystemExit if the file already exists in the library."""
        args = argparse.Namespace(path=tmp_path)

        add.parse_args(Mock(), tmp_session, args)

        with pytest.raises(SystemExit):
            add.parse_args(Mock(), tmp_session, args)


@pytest.mark.integration
class TestCommand:
    """Test cli integration with the add command."""

    def test_basic(self, tmp_path, tmp_config):
        """Music is added to the library when the `add` command is invoked."""
        args = ["moe", "add", str(tmp_path)]

        with patch("sys.argv", args):
            with patch("moe.cli.Config", return_value=tmp_config):
                cli.main()

        query = library.Session().query(library.Track._id).scalar()

        assert query
