"""Test the info plugin."""

import argparse
import re
from unittest.mock import Mock

import pytest

from moe import cli
from moe.core import library
from moe.plugins import info


class TestParseArgs:
    """Test the plugin argument parser."""

    def test_track(self, capsys, tmp_session, mock_track):
        """Tracks are printed to stdout with valid query."""
        args = argparse.Namespace(query="_id:1")

        tmp_session.add(mock_track)
        tmp_session.commit()

        info.parse_args(Mock(), tmp_session, args)

        captured_text = capsys.readouterr()

        assert captured_text.out


class TestPrintInfos:
    """Test how multiple items get printed together."""

    def test_newline_between(self, capsys, mock_track_factory):
        """Items should be *separated* by newlines.

        There should not be a newline after the last item.
        """
        track1 = mock_track_factory()
        track2 = mock_track_factory()

        info.print_infos([track1, track2])

        captured_out = capsys.readouterr().out

        sep_out = captured_out.split("\n\n")

        assert len(sep_out) == 2


class TestGetInfo:
    """Test how an individual item is represented for our plugin."""

    def test_no_private_fields(self, capsys, mock_track):
        """Private attributes should not be included."""
        track_info = info.get_info(mock_track)

        # assumes each field and it's value is printed on a single line
        assert not re.search(r"(\n|^)_", track_info)


@pytest.mark.integration
class TestCommand:
    """Test cli integration with the info command."""

    def test_parse_args(self, capsys, tmp_live, tmp_path):
        """A track's info is printed when the `info` command is invoked."""
        config, pm = tmp_live
        with library.session_scope() as session:
            session.add(library.Track(path=tmp_path))

        args = ["info", "_id:1"]
        cli._parse_args(args, pm, config)

        captured_text = capsys.readouterr()

        assert captured_text.out
