"""Test the core api of the ``remove`` plugin."""

import pytest
import sqlalchemy
import sqlalchemy.event
import sqlalchemy.orm

import moe
from moe import remove as moe_rm
from moe.config import ExtraPlugin
from moe.library import Album, Extra, Track
from tests.conftest import album_factory, extra_factory, track_factory


@pytest.fixture
def _tmp_rm_config(tmp_config):
    """A temporary config for the edit plugin with the cli."""
    tmp_config('default_plugins = ["remove"]', tmp_db=True)


def rm_track_before_flush(session, flush_context, instances):
    """Remove a track while the session is already flushing."""
    for item in session.new | session.dirty:
        if isinstance(item, Track) and item.title == "remove me":
            moe_rm.remove_item(session, item)


class RmPlugin:
    """Test plugin for remove."""

    @staticmethod
    @moe.hookimpl
    def register_sa_event_listeners():
        """Registers event listeners for editing and processing new items."""
        sqlalchemy.event.listen(
            sqlalchemy.orm.session.Session,
            "before_flush",
            rm_track_before_flush,
        )


class TestRemoveItem:
    """Tests `remove_item()`."""

    @pytest.mark.usefixtures("_tmp_rm_config")
    def test_track(self, tmp_session):
        """Tracks are removed from the database with valid query."""
        track = track_factory()
        tmp_session.add(track)
        tmp_session.flush()

        moe_rm.remove_item(tmp_session, track)

        assert not tmp_session.query(Track).scalar()

    @pytest.mark.usefixtures("_tmp_rm_config")
    def test_album(self, tmp_session):
        """Albums are removed from the database with valid query.

        Removing an album should also remove any associated tracks and extras.
        """
        album = album_factory()
        tmp_session.add(album)
        tmp_session.flush()

        moe_rm.remove_item(tmp_session, album)

        assert not tmp_session.query(Album).scalar()
        assert not tmp_session.query(Track).scalar()
        assert not tmp_session.query(Extra).scalar()

    @pytest.mark.usefixtures("_tmp_rm_config")
    def test_extra(self, tmp_session):
        """Extras are removed from the database with valid query."""
        extra = extra_factory()
        tmp_session.add(extra)
        tmp_session.flush()

        moe_rm.remove_item(tmp_session, extra)

        assert not tmp_session.query(Extra).scalar()

    @pytest.mark.usefixtures("_tmp_rm_config")
    def test_pending(self, tmp_session):
        """We can remove items that have not yet been flushed."""
        track = track_factory()
        tmp_session.add(track)

        moe_rm.remove_item(tmp_session, track)
        tmp_session.flush()

        assert not tmp_session.query(Track).all()

    def test_in_flush(self, tmp_config, tmp_session):
        """If the session is already flushing, ensure the delete happens first.

        This is to prevent potential duplciates from inserting into the database before
        their conflicts can be removed.
        """
        tmp_config(
            "default_plugins = ['remove']",
            extra_plugins=[ExtraPlugin(RmPlugin, "rm_test")],
            tmp_db=True,
        )
        track = track_factory()
        conflict_track = track_factory(path=track.path, title="remove me")

        tmp_session.add(track)
        tmp_session.flush()
        tmp_session.add(conflict_track)
        tmp_session.flush()

        db_track = tmp_session.query(Track).one()
        assert db_track == track

    def test_in_flush_rm_existing(self, tmp_config, tmp_session):
        """Remove an already existing item while a session is flushing."""
        tmp_config(
            "default_plugins = ['remove']",
            extra_plugins=[ExtraPlugin(RmPlugin, "rm_test")],
            tmp_db=True,
        )
        track = track_factory()
        conflict_track = track_factory(path=track.path)

        tmp_session.add(track)
        tmp_session.flush()
        track.title = "remove me"
        tmp_session.add(conflict_track)
        tmp_session.flush()

        db_track = tmp_session.query(Track).one()
        assert db_track == conflict_track


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation."""

    def test_remove_core(self, tmp_config):
        """Enable the remove core plugin if specified in the config."""
        config = tmp_config(settings='default_plugins = ["remove"]')

        assert config.pm.has_plugin("remove_core")
