"""Tests the ``remove`` plugin."""

from types import FunctionType
from typing import Iterator
from unittest.mock import patch

import pytest

import moe.cli
from tests.conftest import album_factory, extra_factory, track_factory


@pytest.fixture
def mock_rm():
    """Mock the `remove_item()` api call."""
    with patch("moe.remove.remove_item", autospec=True) as mock_rm:
        yield mock_rm


@pytest.fixture
def mock_query() -> Iterator[FunctionType]:
    """Mock a database query call.

    Use ``mock_query.return_value` to set the return value of a query.

    Yields:
        Mock query
    """
    with patch("moe.remove.rm_cli.cli_query", autospec=True) as mock_query:
        yield mock_query


@pytest.fixture
def _tmp_rm_config(tmp_config):
    """A temporary config for the edit plugin with the cli."""
    tmp_config('default_plugins = ["cli", "remove"]')


@pytest.mark.usefixtures("_tmp_rm_config")
class TestCommand:
    """Test the `remove` command."""

    def test_track(self, mock_query, mock_rm):
        """Tracks are removed from the database with valid query."""
        track = track_factory()
        cli_args = ["remove", "*"]
        mock_query.return_value = [track]

        moe.cli.main(cli_args)

        mock_query.assert_called_once_with("*", query_type="track")
        mock_rm.assert_called_once_with(track)

    def test_album(self, mock_query, mock_rm):
        """Albums are removed from the database with valid query."""
        album = album_factory()
        cli_args = ["remove", "-a", "*"]
        mock_query.return_value = [album]

        moe.cli.main(cli_args)

        mock_query.assert_called_once_with("*", query_type="album")
        mock_rm.assert_called_once_with(album)

    def test_extra(self, mock_query, mock_rm):
        """Extras are removed from the database with valid query."""
        extra = extra_factory()
        cli_args = ["remove", "-e", "*"]
        mock_query.return_value = [extra]

        moe.cli.main(cli_args)

        mock_query.assert_called_once_with("*", query_type="extra")
        mock_rm.assert_called_once_with(extra)

    def test_multiple_items(self, mock_query, mock_rm):
        """All items returned from the query are removed."""
        cli_args = ["remove", "*"]
        tracks = [track_factory(), track_factory()]
        mock_query.return_value = tracks

        moe.cli.main(cli_args)

        for track in tracks:
            mock_rm.assert_any_call(track)
        assert mock_rm.call_count == 2


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation."""

    def test_no_cli(self, tmp_config):
        """Don't enable the remove cli plugin if the `cli` plugin is not enabled."""
        config = tmp_config(settings='default_plugins = ["remove"]')

        assert not config.pm.has_plugin("remove_cli")

    def test_cli(self, tmp_config):
        """Enable the remove cli plugin if the `cli` plugin is enabled."""
        config = tmp_config(settings='default_plugins = ["remove", "cli"]')

        assert config.pm.has_plugin("remove_cli")
