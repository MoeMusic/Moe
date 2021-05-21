"""Test the info plugin."""

import argparse
import pathlib
import re
from unittest.mock import Mock, patch

import pytest

from moe import cli
from moe.core.library.session import session_scope
from moe.core.library.track import Track
from moe.plugins import info


class TestParseArgs:
    """Test the plugin argument parser."""

    def test_track(self, capsys, tmp_session, mock_track):
        """Tracks are printed to stdout with valid query."""
        args = argparse.Namespace(query=f"title:{mock_track.title}", album=False)

        mock_track.albumartist = "test"
        tmp_session.add(mock_track)

        info.parse_args(Mock(), tmp_session, args)

        captured_text = capsys.readouterr()

        assert captured_text.out

    def test_album(self, capsys, tmp_session, mock_track):
        """Albums are printed to stdout with valid query."""
        args = argparse.Namespace(query=f"title:{mock_track.title}", album=True)
        mock_track.album = "album title"

        tmp_session.add(mock_track)

        info.parse_args(Mock(), tmp_session, args)

        captured_text = capsys.readouterr()

        assert captured_text.out

    def test_exit_code(self, capsys, tmp_session):
        """If no track infos are printed, we should return a non-zero exit code."""
        args = argparse.Namespace(query="bad", album=False)

        with pytest.raises(SystemExit) as error:
            info.parse_args(Mock(), tmp_session, args)

        assert error.value.code != 0


class TestFmtInfos:
    """Test how multiple items are represented together."""

    def test_newline_between(self, capsys, mock_track_factory):
        """Items should be *separated* by newlines.

        There should not be a newline after the last item.
        """
        track1 = mock_track_factory()
        track2 = mock_track_factory()

        track_infos = info.fmt_infos([track1, track2])

        sep_infos = track_infos.split("\n\n")

        assert len(sep_infos) == 2
        assert sep_infos[0].strip() == info.fmt_info(track1).strip()
        assert sep_infos[1].strip() == info.fmt_info(track2).strip()


class TestFmtInfo:
    """Test how an individual item is represented for our plugin."""

    def test_format(self, capsys, mock_track):
        """Should format as attribute: value. One pair per line."""
        mock_track.path.__str__.return_value = "test path"

        assert re.match(r"(\w+:\s.+\n)+", info.fmt_info(mock_track))


@pytest.mark.integration
class TestCommand:
    """Test cli integration with the info command."""

    def test_parse_args(self, capsys, tmp_config):
        """A track's info is printed when the `info` command is invoked."""
        track = Track(
            path=pathlib.Path("tests/resources/album/01.mp3"),
            album="Doggystyle",
            albumartist="Snoop Dogg",
            year=1993,
            track_num=1,
        )
        args = ["moe", "info", "track_num:1"]

        tmp_config._init_db()
        with session_scope() as session:
            session.add(track)

        with patch("sys.argv", args):
            with patch("moe.cli.Config", return_value=tmp_config):
                cli.main()

        assert capsys.readouterr().out
