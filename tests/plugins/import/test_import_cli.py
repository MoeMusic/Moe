"""Tests the import cli plugin."""

import copy
import datetime
import random
from unittest.mock import Mock, patch

import pytest

import moe
import moe.cli
from moe.config import ExtraPlugin
from moe.library.album import Album
from moe.plugins import moe_import


class TestPrompt:
    """Test the import prompt."""

    def test_same_album(self, capsys, mock_album):
        """Don't do anything if no album changes."""
        new_album = copy.deepcopy(mock_album)
        assert mock_album is not new_album

        moe_import.import_prompt(Mock(), mock_album, new_album)

        captured_txt = capsys.readouterr()
        assert not captured_txt.out

    def test_partial_album_exists_merge(self, mock_album, tmp_config, tmp_session):
        """Merge existing tracks with those being added."""
        config = tmp_config("default_plugins = ['cli', 'import']", tmp_db=True)
        existing_album = copy.deepcopy(mock_album)
        new_album = copy.deepcopy(mock_album)
        existing_album.tracks.pop(0)
        mock_album.tracks.pop(1)
        tmp_session.add(existing_album)
        tmp_session.flush()

        with patch.object(moe_import.import_cli, "_get_input", return_value="a"):
            moe_import.import_prompt(config, mock_album, new_album)

        mock_album.merge(mock_album.get_existing())
        tmp_session.merge(mock_album)

        album = tmp_session.query(Album).one()
        assert len(album.tracks) == 2

    def test_multi_disc_album(self, mock_album, tmp_config, tmp_session):
        """Prompt supports multi_disc albums."""
        config = tmp_config("default_plugins = ['cli', 'import']", tmp_db=True)
        mock_album.disc_total = 2
        mock_album.tracks[1].disc = 2
        mock_album.tracks[1].track_num = 1
        new_album = copy.deepcopy(mock_album)

        with patch.object(moe_import.import_cli, "_get_input", return_value="a"):
            moe_import.import_prompt(config, mock_album, new_album)

        mock_album.merge(mock_album.get_existing())
        tmp_session.merge(mock_album)

        album = tmp_session.query(Album).one()
        assert album.disc_total == 2
        assert album.get_track(1, disc=2)


class TestFmtAlbumChanges:
    """Test formatting of album changes.

    These test cases aren't specifically testing what is output, as that
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

        print(moe_import.import_cli._fmt_album_changes(old_album, new_album))

    def test_unmatched_tracks(self, mock_album):
        """Print prompt for albums with non-matching tracks."""
        old_album = mock_album
        new_album = copy.deepcopy(mock_album)

        for track in old_album.tracks:
            track.track_num = random.randint(1, 1000)

        assert old_album is not new_album

        print(moe_import.import_cli._fmt_album_changes(old_album, new_album))

    def test_multi_disc_album(self, mock_album, mock_track_factory):
        """Prompt supports multi_disc albums."""
        mock_album.disc_total = 2
        mock_album.tracks[1].disc = 2
        mock_album.tracks[1].track_num = 1
        mock_track_factory(track_num=2, album=mock_album)
        new_album = copy.deepcopy(mock_album)

        print(moe_import.import_cli._fmt_album_changes(mock_album, new_album))


class ImportPlugin:
    """Test plugin that implements the ``import_metadata`` hook for testing."""

    @staticmethod
    @moe.hookimpl
    def add_import_prompt_choice(prompt_choices):
        """Changes the album title."""

        def test_choice(config, old_album, new_album):
            old_album.title = "ImportPlugin"

        prompt_choices.append(
            moe.cli.PromptChoice(
                title="Test choice", shortcut_key="t", func=test_choice
            )
        )


class TestHookSpecs:
    """Test the various plugin hook specifications."""

    def test_add_import_prompt_choice(self, mock_album, tmp_config):
        """Plugins can add prompt choices to the import prompt."""
        new_album = copy.deepcopy(mock_album)
        mock_album.title = "not ImportPlugin"
        config = tmp_config(
            "default_plugins = ['cli', 'import']",
            tmp_db=True,
            extra_plugins=[ExtraPlugin(ImportPlugin, "import_plugin")],
        )
        with patch.object(moe_import.import_cli, "_get_input", return_value="t"):
            moe_import.import_prompt(config, mock_album, new_album)

        assert mock_album.title == "ImportPlugin"


class TestProcessCandidates:
    """Test the `process_candidates` hook implementation."""

    def test_process_candidates(self, tmp_config):
        """The `import_prompt` should be used to process the candidate albums."""
        config = tmp_config("default_plugins = ['cli', 'import']")
        mock_old_album = Mock()
        mock_candidates = [Mock()]

        with patch(
            "moe.plugins.moe_import.import_cli.import_prompt"
        ) as mock_import_prompt:
            config.plugin_manager.hook.process_candidates(
                config=config, old_album=mock_old_album, candidates=mock_candidates
            )

        mock_import_prompt.assert_called_once_with(
            config, mock_old_album, mock_candidates[0]
        )

    def test_abort_import(self, tmp_config):
        """Raise SystemExit if the import is aborted."""
        config = tmp_config("default_plugins = ['cli', 'import']")

        with pytest.raises(SystemExit) as error:
            with patch.object(
                moe_import.import_cli,
                "import_prompt",
                side_effect=moe_import.AbortImport,
            ):
                config.plugin_manager.hook.process_candidates(
                    config=config,
                    old_album=Mock(),
                    candidates=[Mock()],
                )

        assert error.value.code != 0

    def test_process_no_candidates(self, tmp_config):
        """Don't display the import prompt if there are no candidates to process."""
        config = tmp_config("default_plugins = ['cli', 'import']")

        with patch(
            "moe.plugins.moe_import.import_cli.import_prompt"
        ) as mock_import_prompt:
            config.plugin_manager.hook.process_candidates(
                config=config, old_album=Mock(), candidates=[]
            )

        mock_import_prompt.assert_not_called()


