"""Test shared library functionality."""


import pytest

import moe
from moe.config import ExtraPlugin, MoeSession
from moe.library.album import Album
from moe.library.extra import Extra
from moe.library.track import Track


class LibItemPlugin:
    """Plugin that implements the library item hooks for testing."""

    @staticmethod
    @moe.hookimpl
    def create_custom_album_fields(config):
        """Adds relevant musicbrainz fields to a track."""
        return {"changed": None, "new": None, "removed": None}

    @staticmethod
    @moe.hookimpl
    def create_custom_extra_fields(config):
        """Adds relevant musicbrainz fields to a track."""
        return {"changed": None, "new": None, "removed": None}

    @staticmethod
    @moe.hookimpl
    def create_custom_track_fields(config):
        """Adds relevant musicbrainz fields to a track."""
        return {"changed": None, "new": None, "removed": None}

    @staticmethod
    @moe.hookimpl
    def edit_changed_items(config, items):
        """Edit changed items."""
        for item in items:
            item.changed = "edited"

    @staticmethod
    @moe.hookimpl
    def edit_new_items(config, items):
        """Edit new items."""
        for item in items:
            item.new = "edited"

    @staticmethod
    @moe.hookimpl
    def process_changed_items(config, items):
        """Process changed items."""
        for item in items:
            item.changed = "processed"

    @staticmethod
    @moe.hookimpl
    def process_new_items(config, items):
        """Process new items."""
        for item in items:
            item.new = "processed"

    @staticmethod
    @moe.hookimpl
    def process_removed_items(config, items):
        """Process removed items."""
        for item in items:
            item.removed = "processed"


class TestHooks:
    """Test the core util hook specifications."""

    def test_edit_changed_items(
        self, album_factory, extra_factory, track_factory, tmp_config
    ):
        """Ensure plugins can implement the `edit_edited_items` hook."""
        config = tmp_config(
            "default_plugins = []",
            extra_plugins=[ExtraPlugin(LibItemPlugin, "lib_item_test")],
            tmp_db=True,
        )
        album = album_factory(config)
        extra = extra_factory(config)
        track = track_factory(config)
        assert not album.changed
        assert not extra.changed
        assert not track.changed

        session = MoeSession()
        session.add(album)
        session.add(extra)
        session.add(track)
        session.commit()

        album.changed = "triggered"
        extra.changed = "triggered"
        track.changed = "triggered"
        session.commit()

        assert album.changed == "edited"
        assert extra.changed == "edited"
        assert track.changed == "edited"

    def test_edit_new_items(
        self, album_factory, extra_factory, track_factory, tmp_config
    ):
        """Ensure plugins can implement the `edit_new_items` hook."""
        config = tmp_config(
            "default_plugins = []",
            extra_plugins=[ExtraPlugin(LibItemPlugin, "lib_item_test")],
            tmp_db=True,
        )
        album = album_factory(config)
        extra = extra_factory(config)
        track = track_factory(config)
        assert not album.new
        assert not extra.new
        assert not track.new

        session = MoeSession()
        session.add(album)
        session.add(extra)
        session.add(track)
        session.commit()

        assert album.new == "edited"
        assert extra.new == "edited"
        assert track.new == "edited"

    def test_process_changed_items(
        self, album_factory, extra_factory, track_factory, tmp_config
    ):
        """Ensure plugins can implement the `edit_edited_items` hook."""
        config = tmp_config(
            "default_plugins = []",
            extra_plugins=[ExtraPlugin(LibItemPlugin, "lib_item_test")],
            tmp_db=True,
        )
        album = album_factory(config)
        extra = extra_factory(config)
        track = track_factory(config)
        assert not album.changed
        assert not extra.changed
        assert not track.changed

        session = MoeSession()
        session.add(album)
        session.add(extra)
        session.add(track)
        session.commit()

        album.changed = "triggered"
        extra.changed = "triggered"
        track.changed = "triggered"
        session.flush()
        assert album.changed == "processed"
        assert extra.changed == "processed"
        assert track.changed == "processed"

        # changes won't persist
        session.commit()
        assert album.changed != "processed"
        assert extra.changed != "processed"
        assert track.changed != "processed"

    def test_process_new_items(
        self, album_factory, extra_factory, track_factory, tmp_config
    ):
        """Ensure plugins can implement the `edit_new_items` hook."""
        config = tmp_config(
            "default_plugins = []",
            extra_plugins=[ExtraPlugin(LibItemPlugin, "lib_item_test")],
            tmp_db=True,
        )
        album = album_factory(config)
        extra = extra_factory(config)
        track = track_factory(config)
        assert not album.new
        assert not extra.new
        assert not track.new

        session = MoeSession()
        session.add(album)
        session.add(extra)
        session.add(track)

        session.flush()
        assert album.new == "processed"
        assert extra.new == "processed"
        assert track.new == "processed"

        # changes won't persist
        session.commit()
        assert album.new != "processed"
        assert extra.new != "processed"
        assert track.new != "processed"

    def test_process_removed_items(
        self, album_factory, extra_factory, track_factory, tmp_config
    ):
        """Ensure plugins can implement the `edit_removed_items` hook."""
        config = tmp_config(
            "default_plugins = []",
            extra_plugins=[ExtraPlugin(LibItemPlugin, "lib_item_test")],
            tmp_db=True,
        )
        album = album_factory(config)
        extra = extra_factory(config, album=album)
        track = track_factory(config, album=album)
        assert not album.removed
        assert not extra.removed
        assert not track.removed

        session = MoeSession()
        session.add(album)
        session.add(extra)
        session.add(track)
        session.commit()

        session.delete(album)
        session.delete(extra)
        session.delete(track)
        session.flush()

        assert album.removed == "processed"
        assert extra.removed == "processed"
        assert track.removed == "processed"
        assert not session.query(Album).all()
        assert not session.query(Extra).all()
        assert not session.query(Track).all()


