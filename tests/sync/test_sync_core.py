"""Test sync plugin core."""

import moe
from moe import config
from moe import sync as moe_sync
from moe.config import ExtraPlugin
from moe.library import Track
from tests.conftest import track_factory


class SyncPlugin:
    """Test plugin for sync hookspecs."""

    @staticmethod
    @moe.hookimpl
    def sync_metadata(item):
        """Syncs item metadata for testing."""
        if isinstance(item, Track):
            item.title = "synced"


class TestHooks:
    """Test sync hookspecs."""

    def test_sync_metadata(self, tmp_config):
        """Plugins can implement the `sync_metadata` hook."""
        tmp_config(
            settings="default_plugins=['sync']",
            extra_plugins=[ExtraPlugin(SyncPlugin, "sync_plugin")],
        )

        track = track_factory()

        config.CONFIG.pm.hook.sync_metadata(item=track)


class TestSyncItems:
    """Test ``sync_item()``."""

    def test_sync_item(self):
        """Call the `sync_metadata` hook when syncing items."""
        track = track_factory()

        moe_sync.sync_item(track)

        config.CONFIG.pm.hook.sync_metadata.assert_called_once_with(item=track)
