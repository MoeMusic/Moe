"""Tests the ``move`` cli plugin."""

from types import FunctionType
from typing import Iterator
from unittest.mock import patch

import pytest

import moe.cli


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
    with patch("moe.plugins.move.move_cli.query", autospec=True) as mock_query:
        yield mock_query


@pytest.fixture
def tmp_move_config(tmp_config):
    """Creates a configuration with a temporary library path."""
    return tmp_config("default_plugins = ['cli', 'move']")


class TestCommand:
    """Test the `move` command."""

    def test_dry_run(self, mock_album, mock_query, mock_move, tmp_move_config):
        """If `dry-run` is specified, don't actually move the items."""
        cli_args = ["move", "--dry-run"]
        mock_query.return_value = [mock_album]

        moe.cli.main(cli_args, tmp_move_config)

        mock_move.assert_not_called()

    def test_move(self, album_factory, mock_query, mock_move, tmp_move_config):
        """Test all items in the library are moved when the command is invoked."""
        albums = [album_factory(), album_factory()]
        mock_query.return_value = albums
        cli_args = ["move"]

        moe.cli.main(cli_args, tmp_move_config)

        for album in albums:
            mock_move.assert_any_call(tmp_move_config, album)
        assert mock_move.call_count == len(albums)

    def test_no_items(self, capsys, mock_query, tmp_move_config):
        """If no items found to move, exit with non-zero code."""
        cli_args = ["move", "*"]
        mock_query.return_value = []

        with pytest.raises(SystemExit) as error:
            moe.cli.main(cli_args, tmp_move_config)

        assert error.value.code != 0


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation."""

    def test_no_cli(self, tmp_config):
        """Don't enable the move cli plugin if the `cli` plugin is not enabled."""
        config = tmp_config(settings='default_plugins = ["move"]')

        assert not config.plugin_manager.has_plugin("move_cli")

    def test_cli(self, tmp_config):
        """Enable the move cli plugin if the `cli` plugin is enabled."""
        config = tmp_config(settings='default_plugins = ["move", "cli"]')

        assert config.plugin_manager.has_plugin("move_cli")
