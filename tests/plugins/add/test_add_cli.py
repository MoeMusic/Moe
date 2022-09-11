"""Tests the add plugin."""

from types import FunctionType
from typing import Iterator
from unittest.mock import patch

import pytest

import moe.cli
from moe.config import Config


@pytest.fixture
def mock_add() -> Iterator[FunctionType]:
    """Mock the `edit_item()` api call."""
    with patch("moe.plugins.add.add_item", autospec=True) as mock_add:
        yield mock_add


@pytest.fixture
def tmp_add_config(tmp_config) -> Config:
    """A temporary config for the add plugin with the cli."""
    return tmp_config('default_plugins = ["cli", "add"]')


class TestCommand:
    """Test the `add` command."""

    def test_track_file(self, real_track, mock_add, tmp_add_config):
        """Track files are added as tracks."""
        cli_args = ["add", str(real_track.path)]

        moe.cli.main(cli_args, tmp_add_config)

        mock_add.assert_called_once_with(tmp_add_config, real_track)

    def test_non_track_file(self, real_extra, mock_add, tmp_add_config):
        """Raise SystemExit if bad track file given."""
        cli_args = ["add", str(real_extra.path)]

        with pytest.raises(SystemExit) as err:
            moe.cli.main(cli_args, tmp_add_config)

        assert err.value.code != 0
        mock_add.assert_not_called()

    def test_bad_album_dir(self, tmp_path, mock_add, tmp_add_config):
        """Raise SystemExit if bad album directory given."""
        cli_args = ["add", str(tmp_path)]

        with pytest.raises(SystemExit) as err:
            moe.cli.main(cli_args, tmp_add_config)

        assert err.value.code != 0
        mock_add.assert_not_called()

    def test_multiple_items(self, real_track, real_album, mock_add, tmp_add_config):
        """Items are added to the library when given a path."""
        cli_args = ["add", str(real_track.path), str(real_album.path)]

        moe.cli.main(cli_args, tmp_add_config)

        mock_add.assert_any_call(tmp_add_config, real_track)
        mock_add.assert_any_call(tmp_add_config, real_album)
        assert mock_add.call_count == 2

    def test_single_error(self, tmp_path, real_track, mock_add, tmp_add_config):
        """Don't exit after the first failed item if more to be added.

        Still exit with non-zero code if any failures occured.
        """
        cli_args = ["add", str(tmp_path), str(real_track.path)]

        with pytest.raises(SystemExit) as error:
            moe.cli.main(cli_args, tmp_add_config)

        assert error.value.code != 0
        mock_add.assert_called_once_with(tmp_add_config, real_track)


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation."""

    def test_no_cli(self, tmp_config):
        """Don't enable the add cli plugin if the `cli` plugin is not enabled."""
        config = tmp_config(settings='default_plugins = ["add"]')

        assert not config.plugin_manager.has_plugin("add_cli")

    def test_cli(self, caplog, tmp_config):
        """Enable the add cli plugin if the `cli` plugin is enabled."""
        config = tmp_config(settings='default_plugins = ["add", "cli"]')

        assert config.plugin_manager.has_plugin("add_cli")
