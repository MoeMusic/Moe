"""Test the core api of the ``remove`` plugin."""

from moe.library.album import Album
from moe.library.extra import Extra
from moe.library.track import Track
from moe.plugins import remove as moe_rm


class TestRemoveItem:
    """Tests `remove_item()`."""

    def test_track(self, mock_track, tmp_session):
        """Tracks are removed from the database with valid query."""
        tmp_session.add(mock_track)
        tmp_session.flush()

        moe_rm.remove_item(mock_track)

        assert not tmp_session.query(Track).scalar()

    def test_album(self, mock_album, tmp_session):
        """Albums are removed from the database with valid query.

        Removing an album should also remove any associated tracks and extras.
        """
        mock_album = tmp_session.merge(mock_album)
        tmp_session.flush()

        moe_rm.remove_item(mock_album)

        assert not tmp_session.query(Album).scalar()
        assert not tmp_session.query(Track).scalar()
        assert not tmp_session.query(Extra).scalar()

    def test_extra(self, mock_extra, tmp_session):
        """Extras are removed from the database with valid query."""
        tmp_session.add(mock_extra)
        tmp_session.flush()

        moe_rm.remove_item(mock_extra)

        assert not tmp_session.query(Extra).scalar()


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation."""

    def test_remove_core(self, tmp_config):
        """Enable the remove core plugin if specified in the config."""
        config = tmp_config(settings='default_plugins = ["remove"]')

        assert config.plugin_manager.has_plugin("remove_core")
