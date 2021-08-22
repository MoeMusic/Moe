"""Tests the musicbrainz plugin."""

import datetime
from unittest.mock import patch

import musicbrainzngs  # noqa: F401
import pytest

import tests.plugins.musicbrainz.resources as mb_rsrc
from moe.plugins import musicbrainz as moe_mb


@pytest.fixture
def mock_mb_by_id():
    """Mock the musicbrainzngs api call `get_release_by_id`."""
    with patch(
        "moe.plugins.musicbrainz.mb_core.musicbrainzngs.get_release_by_id",
        autospec=True,
    ) as mock_mb_by_id:
        yield mock_mb_by_id


class TestImportCandidates:
    """Test the ``import_candidtates`` hook implementation."""

    def test_get_matching_albums(self, mock_album, tmp_config):
        """Get matching albums when searching for candidates to import."""
        config = tmp_config("default_plugins = ['import', 'musicbrainz']")

        with patch.object(moe_mb.mb_core, "get_matching_album") as mock_gma:
            mock_gma.return_value = mock_album
            candidates = config.plugin_manager.hook.import_candidates(
                config=config, album=mock_album
            )

        mock_gma.assert_called_once_with(mock_album)
        assert candidates == [mock_album]


class TestGetMatchingAlbum:
    """Test `get_matching_album()`."""

    @pytest.mark.network
    def test_network(self, mock_album):
        """Make sure we can actually hit the real API.

        Since `get_matching_album` also calls `get_album_by_id`, this test serves as a
        network test for both.
        """
        mock_album.artist = "Kanye West"
        mock_album.title = "My Beautiful Dark Twisted Fantasy"

        mb_album = moe_mb.get_matching_album(mock_album)

        # don't test every field since we can't actually guarantee the accuracy of
        # musicbrainz's search results every time
        assert mb_album.artist == mock_album.artist
        assert mb_album.title == mock_album.title

    def test_album_search(self, mock_album, mock_mb_by_id):
        """Searching for a release uses the expected parameters."""
        mock_album.artist = "Kanye West"
        mock_album.title = "My Beautiful Dark Twisted Fantasy"
        mock_album.date = datetime.date(2010, 11, 22)
        search_criteria = {
            "artist": "Kanye West",
            "release": "My Beautiful Dark Twisted Fantasy",
            "date": "2010-11-22",
        }
        mock_mb_by_id.return_value = mb_rsrc.full_release.release

        with patch(
            "moe.plugins.musicbrainz.mb_core.musicbrainzngs.search_releases",
            return_value=mb_rsrc.full_release.search,
            autospec=True,
        ) as mock_mb_search:
            mb_album = moe_mb.get_matching_album(mock_album)

        mock_mb_search.assert_called_once_with(limit=1, **search_criteria)
        assert mb_album == mb_rsrc.full_release.album

    def test_dont_search_if_mbid(self, mock_album):
        """Use ``mb_album_id`` to search by id if it exists."""
        mock_album.mb_album_id = "1"

        with patch(
            "moe.plugins.musicbrainz.mb_core.get_album_by_id",
        ) as mock_mb_by_id:
            moe_mb.get_matching_album(mock_album)

        mock_mb_by_id.assert_called_once_with(mock_album.mb_album_id)


class TestGetAlbumById:
    """Test `get_album_by_id()`.

    You can use the following code to print the result of a musicbrainz api query.

        def test_print_result(self):
            id = "3af9a6ca-c38a-41a7-a53c-32a97e869e8e"
            includes = ["artist-credits", "recordings"]
            print(musicbrainzngs.get_release_by_id(id, includes))
            assert 0

    Make sure to add any ``includes`` for whatever is needed for the test.
    """

    def test_album_search(self, mock_mb_by_id):
        """Searching for a release returns the expected album."""
        mb_album_id = "2fcfcaaa-6594-4291-b79f-2d354139e108"
        mock_mb_by_id.return_value = mb_rsrc.full_release.release

        mb_album = moe_mb.get_album_by_id(mb_album_id)

        mock_mb_by_id.assert_called_once_with(
            mb_album_id, includes=moe_mb.mb_core.RELEASE_INCLUDES
        )
        assert mb_album == mb_rsrc.full_release.album

    def test_partial_date_year_mon(self, mock_mb_by_id):
        """If given date is missing the day, default to 1."""
        mb_album_id = "112dec42-65f2-3bde-8d7d-26deddde10b2"
        mock_mb_by_id.return_value = mb_rsrc.partial_date.partial_date_year_mon

        mb_album = moe_mb.get_album_by_id(mb_album_id)

        assert mb_album.date == datetime.date(1992, 12, 1)

    def test_partial_date_year(self, mock_mb_by_id):
        """If given date is missing the day and month, default to 1 for each."""
        mb_album_id = "112dec42-65f2-3bde-8d7d-26deddde10b2"
        mock_mb_by_id.return_value = mb_rsrc.partial_date.partial_date_year

        mb_album = moe_mb.get_album_by_id(mb_album_id)

        assert mb_album.date == datetime.date(1992, 1, 1)

    def test_multi_disc_release(self, mock_mb_by_id):
        """We can add a release with multiple discs."""
        mb_album_id = "3af9a6ca-c38a-41a7-a53c-32a97e869e8e"
        mock_mb_by_id.return_value = mb_rsrc.multi_disc.release

        mb_album = moe_mb.get_album_by_id(mb_album_id)

        assert mb_album.disc_total == 2
        assert any(track.disc == 1 for track in mb_album.tracks)
        assert any(track.disc == 2 for track in mb_album.tracks)


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation."""

    def test_musicbrainz_core(self, tmp_config):
        """Enable the musicbrainz core plugin if specified in the config."""
        config = tmp_config(settings='default_plugins = ["musicbrainz"]')

        assert config.plugin_manager.has_plugin("musicbrainz_core")
