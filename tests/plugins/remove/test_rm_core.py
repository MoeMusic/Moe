"""Test the core api of the ``remove`` plugin."""

from unittest.mock import MagicMock

import pytest
import sqlalchemy
import sqlalchemy.event
import sqlalchemy.orm

import moe
from moe.config import Config, ExtraPlugin, MoeSession
from moe.library.album import Album
from moe.library.extra import Extra
from moe.library.track import Track
from moe.plugins import remove as moe_rm


@pytest.fixture
def tmp_rm_config(tmp_config) -> Config:
    """A temporary config for the edit plugin with the cli."""
    return tmp_config('default_plugins = ["remove"]', tmp_db=True)


def rm_track_before_flush(session, flush_context, instances):
    """Remove a track while the session is already flushing."""
    for item in session.new | session.dirty:
        if isinstance(item, Track) and item.title == "remove me":
            moe_rm.remove_item(MagicMock(), item)


class RmPlugin:
    """Test plugin for remove."""

    @staticmethod
    @moe.hookimpl
    def register_sa_event_listeners(config, session):
        """Registers event listeners for editing and processing new items."""
        sqlalchemy.event.listen(
            session,
            "before_flush",
            rm_track_before_flush,
        )


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

    def test_pending(self, mock_track, tmp_rm_config):
        """We can remove items that have not yet been flushed."""
        session = MoeSession()
        session.add(mock_track)

        moe_rm.remove_item(tmp_rm_config, mock_track)
        session.flush()

        assert not session.query(Track).all()

    def test_in_flush(self, track_factory, tmp_config):
        """If the session is already flushing, ensure the delete happens first.

        This is to prevent potential duplciates from inserting into the database before
        their conflicts can be removed.
        """
        tmp_config(
            "default_plugins = ['remove']",
            extra_plugins=[ExtraPlugin(RmPlugin, "rm_test")],
            tmp_db=True,
        )
        session = MoeSession()
        track = track_factory()
        conflict_track = track_factory(path=track.path, title="remove me")

        session.add(track)
        session.flush()
        session.add(conflict_track)
        session.flush()

        db_track = session.query(Track).one()
        assert db_track == track

    def test_in_flush_rm_existing(self, track_factory, tmp_config):
        """Remove an already existing item while a session is flushing."""
        tmp_config(
            "default_plugins = ['remove']",
            extra_plugins=[ExtraPlugin(RmPlugin, "rm_test")],
            tmp_db=True,
        )
        session = MoeSession()
        track = track_factory()
        conflict_track = track_factory(path=track.path)

        session.add(track)
        session.flush()
        track.title = "remove me"
        session.add(conflict_track)
        session.flush()

        db_track = session.query(Track).one()
        assert db_track == conflict_track


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation."""

    def test_remove_core(self, tmp_config):
        """Enable the remove core plugin if specified in the config."""
        config = tmp_config(settings='default_plugins = ["remove"]')

        assert config.plugin_manager.has_plugin("remove_core")
