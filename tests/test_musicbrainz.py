"""Tests the musicbrainz plugin."""

import datetime
import operator
from unittest.mock import Mock, patch

import pytest

import tests.resources.musicbrainz.edge as mb_edge
import tests.resources.musicbrainz.full_release as mb_full_release
from moe import cli as moe_cli
from moe.core.library.album import Album
from moe.core.library.session import session_scope
from moe.plugins import musicbrainz


@pytest.fixture
def mock_mb_album(mock_album) -> Album:
    """Creates a specific musicbrainz album for testing from a ``mock_album``.

    Defines the fields we want to use for musicbrainz API queries so we can safely
    mock the API without worrying about changes to ``mock_album``.

    Returns:
        Updated mock album.
    """
    mock_album.artist = "Kanye West"
    mock_album.title = "My Beautiful Dark Twisted Fantasy"
    mock_album.date = datetime.date(2010, 11, 22)

    return mock_album


class TestPreAdd:
    """Test the ``pre_add()`` hook entry into the plugin."""

    def test_release_search(self, mock_mb_album):
        """Searching for a release uses the expected parameters."""
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
                musicbrainz.pre_add(Mock(), Mock(), mock_mb_album)

        mock_mb_search.assert_called_once_with(limit=1, **search_criteria)

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
                mb_album = musicbrainz.pre_add(Mock(), Mock(), Mock())

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

    def test_partial_date_year_mon(self):
        """If given date is missing the day, default to 1."""
        with patch(
            "moe.plugins.musicbrainz.musicbrainzngs.search_releases",
            return_value=mb_edge.search,
            autospec=True,
        ):
            with patch(
                "moe.plugins.musicbrainz.musicbrainzngs.get_release_by_id",
                return_value=mb_edge.partial_date_year_mon,
                autospec=True,
            ):
                mb_album = musicbrainz.pre_add(Mock(), Mock(), Mock())

        assert mb_album.date == datetime.date(1992, 12, 1)

    def test_partial_date_year(self):
        """If given date is missing the day and month, default to 1 for each."""
        with patch(
            "moe.plugins.musicbrainz.musicbrainzngs.search_releases",
            return_value=mb_edge.search,
            autospec=True,
        ):
            with patch(
                "moe.plugins.musicbrainz.musicbrainzngs.get_release_by_id",
                return_value=mb_edge.partial_date_year,
                autospec=True,
            ):
                mb_album = musicbrainz.pre_add(Mock(), Mock(), Mock())

        assert mb_album.date == datetime.date(1992, 1, 1)


@pytest.mark.network
class TestNetwork:
    """Test we can hit the actual API."""

    def test_pre_add(self, mock_mb_album):
        """Make sure we can actually hit the real API."""
        mb_album = musicbrainz.pre_add(Mock(), Mock(), mock_mb_album)

        assert mb_album.artist == mock_mb_album.artist
        assert mb_album.title == mock_mb_album.title
        assert mb_album.date == mock_mb_album.date


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
        cli_args = ["moe", "add", str(real_album.path)]
        config = tmp_config(settings='default_plugins = ["add", "musicbrainz"]')

        with patch("sys.argv", cli_args):
            with patch("moe.cli.Config", return_value=config):
                with patch("builtins.input", lambda _: "a"):  # apply changes
                    moe_cli.main()

        with session_scope() as session:
            album = session.query(Album).one()

            assert album.artist == "Kanye West"
            assert album.date == datetime.date(2010, 11, 22)
            assert album.mb_id == "2fcfcaaa-6594-4291-b79f-2d354139e108"
            assert album.title == "My Beautiful Dark Twisted Fantasy"
