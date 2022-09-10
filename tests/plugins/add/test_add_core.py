"""Tests the add plugin."""

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

    @staticmethod
    @moe.hookimpl
    def post_add(config: Config, item: LibItem):
        """Apply the new title onto the old album."""
        if isinstance(item, Track):
            item.genre = "post_add"


class TestAddItem:
    """General functionality of `add_item`."""

    def test_track(self, mock_track, tmp_session, tmp_add_config):
        """We can add tracks to the library."""
        add.add_item(tmp_add_config, mock_track)

        assert tmp_session.query(Track).one() == mock_track

    def test_album(self, mock_album, tmp_session, tmp_add_config):
        """We can add albums to the library."""
        add.add_item(tmp_add_config, mock_album)

        assert tmp_session.query(Album).one() == mock_album

    def test_extra(self, real_extra, tmp_session, tmp_add_config):
        """We can add extras to the library."""
        add.add_item(tmp_add_config, real_extra)

        assert tmp_session.query(Extra).one() == real_extra

    def test_hooks(self, mock_track, tmp_config, tmp_session):
        """The pre and post add hooks are called when adding an item."""
        config = tmp_config(
            "default_plugins = ['add']",
            extra_plugins=[ExtraPlugin(AddPlugin, "add_plugin")],
            tmp_db=True,
        )

        add.add_item(config, mock_track)

        db_track = tmp_session.query(Track).one()

        assert db_track.title == "pre_add"
        assert db_track.genre == "post_add"

    def test_duplicate_track(
        self, tmp_path, track_factory, tmp_session, tmp_add_config
    ):
        """Raise AddError if duplicate track found."""
        track = track_factory(mb_track_id="123")
        dup_track = track_factory(mb_track_id="123")

        tmp_session.add(dup_track)
        assert track.get_existing()

        with pytest.raises(add.AddError):
            add.add_item(tmp_add_config, track)

    def test_duplicate_album(self, album_factory, tmp_session, tmp_add_config):
        """Raise an AddError if there is a duplicate album in the database."""
        mb_album_id = "123"
        album = album_factory(mb_album_id=mb_album_id)
        dup_album = album_factory(mb_album_id=mb_album_id)

        tmp_session.merge(dup_album)
        assert album.get_existing()

        with pytest.raises(add.AddError):
            add.add_item(tmp_add_config, album)

    def test_duplicate_album_from_track(
        self, tmp_path, album_factory, tmp_session, tmp_add_config
    ):
        """Raise AddError if adding a track with a duplicate associated album."""
        album = album_factory(mb_album_id="123")
        dup_album = album_factory(mb_album_id="123")

        tmp_session.merge(dup_album)
        assert album.get_existing()
        assert not album.tracks[0].get_existing()

        with pytest.raises(add.AddError):
            add.add_item(tmp_add_config, album.tracks[0])

    def test_duplicate_track_from_album(
        self, track_factory, tmp_session, tmp_add_config
    ):
        """Raise AddError if there is a duplicate track from an album in the db."""
        mb_track_id = "123"
        track = track_factory(mb_track_id=mb_track_id)
        dup_track = track_factory(mb_track_id=mb_track_id)

        tmp_session.merge(dup_track)
        assert track.get_existing()

        with pytest.raises(add.AddError):
            add.add_item(tmp_add_config, track.album_obj)

    def test_duplicate_extra_from_album(
        self, extra_factory, tmp_session, tmp_add_config
    ):
        """Raise AddError if there is a duplicate extra from an album in the db."""
        extra = extra_factory()
        dup_extra = extra_factory()
        extra.path = dup_extra.path

        tmp_session.merge(dup_extra)
        assert extra.get_existing()

        with pytest.raises(add.AddError):
            add.add_item(tmp_add_config, extra.album_obj)


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

    def test_post_add(self, mock_track, tmp_config):
        """Ensure plugins can implement the `pre_add` hook."""
        config = tmp_config(
            "default_plugins = ['add']",
            extra_plugins=[ExtraPlugin(AddPlugin, "add_plugin")],
        )

        config.plugin_manager.hook.post_add(config=config, item=mock_track)

        assert mock_track.genre == "post_add"


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation."""

    def test_add_core(self, tmp_config):
        """Enable the add core plugin if specified in the config."""
        config = tmp_config(settings='default_plugins = ["add"]')

        assert config.plugin_manager.has_plugin("add_core")
