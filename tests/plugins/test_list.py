"""Tests the ``list`` plugin."""

from types import FunctionType
from typing import Iterator
from unittest.mock import patch

import pytest

import moe.cli
from moe.query import QueryError
from tests.conftest import album_factory, extra_factory, track_factory


@pytest.fixture
def mock_query() -> Iterator[FunctionType]:
    """Mock a database query call.

    Use ``mock_query.return_value` to set the return value of a query.

    Yields:
        Mock query
    """
    with patch("moe.plugins.list.query", autospec=True) as mock_query:
        yield mock_query


@pytest.fixture
def _tmp_list_config(tmp_config):
    """A temporary config for the list plugin with the cli."""
    tmp_config('default_plugins = ["cli", "list"]')


@pytest.mark.usefixtures("_tmp_list_config")
class TestParseArgs:
    """Test the plugin argument parser."""

    def test_track(self, capsys, mock_query):
        """Tracks are printed to stdout with valid query."""
        track = track_factory()
        cli_args = ["list", "*"]
        mock_query.return_value = [track]

        moe.cli.main(cli_args)

        mock_query.assert_called_once_with("*", query_type="track")
        assert capsys.readouterr().out.strip("\n") == str(track)

    def test_album(self, capsys, mock_query):
        """Albums are printed to stdout with valid query."""
        album = album_factory()
        cli_args = ["list", "-a", "*"]
        mock_query.return_value = [album]

        moe.cli.main(cli_args)

        mock_query.assert_called_once_with("*", query_type="album")
        assert capsys.readouterr().out.strip("\n") == str(album)

    def test_extra(self, capsys, mock_query):
        """Extras are printed to stdout with valid query."""
        extra = extra_factory()
        cli_args = ["list", "-e", "*"]
        mock_query.return_value = [extra]

        moe.cli.main(cli_args)

        mock_query.assert_called_once_with("*", query_type="extra")
        assert capsys.readouterr().out.strip("\n") == str(extra)

    def test_multiple_items(self, capsys, mock_query):
        """All items returned from the query are printed."""
        cli_args = ["list", "*"]
        tracks = [track_factory(), track_factory()]
        mock_query.return_value = tracks

        moe.cli.main(cli_args)

        out_str = "\n".join(str(track) for track in tracks)
        assert capsys.readouterr().out.strip("\n") == out_str

    def test_no_items(self, capsys, mock_query):
        """If no tracks are printed, we should return a non-zero exit code."""
        cli_args = ["list", "*"]
        mock_query.return_value = []

        with pytest.raises(SystemExit) as error:
            moe.cli.main(cli_args)

        assert error.value.code != 0

    def test_paths(self, capsys, mock_query):
        """Tracks are printed to stdout with valid query."""
        track = track_factory()
        cli_args = ["list", "-p", "*"]
        mock_query.return_value = [track]

        moe.cli.main(cli_args)

        mock_query.assert_called_once_with("*", query_type="track")
        assert capsys.readouterr().out.strip("\n") == str(track.path)

    def test_bad_query(self, mock_query):
        """Raise SystemExit if given a bad query."""
        cli_args = ["list", "*"]
        mock_query.side_effect = QueryError

        with pytest.raises(SystemExit) as error:
            moe.cli.main(cli_args)

        assert error.value.code != 0


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation."""

    def test_no_cli(self, tmp_config):
        """Don't enable the list cli plugin if the `cli` plugin is not enabled."""
        config = tmp_config(settings='default_plugins = ["list"]')

        assert not config.pm.has_plugin("list")

    def test_cli(self, tmp_config):
        """Enable the list cli plugin if the `cli` plugin is enabled."""
        config = tmp_config(settings='default_plugins = ["list", "cli"]')

        assert config.pm.has_plugin("list")
