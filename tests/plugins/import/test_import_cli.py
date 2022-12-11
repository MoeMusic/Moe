"""Tests the import cli plugin."""

import datetime
from unittest.mock import Mock, patch

import pytest

import moe
import moe.cli
from moe import config
from moe.cli import console
from moe.config import ExtraPlugin
from moe.plugins import moe_import
from moe.plugins.moe_import.import_core import CandidateAlbum
from moe.util.cli import PromptChoice
from tests.conftest import album_factory, extra_factory, track_factory


@pytest.fixture
def _tmp_import_config(tmp_config):
    """A temporary config for the import plugin with the cli."""
    tmp_config('default_plugins = ["cli", "import"]')


class TestPrompt:
    """Test the import prompt."""

    def test_multi_disc_album(self, tmp_config, tmp_session):
        """Prompt supports multi_disc albums."""
        tmp_config("default_plugins = ['cli', 'import']", tmp_db=True)
        album = album_factory(num_discs=2)
        candidate = CandidateAlbum(
            album=album_factory(num_discs=2), match_value=1, source_str="Tests"
        )

        mock_choice = PromptChoice("mock", "m", moe_import.import_cli._apply_changes)
        with patch(
            "moe.plugins.moe_import.import_cli.choice_prompt",
            return_value=mock_choice,
            autospec=True,
        ):
            moe_import.import_cli.import_prompt(album, candidate)

        assert album.disc_total == 2
        assert album.get_track(1, disc=2)


class ImportPlugin:
    """Test plugin that implements the ``import_metadata`` hook for testing."""

    @staticmethod
    def change_title(old_album, new_album):
        """Change the albums title for testing."""
        old_album.title = "ImportPlugin"

    test_choice = PromptChoice(
        title="Test choice", shortcut_key="t", func=change_title.__func__
    )

    @staticmethod
    @moe.hookimpl
    def add_import_prompt_choice(prompt_choices):
        """Changes the album title."""
        prompt_choices.append(ImportPlugin.test_choice)


class TestHookSpecs:
    """Test the various plugin hook specifications."""

    def test_add_import_prompt_choice(self, tmp_config):
        """Plugins can add prompt choices to the import prompt."""
        album = album_factory()
        candidate = CandidateAlbum(
            album=album_factory(), match_value=1, source_str="tests"
        )
        album.title = "not ImportPlugin"
        tmp_config(
            "default_plugins = ['cli', 'import']",
            tmp_db=True,
            extra_plugins=[ExtraPlugin(ImportPlugin, "import_plugin")],
        )
        with patch(
            "moe.plugins.moe_import.import_cli.choice_prompt",
            return_value=ImportPlugin.test_choice,
            autospec=True,
        ):
            moe_import.import_cli.import_prompt(album, candidate)

        assert album.title == "ImportPlugin"


@pytest.mark.usefixtures("_tmp_import_config")
class TestProcessCandidates:
    """Test the `process_candidates` hook implementation."""

    def test_process_candidates(self):
        """The `candidate_prompt` should be used to process the candidate albums."""
        mock_new_album = Mock()
        mock_candidates = [Mock()]

        with patch(
            "moe.plugins.moe_import.import_cli.candidate_prompt", autospec=True
        ) as mock_candidate_prompt:
            config.CONFIG.pm.hook.process_candidates(
                new_album=mock_new_album,
                candidates=mock_candidates,
            )

        mock_candidate_prompt.assert_called_once_with(mock_new_album, mock_candidates)

    def test_abort_import(self):
        """Raise SystemExit if the import is aborted."""
        with patch(
            "moe.plugins.moe_import.import_cli.candidate_prompt",
            side_effect=moe_import.import_cli.AbortImport,
            autospec=True,
        ):
            with pytest.raises(SystemExit) as error:
                config.CONFIG.pm.hook.process_candidates(
                    new_album=Mock(), candidates=[Mock()]
                )

        assert error.value.code == 0

    def test_process_no_candidates(self):
        """Don't display the import prompt if there are no candidates to process."""
        with patch(
            "moe.plugins.moe_import.import_cli.candidate_prompt", autospec=True
        ) as mock_import_prompt:
            config.CONFIG.pm.hook.process_candidates(new_album=Mock(), candidates=[])

        mock_import_prompt.assert_not_called()


