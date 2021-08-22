"""Tests the ``remove`` plugin."""

from unittest.mock import patch

import pytest

import moe


@pytest.fixture
def mock_rm():
    """Mock the `remove_item()` api call."""
    with patch("moe.plugins.remove.remove_item", autospec=True) as mock_rm:
        yield mock_rm


@pytest.fixture
def tmp_rm_config(tmp_config):
    """A temporary config for the edit plugin with the cli."""
    return tmp_config('default_plugins = ["cli", "remove"]')


class TestCommand:
    """Test the `remove` command."""

    def test_track(self, mock_track, mock_query, mock_rm, tmp_rm_config):
        """Tracks are removed from the database with valid query."""
        cli_args = ["remove", "*"]
        mock_query.return_value = [mock_track]

        moe.cli.main(cli_args, tmp_rm_config)

        mock_query.assert_called_once_with("*", query_type="track")
        mock_rm.assert_called_once_with(mock_track)

    def test_album(self, mock_album, mock_query, mock_rm, tmp_rm_config):
        """Albums are removed from the database with valid query."""
        cli_args = ["remove", "-a", "*"]
        mock_query.return_value = [mock_album]

        moe.cli.main(cli_args, tmp_rm_config)

        mock_query.assert_called_once_with("*", query_type="album")
        mock_rm.assert_called_once_with(mock_album)

    def test_extra(self, mock_extra, mock_query, mock_rm, tmp_rm_config):
        """Extras are removed from the database with valid query."""
        cli_args = ["remove", "-e", "*"]
        mock_query.return_value = [mock_extra]

        moe.cli.main(cli_args, tmp_rm_config)

        mock_query.assert_called_once_with("*", query_type="extra")
        mock_rm.assert_called_once_with(mock_extra)

    def test_multiple_items(
        self, mock_track_factory, mock_query, mock_rm, tmp_rm_config
    ):
        """All items returned from the query are removed."""
        cli_args = ["remove", "*"]
        mock_tracks = [mock_track_factory(), mock_track_factory()]
        mock_query.return_value = mock_tracks

        moe.cli.main(cli_args, tmp_rm_config)

        for mock_track in mock_tracks:
            mock_rm.assert_any_call(mock_track)
        assert mock_rm.call_count == 2

    def test_exit_code(self, mock_query, mock_rm, tmp_rm_config):
        """Return a non-zero exit code if no items are removed."""
        cli_args = ["remove", "*"]
        mock_query.return_value = []

        with pytest.raises(SystemExit) as error:
            moe.cli.main(cli_args, tmp_rm_config)

        assert error.value.code != 0
        mock_rm.assert_not_called()


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation."""

    def test_no_cli(self, tmp_config):
        """Don't enable the remove cli plugin if the `cli` plugin is not enabled."""
        config = tmp_config(settings='default_plugins = ["remove"]')

        assert not config.plugin_manager.has_plugin("remove_cli")

    def test_cli(self, tmp_config):
        """Enable the remove cli plugin if the `cli` plugin is enabled."""
        config = tmp_config(settings='default_plugins = ["remove", "cli"]')

        assert config.plugin_manager.has_plugin("remove_cli")
