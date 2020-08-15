"""Test the remove plugin."""

import argparse
import pathlib
from unittest.mock import Mock

import pytest

from moe import cli
from moe.core import library
from moe.plugins import rm


class TestParseArgs:
    """Test the plugin argument parser."""

    def test_track(self, tmp_session):
        """Tracks are removed from the database with valid query."""
        args = argparse.Namespace(query="id:1")

        tmp_session.add(library.Track(path=pathlib.Path("/tmp_path")))
        tmp_session.commit()

        rm.parse_args(Mock(), tmp_session, args)

        query = tmp_session.query(library.Track.path).scalar()

        assert not query


@pytest.mark.integration
class TestCommand:
    """Test cli integration with the rm command."""

    def test_parse_args(self, tmp_live):
        """Music is removed from the library when the `rm` command is invoked."""
        config, pm = tmp_live

        args = ["rm", "id:1"]
        cli._parse_args(args, pm, config)

        query = library.Session().query(library.Track.id).scalar()

        assert not query
