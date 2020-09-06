"""Test the remove plugin."""

import argparse
from unittest.mock import Mock, patch

import pytest

from moe import cli
from moe.core.library.album import Album
from moe.core.library.session import session_scope
from moe.core.library.track import Track
from moe.plugins import rm


class TestParseArgs:
    """Test the plugin argument parser."""

    def test_track(self, tmp_session, mock_track):
        """Tracks are removed from the database with valid query."""
        args = argparse.Namespace(query="_id:1", album=False)
        tmp_session.add(mock_track)

        rm.parse_args(Mock(), tmp_session, args)

        query = tmp_session.query(Track.path).scalar()

        assert not query

    def test_album(self, tmp_session, mock_track):
        """Albums are removed from the database with valid query."""
        args = argparse.Namespace(query="_id:1", album=True)
        tmp_session.add(mock_track)

        rm.parse_args(Mock(), tmp_session, args)

        query = tmp_session.query(Album).scalar()

        assert not query

    def test_album_tracks(self, tmp_session, mock_track):
        """Respective tracks should also be removed if an album is removed."""
        args = argparse.Namespace(query="_id:1", album=True)
        tmp_session.add(mock_track)

        rm.parse_args(Mock(), tmp_session, args)

        query = tmp_session.query(Track).scalar()

        assert not query

    def test_exit_code(self, capsys, tmp_session, mock_track):
        """If no tracks are printed, we should return a non-zero exit code."""
        args = argparse.Namespace(query="_id:1", album=False)

        with pytest.raises(SystemExit) as error:
            rm.parse_args(Mock(), tmp_session, args)

        assert error.value.code != 0


@pytest.mark.integration
class TestCommand:
    """Test cli integration with the rm command."""

    def test_parse_args(self, tmp_path, tmp_config, mock_track):
        """Music is removed from the library when the `rm` command is invoked."""
        args = ["moe", "rm", "_id:1"]

        tmp_config.init_db()
        with session_scope() as session:
            session.add(mock_track)

        with patch("sys.argv", args):
            with patch("moe.cli.Config", return_value=tmp_config):
                cli.main()

        with session_scope() as session2:
            assert not session2.query(Track._id).scalar()
