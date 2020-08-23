"""Test the remove plugin."""

import argparse
from unittest.mock import Mock, patch

import pytest

from moe import cli
from moe.core import library
from moe.plugins import rm


class TestParseArgs:
    """Test the plugin argument parser."""

    def test_track(self, tmp_session, mock_track):
        """Tracks are removed from the database with valid query."""
        args = argparse.Namespace(query="_id:1", album=False)

        tmp_session.add(mock_track)
        tmp_session.commit()

        rm.parse_args(Mock(), tmp_session, args)

        query = tmp_session.query(library.Track.path).scalar()

        assert not query

    def test_album(self, tmp_session, mock_track):
        """Albums are removed from the database with valid query."""
        args = argparse.Namespace(query="_id:1", album=True)

        tmp_session.add(mock_track)
        tmp_session.commit()

        rm.parse_args(Mock(), tmp_session, args)

        query = tmp_session.query(library.Album).scalar()

        assert not query

    def test_album_tracks(self, tmp_session, mock_track):
        """Respective tracks should also be removed if an album is removed."""
        args = argparse.Namespace(query="_id:1", album=True)

        tmp_session.add(mock_track)
        tmp_session.commit()

        rm.parse_args(Mock(), tmp_session, args)

        query = tmp_session.query(library.Track).scalar()

        assert not query

    def test_exit_code(self, capsys, tmp_session, mock_track):
        """If no tracks are printed, we should return a non-zero exit code."""
        args = argparse.Namespace(query="_id:1", album=False)

        with pytest.raises(SystemExit):
            rm.parse_args(Mock(), tmp_session, args)


@pytest.mark.integration
class TestCommand:
    """Test cli integration with the rm command."""

    def test_parse_args(self, tmp_path, tmp_config, mock_track):
        """Music is removed from the library when the `rm` command is invoked."""
        args = ["moe", "rm", "_id:1"]

        with library.session_scope() as session:
            session.add(mock_track)

        with patch("sys.argv", args):
            with patch("moe.cli.Config", return_value=tmp_config):
                cli.main()

        query = library.Session().query(library.Track._id).scalar()

        assert not query
