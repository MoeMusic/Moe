"""Tests the ``move`` cli plugin."""

from types import FunctionType
from typing import Iterator
from unittest.mock import patch

import pytest

import moe.cli
from moe import config
from tests.conftest import album_factory


@pytest.fixture
def mock_move():
    """Mock the `move_item()` api call."""
    with patch("moe.plugins.move.move_item", autospec=True) as mock_edit:
        yield mock_edit


@pytest.fixture
def mock_query() -> Iterator[FunctionType]:
    """Mock a database query call.

    Use ``mock_query.return_value` to set the return value of a query.

    Yields:
        Mock query
    """
    with patch("moe.plugins.move.move_cli.cli_query", autospec=True) as mock_query:
        yield mock_query


@pytest.fixture
def _tmp_move_config(tmp_config):
    """Creates a configuration with a temporary library path."""
    tmp_config("default_plugins = ['cli', 'move']")


@pytest.mark.usefixtures("_tmp_move_config")
class TestCommand:
    """Test the `move` command."""

    def test_dry_run(self, tmp_path, mock_query, mock_move):
        """If `dry-run` is specified, don't actually move the items."""
        album = album_factory(path=tmp_path)
        cli_args = ["move", "--dry-run"]
        mock_query.return_value = [album]

        moe.cli.main(cli_args)

        mock_move.assert_not_called()
        mock_query.assert_called_once_with("*", "album")

    def test_move(self, mock_query, mock_move):
        """Test all items in the library are moved when the command is invoked."""
        albums = [album_factory(), album_factory()]
        mock_query.return_value = albums
        cli_args = ["move"]

        moe.cli.main(cli_args)

        for album in albums:
            mock_move.assert_any_call(album)
        assert mock_move.call_count == len(albums)
        mock_query.assert_called_once_with("*", "album")


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation."""

    def test_no_cli(self, tmp_config):
        """Don't enable the move cli plugin if the `cli` plugin is not enabled."""
        tmp_config(settings='default_plugins = ["move"]')

        assert not config.CONFIG.pm.has_plugin("move_cli")

    def test_cli(self, tmp_config):
        """Enable the move cli plugin if the `cli` plugin is enabled."""
        tmp_config(settings='default_plugins = ["move", "cli"]')

        assert config.CONFIG.pm.has_plugin("move_cli")
