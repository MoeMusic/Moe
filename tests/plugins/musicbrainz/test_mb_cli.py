"""Test the musicbrainz cli plugin."""

from types import FunctionType
from typing import Iterator
from unittest.mock import Mock, patch

import pytest

import moe
import moe.cli
from moe import config
from moe.query import QueryError
from tests.conftest import album_factory, extra_factory, track_factory


@pytest.fixture
def mock_query() -> Iterator[FunctionType]:
    """Mock a database query call.

    Use ``mock_query.return_value` to set the return value of a query.

    Yields:
        Mock query
    """
    with patch("moe.plugins.musicbrainz.mb_cli.query", autospec=True) as mock_query:
        yield mock_query


@pytest.fixture
def _tmp_mb_config(tmp_config):
    """A temporary config for the edit plugin with the cli."""
    tmp_config('default_plugins = ["cli", "musicbrainz"]')


@pytest.mark.usefixtures("_tmp_mb_config")
class TestCollectionCommand:
    """Test the `mbcol` command."""

    def test_track(self, mock_query):
        """Tracks associated album's are used."""
        cli_args = ["mbcol", "*"]
        track = track_factory()
        track.album_obj.mb_album_id = "123"
        mock_query.return_value = [track]

        with patch(
            "moe.plugins.musicbrainz.mb_cli.moe_mb.set_collection", autospec=True
        ) as mock_set:
            moe.cli.main(cli_args)

        mock_set.assert_called_once_with({"123"})

    def test_extra(self, mock_query):
        """Extras associated album's are used."""
        cli_args = ["mbcol", "*"]
        extra = extra_factory()
        extra.album_obj.mb_album_id = "123"
        mock_query.return_value = [extra]

        with patch(
            "moe.plugins.musicbrainz.mb_cli.moe_mb.set_collection", autospec=True
        ) as mock_set:
            moe.cli.main(cli_args)

        mock_set.assert_called_once_with({"123"})

    def test_album(self, mock_query):
        """Albums associated releases are used."""
        cli_args = ["mbcol", "*"]
        album = album_factory(custom_fields={"mb_album_id": "123"})
        mock_query.return_value = [album]

        with patch(
            "moe.plugins.musicbrainz.mb_cli.moe_mb.set_collection", autospec=True
        ) as mock_set:
            moe.cli.main(cli_args)

        mock_set.assert_called_once_with({"123"})

    def test_remove(self, mock_query):
        """Releases are removed from a collection if `--remove` option used."""
        cli_args = ["mbcol", "--remove", "*"]
        track = track_factory()
        track.album_obj.mb_album_id = "123"
        mock_query.return_value = [track]

        with patch(
            "moe.plugins.musicbrainz.mb_cli.moe_mb.rm_releases_from_collection",
            autospec=True,
        ) as mock_rm:
            moe.cli.main(cli_args)

        mock_rm.assert_called_once_with({"123"})

    def test_add(self, mock_query):
        """Releases are added to a collection if `--add` option used."""
        cli_args = ["mbcol", "--add", "*"]
        track = track_factory()
        track.album_obj.mb_album_id = "123"
        mock_query.return_value = [track]

        with patch(
            "moe.plugins.musicbrainz.mb_cli.moe_mb.add_releases_to_collection",
            autospec=True,
        ) as mock_add:
            moe.cli.main(cli_args)

        mock_add.assert_called_once_with({"123"})

    def test_exit_code(self, mock_query):
        """Return a non-zero exit code if no items are returned from the query."""
        cli_args = ["mbcol", "*"]
        mock_query.return_value = []

        with pytest.raises(SystemExit) as error:
            moe.cli.main(cli_args)

        assert error.value.code != 0

    def test_bad_query(self, mock_query):
        """Return a non-zero exit code if a bad query is given."""
        cli_args = ["mbcol", "*"]
        mock_query.side_effect = QueryError

        with pytest.raises(SystemExit) as error:
            moe.cli.main(cli_args)

        assert error.value.code != 0

    def test_no_releases_found(self, mock_query):
        """Return a non-zero exit code if no releases found in the queried items."""
        cli_args = ["mbcol", "*"]
        mock_query.return_value = [track_factory()]

        with pytest.raises(SystemExit) as error:
            moe.cli.main(cli_args)

        assert error.value.code != 0


@pytest.mark.usefixtures("_tmp_mb_config")
class TestAddImportPromptChoice:
    """Test the `add_import_prompt_choice` hook implementation."""

    def test_add_choice(self, tmp_config):
        """The "m" key to add a musicbrainz id is added."""
        prompt_choices = []

        config.CONFIG.pm.hook.add_import_prompt_choice(prompt_choices=prompt_choices)

        assert any(choice.shortcut_key == "m" for choice in prompt_choices)

    def test_enter_id(self, tmp_config):
        """When selected, the 'm' key should allow the user to enter an mb_id."""
        old_album = album_factory()
        new_album = album_factory()
        prompt_choices = []
        config.CONFIG.pm.hook.add_import_prompt_choice(prompt_choices=prompt_choices)

        mock_album = Mock()
        with patch(
            "moe.plugins.musicbrainz.mb_cli.questionary.text",
            **{"return_value.ask.return_value": "new id"}
        ):
            with patch(
                "moe.plugins.musicbrainz.mb_cli.moe_mb.get_album_by_id",
                return_value=mock_album,
                autospec=True,
            ) as mock_get_album:
                with patch(
                    "moe.plugins.musicbrainz.mb_cli.moe_import.import_prompt",
                    autospec=True,
                ) as mock_prompt:
                    prompt_choices[0].func(old_album, new_album)

        mock_get_album.assert_called_once_with("new id")
        mock_prompt.assert_called_once_with(old_album, mock_album)


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation."""

    def test_no_cli(self, tmp_config):
        """Don't enable the musicbrainz cli plugin if the `cli` plugin is disabled."""
        tmp_config(settings='default_plugins = ["musicbrainz"]')

        assert not config.CONFIG.pm.has_plugin("musicbrainz_cli")

    def test_cli(self, tmp_config):
        """Enable the musicbrainz cli plugin if the `cli` plugin is enabled."""
        tmp_config(settings='default_plugins = ["musicbrainz", "cli"]')

        assert config.CONFIG.pm.has_plugin("musicbrainz_cli")
