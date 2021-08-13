"""Test the musicbrainz cli plugin."""

from unittest.mock import Mock, patch

import pytest

import tests.test_musicbrainz.resources as mb_rsrc
from moe import cli
from moe.core.library.album import Album
from moe.core.library.session import session_scope
from moe.plugins import moe_import
from moe.plugins import musicbrainz as moe_mb


@patch(
    "moe.plugins.musicbrainz.mb_core.musicbrainzngs.search_releases",
    return_value=mb_rsrc.full_release.search,
    autospec=True,
)
@patch(
    "moe.plugins.musicbrainz.mb_core.musicbrainzngs.get_release_by_id",
    return_value=mb_rsrc.full_release.release,
    autospec=True,
)
@pytest.mark.integration
class TestAdd:
    """Test integration with the add plugin."""

    def test_album(self, mock_mb_by_id, mock_mb_search, real_album, tmp_config):
        """We can import and add an album to the library."""
        cli_args = ["add", str(real_album.path)]
        config = tmp_config(
            settings='default_plugins = ["add", "cli", "import", "musicbrainz"]'
        )

        mock_q = Mock()
        mock_q.ask.return_value = moe_import.import_cli._apply_changes
        with patch(
            "moe.plugins.moe_import.import_cli.questionary.rawselect",
            return_value=mock_q,
        ):
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
        config = tmp_config(
            settings='default_plugins = ["add", "cli", "import", "musicbrainz"]'
        )

        mock_q = Mock()
        mock_q.ask.side_effect = [
            moe_mb.mb_cli._enter_id,
            moe_import.import_cli._apply_changes,
        ]
        with patch(
            "moe.plugins.moe_import.import_cli.questionary.rawselect",
            return_value=mock_q,
        ):
            mock_q = Mock()
            mock_q.ask.return_value = "new id"
            with patch(
                "moe.plugins.moe_import.import_cli.questionary.text",
                return_value=mock_q,
            ):
                cli.main(cli_args, config)

        mock_mb_by_id.assert_called_with(
            "new id", includes=moe_mb.mb_core.RELEASE_INCLUDES
        )

        ref_album = mb_rsrc.full_release.album
        with session_scope() as session:
            db_album = session.query(Album).one()

            assert db_album.artist == ref_album.artist
            assert db_album.date == ref_album.date
            assert db_album.mb_album_id == ref_album.mb_album_id
            assert db_album.title == ref_album.title
