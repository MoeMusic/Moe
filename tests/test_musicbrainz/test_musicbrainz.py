"""Tests the musicbrainz plugin."""

import datetime
from unittest.mock import Mock, patch

import musicbrainzngs  # noqa: F401
import pytest

import tests.test_musicbrainz.resources as mb_rsrc
from moe import cli
from moe.core.library.album import Album
from moe.core.library.session import session_scope
from moe.plugins import musicbrainz
from moe.plugins.add import prompt


class TestImportAlbum:
    """Test the ``import_album()`` hook entry into the plugin."""


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

        mb_album = musicbrainz.get_matching_album(mock_album)

        # don't test every field since we can't actually guarantee the accuracy of
        # musicbrainz's search results every time
        assert mb_album.artist == mock_album.artist
        assert mb_album.title == mock_album.title

    def test_album_search(self, mock_album):
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
            return_value=mb_rsrc.full_release.search,
            autospec=True,
        ) as mock_mb_search:
            with patch(
                "moe.plugins.musicbrainz.musicbrainzngs.get_release_by_id",
                return_value=mb_rsrc.full_release.release,
                autospec=True,
            ):
                mb_album = musicbrainz.get_matching_album(mock_album)

        mock_mb_search.assert_called_once_with(limit=1, **search_criteria)
        assert mb_album == mb_rsrc.full_release.album

    def test_dont_search_if_mbid(self, mock_album):
        """Use ``mb_album_id`` to search by id if it exists."""
        mock_album.mb_album_id = "1"

        with patch(
            "moe.plugins.musicbrainz.get_album_by_id",
        ) as mock_mb_by_id:
            musicbrainz.get_matching_album(mock_album)

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

    def test_album_search(self):
        """Searching for a release returns the expected album."""
        mb_album_id = "2fcfcaaa-6594-4291-b79f-2d354139e108"

        with patch(
            "moe.plugins.musicbrainz.musicbrainzngs.get_release_by_id",
            return_value=mb_rsrc.full_release.release,
            autospec=True,
        ) as mock_mb_by_id:
            mb_album = musicbrainz.get_album_by_id(mb_album_id)

        mock_mb_by_id.assert_called_once_with(
            mb_album_id, includes=musicbrainz.RELEASE_INCLUDES
        )
        assert mb_album == mb_rsrc.full_release.album

    def test_partial_date_year_mon(self):
        """If given date is missing the day, default to 1."""
        mb_album_id = "112dec42-65f2-3bde-8d7d-26deddde10b2"

        with patch(
            "moe.plugins.musicbrainz.musicbrainzngs.get_release_by_id",
            return_value=mb_rsrc.partial_date.partial_date_year_mon,
            autospec=True,
        ):
            mb_album = musicbrainz.get_album_by_id(mb_album_id)

        assert mb_album.date == datetime.date(1992, 12, 1)

    def test_partial_date_year(self):
        """If given date is missing the day and month, default to 1 for each."""
        mb_album_id = "112dec42-65f2-3bde-8d7d-26deddde10b2"

        with patch(
            "moe.plugins.musicbrainz.musicbrainzngs.get_release_by_id",
            return_value=mb_rsrc.partial_date.partial_date_year,
            autospec=True,
        ):
            mb_album = musicbrainz.get_album_by_id(mb_album_id)

        assert mb_album.date == datetime.date(1992, 1, 1)

    def test_multi_disc_release(self):
        """We can add a release with multiple discs."""
        mb_album_id = "3af9a6ca-c38a-41a7-a53c-32a97e869e8e"

        with patch(
            "moe.plugins.musicbrainz.musicbrainzngs.get_release_by_id",
            return_value=mb_rsrc.multi_disc.release,
            autospec=True,
        ):
            mb_album = musicbrainz.get_album_by_id(mb_album_id)

        assert mb_album.disc_total == 2
        assert any(track.disc == 1 for track in mb_album.tracks)
        assert any(track.disc == 2 for track in mb_album.tracks)


@patch(
    "moe.plugins.musicbrainz.musicbrainzngs.search_releases",
    return_value=mb_rsrc.full_release.search,
    autospec=True,
)
@patch(
    "moe.plugins.musicbrainz.musicbrainzngs.get_release_by_id",
    return_value=mb_rsrc.full_release.release,
    autospec=True,
)
@pytest.mark.integration
class TestAdd:
    """Test integration with the add plugin."""

    def test_album(self, mock_mb_by_id, mock_mb_search, real_album, tmp_config):
        """We can import and add an album to the library."""
        cli_args = ["add", str(real_album.path)]
        config = tmp_config(settings='default_plugins = ["add", "musicbrainz"]')

        mock_q = Mock()
        mock_q.ask.return_value = prompt._apply_changes
        with patch("moe.plugins.add.prompt.questionary.rawselect", return_value=mock_q):
            cli.main(cli_args, config)

        ref_album = mb_rsrc.full_release.album
        with session_scope() as session:
            db_album = session.query(Album).one()

            assert db_album.artist == ref_album.artist
            assert db_album.date == ref_album.date
            assert db_album.mb_album_id == ref_album.mb_album_id
            assert db_album.title == ref_album.title

    def test_prompt_choice(self, mock_mb_by_id, mock_mb_search, real_album, tmp_config):
        """We can search from user input."""
        cli_args = ["add", str(real_album.path)]
        config = tmp_config(settings='default_plugins = ["add", "musicbrainz"]')

        mock_q = Mock()
        mock_q.ask.side_effect = [musicbrainz._enter_id, prompt._apply_changes]
        with patch("moe.plugins.add.prompt.questionary.rawselect", return_value=mock_q):
            mock_q = Mock()
            mock_q.ask.return_value = "new id"
            with patch("moe.plugins.add.prompt.questionary.text", return_value=mock_q):
                cli.main(cli_args, config)

        mock_mb_by_id.assert_called_with(
            "new id", includes=musicbrainz.RELEASE_INCLUDES
        )

        ref_album = mb_rsrc.full_release.album
        with session_scope() as session:
            db_album = session.query(Album).one()

            assert db_album.artist == ref_album.artist
            assert db_album.date == ref_album.date
            assert db_album.mb_album_id == ref_album.mb_album_id
            assert db_album.title == ref_album.title
