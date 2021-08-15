"""Tests the add plugin interactive prompt."""

import copy
import datetime
import random
from unittest.mock import MagicMock, Mock, patch

import pytest
from sqlalchemy.orm.session import Session

import moe
from moe.core.config import Config
from moe.core.library.album import Album
from moe.core.library.session import session_scope
from moe.plugins import moe_import


class ImportPlugin:
    """Test plugin that implements the ``import_metadata`` hook for testing."""

    @staticmethod
    @moe.hookimpl
    def import_candidates(config: Config, session: Session, album: Album) -> Album:
        """Changes the album title."""
        album.title = "pre-add plugin"
        return album


class TestPrompt:
    """Test the import prompt."""

    def test_same_album(self, capsys, mock_album):
        """Don't do anything if no album changes."""
        new_album = copy.deepcopy(mock_album)
        assert mock_album is not new_album

        moe_import.import_prompt(Mock(), Mock(), mock_album, new_album)

        captured_txt = capsys.readouterr()
        assert not captured_txt.out

    def test_apply_changes(self, mock_album, tmp_config, tmp_session):
        """If selected, apply the changes to the old album."""
        config = tmp_config("default_plugins = ['import']")
        new_album = copy.deepcopy(mock_album)
        new_album.title = "new title"
        assert mock_album.title != new_album.title

        # new albums won't have paths
        new_album.path = None
        for new_track in new_album.tracks:
            new_track.path = None
        for new_extra in new_album.extras:
            new_extra.album_obj = None

        mock_q = Mock()
        mock_q.ask.return_value = moe_import.import_cli._apply_changes
        with patch(
            "moe.plugins.moe_import.import_cli.questionary.rawselect",
            return_value=mock_q,
        ):
            moe_import.import_prompt(config, tmp_session, mock_album, new_album)

        mock_album = tmp_session.merge(mock_album)
        assert mock_album.title == new_album.title
        assert mock_album.path == mock_album.path

        assert mock_album.tracks
        for added_track in mock_album.tracks:
            old_track = mock_album.get_track(added_track.track_num)
            assert added_track.path == old_track.path

        assert mock_album.extras

    def test_abort_changes(self, mock_album, tmp_config):
        """If selected, abort the changes to the old album."""
        config = tmp_config("default_plugins = ['import']")
        new_album = copy.deepcopy(mock_album)
        new_album.title = "new title"
        assert mock_album.title != new_album.title

        mock_q = Mock()
        mock_q.ask.return_value = moe_import.import_cli._abort_changes
        with patch(
            "moe.plugins.moe_import.import_cli.questionary.rawselect",
            return_value=mock_q,
        ):
            with pytest.raises(moe_import.AbortImport):
                moe_import.import_prompt(config, MagicMock(), mock_album, new_album)

        assert mock_album.is_unique(new_album)

    def test_partial_album_exists_merge(self, mock_album, tmp_config, tmp_session):
        """Merge existing tracks with those being added."""
        config = tmp_config("default_plugins = ['import']")
        existing_album = copy.deepcopy(mock_album)
        new_album = copy.deepcopy(mock_album)
        existing_album.tracks.pop(0)
        mock_album.tracks.pop(1)
        tmp_session.add(existing_album)
        tmp_session.commit()

        mock_q = Mock()
        mock_q.ask.return_value = moe_import.import_cli._apply_changes
        with patch(
            "moe.plugins.moe_import.import_cli.questionary.rawselect",
            return_value=mock_q,
        ):
            moe_import.import_prompt(config, tmp_session, mock_album, new_album)

        mock_album.merge(mock_album.get_existing(tmp_session))
        tmp_session.merge(mock_album)

        album = tmp_session.query(Album).one()
        assert len(album.tracks) == 2

    def test_multi_disc_album(self, mock_album, tmp_config, tmp_session):
        """Prompt supports multi_disc albums."""
        config = tmp_config("default_plugins = ['import']")
        mock_album.disc_total = 2
        mock_album.tracks[1].disc = 2
        mock_album.tracks[1].track_num = 1
        new_album = copy.deepcopy(mock_album)

        mock_q = Mock()
        mock_q.ask.return_value = moe_import.import_cli._apply_changes
        with patch(
            "moe.plugins.moe_import.import_cli.questionary.rawselect",
            return_value=mock_q,
        ):
            moe_import.import_prompt(config, MagicMock(), mock_album, new_album)

        mock_album.merge(mock_album.get_existing(tmp_session))
        tmp_session.merge(mock_album)

        album = tmp_session.query(Album).one()
        assert album.disc_total == 2
        assert album.get_track(1, disc=2)


class TestFmtAlbumChanges:
    """Test formatting of album changes.

    Some of these test cases aren't specifically testing what is output, as that
    is more of an implementation detail and harder to test than it's worth. Rather,
    these test cases are used to help see what is being printed for various scenarios
    (add ``assert 0`` to the end of any test case to see it's output to stdout).
    """

    def test_full_diff_album(self, mock_album):
        """Print prompt for fully different albums."""
        old_album = mock_album
        new_album = copy.deepcopy(mock_album)
        old_album.tracks[0].title = "really really long old title"
        new_album.title = "new title"
        new_album.artist = "new artist"
        new_album.date = datetime.date(1999, 12, 31)
        new_album.mb_album_id = "1234"

        for track in new_album.tracks:
            track.title = "new title"

        assert old_album is not new_album

        print(  # noqa: WPS421
            moe_import.import_cli._fmt_album_changes(old_album, new_album)
        )

    def test_unmatched_tracks(self, mock_album):
        """Print prompt for albums with non-matching tracks."""
        old_album = mock_album
        new_album = copy.deepcopy(mock_album)

        for track in old_album.tracks:
            track.track_num = random.randint(1, 1000)

        assert old_album is not new_album

        print(  # noqa: WPS421
            moe_import.import_cli._fmt_album_changes(old_album, new_album)
        )

    def test_multi_disc_album(self, mock_album):
        """Prompt supports multi_disc albums."""
        mock_album.disc_total = 2
        mock_album.tracks[1].disc = 2
        mock_album.tracks[1].track_num = 1
        new_album = copy.deepcopy(mock_album)

        print(  # noqa: WPS421
            moe_import.import_cli._fmt_album_changes(mock_album, new_album)
        )


@pytest.mark.integration
class TestImportAlbum:
    """Test integration with the ``import_album`` hook and thus the add prompt."""

    def test_album(self, real_album, tmp_config):
        """Prompt is run with a plugin implementing the ``import_album`` hook."""
        cli_args = ["add", str(real_album.path)]
        config = tmp_config(settings='default_plugins = ["add", "cli", "import"]')
        config.plugin_manager.register(ImportPlugin)

        mock_q = Mock()
        mock_q.ask.return_value = moe_import.import_cli._apply_changes
        with patch(
            "moe.plugins.moe_import.import_cli.questionary.rawselect",
            return_value=mock_q,
        ):
            moe.cli.main(cli_args, config)

        with session_scope() as session:
            album = session.query(Album).one()
            assert album.title == "pre-add plugin"
