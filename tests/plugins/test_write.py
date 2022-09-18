"""Tests the ``write`` plugin."""

import datetime
from unittest.mock import patch

import pytest

from moe import config
from moe.library.track import Track
from moe.plugins import write as moe_write
from tests.conftest import album_factory, extra_factory, track_factory


@pytest.fixture
def mock_write():
    """Mock the `write_tags` api call."""
    with patch("moe.plugins.write.write_tags", autospec=True) as mock_edit:
        yield mock_edit


@pytest.fixture
def _tmp_write_config(tmp_config):
    """Mock the `write_tags` api call."""
    tmp_config("default_plugins = ['write']")


class TestWriteTags:
    """Tests `write_tags()`."""

    def test_write_tags(self):
        """We can write track changes to the file."""
        track = track_factory(exists=True)
        album = "Bigger, Better, Faster, More!"
        albumartist = "4 Non Blondes"
        artist = "4 Non Blondes"
        date = datetime.date(1996, 10, 13)
        disc = 2
        disc_total = 2
        genres = {"alternative", "rock"}
        title = "What's Up"
        track_num = 3

        track.album = album
        track.albumartist = albumartist
        track.artist = artist
        track.date = date
        track.disc = disc
        track.disc_total = disc_total
        track.genres = genres
        track.title = title
        track.track_num = track_num

        moe_write.write_tags(track)

        new_track = Track.from_file(track.path)
        assert new_track.album == album
        assert new_track.albumartist == albumartist
        assert new_track.artist == artist
        assert new_track.date == date
        assert new_track.disc == disc
        assert new_track.disc_total == disc_total
        assert set(new_track.genres) == set(genres)
        assert new_track.title == title
        assert new_track.track_num == track_num


@pytest.mark.usefixtures("_tmp_write_config")
class TestProcessNewItems:
    """Test the `process_new_items` hook implementation."""

    def test_process_track(self, mock_write):
        """Any altered Tracks have their tags written."""
        track = track_factory()
        config.CONFIG.pm.hook.process_new_items(items=[track])

        mock_write.assert_called_once_with(track)

    def test_process_extra(self, mock_write):
        """Any altered extras are ignored."""
        config.CONFIG.pm.hook.process_new_items(items=[extra_factory()])

        mock_write.assert_not_called()

    def test_process_album(self, mock_write):
        """Any altered albums are ignored."""
        config.CONFIG.pm.hook.process_new_items(items=[album_factory()])

        mock_write.assert_not_called()

    def test_process_multiple_tracks(self, mock_write):
        """All altered tracks are written."""
        tracks = [track_factory(), track_factory()]

        config.CONFIG.pm.hook.process_new_items(items=tracks)

        for track in tracks:
            mock_write.assert_any_call(track)
        assert mock_write.call_count == 2
