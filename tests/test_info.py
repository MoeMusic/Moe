"""Tests the ``info`` plugin."""

import argparse
import re
from unittest.mock import Mock, patch

import pytest

from moe import cli
from moe.core.library.session import session_scope
from moe.plugins import info


class TestParseArgs:
    """Test the plugin argument parser."""

    def test_track(self, capsys, mock_track):
        """Tracks are printed to stdout with valid query."""
        args = argparse.Namespace(query="", album=False)

        mock_track.albumartist = "test"

        with patch("moe.core.query.query", return_value=[mock_track]) as mock_query:
            mock_session = Mock()

            info.parse_args(config=Mock(), session=mock_session, args=args)

            mock_query.assert_called_once_with("", mock_session, album_query=False)

        captured_text = capsys.readouterr()

        assert captured_text.out

    def test_album(self, capsys, mock_track):
        """Albums are printed to stdout with valid query."""
        args = argparse.Namespace(query="", album=True)
        mock_track.album = "album title"

        with patch(
            "moe.core.query.query", return_value=[mock_track.album_obj]
        ) as mock_query:
            mock_session = Mock()

            info.parse_args(config=Mock(), session=mock_session, args=args)

            mock_query.assert_called_once_with("", mock_session, album_query=True)

        captured_text = capsys.readouterr()

        assert captured_text.out

    def test_exit_code(self, capsys):
        """If no track infos are printed, we should return a non-zero exit code."""
        args = argparse.Namespace(query="bad", album=False)

        with pytest.raises(SystemExit) as error:
            info.parse_args(config=Mock(), session=Mock(), args=args)

        assert error.value.code != 0


class TestFmtInfos:
    """Test how multiple items are represented together."""

    def test_newline_between(self, capsys, mock_track_factory):
        """Items should be *separated* by newlines.

        There should not be a newline after the last item.
        """
        track1 = mock_track_factory()
        track2 = mock_track_factory()

        track_infos = info._fmt_infos([track1, track2])

        sep_infos = track_infos.split("\n\n")

        assert len(sep_infos) == 2
        assert sep_infos[0].strip() == info._fmt_info(track1).strip()
        assert sep_infos[1].strip() == info._fmt_info(track2).strip()


class TestFmtInfo:
    """Test how an individual item is represented for our plugin."""

    def test_format(self, capsys, mock_track):
        """Should format as attribute: value. One pair per line."""
        mock_track.path.__str__.return_value = "test path"

        assert re.match(r"(\w+:\s.+\n)+", info._fmt_info(mock_track))


@pytest.mark.integration
class TestCommand:
    """Test cli integration with the info command."""

    def test_parse_args(self, capsys, real_track, tmp_config):
        """A track's info is printed when the `info` command is invoked."""
        cli_args = ["moe", "info", "*"]

        config = tmp_config(settings='default_plugins = ["info"]')
        config.init_db()
        with session_scope() as session:
            session.add(real_track)

        with patch("sys.argv", cli_args):
            with patch("moe.cli.Config", return_value=config):
                cli.main()

        assert capsys.readouterr().out
