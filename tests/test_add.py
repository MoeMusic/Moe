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

    def test_track(self, tmp_session):
        """Tracks are added to the database."""
        music_file = pathlib.Path("tests/resources/audio_files/full.mp3")
        args = argparse.Namespace(path=str(music_file))

        add.parse_args(Mock(), tmp_session, args)

        test_path = tmp_session.query(library.Track.path).scalar()

        assert test_path == music_file.resolve()

    def test_file_not_found(self, tmp_session):
        """We should raise SystemExit if we can't find the file to add."""
        args = argparse.Namespace(path="does not exist")

        with pytest.raises(SystemExit) as error:
            add.parse_args(Mock(), Mock(), args)

        assert error.value.code != 0

    def test_duplicate_file(self, tmp_session):
        """We should raise SystemExit if the file already exists in the library."""
        args = argparse.Namespace(path="tests/resources/audio_files/full.mp3")

        add.parse_args(Mock(), tmp_session, args)

        with pytest.raises(SystemExit) as error:
            add.parse_args(Mock(), tmp_session, args)

        assert error.value.code != 0


@pytest.mark.integration
class TestCommand:
    """Test cli integration with the add command."""

    def test_basic(self, tmp_config):
        """Music is added to the library when the `add` command is invoked."""
        args = ["moe", "add", "tests/resources/audio_files/full.mp3"]

        with patch("sys.argv", args):
            with patch("moe.cli.Config", return_value=tmp_config):
                cli.main()

        query = library.Session().query(library.Track._id).scalar()

        assert query
