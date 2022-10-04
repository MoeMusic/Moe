"""Test sync plugin cli."""

from unittest.mock import call, patch

import pytest

import moe
import moe.cli
from tests.conftest import track_factory


@pytest.fixture
def mock_sync():
    """Mock the `sync_item()` api call."""
    with patch(
        "moe.plugins.sync.sync_cli.moe_sync.sync_item", autospec=True
    ) as mock_sync:
        yield mock_sync


@pytest.fixture
def mock_query():
    """Mock a database query call.

    Use ``mock_query.return_value` to set the return value of a query.

    Yields:
        Mock query
    """
    with patch("moe.plugins.sync.sync_cli.cli_query", autospec=True) as mock_query:
        yield mock_query


@pytest.fixture
def _tmp_sync_config(tmp_config):
    """A temporary config for the list plugin with the cli."""
    tmp_config('default_plugins = ["cli", "sync"]')


@pytest.mark.usefixtures("_tmp_sync_config")
class TestCommand:
    """Test the `sync` command."""

    def test_items(self, mock_query, mock_sync):
        """Tracks are synced with a valid query."""
        track1 = track_factory()
        track2 = track_factory()
        cli_args = ["sync", "*"]
        mock_query.return_value = [track1, track2]

        moe.cli.main(cli_args)

        mock_query.assert_called_once_with("*", query_type="track")
        mock_sync.assert_has_calls([call(track1), call(track2)])
