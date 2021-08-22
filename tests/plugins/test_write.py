"""Tests the ``write`` plugin."""

import datetime
from unittest.mock import patch

import pytest

from moe.library.track import Track
from moe.plugins import write as moe_write


@pytest.fixture
def mock_write():
    """Mock the `write_tags` api call."""
    with patch("moe.plugins.write.write_tags", autospec=True) as mock_edit:
        yield mock_edit


@pytest.fixture
def tmp_write_config(tmp_config):
    """Mock the `write_tags` api call."""
    return tmp_config("default_plugins = ['write']")


class TestWriteTags:
    """Tests `write_tags()`."""

    def test_write_tags(self, real_track):
        """We can write track changes to the file."""
        album = "Bigger, Better, Faster, More!"
        albumartist = "4 Non Blondes"
        artist = "4 Non Blondes"
        date = datetime.date(1996, 10, 13)
        disc = 2
        disc_total = 2
        mb_album_id = "123"
        mb_track_id = "1234"
        genres = ["alternative", "rock"]
        title = "What's Up"
        track_num = 3

        real_track.album = album
        real_track.albumartist = albumartist
        real_track.artist = artist
        real_track.date = date
        real_track.disc = disc
        real_track.disc_total = disc_total
        real_track.mb_album_id = mb_album_id
        real_track.mb_track_id = mb_track_id
        real_track.genres = genres
        real_track.title = title
        real_track.track_num = track_num

        moe_write.write_tags(real_track)

        new_track = Track.from_tags(path=real_track.path)
        assert new_track.album == album
        assert new_track.albumartist == albumartist
        assert new_track.artist == artist
        assert new_track.date == date
        assert new_track.disc == disc
        assert new_track.disc_total == disc_total
        assert set(new_track.genres) == set(genres)
        assert new_track.mb_album_id == mb_album_id
        assert new_track.mb_track_id == mb_track_id
        assert new_track.title == title
        assert new_track.track_num == track_num


class TestProcessNewItems:
    """Test the `process_new_items` hook implementation."""

    def test_process_track(self, mock_track, mock_write, tmp_write_config):
        """Any altered Tracks have their tags written."""
        tmp_write_config.plugin_manager.hook.process_new_items(
            config=tmp_write_config, items=[mock_track]
        )

        mock_write.assert_called_once_with(mock_track)

    def test_process_extra(self, mock_extra, mock_write, tmp_write_config):
        """Any altered extras are ignored."""
        tmp_write_config.plugin_manager.hook.process_new_items(
            config=tmp_write_config, items=[mock_extra]
        )

        mock_write.assert_not_called()

    def test_process_album(self, mock_album, mock_write, tmp_write_config):
        """Any altered albums are ignored."""
        tmp_write_config.plugin_manager.hook.process_new_items(
            config=tmp_write_config, items=[mock_album]
        )

        mock_write.assert_not_called()

    def test_process_multiple_tracks(
        self, mock_track_factory, mock_write, tmp_write_config
    ):
        """All altered tracks are written."""
        mock_tracks = [mock_track_factory(), mock_track_factory()]

        tmp_write_config.plugin_manager.hook.process_new_items(
            config=tmp_write_config, items=mock_tracks
        )

        for mock_track in mock_tracks:
            mock_write.assert_any_call(mock_track)
        assert mock_write.call_count == 2
