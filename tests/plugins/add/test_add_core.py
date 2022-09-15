"""Tests the add plugin."""

from unittest.mock import MagicMock

import pytest

import moe
from moe.config import Config, ExtraPlugin
from moe.library.album import Album
from moe.library.extra import Extra
from moe.library.lib_item import LibItem
from moe.library.track import Track
from moe.plugins import add


@pytest.fixture
def tmp_add_config(tmp_config) -> Config:
    """A temporary config for the edit plugin with the cli."""
    return tmp_config('default_plugins = ["add"]', tmp_db=True)


class AddPlugin:
    """Test plugin that implements the add hookspecs."""

    @staticmethod
    @moe.hookimpl
    def pre_add(config: Config, item: LibItem):
        """Changes the album title."""
        if isinstance(item, Track):
            item.title = "pre_add"


class TestAddItem:
    """General functionality of `add_item`."""

    def test_track(self, mock_track, tmp_session, tmp_add_config):
        """We can add tracks to the library."""
        add.add_item(tmp_add_config, mock_track)
        tmp_session.flush()

        assert tmp_session.query(Track).one() == mock_track

    def test_album(self, mock_album, tmp_session, tmp_add_config):
        """We can add albums to the library."""
        add.add_item(tmp_add_config, mock_album)
        tmp_session.flush()

        assert tmp_session.query(Album).one() == mock_album

    def test_extra(self, real_extra, tmp_session, tmp_add_config):
        """We can add extras to the library."""
        add.add_item(tmp_add_config, real_extra)
        tmp_session.flush()

        assert tmp_session.query(Extra).one() == real_extra

    def test_hooks(self, mock_track, tmp_config, tmp_session):
        """The pre and post add hooks are called when adding an item."""
        config = tmp_config(
            "default_plugins = ['add']",
            extra_plugins=[ExtraPlugin(AddPlugin, "add_plugin")],
            tmp_db=True,
        )

        add.add_item(config, mock_track)
        tmp_session.flush()

        db_track = tmp_session.query(Track).one()

        assert db_track.title == "pre_add"

    def test_duplicate_list_fields_album(self, album_factory, tmp_session):
        """Duplicate list fields don't error when adding an album."""
        album = album_factory(num_tracks=2)
        track1 = album.tracks[0]
        track2 = album.tracks[1]
        track1.genre = "pop"
        track2.genre = "pop"

        add.add_item(MagicMock(), album)

        db_tracks = tmp_session.query(Track).all()
        for track in db_tracks:
            assert track.genre == "pop"

    def test_duplicate_list_field_tracks(self, track_factory, tmp_session):
        """Duplicate list fields don't error when adding multiple tracks."""
        track1 = track_factory(genre="pop")
        track2 = track_factory(genre="pop")

        add.add_item(MagicMock(), track1)
        add.add_item(MagicMock(), track2)

        db_tracks = tmp_session.query(Track).all()
        for track in db_tracks:
            assert track.genre == "pop"


class TestHookSpecs:
    """Test the various hook specifications."""

    def test_pre_add(self, mock_track, tmp_config):
        """Ensure plugins can implement the `pre_add` hook."""
        config = tmp_config(
            "default_plugins = ['add']",
            extra_plugins=[ExtraPlugin(AddPlugin, "add_plugin")],
        )

        config.plugin_manager.hook.pre_add(config=config, item=mock_track)

        assert mock_track.title == "pre_add"


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation."""

    def test_add_core(self, tmp_config):
        """Enable the add core plugin if specified in the config."""
        config = tmp_config(settings='default_plugins = ["add"]')

        assert config.plugin_manager.has_plugin("add_core")