class TestCustomFields:
    """Test general custom field functionality."""

    def test_db_persistence(self, mock_track, tmp_session):
        """Ensure custom fields persist in the database."""
        mock_track.custom_fields = ["db", "my_list", "non_string"]
        mock_track._custom_fields["db"] = "persist"
        mock_track._custom_fields["my_list"] = [1, "change me"]

        mock_track.db = "persisted"
        mock_track.my_list[1] = "changed"
        tmp_session.add(mock_track)
        tmp_session.flush()

        db_track = tmp_session.query(Track).one()
        assert db_track.db == "persisted"
        assert db_track.my_list == [1, "changed"]

    def test_db_changes(self, track_factory, tmp_config):
        """Ensure custom fields changes also persist in the database."""
        config = tmp_config(settings="default_plugins = []", tmp_db=True)
        track = track_factory(config=config)
        track.custom_fields = ["db", "my_list", "growing_list"]
        track._custom_fields["db"] = "persist"
        track._custom_fields["my_list"] = ["wow", "change me"]
        track._custom_fields["growing_list"] = ["one"]

        session = MoeSession()
        session.add(track)
        session.commit()
        track.db = "persisted"
        track.my_list[1] = "changed"
        track.growing_list.append("two")
        assert track in session.dirty

        db_track = session.query(Track).one()
        assert db_track.db == "persisted"
        assert db_track.my_list == ["wow", "changed"]
        assert db_track.growing_list == ["one", "two"]

    def test_set_non_key(self, mock_track):
        """Don't set just any attribute as a custom field if the key doesn't exist."""
        mock_track.custom_key = 1

        with pytest.raises(KeyError):
            assert mock_track._custom_fields["custom_key"] == 1

    def test_get_custom_field(self, mock_track):
        """We can get a custom field like a normal attribute."""
        mock_track.custom_fields = ["custom"]
        mock_track._custom_fields["custom"] = "field"

        assert mock_track.custom == "field"

    def test_set_custom_field(self, mock_track):
        """We can set a custom field like a normal attribute."""
        mock_track.custom_fields = ["custom_key"]
        mock_track._custom_fields["custom_key"] = None
        mock_track.custom_key = "test"

        assert mock_track._custom_fields["custom_key"] == "test"
