"""Tests the add plugin."""

from pathlib import Path
from types import FunctionType
from typing import Iterator
from unittest.mock import patch

import pytest

import moe
from moe.config import Config
from moe.plugins import add


@pytest.fixture
def mock_add() -> Iterator[FunctionType]:
    """Mock the `edit_item()` api call."""
    with patch("moe.plugins.add.add_item", autospec=True) as mock_add:
        yield mock_add


@pytest.fixture
def tmp_add_config(tmp_config) -> Config:
    """A temporary config for the edit plugin with the cli."""
    return tmp_config('default_plugins = ["cli", "add"]')


class TestCommand:
    """Test the `add` command."""

    def test_item(self, mock_add, tmp_add_config):
        """Items are added to the library when given a path."""
        mock_path = Path("")
        cli_args = ["add", str(mock_path)]

        moe.cli.main(cli_args, tmp_add_config)

        mock_add.assert_called_once_with(tmp_add_config, mock_path)

    def test_multiple_items(self, mock_add, tmp_add_config):
        """Items are added to the library when given a path."""
        mock_path1 = Path("1")
        mock_path2 = Path("2")
        cli_args = ["add", str(mock_path1), str(mock_path2)]

        moe.cli.main(cli_args, tmp_add_config)

        mock_add.assert_any_call(tmp_add_config, mock_path1)
        mock_add.assert_any_call(tmp_add_config, mock_path2)
        assert mock_add.call_count == 2

    def test_single_error(self, mock_add, tmp_add_config):
        """Don't exit after the first failed item if more to be added.

        Still exit with non-zero code if any failures occured.
        """
        mock_path1 = Path("1")
        mock_path2 = Path("2")
        cli_args = ["add", str(mock_path1), str(mock_path2)]

        mock_add.side_effect = [add.AddError, None]
        with pytest.raises(SystemExit) as error:
            moe.cli.main(cli_args, tmp_add_config)

        assert error.value.code != 0
        mock_add.assert_any_call(tmp_add_config, mock_path2)


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation."""

    def test_no_cli(self, tmp_config):
        """Don't enable the add cli plugin if the `cli` plugin is not enabled."""
        config = tmp_config(settings='default_plugins = ["add"]')

        assert not config.plugin_manager.has_plugin("add_cli")

    def test_cli(self, tmp_config):
        """Enable the add cli plugin if the `cli` plugin is enabled."""
        config = tmp_config(settings='default_plugins = ["add", "cli"]')

        assert config.plugin_manager.has_plugin("add_cli")
