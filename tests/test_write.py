"""Tests the ``write`` plugin."""

import datetime
from unittest.mock import MagicMock, patch

import mediafile
import pytest

import moe
from moe import config
from moe import write as moe_write
from moe.library import Track
from tests.conftest import album_factory, extra_factory, track_factory


@pytest.fixture
def mock_write():
    """Mock the `write_tags` api call."""
    with patch("moe.write.write_tags", autospec=True) as mock_edit:
        yield mock_edit


@pytest.fixture
def _tmp_write_config(tmp_config):
    """Mock the `write_tags` api call."""
    tmp_config("default_plugins = ['write']")


class WritePlugin:
    """Implement the write plugin hookspecs for testing."""

    @staticmethod
    @moe.hookimpl
    def write_custom_tags(track):
        """Write the title."""
        audio_file = mediafile.MediaFile(track.path)
        audio_file.title = "new title"
        audio_file.save()


class TestHooks:
    """Test any write plugin hookspecs."""

    def test_write_custom_tags(self, tmp_config):
        """Plugins can write tags to a track."""
        tmp_config(
            "default_plugins = ['write']",
            extra_plugins=[config.ExtraPlugin(WritePlugin, "write_test")],
        )
        track = track_factory(title="old title", exists=True)

        config.CONFIG.pm.hook.write_custom_tags(track=track)

        new_track = Track.from_file(track.path)
        assert new_track.title == "new title"


class TestWriteTags:
    """Tests `write_tags()`."""

    def test_write_tags(self, tmp_config):
        """Test writing and reading tags to a track."""
        tmp_config()
        track = track_factory(exists=True)
        artist = "4 Non Blondes"
        artists = {"4 Non Blondes", "Me"}
        barcode = "1234"
        catalog_nums = {"1", "2"}
        composer = "Elephant Seal"
        composer_sort = "Seal, Elephant"
        country = "US"
        date = datetime.date(1996, 10, 13)
        disc = 2
        disc_total = 2
        genres = {"alternative", "rock"}
        label = "Interscope Records"
        media = "CD"
        original_date = datetime.date(1996, 1, 13)
        title = "What's Up"
        track_num = 3
        track_total = 10

        track.artist = artist
        track.artists = artists
        track.album.barcode = barcode
        track.album.catalog_nums = catalog_nums
        track.album.country = country
        track.album.date = date
        track.album.original_date = original_date
        track.composer = composer
        track.composer_sort = composer_sort
        track.disc = disc
        track.album.disc_total = disc_total
        track.genres = genres
        track.album.label = label
        track.album.media = media
        track.title = title
        track.track_num = track_num
        track.album.track_total = track_total

        moe_write.write_tags(track)

        new_track = Track.from_file(track.path)
        new_album = new_track.album

        assert new_track.artist == artist
        assert new_track.artists == artists
        assert new_track.composer == composer
        assert new_track.composer_sort == composer_sort
        assert new_track.disc == disc
        assert new_track.genres == genres
        assert new_track.title == title
        assert new_track.track_num == track_num

        assert new_album.barcode == barcode
        assert new_album.catalog_nums == catalog_nums
        assert new_album.country == country
        assert new_album.date == date
        assert new_album.disc_total == disc_total
        assert new_album.label == label
        assert new_album.media == media
        assert new_album.original_date == original_date
        assert new_album.track_total == track_total


@pytest.mark.usefixtures("_tmp_write_config")
class TestProcessNewItems:
    """Test the `process_new_items` hook implementation."""

    def test_process_track(self, mock_write):
        """Any altered Tracks have their tags written."""
        track = track_factory()
        mock_session = MagicMock()

        config.CONFIG.pm.hook.process_new_items(session=mock_session, items=[track])

        mock_write.assert_called_once_with(track)

    def test_process_extra(self, mock_write):
        """Any altered extras are ignored."""
        mock_session = MagicMock()

        config.CONFIG.pm.hook.process_new_items(
            session=mock_session, items=[extra_factory()]
        )

        mock_write.assert_not_called()

    def test_process_album(self, mock_write):
        """Any altered albums are ignored."""
        mock_session = MagicMock()

        config.CONFIG.pm.hook.process_new_items(
            session=mock_session, items=[album_factory()]
        )

        mock_write.assert_not_called()

    def test_process_multiple_tracks(self, mock_write):
        """All altered tracks are written."""
        tracks = [track_factory(), track_factory()]
        mock_session = MagicMock()

        config.CONFIG.pm.hook.process_new_items(session=mock_session, items=tracks)

        for track in tracks:
            mock_write.assert_any_call(track)
        assert mock_write.call_count == 2


@pytest.mark.usefixtures("_tmp_write_config")
class TestProcessChangedItems:
    """Test the `process_changed_items` hook implementation."""

    def test_process_track(self, mock_write):
        """Any altered Tracks have their tags written."""
        track = track_factory()
        mock_session = MagicMock()

        config.CONFIG.pm.hook.process_changed_items(session=mock_session, items=[track])

        mock_write.assert_called_once_with(track)

    def test_process_extra(self, mock_write):
        """Any altered extras are ignored."""
        mock_session = MagicMock()

        config.CONFIG.pm.hook.process_changed_items(
            session=mock_session, items=[extra_factory()]
        )

        mock_write.assert_not_called()

    def test_process_album(self, mock_write):
        """Any altered albums should have their tracks written."""
        album = album_factory()
        mock_session = MagicMock()

        config.CONFIG.pm.hook.process_changed_items(session=mock_session, items=[album])

        for track in album.tracks:
            mock_write.assert_any_call(track)

    def test_process_multiple_tracks(self, mock_write):
        """All altered tracks are written."""
        tracks = [track_factory(), track_factory()]
        mock_session = MagicMock()

        config.CONFIG.pm.hook.process_changed_items(session=mock_session, items=tracks)

        for track in tracks:
            mock_write.assert_any_call(track)
        assert mock_write.call_count == 2

    def test_dont_write_tracks_twice(self, mock_write):
        """Don't write a track twice if it's album is also in `items`."""
        track = track_factory()
        mock_session = MagicMock()

        config.CONFIG.pm.hook.process_changed_items(
            session=mock_session, items=[track, track.album]
        )

        mock_write.assert_called_once_with(track)
