"""Test shared library functionality."""


import moe
from moe.config import ExtraPlugin
from moe.library.track import Track


class LibItemPlugin:
    """Plugin that implements the library item hooks for testing."""

    @staticmethod
    @moe.hookimpl
    def process_new_items(config, items):
        """Process the incoming items."""
        for item in items:
            if isinstance(item, Track):
                item.track_num = 3


class TestHooks:
    """Test the core util hook specifications."""

    def test_process_new_items(self, mock_track, tmp_config, tmp_session):
        """Ensure plugins can implement the `add_hooks` hook."""
        tmp_config(
            "default_plugins = []",
            extra_plugins=[ExtraPlugin(LibItemPlugin, "config_plugin")],
            tmp_db=True,
        )

        tmp_session.add(mock_track)
        tmp_session.flush()

        assert mock_track.track_num == 3