class TestAddImportPromptChoice:
    """Test the `add_import_prompt_choice` hook implementation."""

    def test_add_choices(self, tmp_config):
        """The apply and abort import prompt choices are added."""
        config = tmp_config("default_plugins = ['cli', 'import']")
        prompt_choices = []

        config.plugin_manager.hook.add_import_prompt_choice(
            prompt_choices=prompt_choices
        )

        assert len(prompt_choices) == 2
        assert any(choice.shortcut_key == "a" for choice in prompt_choices)
        assert any(choice.shortcut_key == "x" for choice in prompt_choices)

    def test_apply(self, mock_album, tmp_config, tmp_session):
        """`apply` prompt choice should apply new album changes onto the old album."""
        config = tmp_config("default_plugins = ['cli', 'import']", tmp_db=True)
        new_album = copy.deepcopy(mock_album)
        new_album.title = "new title"
        assert mock_album.title != new_album.title

        # new albums won't have paths
        new_album.path = None
        for new_track in new_album.tracks:
            new_track.path = None
        for new_extra in new_album.extras:
            new_extra.album_obj = None

        with patch.object(moe_import.import_cli, "_get_input", return_value="a"):
            moe_import.import_prompt(config, mock_album, new_album)

        mock_album = tmp_session.merge(mock_album)
        assert mock_album.title == new_album.title
        assert mock_album.path == mock_album.path

        assert mock_album.tracks
        for added_track in mock_album.tracks:
            old_track = mock_album.get_track(added_track.track_num)
            assert added_track.path == old_track.path

        assert mock_album.extras

    def test_abort(self, mock_album, tmp_config):
        """The `abort` prompt choice should raise an AbortImport error."""
        config = tmp_config("default_plugins = ['cli', 'import']", tmp_db=True)
        new_album = copy.deepcopy(mock_album)
        new_album.title = "new title"
        assert mock_album.title != new_album.title

        with pytest.raises(moe_import.AbortImport):
            with patch.object(moe_import.import_cli, "_get_input", return_value="x"):
                moe_import.import_prompt(config, mock_album, new_album)

        assert mock_album.is_unique(new_album)


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation."""

    def test_no_cli(self, tmp_config):
        """Don't enable the edit cli plugin if the `cli` plugin is not enabled."""
        config = tmp_config(settings='default_plugins = ["edit"]')

        assert not config.plugin_manager.has_plugin("edit_cli")

    def test_cli(self, tmp_config):
        """Enable the edit cli plugin if the `cli` plugin is enabled."""
        config = tmp_config(settings='default_plugins = ["edit", "cli"]')

        assert config.plugin_manager.has_plugin("edit_cli")
