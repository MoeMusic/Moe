"""Tests the add plugin."""

from types import FunctionType
from typing import Iterator
from unittest.mock import patch

import pytest

import moe.cli
from tests.conftest import album_factory, extra_factory, track_factory


@pytest.fixture
def mock_add() -> Iterator[FunctionType]:
    """Mock the `edit_item()` api call."""
    with patch("moe.plugins.add.add_item", autospec=True) as mock_add:
        yield mock_add


@pytest.fixture
def _tmp_add_config(tmp_config):
    """A temporary config for the add plugin with the cli."""
    tmp_config('default_plugins = ["cli", "add", "write"]')


@pytest.mark.usefixtures("_tmp_add_config")
class TestCommand:
    """Test the `add` command."""

    def test_track_file(self, mock_add):
        """Track files are added as tracks."""
        track = track_factory(exists=True)
        cli_args = ["add", str(track.path)]

        moe.cli.main(cli_args)

        mock_add.assert_called_once_with(track)

    def test_non_track_file(self, mock_add):
        """Raise SystemExit if bad track file given."""
        cli_args = ["add", str(extra_factory(exists=True).path)]

        with pytest.raises(SystemExit) as err:
            moe.cli.main(cli_args)

        assert err.value.code != 0
        mock_add.assert_not_called()

    def test_bad_album_dir(self, tmp_path, mock_add):
        """Raise SystemExit if bad album directory given."""
        cli_args = ["add", str(tmp_path)]

        with pytest.raises(SystemExit) as err:
            moe.cli.main(cli_args)

        assert err.value.code != 0
        mock_add.assert_not_called()

    def test_multiple_items(self, mock_add):
        """Items are added to the library when given a path."""
        track = track_factory(exists=True)
        album = album_factory(exists=True)
        cli_args = ["add", str(track.path), str(album.path)]

        moe.cli.main(cli_args)

        mock_add.assert_any_call(track)
        mock_add.assert_any_call(album)
        assert mock_add.call_count == 2

    def test_single_error(self, tmp_path, mock_add):
        """Don't exit after the first failed item if more to be added.

        Still exit with non-zero code if any failures occured.
        """
        track = track_factory(exists=True)
        cli_args = ["add", str(tmp_path), str(track.path)]

        with pytest.raises(SystemExit) as error:
            moe.cli.main(cli_args)

        assert error.value.code != 0
        mock_add.assert_called_once_with(track)


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation."""

    def test_no_cli(self, tmp_config):
        """Don't enable the add cli plugin if the `cli` plugin is not enabled."""
        config = tmp_config(settings='default_plugins = ["add"]')

        assert not config.pm.has_plugin("add_cli")

    def test_cli(self, caplog, tmp_config):
        """Enable the add cli plugin if the `cli` plugin is enabled."""
        config = tmp_config(settings='default_plugins = ["add", "cli"]')

        assert config.pm.has_plugin("add_cli")
