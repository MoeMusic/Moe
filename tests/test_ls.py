"""Test the list plugin."""

import argparse
from unittest.mock import Mock

import pytest

from moe import cli
from moe.core import library
from moe.plugins import ls


class TestParseArgs:
    """Test the plugin argument parser."""

    def test_track(self, capsys, tmp_session, mock_track):
        """Tracks are printed to stdout with valid query."""
        args = argparse.Namespace(query="_id:1")

        tmp_session.add(mock_track)
        tmp_session.commit()

        ls.parse_args(Mock(), tmp_session, args)

        captured_text = capsys.readouterr()

        assert captured_text.out

    def test_exit_code(self, capsys, tmp_session, mock_track):
        """If no tracks are printed, we should return a non-zero exit code."""
        args = argparse.Namespace(query="_id:1")

        with pytest.raises(SystemExit) as pytest_e:
            ls.parse_args(Mock(), tmp_session, args)

            assert pytest_e.value.code != 0


@pytest.mark.integration
class TestCommand:
    """Test cli integration with the ls command."""

    def test_parse_args(self, capsys, tmp_path, tmp_live):
        """Music is listed from the library when the `ls` command is invoked."""
        config, pm = tmp_live
        with library.session_scope() as session:
            session.add(library.Track(path=tmp_path))

        args = ["ls", "_id:1"]
        cli._parse_args(args, pm, config)

        captured_text = capsys.readouterr()

        assert captured_text.out
