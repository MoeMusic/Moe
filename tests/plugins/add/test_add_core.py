"""Tests the add plugin."""

import pytest

import moe
from moe import config
from moe.config import ExtraPlugin
from moe.library import Album, Extra, LibItem, Track
from moe.plugins import add
from tests.conftest import album_factory, extra_factory, track_factory


@pytest.fixture
def _tmp_add_config(tmp_config):
    """A temporary config for the edit plugin with the cli."""
    tmp_config('default_plugins = ["add"]', tmp_db=True)


class AddPlugin:
    """Test plugin that implements the add hookspecs."""

    @staticmethod
    @moe.hookimpl
    def pre_add(item: LibItem):
        """Changes the album title."""
        if isinstance(item, Track):
            item.title = "pre_add"


class TestAddItem:
    """General functionality of `add_item`."""

    @pytest.mark.usefixtures("_tmp_add_config")
    def test_track(self, tmp_session):
        """We can add tracks to the library."""
        track = track_factory()
        add.add_item(track)

        assert tmp_session.query(Track).one() == track

    @pytest.mark.usefixtures("_tmp_add_config")
    def test_album(self, tmp_session):
        """We can add albums to the library."""
        album = album_factory()
        add.add_item(album)

        assert tmp_session.query(Album).one() == album

    @pytest.mark.usefixtures("_tmp_add_config")
    def test_extra(self, tmp_session):
        """We can add extras to the library."""
        extra = extra_factory()
        add.add_item(extra)

        assert tmp_session.query(Extra).one() == extra

    def test_hooks(self, tmp_config, tmp_session):
        """The pre and post add hooks are called when adding an item."""
        tmp_config(
            "default_plugins = ['add']",
            extra_plugins=[ExtraPlugin(AddPlugin, "add_plugin")],
            tmp_db=True,
        )

        add.add_item(track_factory())

        db_track = tmp_session.query(Track).one()
        assert db_track.title == "pre_add"

    @pytest.mark.usefixtures("_tmp_add_config")
    def test_duplicate_list_fields_album(self, tmp_session):
        """Duplicate list fields don't error when adding an album."""
        album = album_factory(num_tracks=2)
        track1 = album.tracks[0]
        track2 = album.tracks[1]
        track1.genre = "pop"
        track2.genre = "pop"

        add.add_item(album)

        db_tracks = tmp_session.query(Track).all()
        for track in db_tracks:
            assert track.genre == "pop"

    @pytest.mark.usefixtures("_tmp_add_config")
    def test_duplicate_list_field_tracks(self, tmp_session):
        """Duplicate list fields don't error when adding multiple tracks."""
        track1 = track_factory(genre="pop")
        track2 = track_factory(genre="pop")

        add.add_item(track1)
        add.add_item(track2)

        db_tracks = tmp_session.query(Track).all()
        for track in db_tracks:
            assert track.genre == "pop"


class TestHookSpecs:
    """Test the various hook specifications."""

    def test_pre_add(self, tmp_config):
        """Ensure plugins can implement the `pre_add` hook."""
        track = track_factory()
        tmp_config(
            "default_plugins = ['add']",
            extra_plugins=[ExtraPlugin(AddPlugin, "add_plugin")],
        )

        config.CONFIG.pm.hook.pre_add(item=track)

        assert track.title == "pre_add"


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation."""

    def test_add_core(self, tmp_config):
        """Enable the add core plugin if specified in the config."""
        tmp_config(settings='default_plugins = ["add"]')

        assert config.CONFIG.pm.has_plugin("add_core")
