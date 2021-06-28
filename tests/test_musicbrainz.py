"""Tests the musicbrainz plugin."""

import datetime
import operator
from unittest.mock import Mock, patch

import pytest

import tests.resources.musicbrainz.edge as mb_edge
import tests.resources.musicbrainz.full_release as mb_full_release
from moe import cli
from moe.core.library.album import Album
from moe.core.library.session import session_scope
from moe.plugins import musicbrainz


class TestPreAdd:
    """Test the ``import_album()`` hook entry into the plugin."""

    def test_release_search(self, mock_album):
        """Searching for a release uses the expected parameters."""
        mock_album.artist = "Kanye West"
        mock_album.title = "My Beautiful Dark Twisted Fantasy"
        mock_album.date = datetime.date(2010, 11, 22)
        search_criteria = {
            "artist": "Kanye West",
            "release": "My Beautiful Dark Twisted Fantasy",
            "date": "2010-11-22",
        }

        with patch(
            "moe.plugins.musicbrainz.musicbrainzngs.search_releases",
            return_value=mb_full_release.search,
            autospec=True,
        ) as mock_mb_search:
            with patch(
                "moe.plugins.musicbrainz.musicbrainzngs.get_release_by_id",
                return_value=mb_full_release.release,
                autospec=True,
            ):
                musicbrainz.import_album(Mock(), Mock(), mock_album)

        mock_mb_search.assert_called_once_with(limit=1, **search_criteria)

    def test_dont_search_if_mbid(self, mock_album):
        """Use ``mb_id`` if it exists."""
        mock_album.mb_id = "1"
        with patch(
            "moe.plugins.musicbrainz.musicbrainzngs.get_release_by_id",
            return_value=mb_full_release.release,
            autospec=True,
        ) as mock_mb_by_id:
            musicbrainz.import_album(Mock(), Mock(), mock_album)

        mock_mb_by_id.assert_called_once_with(
            mock_album.mb_id, includes=musicbrainz.RELEASE_INCLUDES
        )

    def test_return_album(self):
        """An Album with all the updated musicbrainz info is returned."""
        with patch(
            "moe.plugins.musicbrainz.musicbrainzngs.search_releases",
            return_value=mb_full_release.search,
            autospec=True,
        ):
            with patch(
                "moe.plugins.musicbrainz.musicbrainzngs.get_release_by_id",
                return_value=mb_full_release.release,
                autospec=True,
            ):
                mb_album = musicbrainz.import_album(Mock(), Mock(), Mock())

        assert mb_album.artist == "Kanye West"
        assert mb_album.date == datetime.date(2010, 11, 22)
        assert mb_album.mb_id == "2fcfcaaa-6594-4291-b79f-2d354139e108"
        assert mb_album.title == "My Beautiful Dark Twisted Fantasy"

        mb_album.tracks.sort(key=operator.attrgetter("track_num"))
        for track_num, track in enumerate(mb_album.tracks, start=1):
            assert track.track_num == track_num

            if track_num == 2:
                assert track.artist == "Kanye West feat. Kid Cudi & Raekwon"
                assert track.mb_id == "b3c6aa0a-6960-4db6-bf27-ed50de88309c"
                assert track.title == "Gorgeous"

    def test_partial_date_year_mon(self, mock_album):
        """If given date is missing the day, default to 1."""
        mock_album.mb_id = "112dec42-65f2-3bde-8d7d-26deddde10b2"
        with patch(
            "moe.plugins.musicbrainz.musicbrainzngs.get_release_by_id",
            return_value=mb_edge.partial_date_year_mon,
            autospec=True,
        ):
            mb_album = musicbrainz.import_album(Mock(), Mock(), mock_album)

        assert mb_album.date == datetime.date(1992, 12, 1)

    def test_partial_date_year(self, mock_album):
        """If given date is missing the day and month, default to 1 for each."""
        mock_album.mb_id = "112dec42-65f2-3bde-8d7d-26deddde10b2"
        with patch(
            "moe.plugins.musicbrainz.musicbrainzngs.get_release_by_id",
            return_value=mb_edge.partial_date_year,
            autospec=True,
        ):
            mb_album = musicbrainz.import_album(Mock(), Mock(), mock_album)

        assert mb_album.date == datetime.date(1992, 1, 1)


@pytest.mark.network
class TestNetwork:
    """Test we can hit the actual API."""

    def test_real_import_album(self, mock_album):
        """Make sure we can actually hit the real API."""
        mock_album.artist = "Kanye West"
        mock_album.title = "My Beautiful Dark Twisted Fantasy"

        mb_album = musicbrainz.import_album(Mock(), Mock(), mock_album)

        assert mb_album.artist == mock_album.artist
        assert mb_album.title == mock_album.title


@patch(
    "moe.plugins.musicbrainz.musicbrainzngs.search_releases",
    return_value=mb_full_release.search,
    autospec=True,
)
@patch(
    "moe.plugins.musicbrainz.musicbrainzngs.get_release_by_id",
    return_value=mb_full_release.release,
    autospec=True,
)
@pytest.mark.integration
class TestAdd:
    """Test integration with the add plugin."""

    def test_album(self, mock_mb_by_id, mock_mb_search, real_album, tmp_config):
        """We can import and add an album to the library."""
        cli_args = ["add", str(real_album.path)]
        config = tmp_config(settings='default_plugins = ["add", "musicbrainz"]')

        with patch("builtins.input", lambda _: "a"):  # apply changes
            cli.main(cli_args, config)

        with session_scope() as session:
            album = session.query(Album).one()

            assert album.artist == "Kanye West"
            assert album.date == datetime.date(2010, 11, 22)
            assert album.mb_id == "2fcfcaaa-6594-4291-b79f-2d354139e108"
            assert album.title == "My Beautiful Dark Twisted Fantasy"
