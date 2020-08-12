"""Test the list plugin."""

import argparse
import pathlib
from unittest.mock import Mock

from moe.core import library
from moe.plugins import ls


class TestParseArgs:
    """Test music is listed from the database when invoked."""

    def test_track(self, capsys, tmp_session):
        """Tracks are printed to stdout."""
        args = argparse.Namespace(query="id:1")

        tmp_session.add(library.Track(path=pathlib.Path("/tmp_path")))
        tmp_session.commit()

        ls.parse_args(Mock(), tmp_session, args)

        captured_text = capsys.readouterr()

        assert captured_text.out
