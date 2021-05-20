"""Test the list plugin."""

import argparse
import pathlib
from unittest.mock import patch

import pytest

from moe import cli
from moe.core.library.session import session_scope
from moe.core.library.track import Track
from moe.plugins import ls


class TestParseArgs:
    """Test the plugin argument parser."""

    def test_track(self, capsys, tmp_session, mock_track):
        """Tracks are printed to stdout with valid query."""
        args = argparse.Namespace(query=f"title:{mock_track.title}", album=False)
        tmp_session.add(mock_track)

        ls.parse_args(tmp_session, args)

        captured_text = capsys.readouterr()

        assert captured_text.out.strip() == str(mock_track).strip()

    def test_album(self, capsys, tmp_session, mock_track):
        """Albums are printed to stdout with valid query."""
        args = argparse.Namespace(query=f"title:{mock_track.title}", album=True)
        tmp_session.add(mock_track)

        ls.parse_args(tmp_session, args)

        captured_text = capsys.readouterr()

        assert captured_text.out.strip() == str(mock_track._album_obj).strip()

    def test_exit_code(self, capsys, tmp_session):
        """If no tracks are printed, we should return a non-zero exit code."""
        args = argparse.Namespace(query="bad", album=False)

        with pytest.raises(SystemExit) as error:
            ls.parse_args(tmp_session, args)

        assert error.value.code != 0


@pytest.mark.integration
class TestCommand:
    """Test cli integration with the ls command."""

    def test_parse_args(self, capsys, tmp_config):
        """Music is listed from the library when the `ls` command is invoked."""
        track = Track(
            path=pathlib.Path("tests/resources/album/01.mp3"),
            album="Doggystyle",
            albumartist="Snoop Dogg",
            year=1993,
            track_num=1,
        )
        args = ["moe", "ls", "track_num:1"]

        tmp_config._init_db()
        with session_scope() as session:
            session.add(track)

        with patch("sys.argv", args):
            with patch("moe.cli.config", tmp_config):
                cli.main()

        assert capsys.readouterr().out
