"""Tests the core ``edit`` plugin."""

import datetime

import pytest

from moe.plugins import edit


class TestEditItem:
    """Test `edit_item()`."""

    def test_track(self, mock_track):
        """We can edit a track's field."""
        edit.edit_item(mock_track, "title", "new title")

        assert mock_track.title == "new title"

    def test_album(self, mock_album):
        """We can edit an album's field."""
        edit.edit_item(mock_album, "title", "new title")

        assert mock_album.title == "new title"

    def test_int_field(self, mock_track):
        """We can edit integer fields."""
        edit.edit_item(mock_track, "track_num", "3")

        assert mock_track.track_num == 3

    def test_date_field(self, mock_track):
        """We can edit the date."""
        edit.edit_item(mock_track, "date", "2020-11-01")

        assert mock_track.date == datetime.date(2020, 11, 1)

    def test_invalid_date_field(self, mock_track):
        """Invalid dates should raise an EditError."""
        with pytest.raises(edit.EditError):
            edit.edit_item(mock_track, "date", "2020")

    def test_list_field(self, mock_track):
        """We can edit list fields."""
        edit.edit_item(mock_track, "genre", "a; b")

        assert set(mock_track.genres) == {"a", "b"}

    def test_non_editable_fields(self, mock_track):
        """Editing paths is not currently supported."""
        with pytest.raises(edit.EditError):
            edit.edit_item(mock_track, "path", "~")

    def test_invalid_track_field(self, mock_track):
        """Raise EditError if attempting to edit an invalid field."""
        with pytest.raises(edit.EditError):
            edit.edit_item(mock_track, "lol", "bad field")

    def test_invalid_album_field(self, mock_album):
        """Raise SystemExit if attempting to edit an invalid field."""
        with pytest.raises(edit.EditError):
            edit.edit_item(mock_album, "lol", "bad field")


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation."""

    def test_edit_core(self, tmp_config):
        """Enable the edit core plugin if specified in the config."""
        config = tmp_config(settings='default_plugins = ["edit"]')

        assert config.plugin_manager.has_plugin("edit_core")
