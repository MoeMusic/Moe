"""Tests the import cli plugin."""

import copy
from unittest.mock import Mock, patch

import pytest

import moe
import moe.cli
from moe.config import Config, ExtraPlugin
from moe.plugins import moe_import


@pytest.fixture
def tmp_import_config(tmp_config) -> Config:
    """A temporary config for the import plugin with the cli."""
    return tmp_config('default_plugins = ["cli", "import"]')


class TestPrompt:
    """Test the import prompt."""

    def test_same_album(self, capsys, mock_album):
        """Don't do anything if no album changes."""
        new_album = copy.deepcopy(mock_album)
        assert mock_album is not new_album

        moe_import.import_prompt(Mock(), mock_album, new_album)

        captured_txt = capsys.readouterr()
        assert not captured_txt.out

    def test_multi_disc_album(self, mock_album, tmp_config, tmp_session):
        """Prompt supports multi_disc albums."""
        config = tmp_config("default_plugins = ['cli', 'import']", tmp_db=True)
        mock_album.disc_total = 2
        mock_album.tracks[1].disc = 2
        mock_album.tracks[1].track_num = 1
        new_album = copy.deepcopy(mock_album)

        mock_choice = moe.cli.PromptChoice(
            "mock", "m", moe_import.import_cli._apply_changes
        )
        with patch.object(moe.cli, "choice_prompt", return_value=mock_choice):
            moe_import.import_prompt(config, mock_album, new_album)

        assert mock_album.disc_total == 2
        assert mock_album.get_track(1, disc=2)


class ImportPlugin:
    """Test plugin that implements the ``import_metadata`` hook for testing."""

    @staticmethod
    def change_title(config, old_album, new_album):
        """Change the albums title for testing."""
        old_album.title = "ImportPlugin"

    test_choice = moe.cli.PromptChoice(
        title="Test choice", shortcut_key="t", func=change_title.__func__
    )

    @staticmethod
    @moe.hookimpl
    def add_import_prompt_choice(prompt_choices):
        """Changes the album title."""
        prompt_choices.append(ImportPlugin.test_choice)


class TestHookSpecs:
    """Test the various plugin hook specifications."""

    def test_add_import_prompt_choice(self, mock_album_factory, tmp_config):
        """Plugins can add prompt choices to the import prompt."""
        old_album = mock_album_factory()
        new_album = mock_album_factory()
        old_album.title = "not ImportPlugin"
        config = tmp_config(
            "default_plugins = ['cli', 'import']",
            tmp_db=True,
            extra_plugins=[ExtraPlugin(ImportPlugin, "import_plugin")],
        )
        with patch.object(
            moe.cli, "choice_prompt", return_value=ImportPlugin.test_choice
        ):
            moe_import.import_prompt(config, old_album, new_album)

        assert old_album.title == "ImportPlugin"


class TestProcessCandidates:
    """Test the `process_candidates` hook implementation."""

    def test_process_candidates(self, tmp_import_config):
        """The `import_prompt` should be used to process the candidate albums."""
        mock_old_album = Mock()
        mock_candidates = [Mock()]

        with patch(
            "moe.plugins.moe_import.import_cli.import_prompt"
        ) as mock_import_prompt:
            tmp_import_config.plugin_manager.hook.process_candidates(
                config=tmp_import_config,
                old_album=mock_old_album,
                candidates=mock_candidates,
            )

        mock_import_prompt.assert_called_once_with(
            tmp_import_config, mock_old_album, mock_candidates[0]
        )

    def test_abort_import(self, tmp_import_config):
        """Raise SystemExit if the import is aborted."""
        with patch.object(
            moe_import.import_cli,
            "import_prompt",
            side_effect=moe_import.AbortImport,
        ):
            with pytest.raises(SystemExit) as error:
                tmp_import_config.plugin_manager.hook.process_candidates(
                    config=tmp_import_config,
                    old_album=Mock(),
                    candidates=[Mock()],
                )

        assert error.value.code == 0

    def test_process_no_candidates(self, tmp_import_config):
        """Don't display the import prompt if there are no candidates to process."""
        with patch(
            "moe.plugins.moe_import.import_cli.import_prompt"
        ) as mock_import_prompt:
            tmp_import_config.plugin_manager.hook.process_candidates(
                config=tmp_import_config, old_album=Mock(), candidates=[]
            )

        mock_import_prompt.assert_not_called()


