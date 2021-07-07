"""Tests the ``list`` plugin."""

import argparse
from unittest.mock import Mock, patch

import pytest

import moe
from moe.core.library.session import session_scope
from moe.plugins import list


class TestParseArgs:
    """Test the plugin argument parser."""

    def test_track(self, capsys, mock_track):
        """Tracks are printed to stdout with valid query."""
        args = argparse.Namespace(query="", album=False, extra=False)

        with patch("moe.core.query.query", return_value=[mock_track]) as mock_query:
            mock_session = Mock()

            list._parse_args(config=Mock(), session=mock_session, args=args)

            mock_query.assert_called_once_with("", mock_session, query_type="track")

        captured_text = capsys.readouterr()

        assert captured_text.out.strip() == str(mock_track).strip()

    def test_album(self, capsys, mock_album):
        """Albums are printed to stdout with valid query."""
        args = argparse.Namespace(query="", album=True, extra=False)

        with patch("moe.core.query.query", return_value=[mock_album]) as mock_query:
            mock_session = Mock()

            list._parse_args(config=Mock(), session=mock_session, args=args)

            mock_query.assert_called_once_with("", mock_session, query_type="album")

        captured_text = capsys.readouterr()

        assert captured_text.out.strip() == str(mock_album).strip()

    def test_extra(self, capsys, mock_album):
        """Extras are printed to stdout with valid query."""
        args = argparse.Namespace(query="", album=False, extra=True)

        extra = mock_album.extras.pop()
        with patch("moe.core.query.query", return_value=[extra]) as mock_query:
            mock_session = Mock()

            list._parse_args(config=Mock(), session=mock_session, args=args)

            mock_query.assert_called_once_with("", mock_session, query_type="extra")

        captured_text = capsys.readouterr()

        assert captured_text.out.strip() == str(extra).strip()

    def test_exit_code(self, capsys):
        """If no tracks are printed, we should return a non-zero exit code."""
        args = argparse.Namespace(query="bad", album=False, extra=False)

        with pytest.raises(SystemExit) as error:
            list._parse_args(config=Mock(), session=Mock(), args=args)

        assert error.value.code != 0


@pytest.mark.integration
class TestCommand:
    """Test cli integration with the list command."""

    def test_parse_args(self, capsys, real_track, tmp_config):
        """Music is listed from the library when the `list` command is invoked."""
        cli_args = ["list", "*"]

        config = tmp_config(settings='default_plugins = ["list"]')
        config.init_db()
        with session_scope() as session:
            session.add(real_track)

        moe.cli.main(cli_args, config)

        assert capsys.readouterr().out
