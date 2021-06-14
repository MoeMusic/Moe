"""Tests the ``info`` plugin."""

import argparse
import re
import types
from unittest.mock import Mock, patch

import pytest

from moe import cli
from moe.core.library.session import session_scope
from moe.plugins import info


class TestParseArgs:
    """Test the plugin argument parser."""

    def test_track(self, capsys, mock_track):
        """Tracks are printed to stdout with valid query."""
        args = argparse.Namespace(query="", album=False, extra=False)

        mock_track.albumartist = "test"

        with patch("moe.core.query.query", return_value=[mock_track]) as mock_query:
            mock_session = Mock()

            info.parse_args(config=Mock(), session=mock_session, args=args)

            mock_query.assert_called_once_with("", mock_session, query_type="track")

        captured_text = capsys.readouterr()

        assert captured_text.out

    def test_album(self, capsys, mock_album):
        """Albums are printed to stdout with valid query."""
        args = argparse.Namespace(query="", album=True, extra=False)
        mock_album.title = "album title"

        with patch("moe.core.query.query", return_value=[mock_album]) as mock_query:
            mock_session = Mock()

            info.parse_args(config=Mock(), session=mock_session, args=args)

            mock_query.assert_called_once_with("", mock_session, query_type="album")

        captured_text = capsys.readouterr()

        assert captured_text.out

    def test_extra(self, capsys, mock_album):
        """Extras are printed to stdout with valid query."""
        args = argparse.Namespace(query="", album=False, extra=True)

        extra = mock_album.extras.pop()
        with patch("moe.core.query.query", return_value=[extra]) as mock_query:
            mock_session = Mock()

            info.parse_args(config=Mock(), session=mock_session, args=args)

            mock_query.assert_called_once_with("", mock_session, query_type="extra")

        captured_text = capsys.readouterr()

        assert captured_text.out

    def test_exit_code(self, capsys):
        """If no track infos are printed, we should return a non-zero exit code."""
        args = argparse.Namespace(query="bad", album=False, extra=False)

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


class TestTrackDict:
    """Test dict representation of a Track."""

    def test_no_private_attributes(self, mock_track):
        """Private attributes should not be included."""
        private_re = "^_.*"
        for key in info._item_dict(mock_track).keys():
            assert not re.match(private_re, key)

    def test_no_methods(self, mock_track):
        """Methods should not be included."""
        for key in info._item_dict(mock_track).keys():
            assert not isinstance(getattr(mock_track, key), types.MethodType)

    def test_no_sqlalchemy_attrs(self, mock_track):
        """Sqlalchemy attributes are not relevant and should not be included."""
        assert "metadata" not in info._item_dict(mock_track).keys()
        assert "registry" not in info._item_dict(mock_track).keys()


class TestAlbumDict:
    """Test dict representation of an Album."""

    def test_second_track_attribute_dne(self, mock_track_factory):
        """If varying existence of fields between tracks, set field to Various.

        For example, if track 1 has a year, but track 2 doesn't. The album should
        display `year: Various`.
        """
        track1 = mock_track_factory()
        track2 = mock_track_factory()

        track1.artist = "don't show this"
        track2.artist = ""
        track1.album_obj = track2.album_obj

        assert info._item_dict(track1.album_obj)["artist"] == "Various"

    def test_second_track_attribute_different(self, mock_track_factory):
        """If varying field values between tracks, set field to Various."""
        track1 = mock_track_factory()
        track2 = mock_track_factory()

        track1.artist = "don't show this"
        track2.artist = "different"
        track1.album_obj = track2.album_obj

        assert info._item_dict(track1.album_obj)["artist"] == "Various"


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