@pytest.mark.usefixtures("_tmp_import_config")
class TestAddImportPromptChoice:
    """Test the `add_import_prompt_choice` hook implementation."""

    def test_add_choices(self):
        """The apply and abort import prompt choices are added."""
        prompt_choices = []

        config.CONFIG.pm.hook.add_import_prompt_choice(prompt_choices=prompt_choices)

        assert len(prompt_choices) == 2
        assert any(choice.shortcut_key == "a" for choice in prompt_choices)
        assert any(choice.shortcut_key == "x" for choice in prompt_choices)

    def test_apply_tracks(self):
        """`apply` prompt choice should apply any matching Tracks.

        Missing and unmatched tracks should not be present in the final album.
        """
        album = album_factory()
        candidate = CandidateAlbum(
            album=album_factory(), match_value=1, source_str="test"
        )
        missing_track = track_factory(
            album=candidate.album, track_num=len(album.tracks) + 1
        )
        unmatched_track = track_factory(
            album=album, track_num=missing_track.track_num + 1
        )
        assert not album.get_track(missing_track.track_num)
        assert not candidate.album.get_track(unmatched_track.track_num)

        mock_choice = PromptChoice("mock", "m", moe_import.import_cli._apply_changes)
        with patch(
            "moe.plugins.moe_import.import_cli.choice_prompt",
            return_value=mock_choice,
            autospec=True,
        ):
            moe_import.import_cli.import_prompt(album, candidate)

        assert album.tracks
        assert not album.get_track(missing_track.track_num)
        assert not album.get_track(unmatched_track.track_num)

    def test_apply_diff_get_track(self):
        """Apply matches that don't have corresponding track and disc numbers.

        Track conflicts are defined by their track and disc on an album, and are the
        basis for determing how to merge tracks of an album. We should ensure that if
        two matching tracks don't conflict (i.e. matching track and disc numbers), that
        they can still merge properly.
        """
        album = album_factory(num_tracks=0)
        candidate = CandidateAlbum(
            album=album_factory(num_tracks=0), match_value=1, source_str="tests"
        )
        track_factory(album=album, track_num=1, title="old track 1")
        track_factory(album=candidate.album, track_num=1, title="new track 1")
        track_factory(album=album, track_num=2, title="old track 2")
        track_factory(album=candidate.album, track_num=2, title="new track 2")

        mock_choice = PromptChoice("mock", "m", moe_import.import_cli._apply_changes)
        mock_matches = [
            (album.get_track(1), candidate.album.get_track(2)),
            (album.get_track(2), candidate.album.get_track(1)),
        ]
        with patch(
            "moe.plugins.moe_import.import_cli.get_matching_tracks",
            return_value=mock_matches,
            autospec=True,
        ):
            with patch(
                "moe.plugins.moe_import.import_cli.choice_prompt",
                return_value=mock_choice,
                autospec=True,
            ):
                moe_import.import_cli.import_prompt(album, candidate)

        old_track1 = album.get_track(1)
        assert old_track1
        new_track1 = candidate.album.get_track(1)
        assert new_track1
        old_track2 = album.get_track(2)
        assert old_track2
        new_track2 = candidate.album.get_track(2)
        assert new_track2
        assert old_track1.title == new_track1.title
        assert old_track2.title == new_track2.title

    def test_apply_extras(self):
        """`apply` prompt choice should keep any extras."""
        album = album_factory()
        candidate = CandidateAlbum(
            album=album_factory(), match_value=1, source_str="tests"
        )
        new_extra = extra_factory(album=album)

        mock_choice = PromptChoice("mock", "m", moe_import.import_cli._apply_changes)
        with patch(
            "moe.plugins.moe_import.import_cli.choice_prompt",
            return_value=mock_choice,
            autospec=True,
        ):
            moe_import.import_cli.import_prompt(album, candidate)

        assert new_extra in album.extras

    def test_apply_fields(self):
        """Fields get applied onto the old album."""
        album = album_factory()
        candidate = CandidateAlbum(
            album=album_factory(title="new title"), match_value=1, source_str="tests"
        )
        assert album.title != candidate.album.title

        # new albums won't have paths
        candidate.album.path = None  # type: ignore
        for new_track in candidate.album.tracks:
            new_track.path = None  # type: ignore
        for new_extra in candidate.album.extras:
            new_extra.album = None  # type: ignore

        mock_choice = PromptChoice("mock", "m", moe_import.import_cli._apply_changes)
        with patch(
            "moe.plugins.moe_import.import_cli.choice_prompt",
            return_value=mock_choice,
            autospec=True,
        ):
            moe_import.import_cli.import_prompt(album, candidate)

        assert album.title == candidate.album.title
        assert album.path == album.path
        for track in album.tracks:
            assert track.path
        for extra in album.tracks:
            assert extra.path

    def test_abort(self):
        """The `abort` prompt choice should raise an AbortImport error."""
        album = album_factory()
        candidate = CandidateAlbum(
            album=album_factory(), match_value=1, source_str="tests"
        )

        mock_choice = PromptChoice("mock", "m", moe_import.import_cli._abort_changes)
        with patch(
            "moe.plugins.moe_import.import_cli.choice_prompt",
            return_value=mock_choice,
            autospec=True,
        ):
            with pytest.raises(moe_import.import_cli.AbortImport):
                moe_import.import_cli.import_prompt(album, candidate)

        assert album != candidate.album


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation."""

    def test_no_cli(self, tmp_config):
        """Don't enable the impot cli plugin if the `cli` plugin is not enabled."""
        tmp_config(settings='default_plugins = ["import"]')

        assert not config.CONFIG.pm.has_plugin("import_cli")

    def test_cli(self, tmp_config):
        """Enable the import cli plugin if the `cli` plugin is enabled."""
        tmp_config(settings='default_plugins = ["import", "cli"]')

        assert config.CONFIG.pm.has_plugin("import_cli")


class TestImportCLIOutput:
    """These tests exist as a convenience to view different changes to the import UI.

    To view the output from any of the tests, simply append an `assert 0` to the end of
    the test.

    Note:
        You will not see rich color with this approach unless you set
        `force_terminal=True` on the Console constructor in `cli.py`.
    """

    def test_full_diff_album(self):
        """Print prompt for fully different albums."""
        album = album_factory(num_tracks=6, num_discs=2, artist="outkist")
        candidate = CandidateAlbum(
            album=album_factory(
                title=album.title,
                date=datetime.date(1999, 12, 31),
                num_tracks=6,
                num_discs=2,
                country="US",
                media="CD",
                label="me",
            ),
            match_value=1,
            source_str="tests",
        )
        album.tracks[0].title = "really really long old title"

        assert album is not candidate.album

        console.print(moe_import.import_cli._fmt_import_updates(album, candidate))
