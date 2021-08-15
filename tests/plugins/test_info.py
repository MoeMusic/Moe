"""Tests the ``info`` plugin."""

import argparse
from unittest.mock import Mock, patch

import pytest

import moe
from moe.config import MoeSession
from moe.plugins import info


class TestParseArgs:
    """Test the plugin argument parser."""

    def test_track(self, capsys, mock_track):
        """Tracks are printed to stdout with valid query."""
        args = argparse.Namespace(query="", album=False, extra=False)

        mock_track.albumartist = "test"

        with patch("moe.query.query", return_value=[mock_track]) as mock_query:
            info._parse_args(config=Mock(), args=args)

            mock_query.assert_called_once_with("", query_type="track")

        captured_text = capsys.readouterr()

        assert captured_text.out

    def test_album(self, capsys, mock_album):
        """Albums are printed to stdout with valid query."""
        args = argparse.Namespace(query="", album=True, extra=False)
        mock_album.title = "album title"

        with patch("moe.query.query", return_value=[mock_album]) as mock_query:
            info._parse_args(config=Mock(), args=args)

            mock_query.assert_called_once_with("", query_type="album")

        captured_text = capsys.readouterr()

        assert captured_text.out

    def test_extra(self, capsys, mock_album):
        """Extras are printed to stdout with valid query."""
        args = argparse.Namespace(query="", album=False, extra=True)

        extra = mock_album.extras.pop()
        with patch("moe.query.query", return_value=[extra]) as mock_query:
            info._parse_args(config=Mock(), args=args)

            mock_query.assert_called_once_with("", query_type="extra")

        captured_text = capsys.readouterr()

        assert captured_text.out

    def test_exit_code(self, capsys, tmp_session):
        """If no track infos are printed, we should return a non-zero exit code."""
        args = argparse.Namespace(query="bad", album=False, extra=False)

        with pytest.raises(SystemExit) as error:
            info._parse_args(config=Mock(), args=args)

        assert error.value.code != 0


@pytest.mark.integration
class TestCommand:
    """Test cli integration with the info command."""

    def test_parse_args(self, capsys, real_track, tmp_config):
        """A track's info is printed when the `info` command is invoked."""
        cli_args = ["info", "*"]

        config = tmp_config(settings='default_plugins = ["cli", "info"]', init_db=True)
        session = MoeSession()
        with session.begin():
            session.add(real_track)

        moe.cli.main(cli_args, config)

        assert capsys.readouterr().out
