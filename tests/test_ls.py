"""Test the list plugin."""

import argparse
from unittest.mock import Mock, patch

import pytest

from moe import cli
from moe.core.library.session import session_scope
from moe.plugins import ls


class TestParseArgs:
    """Test the plugin argument parser."""

    def test_track(self, capsys, tmp_session, mock_track):
        """Tracks are printed to stdout with valid query."""
        args = argparse.Namespace(query=f"title:{mock_track.title}", album=False)
        tmp_session.add(mock_track)

        ls.parse_args(config=Mock(), session=tmp_session, args=args)

        captured_text = capsys.readouterr()

        assert captured_text.out.strip() == str(mock_track).strip()

    def test_album(self, capsys, tmp_session, mock_track):
        """Albums are printed to stdout with valid query."""
        args = argparse.Namespace(query=f"title:{mock_track.title}", album=True)
        tmp_session.add(mock_track)

        ls.parse_args(config=Mock(), session=tmp_session, args=args)

        captured_text = capsys.readouterr()

        assert captured_text.out.strip() == str(mock_track._album_obj).strip()

    def test_exit_code(self, capsys):
        """If no tracks are printed, we should return a non-zero exit code."""
        args = argparse.Namespace(query="bad", album=False)

        with pytest.raises(SystemExit) as error:
            ls.parse_args(config=Mock(), session=Mock(), args=args)

        assert error.value.code != 0


@pytest.mark.integration
class TestCommand:
    """Test cli integration with the ls command."""

    def test_parse_args(self, capsys, real_track, tmp_config):
        """Music is listed from the library when the `ls` command is invoked."""
        args = ["moe", "ls", "*"]

        config = tmp_config(settings='default_plugins = ["ls"]')
        config.init_db()
        with session_scope() as session:
            session.add(real_track)

        with patch("sys.argv", args):
            with patch("moe.cli.Config", return_value=config):
                cli.main()

        assert capsys.readouterr().out
