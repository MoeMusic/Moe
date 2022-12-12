"""Test shared library functionality."""

import moe
from moe.config import ExtraPlugin, MoeSession
from moe.library import Album, Extra, Track
from tests.conftest import album_factory, extra_factory, track_factory


class LibItemPlugin:
    """Plugin that implements the library item hooks for testing."""

    @staticmethod
    @moe.hookimpl
    def edit_changed_items(items):
        """Edit changed items."""
        for item in items:
            item.custom["changed"] = "edited"

    @staticmethod
    @moe.hookimpl
    def edit_new_items(items):
        """Edit new items."""
        for item in items:
            item.custom["new"] = "edited"

    @staticmethod
    @moe.hookimpl
    def process_changed_items(items):
        """Process changed items."""
        for item in items:
            item.custom["changed"] = "processed"

    @staticmethod
    @moe.hookimpl
    def process_new_items(items):
        """Process new items."""
        for item in items:
            item.custom["new"] = "processed"

    @staticmethod
    @moe.hookimpl
    def process_removed_items(items):
        """Process removed items."""
        for item in items:
            item.custom["removed"] = "processed"


class TestHooks:
    """Test the core util hook specifications."""

    def test_edit_changed_items(self, tmp_config):
        """Ensure plugins can implement the `edit_edited_items` hook."""
        tmp_config(
            "default_plugins = []",
            extra_plugins=[ExtraPlugin(LibItemPlugin, "lib_item_test")],
            tmp_db=True,
        )
        album = album_factory()
        extra = extra_factory()
        track = track_factory()

        session = MoeSession()
        session.add(album)
        session.add(extra)
        session.add(track)
        session.commit()

        album.custom["changed"] = "triggered"
        extra.custom["changed"] = "triggered"
        track.custom["changed"] = "triggered"
        session.commit()

        assert album.custom["changed"] == "edited"
        assert extra.custom["changed"] == "edited"
        assert track.custom["changed"] == "edited"

    def test_edit_new_items(self, tmp_config):
        """Ensure plugins can implement the `edit_new_items` hook."""
        tmp_config(
            "default_plugins = []",
            extra_plugins=[ExtraPlugin(LibItemPlugin, "lib_item_test")],
            tmp_db=True,
        )
        album = album_factory()
        extra = extra_factory()
        track = track_factory()

        session = MoeSession()
        session.add(album)
        session.add(extra)
        session.add(track)
        session.commit()

        assert album.custom["new"] == "edited"
        assert extra.custom["new"] == "edited"
        assert track.custom["new"] == "edited"

    def test_process_changed_items(self, tmp_config):
        """Ensure plugins can implement the `edit_edited_items` hook."""
        tmp_config(
            "default_plugins = []",
            extra_plugins=[ExtraPlugin(LibItemPlugin, "lib_item_test")],
            tmp_db=True,
        )
        album = album_factory()
        extra = extra_factory()
        track = track_factory()

        session = MoeSession()
        session.add(album)
        session.add(extra)
        session.add(track)
        session.commit()

        album.custom["changed"] = "triggered"
        extra.custom["changed"] = "triggered"
        track.custom["changed"] = "triggered"
        session.flush()
        assert album.custom["changed"] == "processed"
        assert extra.custom["changed"] == "processed"
        assert track.custom["changed"] == "processed"

        # changes won't persist
        session.commit()
        assert album.custom["changed"] != "processed"
        assert extra.custom["changed"] != "processed"
        assert track.custom["changed"] != "processed"

    def test_process_new_items(self, tmp_config):
        """Ensure plugins can implement the `edit_new_items` hook."""
        tmp_config(
            "default_plugins = []",
            extra_plugins=[ExtraPlugin(LibItemPlugin, "lib_item_test")],
            tmp_db=True,
        )
        album = album_factory()
        extra = extra_factory()
        track = track_factory()

        session = MoeSession()
        session.add(album)
        session.add(extra)
        session.add(track)

        session.flush()
        assert album.custom["new"] == "processed"
        assert extra.custom["new"] == "processed"
        assert track.custom["new"] == "processed"

        # changes won't persist
        session.commit()
        assert album.custom["new"] != "processed"
        assert extra.custom["new"] != "processed"
        assert track.custom["new"] != "processed"

    def test_process_removed_items(self, tmp_config):
        """Ensure plugins can implement the `edit_removed_items` hook."""
        tmp_config(
            "default_plugins = []",
            extra_plugins=[ExtraPlugin(LibItemPlugin, "lib_item_test")],
            tmp_db=True,
        )
        album = album_factory()
        extra = extra_factory(album=album)
        track = track_factory(album=album)

        session = MoeSession()
        session.add(album)
        session.add(extra)
        session.add(track)
        session.commit()

        session.delete(album)
        session.delete(extra)
        session.delete(track)
        session.flush()

        assert album.custom["removed"] == "processed"
        assert extra.custom["removed"] == "processed"
        assert track.custom["removed"] == "processed"
        assert not session.query(Album).all()
        assert not session.query(Extra).all()
        assert not session.query(Track).all()


class TestCustomFields:
    """Test general custom field functionality."""

    def test_db_persistence(self, tmp_session):
        """Ensure custom fields persist in the database."""
        track = track_factory(db="persists", my_list=[1, "change me"])

        track.custom["db"] = "persisted"
        track.custom["my_list"][1] = "changed"
        tmp_session.add(track)
        tmp_session.flush()

        db_track = tmp_session.query(Track).one()
        assert db_track.custom["db"] == "persisted"
        assert db_track.custom["my_list"] == [1, "changed"]

    def test_db_changes(self, tmp_config):
        """Ensure custom fields changes also persist in the database."""
        tmp_config(settings="default_plugins = []", tmp_db=True)
        track = track_factory(
            db="persists", my_list=["wow", "change me"], growing_list=["one"]
        )

        session = MoeSession()
        session.add(track)
        session.commit()
        track.custom["db"] = "persisted"
        track.custom["my_list"][1] = "changed"
        track.custom["growing_list"].append("two")
        assert track in session.dirty

        db_track = session.query(Track).one()
        assert db_track.custom["db"] == "persisted"
        assert db_track.custom["my_list"] == ["wow", "changed"]
        assert db_track.custom["growing_list"] == ["one", "two"]
