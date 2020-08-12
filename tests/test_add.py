"""Test the add plugin."""

import argparse
import pathlib
from unittest.mock import Mock

from moe.core import library
from moe.plugins import add


class TestParseArgs:
    """Test music is added to the database when the `add` command is invoked."""

    def test_track(self, tmp_session):
        """Tracks are added to the database."""
        args = argparse.Namespace(path="testpath")

        add.parse_args(Mock(), tmp_session, args)

        test_path = tmp_session.query(library.Track.path).scalar()

        assert test_path == pathlib.Path("testpath").resolve()
