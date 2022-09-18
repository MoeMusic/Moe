"""Tests the core ``edit`` plugin."""

import datetime

import pytest

from moe.plugins import edit
from tests.conftest import album_factory, track_factory


class TestEditItem:
    """Test `edit_item()`."""

    def test_track(self):
        """We can edit a track's field."""
        track = track_factory()
        edit.edit_item(track, "title", "new title")

        assert track.title == "new title"

    def test_album(self):
        """We can edit an album's field."""
        album = album_factory()
        edit.edit_item(album, "title", "new title")

        assert album.title == "new title"

    def test_int_field(self):
        """We can edit integer fields."""
        track = track_factory()
        edit.edit_item(track, "track_num", "3")

        assert track.track_num == 3

    def test_date_field(self):
        """We can edit the date."""
        track = track_factory()
        edit.edit_item(track, "date", "2020-11-01")

        assert track.date == datetime.date(2020, 11, 1)

    def test_invalid_date_field(self):
        """Invalid dates should raise an EditError."""
        with pytest.raises(edit.EditError):
            edit.edit_item(track_factory(), "date", "2020")

    def test_list_field(self):
        """We can edit list fields."""
        track = track_factory()
        edit.edit_item(track, "genre", "a; b")

        assert set(track.genres) == {"a", "b"}

    def test_non_editable_fields(self):
        """Editing paths is not currently supported."""
        with pytest.raises(edit.EditError):
            edit.edit_item(track_factory(), "path", "~")

    def test_invalid_track_field(self):
        """Raise EditError if attempting to edit an invalid field."""
        with pytest.raises(edit.EditError):
            edit.edit_item(track_factory(), "lol", "bad field")

    def test_invalid_album_field(self):
        """Raise SystemExit if attempting to edit an invalid field."""
        with pytest.raises(edit.EditError):
            edit.edit_item(album_factory(), "lol", "bad field")

    def test_custom_field(self):
        """We can edit custom fields."""
        track = track_factory(custom_fields={"my_title": "test"})
        edit.edit_item(track, "my_title", "new")

        assert track.my_title == "new"


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation."""

    def test_edit_core(self, tmp_config):
        """Enable the edit core plugin if specified in the config."""
        config = tmp_config(settings='default_plugins = ["edit"]')

        assert config.pm.has_plugin("edit_core")
