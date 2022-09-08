"""Tests the ``list`` plugin."""

from types import FunctionType
from typing import Iterator
from unittest.mock import patch

import pytest

import moe.cli
from moe.config import Config


@pytest.fixture
def mock_query() -> Iterator[FunctionType]:
    """Mock a database query call.

    Use ``mock_query.return_value` to set the return value of a query.

    Yields:
        Mock query
    """
    with patch("moe.plugins.list.moe_query", autospec=True) as mock_query:
        yield mock_query


@pytest.fixture
def tmp_list_config(tmp_config) -> Config:
    """A temporary config for the list plugin with the cli."""
    return tmp_config('default_plugins = ["cli", "list"]')


class TestParseArgs:
    """Test the plugin argument parser."""

    def test_track(self, capsys, mock_track, mock_query, tmp_list_config):
        """Tracks are printed to stdout with valid query."""
        cli_args = ["list", "*"]
        mock_query.return_value = [mock_track]

        moe.cli.main(cli_args, tmp_list_config)

        mock_query.assert_called_once_with("*", query_type="track")
        assert capsys.readouterr().out.strip("\n") == str(mock_track)

    def test_album(self, capsys, mock_album, mock_query, tmp_list_config):
        """Albums are printed to stdout with valid query."""
        cli_args = ["list", "-a", "*"]
        mock_query.return_value = [mock_album]

        moe.cli.main(cli_args, tmp_list_config)

        mock_query.assert_called_once_with("*", query_type="album")
        assert capsys.readouterr().out.strip("\n") == str(mock_album)

    def test_extra(self, capsys, mock_extra, mock_query, tmp_list_config):
        """Extras are printed to stdout with valid query."""
        cli_args = ["list", "-e", "*"]
        mock_query.return_value = [mock_extra]

        moe.cli.main(cli_args, tmp_list_config)

        mock_query.assert_called_once_with("*", query_type="extra")
        assert capsys.readouterr().out.strip("\n") == str(mock_extra)

    def test_multiple_items(
        self, capsys, mock_track_factory, mock_query, tmp_list_config
    ):
        """All items returned from the query are printed."""
        cli_args = ["list", "*"]
        mock_tracks = [mock_track_factory(), mock_track_factory()]
        mock_query.return_value = mock_tracks

        moe.cli.main(cli_args, tmp_list_config)

        out_str = "\n".join(str(mock_track) for mock_track in mock_tracks)
        assert capsys.readouterr().out.strip("\n") == out_str

    def test_no_items(self, capsys, mock_query, tmp_list_config):
        """If no tracks are printed, we should return a non-zero exit code."""
        cli_args = ["list", "*"]
        mock_query.return_value = []

        with pytest.raises(SystemExit) as error:
            moe.cli.main(cli_args, tmp_list_config)

        assert error.value.code != 0

    def test_paths(self, capsys, mock_track, mock_query, tmp_list_config):
        """Tracks are printed to stdout with valid query."""
        cli_args = ["list", "-p", "*"]
        mock_query.return_value = [mock_track]

        moe.cli.main(cli_args, tmp_list_config)

        mock_query.assert_called_once_with("*", query_type="track")
        assert capsys.readouterr().out.strip("\n") == str(mock_track.path)


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation."""

    def test_no_cli(self, tmp_config):
        """Don't enable the list cli plugin if the `cli` plugin is not enabled."""
        config = tmp_config(settings='default_plugins = ["list"]')

        assert not config.plugin_manager.has_plugin("list")

    def test_cli(self, tmp_config):
        """Enable the list cli plugin if the `cli` plugin is enabled."""
        config = tmp_config(settings='default_plugins = ["list", "cli"]')

        assert config.plugin_manager.has_plugin("list")
