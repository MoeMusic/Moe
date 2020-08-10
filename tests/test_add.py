"""Test the add plugin."""

import argparse
import pathlib

from moe.lib import library
from moe.plugins import add


class TestParseArgs:
    """Test music is added to the database when invoked."""

    def test_track(self, temp_config_session):
        """Tracks are added to the database."""
        config, session = temp_config_session
        args = argparse.Namespace(path="testpath")

        add.parse_args(config, session, args)

        path = session.query(library.Track.path).scalar()

        assert path == pathlib.PurePath("testpath")
