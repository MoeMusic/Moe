"""Tests the add plugin."""

from types import FunctionType
from typing import Iterator
from unittest.mock import patch

import pytest

import moe
import moe.cli
from moe import config
from moe.library import Album, Track
from moe.plugins.add import add_cli
from moe.plugins.moe_import.import_core import CandidateAlbum
from moe.util.cli import PromptChoice
from tests.conftest import album_factory, extra_factory, track_factory


@pytest.fixture
def mock_add() -> Iterator[FunctionType]:
    """Mock the `add_item()` api call."""
    with patch("moe.plugins.add.add_item", autospec=True) as mock_add:
        yield mock_add


@pytest.fixture
def mock_query() -> Iterator[FunctionType]:
    """Mock a database query call.

    Use ``mock_query.return_value` to set the return value of a query.

    Yields:
        Mock query
    """
    with patch("moe.plugins.add.add_cli.cli_query", autospec=True) as mock_query:
        yield mock_query


@pytest.fixture
def _tmp_add_config(tmp_config):
    """A temporary config for the add plugin with the cli."""
    tmp_config('default_plugins = ["cli", "add", "write"]')


class AddCLIPlugin:
    """Imports fake candidates to test the import prompt hook."""

    @staticmethod
    @moe.hookimpl
    def get_candidates(album: Album) -> list[CandidateAlbum]:
        """Return a fake candidate for testing."""
        return [CandidateAlbum(album=album, match_value=1, source_str="add plugin")]


@pytest.mark.usefixtures("_tmp_add_config")
class TestAddImportPromptChoice:
    """Test the `add_import_prompt_choice` hook implementation."""

    def test_add_choice(self):
        """The "s" key to skip adding an item is added."""
        prompt_choices = []

        config.CONFIG.pm.hook.add_import_prompt_choice(prompt_choices=prompt_choices)

        assert any(choice.shortcut_key == "s" for choice in prompt_choices)

    def test_skip_item(self, tmp_config):
        """We can skip adding items to the library."""
        tmp_config(
            'default_plugins = ["cli", "add", "import", "write"]',
            tmp_db=True,
            extra_plugins=[config.ExtraPlugin(AddCLIPlugin, "add_plugin")],
        )
        cli_args = ["add", str(track_factory(exists=True).path)]

        mock_choice = PromptChoice("mock", "m", add_cli._skip_import)
        with patch(
            "moe.plugins.moe_import.import_cli.choice_prompt",
            return_value=mock_choice,
            autospec=True,
        ):
            moe.cli.main(cli_args)

        assert not config.MoeSession().query(Track).all()


@pytest.mark.usefixtures("_tmp_add_config")
class TestCommand:
    """Test the `add` command."""

    def test_track_file(self, mock_add):
        """Track files are added as tracks."""
        track = track_factory(exists=True)
        cli_args = ["add", str(track.path)]

        moe.cli.main(cli_args)

        mock_add.assert_called_once_with(track)

    def test_non_track_file(self, mock_add):
        """Raise SystemExit if bad track file given."""
        cli_args = ["add", str(extra_factory(exists=True).path)]

        with pytest.raises(SystemExit) as err:
            moe.cli.main(cli_args)

        assert err.value.code != 0
        mock_add.assert_not_called()

    def test_bad_album_dir(self, tmp_path, mock_add):
        """Raise SystemExit if bad album directory given."""
        cli_args = ["add", str(tmp_path)]

        with pytest.raises(SystemExit) as err:
            moe.cli.main(cli_args)

        assert err.value.code != 0
        mock_add.assert_not_called()

    def test_multiple_items(self, mock_add):
        """Items are added to the library when given a path."""
        track = track_factory(exists=True)
        album = album_factory(exists=True)
        cli_args = ["add", str(track.path), str(album.path)]

        moe.cli.main(cli_args)

        mock_add.assert_any_call(track)
        mock_add.assert_any_call(album)
        assert mock_add.call_count == 2

    def test_single_error(self, tmp_path, mock_add):
        """Don't exit after the first failed item if more to be added.

        Still exit with non-zero code if any failures occured.
        """
        track = track_factory(exists=True)
        cli_args = ["add", str(tmp_path), str(track.path)]

        with pytest.raises(SystemExit) as error:
            moe.cli.main(cli_args)

        assert error.value.code != 0
        mock_add.assert_called_once_with(track)

    def test_extra_file(self, mock_add, mock_query):
        """Extra files are added as tracks."""
        extra = extra_factory(exists=True)
        cli_args = ["add", "-a", "*", str(extra.path)]
        mock_query.return_value = [extra.album]

        moe.cli.main(cli_args)

        mock_add.assert_called_once_with(extra)

    def test_extra_no_album(self, mock_add):
        """Raise SystemExit if trying to add an extra but no query was given."""
        extra = extra_factory(exists=True)
        cli_args = ["add", str(extra.path)]

        with pytest.raises(SystemExit) as err:
            moe.cli.main(cli_args)

        assert err.value.code != 0
        mock_add.assert_not_called()

    def test_query_multiple_albums(self, mock_add, mock_query):
        """Raise SystemExit the given query returns multiple albums."""
        extra = extra_factory(exists=True)
        cli_args = ["add", "-a", "*", str(extra.path)]
        mock_query.return_value = [album_factory(), album_factory()]

        with pytest.raises(SystemExit) as err:
            moe.cli.main(cli_args)

        assert err.value.code != 0
        mock_add.assert_not_called()


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation."""

    def test_no_cli(self, tmp_config):
        """Don't enable the add cli plugin if the `cli` plugin is not enabled."""
        config = tmp_config(settings='default_plugins = ["add"]')

        assert not config.pm.has_plugin("add_cli")

    def test_cli(self, caplog, tmp_config):
        """Enable the add cli plugin if the `cli` plugin is enabled."""
        config = tmp_config(settings='default_plugins = ["add", "cli"]')

        assert config.pm.has_plugin("add_cli")
