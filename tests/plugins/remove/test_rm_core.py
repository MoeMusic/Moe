"""Test the core api of the ``remove`` plugin."""

import pytest

from moe.config import Config
from moe.library.album import Album
from moe.library.extra import Extra
from moe.library.track import Track
from moe.plugins import remove as moe_rm


@pytest.fixture
def tmp_rm_config(tmp_config) -> Config:
    """A temporary config for the edit plugin with the cli."""
    return tmp_config('default_plugins = ["remove"]', tmp_db=True)


class TestRemoveItem:
    """Tests `remove_item()`."""

    def test_track(self, mock_track, tmp_session, tmp_rm_config):
        """Tracks are removed from the database with valid query."""
        tmp_session.add(mock_track)
        tmp_session.flush()

        moe_rm.remove_item(tmp_rm_config, mock_track)

        assert not tmp_session.query(Track).scalar()

    def test_album(self, mock_album, tmp_session, tmp_rm_config):
        """Albums are removed from the database with valid query.

        Removing an album should also remove any associated tracks and extras.
        """
        mock_album = tmp_session.merge(mock_album)
        tmp_session.flush()

        moe_rm.remove_item(tmp_rm_config, mock_album)

        assert not tmp_session.query(Album).scalar()
        assert not tmp_session.query(Track).scalar()
        assert not tmp_session.query(Extra).scalar()

    def test_extra(self, mock_extra, tmp_session, tmp_rm_config):
        """Extras are removed from the database with valid query."""
        tmp_session.add(mock_extra)
        tmp_session.flush()

        moe_rm.remove_item(tmp_rm_config, mock_extra)

        assert not tmp_session.query(Extra).scalar()


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation."""

    def test_remove_core(self, tmp_config):
        """Enable the remove core plugin if specified in the config."""
        config = tmp_config(settings='default_plugins = ["remove"]')

        assert config.plugin_manager.has_plugin("remove_core")
