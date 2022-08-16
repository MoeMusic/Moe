"""Tests the ``info`` plugin."""

import pytest

import moe.cli
from moe.config import Config


@pytest.fixture
def tmp_info_config(tmp_config) -> Config:
    """A temporary config for the info plugin with the cli."""
    return tmp_config('default_plugins = ["cli", "info"]')


class TestCommand:
    """Test the plugin argument parser.

    To see the actual ouput of any of the tests, comment out
    `assert capsys.readouterr().out` and add `assert 0` to the end of the test.
    """

    def test_track(self, capsys, mock_track, mock_query, tmp_info_config):
        """Tracks are printed to stdout with valid query."""
        cli_args = ["info", "*"]
        mock_query.return_value = [mock_track]

        moe.cli.main(cli_args, tmp_info_config)

        mock_query.assert_called_once_with("*", query_type="track")
        assert capsys.readouterr().out

    def test_album(self, capsys, mock_album, mock_query, tmp_info_config):
        """Albums are printed to stdout with valid query."""
        cli_args = ["info", "-a", "*"]
        mock_query.return_value = [mock_album]

        moe.cli.main(cli_args, tmp_info_config)

        mock_query.assert_called_once_with("*", query_type="album")
        assert capsys.readouterr().out

    def test_extra(self, capsys, mock_extra, mock_query, tmp_info_config):
        """Extras are printed to stdout with valid query."""
        cli_args = ["info", "-e", "*"]
        mock_query.return_value = [mock_extra]

        moe.cli.main(cli_args, tmp_info_config)

        mock_query.assert_called_once_with("*", query_type="extra")
        assert capsys.readouterr().out

    def test_multiple_items(
        self, capsys, mock_track_factory, mock_query, tmp_info_config
    ):
        """All items returned from the query are printed."""
        cli_args = ["info", "*"]
        mock_query.return_value = [mock_track_factory(), mock_track_factory()]

        moe.cli.main(cli_args, tmp_info_config)

        assert capsys.readouterr().out

    def test_no_items(self, capsys, mock_query, tmp_info_config):
        """If no item infos are printed, we should return a non-zero exit code."""
        cli_args = ["info", "*"]
        mock_query.return_value = []

        with pytest.raises(SystemExit) as error:
            moe.cli.main(cli_args, tmp_info_config)

        assert error.value.code != 0


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation."""

    def test_no_cli(self, tmp_config):
        """Don't enable the info cli plugin if the `cli` plugin is not enabled."""
        config = tmp_config(settings='default_plugins = ["info"]')

        assert not config.plugin_manager.has_plugin("info")

    def test_cli(self, tmp_config):
        """Enable the info cli plugin if the `cli` plugin is enabled."""
        config = tmp_config(settings='default_plugins = ["info", "cli"]')

        assert config.plugin_manager.has_plugin("info")
