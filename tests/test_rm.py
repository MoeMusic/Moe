"""Tests the ``remove`` plugin."""

import argparse
import os
from unittest.mock import Mock, patch

import pytest

from moe import cli
from moe.core.config import Config
from moe.core.library.album import Album
from moe.core.library.session import session_scope
from moe.core.library.track import Track
from moe.plugins import rm


class TestParseArgs:
    """Test the plugin argument parser."""

    def test_track(self, tmp_session, mock_track):
        """Tracks are removed from the database with valid query."""
        args = argparse.Namespace(query=f"title:{mock_track.title}", album=False)
        tmp_session.add(mock_track)

        rm.parse_args(config=Mock(), session=tmp_session, args=args)

        assert not tmp_session.query(Track.path).scalar()

    def test_album(self, tmp_session, mock_track):
        """Albums are removed from the database with valid query."""
        args = argparse.Namespace(query=f"title:{mock_track.title}", album=True)
        tmp_session.add(mock_track)

        rm.parse_args(config=Mock(), session=tmp_session, args=args)

        assert not tmp_session.query(Album).scalar()

    def test_album_tracks(self, tmp_session, mock_track):
        """Removing an album should also remove all of its tracks."""
        args = argparse.Namespace(query=f"title:{mock_track.title}", album=True)
        tmp_session.add(mock_track)

        rm.parse_args(config=Mock(), session=tmp_session, args=args)

        assert not tmp_session.query(Track).scalar()

    def test_exit_code(self, capsys):
        """Return a non-zero exit code if no items are removed."""
        args = argparse.Namespace(query="bad", album=False)

        with pytest.raises(SystemExit) as error:
            rm.parse_args(config=Mock(), session=Mock(), args=args)

        assert error.value.code != 0


@pytest.mark.integration
class TestCommand:
    """Test cli integration with the rm command."""

    def test_parse_args(self, real_track, tmp_path):
        """Music is removed from the library when the `rm` command is invoked."""
        cli_args = ["moe", "rm", "*"]
        os.environ["MOE_CONFIG_DIR"] = str(tmp_path)
        os.environ["MOE_DEFAULT_PLUGINS"] = '["rm"]'

        Config().init_db()
        with session_scope() as session:
            session.add(real_track)

        with patch("sys.argv", cli_args):
            cli.main()

        with session_scope() as session2:
            assert not session2.query(Track).scalar()
