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

    def test_track(self, capsys, tmp_session, make_track):
        """Tracks are printed to stdout with valid query."""
        args = argparse.Namespace(query="id:1")

        tmp_session.add(make_track(1))
        tmp_session.commit()

        info.parse_args(Mock(), tmp_session, args)

        captured_text = capsys.readouterr()

        assert captured_text.out


class TestPrintInfos:
    """Test how multiple items get printed together."""

    def test_newline_between(self, capsys, make_track):
        """Items should be *separated* by newlines.

        There should not be a newline after the last item.
        """
        track1 = make_track(1)
        track2 = make_track(2)

        info.print_infos([track1, track2])

        captured_out = capsys.readouterr().out

        sep_out = captured_out.split("\n\n")

        assert len(sep_out) == 2


class TestPrintInfo:
    """Test how an individual item gets printed."""

    def test_no_private_fields(self, capsys, make_track):
        """Private attributes should not be printed."""
        track = make_track(1)

        info.print_info(track)

        captured_out = capsys.readouterr().out

        # assumes each field and it's value is printed on a single line
        assert not re.search(r"(\n|^)_", captured_out)

    def test_no_id(self, capsys, make_track):
        """Primary ID key should not be printed."""
        track = make_track(1)

        info.print_info(track)

        captured_out = capsys.readouterr().out

        # assumes each field and it's value is printed on a single line
        assert not re.search(r"(\n|^)id", captured_out)


@pytest.mark.integration
class TestCommand:
    """Test cli integration with the info command."""

    def test_parse_args(self, capsys, tmp_live, make_track):
        """A track's info is printed when the `info` command is invoked."""
        config, pm = tmp_live
        with library.session_scope() as session:
            session.add(make_track(1))

        args = ["info", "id:1"]
        cli._parse_args(args, pm, config)

        captured_text = capsys.readouterr()

        assert captured_text.out
