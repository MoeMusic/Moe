"""Test the list plugin."""

import argparse
from unittest.mock import Mock, patch

import pytest

from moe import cli
from moe.core import library
from moe.plugins import ls


class TestParseArgs:
    """Test the plugin argument parser."""

    def test_track(self, capsys, tmp_session, mock_track):
        """Tracks are printed to stdout with valid query."""
        args = argparse.Namespace(query="_id:1", album=False)

        tmp_session.add(mock_track)
        tmp_session.commit()

        ls.parse_args(Mock(), tmp_session, args)

        captured_text = capsys.readouterr()

        assert captured_text.out.strip() == str(mock_track).strip()

    def test_album(self, capsys, tmp_session, mock_track):
        """Albums are printed to stdout with valid query."""
        args = argparse.Namespace(query="_id:1", album=True)

        tmp_session.add(mock_track)
        tmp_session.commit()

        ls.parse_args(Mock(), tmp_session, args)

        captured_text = capsys.readouterr()

        assert captured_text.out.strip() == str(mock_track._album_obj).strip()

    def test_exit_code(self, capsys, tmp_session, mock_track):
        """If no tracks are printed, we should return a non-zero exit code."""
        args = argparse.Namespace(query="_id:1", album=False)

        with pytest.raises(SystemExit):
            ls.parse_args(Mock(), tmp_session, args)


@pytest.mark.integration
class TestCommand:
    """Test cli integration with the ls command."""

    def test_parse_args(self, capsys, tmp_config, mock_track):
        """Music is listed from the library when the `ls` command is invoked."""
        args = ["moe", "ls", "_id:1"]

        with library.session_scope() as session:
            session.add(mock_track)

        with patch("sys.argv", args):
            with patch("moe.cli.Config", return_value=tmp_config):
                cli.main()

        captured_text = capsys.readouterr()

        assert captured_text.out
