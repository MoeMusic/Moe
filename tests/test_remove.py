"""Tests the ``remove`` plugin."""

import argparse
from unittest.mock import Mock

import pytest

import moe
from moe.core.library.album import Album
from moe.core.library.extra import Extra
from moe.core.library.session import session_scope
from moe.core.library.track import Track
from moe.plugins import remove


class TestParseArgs:
    """Test the plugin argument parser."""

    def test_track(self, tmp_session, mock_track):
        """Tracks are removed from the database with valid query."""
        args = argparse.Namespace(query="*", album=False, extra=False)
        tmp_session.add(mock_track)

        remove._parse_args(config=Mock(), session=tmp_session, args=args)

        assert not tmp_session.query(Track).scalar()

    def test_album(self, tmp_session, mock_album):
        """Albums are removed from the database with valid query."""
        args = argparse.Namespace(query="*", album=True, extra=False)
        tmp_session.merge(mock_album)

        remove._parse_args(config=Mock(), session=tmp_session, args=args)

        assert not tmp_session.query(Album).scalar()

    def test_extra(self, tmp_session, real_album):
        """Extras are removed from the database with valid query.

        ``mock_album`` isn't working with this test. Likely something to do with
        the Extra primary key ``_filename`` and how we are mocking filesytem paths.
        """
        args = argparse.Namespace(query="*", album=False, extra=True)
        tmp_session.merge(real_album)
        assert real_album.extras

        remove._parse_args(config=Mock(), session=tmp_session, args=args)

        assert not tmp_session.query(Extra).scalar()

    def test_album_tracks(self, tmp_session, mock_album):
        """Removing an album should also remove all of its tracks."""
        args = argparse.Namespace(query="*", album=True, extra=False)
        tmp_session.merge(mock_album)

        remove._parse_args(config=Mock(), session=tmp_session, args=args)

        assert not tmp_session.query(Track).scalar()

    def test_album_extras(self, tmp_session, mock_album):
        """Removing an album should also remove all of its extras."""
        args = argparse.Namespace(query="*", album=True, extra=False)
        tmp_session.merge(mock_album)

        assert mock_album.extras
        remove._parse_args(config=Mock(), session=tmp_session, args=args)

        assert not tmp_session.query(Extra).scalar()

    def test_exit_code(self):
        """Return a non-zero exit code if no items are removed."""
        args = argparse.Namespace(query="bad", album=False, extra=False)

        with pytest.raises(SystemExit) as error:
            remove._parse_args(config=Mock(), session=Mock(), args=args)

        assert error.value.code != 0


@pytest.mark.integration
class TestCommand:
    """Test cli integration with the remove command."""

    def test_parse_args(self, real_track, tmp_path, tmp_config):
        """Music is removed from the library when the `remove` command is invoked."""
        cli_args = ["remove", "*"]
        config = tmp_config(settings='default_plugins = ["remove"]')
        config.init_db()
        with session_scope() as session:
            session.add(real_track)

        moe.cli.main(cli_args, config)

        with session_scope() as session2:
            assert not session2.query(Track).scalar()