class TestAddImportPromptChoice:
    """Test the `add_import_prompt_choice` hook implementation."""

    def test_add_choices(self, tmp_import_config):
        """The apply and abort import prompt choices are added."""
        prompt_choices = []

        tmp_import_config.plugin_manager.hook.add_import_prompt_choice(
            prompt_choices=prompt_choices
        )

        assert len(prompt_choices) == 2
        assert any(choice.shortcut_key == "a" for choice in prompt_choices)
        assert any(choice.shortcut_key == "x" for choice in prompt_choices)

    def test_apply_tracks(
        self, mock_album_factory, mock_track_factory, tmp_import_config
    ):
        """`apply` prompt choice should apply any matching Tracks.

        Missing and unmatched tracks should not be present in the final album.
        """
        old_album = mock_album_factory()
        new_album = mock_album_factory()
        missing_track = mock_track_factory(
            album=new_album, track_num=len(old_album.tracks) + 1
        )
        unmatched_track = mock_track_factory(
            album=old_album, track_num=missing_track.track_num + 1
        )
        assert not old_album.get_track(missing_track.track_num)
        assert not new_album.get_track(unmatched_track.track_num)

        mock_choice = moe.cli.PromptChoice(
            "mock", "m", moe_import.import_cli._apply_changes
        )
        with patch.object(moe.cli, "choice_prompt", return_value=mock_choice):
            moe_import.import_prompt(tmp_import_config, old_album, new_album)

        assert old_album.tracks
        assert not old_album.get_track(missing_track.track_num)
        assert not old_album.get_track(unmatched_track.track_num)

    def test_apply_diff_get_track(
        self, mock_album_factory, mock_track_factory, tmp_import_config
    ):
        """Apply matches that don't have corresponding track and disc numbers.

        Track conflicts are defined by their track and disc on an album, and are the
        basis for determing how to merge tracks of an album. We should ensure that if
        two matching tracks don't conflict (i.e. matching track and disc numbers), that
        they can still merge properly.
        """

        def mock_get_match_value(track_a, track_b, field_weights) -> float:
            """Match tracks with different track and disc numbers."""
            if track_a.track_num == 1 and track_b.track_num == 2:
                return 1
            elif track_a.track_num == 2 and track_b.track_num == 1:
                return 1
            return 0

        old_album = mock_album_factory()
        new_album = mock_album_factory()
        old_album.get_track(1).title = "old track 1"
        new_album.get_track(1).title = "new track 1"
        old_album.get_track(2).title = "old track 2"
        new_album.get_track(2).title = "new track 2"

        org_path1 = old_album.get_track(1).path  # will become track 2
        org_path2 = old_album.get_track(2).path  # will become track 1

        mock_choice = moe.cli.PromptChoice(
            "mock", "m", moe_import.import_cli._apply_changes
        )
        with patch("moe.plugins.add.match.get_match_value", wraps=mock_get_match_value):
            with patch.object(moe.cli, "choice_prompt", return_value=mock_choice):
                moe_import.import_prompt(tmp_import_config, old_album, new_album)

        assert old_album.get_track(1).title == "new track 1"
        assert old_album.get_track(2).title == "new track 2"
        assert old_album.get_track(1).path == org_path2
        assert old_album.get_track(2).path == org_path1

    def test_apply_extras(self, mock_album, mock_extra_factory, tmp_import_config):
        """`apply` prompt choice should keep any extras."""
        new_album = copy.deepcopy(mock_album)
        new_extra = mock_extra_factory(album=mock_album)

        mock_choice = moe.cli.PromptChoice(
            "mock", "m", moe_import.import_cli._apply_changes
        )
        with patch.object(moe.cli, "choice_prompt", return_value=mock_choice):
            moe_import.import_prompt(tmp_import_config, mock_album, new_album)

        assert new_extra in mock_album.extras

    def test_apply_fields(self, mock_album, tmp_import_config):
        """Fields get applied onto the old album."""
        new_album = copy.deepcopy(mock_album)
        new_album.title = "new title"
        assert mock_album.title != new_album.title

        # new albums won't have paths
        new_album.path = None
        for new_track in new_album.tracks:
            new_track.path = None
        for new_extra in new_album.extras:
            new_extra.album_obj = None

        mock_choice = moe.cli.PromptChoice(
            "mock", "m", moe_import.import_cli._apply_changes
        )
        with patch.object(moe.cli, "choice_prompt", return_value=mock_choice):
            moe_import.import_prompt(tmp_import_config, mock_album, new_album)

        assert mock_album.title == new_album.title
        assert mock_album.path == mock_album.path
        for track in mock_album.tracks:
            assert track.path
        for extra in mock_album.tracks:
            assert extra.path

    def test_abort(self, mock_album_factory, tmp_import_config):
        """The `abort` prompt choice should raise an AbortImport error."""
        album1 = mock_album_factory()
        album2 = mock_album_factory()
        album1.mb_album_id = "1234"
        assert album1.mb_album_id != album2.mb_album_id

        mock_choice = moe.cli.PromptChoice(
            "mock", "m", moe_import.import_cli._abort_changes
        )
        with patch.object(moe.cli, "choice_prompt", return_value=mock_choice):
            with pytest.raises(moe_import.AbortImport):
                moe_import.import_prompt(tmp_import_config, album1, album2)

        assert album1 != album2


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation."""

    def test_no_cli(self, tmp_config):
        """Don't enable the impot cli plugin if the `cli` plugin is not enabled."""
        config = tmp_config(settings='default_plugins = ["import"]')

        assert not config.plugin_manager.has_plugin("import_cli")

    def test_cli(self, tmp_config):
        """Enable the import cli plugin if the `cli` plugin is enabled."""
        config = tmp_config(settings='default_plugins = ["import", "cli"]')

        assert config.plugin_manager.has_plugin("import_cli")
