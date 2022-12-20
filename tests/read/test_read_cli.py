"""Test the read cli."""

from types import FunctionType
from typing import Iterator
from unittest.mock import ANY, patch

import pytest

import moe.cli
from tests.conftest import album_factory, track_factory


@pytest.fixture
def mock_read():
    """Mock the `read_item()` api call."""
    with patch("moe.read.read_item", autospec=True) as mock_read:
        yield mock_read


@pytest.fixture
def mock_query() -> Iterator[FunctionType]:
    """Mock a database query call.

    Use ``mock_query.return_value` to set the return value of a query.

    Yields:
        Mock query
    """
    with patch("moe.read.read_cli.cli_query", autospec=True) as mock_query:
        yield mock_query


@pytest.fixture
def _tmp_read_config(tmp_config):
    """A temporary config for the read plugin with the cli."""
    tmp_config('default_plugins = ["cli", "read", "write"]')


@pytest.mark.usefixtures("_tmp_read_config")
class TestCommand:
    """Test the `read` command."""

    def test_track(self, mock_query, mock_read):
        """Tracks are removed from the database with valid query."""
        track = track_factory()
        cli_args = ["read", "*"]
        mock_query.return_value = [track]

        moe.cli.main(cli_args)

        mock_query.assert_called_once_with(ANY, "*", query_type="track")
        mock_read.assert_called_once_with(track)

    def test_album(self, mock_query, mock_read):
        """Albums are removed from the database with valid query."""
        album = album_factory()
        cli_args = ["read", "-a", "*"]
        mock_query.return_value = [album]

        moe.cli.main(cli_args)

        mock_query.assert_called_once_with(ANY, "*", query_type="album")
        mock_read.assert_called_once_with(album)

    def test_multiple_items(self, mock_query, mock_read):
        """We read all items returned from a query."""
        tracks = [track_factory(), track_factory()]
        cli_args = ["read", "*"]
        mock_query.return_value = tracks

        moe.cli.main(cli_args)

        mock_query.assert_called_once_with(ANY, "*", query_type="track")
        for track in tracks:
            mock_read.assert_any_call(track)
        assert mock_read.call_count == 2

    def test_file_dne(self, mock_query, mock_read):
        """Exit with non-zero code if file does not exist."""
        cli_args = ["read", "*"]
        mock_query.return_value = [track_factory()]
        mock_read.side_effect = FileNotFoundError

        with pytest.raises(SystemExit) as err:
            moe.cli.main(cli_args)

        assert err.value.code != 0

    def test_file_dne_multiple_items(self, mock_query, mock_read):
        """Continue reading items even if one errors."""
        cli_args = ["read", "*"]
        mock_query.return_value = [track_factory(), track_factory(), track_factory()]
        mock_read.side_effect = [None, FileNotFoundError, None]

        with pytest.raises(SystemExit) as err:
            moe.cli.main(cli_args)

        assert err.value.code != 0
        assert mock_read.call_count == 3

    def test_rm_item(self, mock_query, mock_read):
        """Remove the item if it doesn't exist and the remove argument is given."""
        cli_args = ["read", "--remove", "*"]
        track = track_factory()
        mock_query.return_value = [track]
        mock_read.side_effect = FileNotFoundError

        with patch("moe.read.read_cli.remove.remove_item") as mock_rm:
            moe.cli.main(cli_args)

        mock_rm.assert_called_once_with(ANY, track)


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation."""

    def test_no_cli(self, tmp_config):
        """Don't enable the read cli plugin if the `cli` plugin is not enabled."""
        config = tmp_config(settings='default_plugins = ["read"]')

        assert not config.pm.has_plugin("read_cli")

    def test_cli(self, tmp_config):
        """Enable the read cli plugin if the `cli` plugin is enabled."""
        config = tmp_config(settings='default_plugins = ["read", "cli"]')

        assert config.pm.has_plugin("read_cli")
