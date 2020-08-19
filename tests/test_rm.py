"""Test the remove plugin."""

import argparse
from unittest.mock import Mock

import pytest

from moe import cli
from moe.core import library
from moe.plugins import rm


class TestParseArgs:
    """Test the plugin argument parser."""

    def test_track(self, tmp_session, mock_track):
        """Tracks are removed from the database with valid query."""
        args = argparse.Namespace(query="_id:1")

        tmp_session.add(mock_track)
        tmp_session.commit()

        rm.parse_args(Mock(), tmp_session, args)

        query = tmp_session.query(library.Track.path).scalar()

        assert not query

    def test_exit_code(self, capsys, tmp_session, mock_track):
        """If no tracks are printed, we should return a non-zero exit code."""
        args = argparse.Namespace(query="_id:1")

        with pytest.raises(SystemExit):
            rm.parse_args(Mock(), tmp_session, args)


@pytest.mark.integration
class TestCommand:
    """Test cli integration with the rm command."""

    def test_parse_args(self, tmp_path, tmp_live):
        """Music is removed from the library when the `rm` command is invoked."""
        config, pm = tmp_live

        with library.session_scope() as session:
            session.add(library.Track(path=tmp_path))

        args = ["rm", "_id:1"]
        cli._parse_args(args, pm, config)

        query = library.Session().query(library.Track._id).scalar()

        assert not query
