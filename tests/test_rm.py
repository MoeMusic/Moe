"""Tests the ``remove`` plugin."""

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
        args = argparse.Namespace(query="*", album=False)
        tmp_session.add(mock_track)
        tmp_session.commit()

        rm.parse_args(config=Mock(), session=tmp_session, args=args)

        assert not tmp_session.query(Track).scalar()

    def test_album(self, tmp_session, mock_track):
        """Albums are removed from the database with valid query."""
        args = argparse.Namespace(query="*", album=True)
        tmp_session.add(mock_track)
        tmp_session.commit()

        rm.parse_args(config=Mock(), session=tmp_session, args=args)

        assert not tmp_session.query(Album).scalar()

    def test_album_tracks(self, tmp_session, mock_track):
        """Removing an album should also remove all of its tracks."""
        args = argparse.Namespace(query="*", album=True)
        tmp_session.add(mock_track)
        tmp_session.commit()

        rm.parse_args(config=Mock(), session=tmp_session, args=args)

        assert not tmp_session.query(Track).scalar()

    def test_exit_code(self):
        """Return a non-zero exit code if no items are removed."""
        args = argparse.Namespace(query="bad", album=False)

        with pytest.raises(SystemExit) as error:
            rm.parse_args(config=Mock(), session=Mock(), args=args)

        assert error.value.code != 0


@pytest.mark.integration
class TestCommand:
    """Test cli integration with the rm command."""

    def test_parse_args(self, real_track, tmp_path, tmp_config):
        """Music is removed from the library when the `rm` command is invoked."""
        cli_args = ["moe", "rm", "*"]

        config = tmp_config(settings='default_plugins = ["rm"]')
        config.init_db()
        with session_scope() as session:
            session.add(real_track)

        with patch("sys.argv", cli_args):
            with patch("moe.cli.Config", return_value=config):
                cli.main()

        with session_scope() as session2:
            assert not session2.query(Track).scalar()
