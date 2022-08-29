"""Tests the add plugin."""

import copy
from pathlib import Path
from types import FunctionType
from typing import Iterator
from unittest.mock import patch

import pytest

import moe.cli
from moe.config import Config
from moe.library.album import Album
from moe.plugins import add


@pytest.fixture
def mock_add() -> Iterator[FunctionType]:
    """Mock the `edit_item()` api call."""
    with patch("moe.plugins.add.add_item", autospec=True) as mock_add:
        yield mock_add


@pytest.fixture
def tmp_add_config(tmp_config) -> Config:
    """A temporary config for the add plugin with the cli."""
    return tmp_config('default_plugins = ["cli", "add"]')


class TestCommand:
    """Test the `add` command."""

    def test_item(self, mock_add, tmp_add_config):
        """Items are added to the library when given a path."""
        mock_path = Path("")
        cli_args = ["add", str(mock_path)]

        moe.cli.main(cli_args, tmp_add_config)

        mock_add.assert_called_once_with(tmp_add_config, mock_path)

    def test_multiple_items(self, mock_add, tmp_add_config):
        """Items are added to the library when given a path."""
        mock_path1 = Path("1")
        mock_path2 = Path("2")
        cli_args = ["add", str(mock_path1), str(mock_path2)]

        moe.cli.main(cli_args, tmp_add_config)

        mock_add.assert_any_call(tmp_add_config, mock_path1)
        mock_add.assert_any_call(tmp_add_config, mock_path2)
        assert mock_add.call_count == 2

    def test_single_error(self, mock_add, tmp_add_config):
        """Don't exit after the first failed item if more to be added.

        Still exit with non-zero code if any failures occured.
        """
        mock_path1 = Path("1")
        mock_path2 = Path("2")
        cli_args = ["add", str(mock_path1), str(mock_path2)]

        mock_add.side_effect = [add.AddError, None]
        with pytest.raises(SystemExit) as error:
            moe.cli.main(cli_args, tmp_add_config)

        assert error.value.code != 0
        mock_add.assert_any_call(tmp_add_config, mock_path2)


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation."""

    def test_no_cli(self, tmp_config):
        """Don't enable the add cli plugin if the `cli` plugin is not enabled."""
        config = tmp_config(settings='default_plugins = ["add"]')

        assert not config.plugin_manager.has_plugin("add_cli")

    def test_cli(self, tmp_config):
        """Enable the add cli plugin if the `cli` plugin is enabled."""
        config = tmp_config(settings='default_plugins = ["add", "cli"]')

        assert config.plugin_manager.has_plugin("add_cli")


class TestPreAdd:
    """Test the `pre_add` hookwrapper implementation."""

    def test_merge_track(self, tmp_session, mock_track, tmp_add_config):
        """When adding a track, call the function with the respective album."""
        tmp_session.merge(mock_track)
        db_album = mock_track.album_obj.get_existing()
        with patch.object(moe.cli, "choice_prompt") as mock_prompt_choice:
            tmp_add_config.plugin_manager.hook.pre_add(
                config=tmp_add_config, item=mock_track
            )

            mock_prompt_choice.return_value.func.assert_called_once_with(
                tmp_add_config, mock_track.album_obj, db_album
            )

    def test_merge_extra(self, tmp_session, mock_extra, tmp_add_config):
        """When adding an extra, call the function with the respective album."""
        tmp_session.merge(mock_extra)
        db_album = mock_extra.album_obj.get_existing()
        with patch.object(moe.cli, "choice_prompt") as mock_prompt_choice:
            tmp_add_config.plugin_manager.hook.pre_add(
                config=tmp_add_config, item=mock_extra
            )

            mock_prompt_choice.return_value.func.assert_called_once_with(
                tmp_add_config, mock_extra.album_obj, db_album
            )

    def test_replace_album(self, mock_album_factory, tmp_session, tmp_add_config):
        """Test the 'replace' merge option with an album."""
        album = mock_album_factory()
        dup_album = mock_album_factory()
        album.title = "keep"
        dup_album.title = "dup"
        album.mb_album_id = None
        dup_album.mb_album_id = "123"
        album.path = dup_album.path

        dup_album = tmp_session.merge(dup_album)
        assert album.get_existing()

        mock_prompt_choice = moe.cli.PromptChoice("mock", "m", add.add_cli._replace)
        with patch.object(moe.cli, "choice_prompt", return_value=mock_prompt_choice):
            tmp_add_config.plugin_manager.hook.pre_add(
                config=tmp_add_config, item=album
            )

        assert not album.get_existing()
        tmp_session.merge(album)

        db_album = tmp_session.query(Album).one()
        assert db_album.title == "keep"  # conflicts not overwritten
        assert not db_album.mb_album_id  # non-existing fields not written

    def test_abort_add(self, mock_album_factory, tmp_session, tmp_add_config):
        """A 'keep right' merge is treated as the user wanting to abort the add."""
        album = mock_album_factory()
        dup_album = mock_album_factory()
        album.mb_album_id = "123"
        dup_album = copy.deepcopy(album)

        dup_album = tmp_session.merge(dup_album)
        assert album.get_existing()

        mock_prompt_choice = moe.cli.PromptChoice("mock", "m", add.add_cli._abort)
        with pytest.raises(add.AddAbortError):
            with patch.object(
                moe.cli, "choice_prompt", return_value=mock_prompt_choice
            ):
                tmp_add_config.plugin_manager.hook.pre_add(
                    config=tmp_add_config, item=album
                )

    def test_merge(self, mock_album_factory, tmp_session, tmp_add_config):
        """Test merging the two albums, without overwriting on conflict."""
        new_album = mock_album_factory()
        dup_album = mock_album_factory()

        new_album.title = "ignore"
        dup_album.title = "keep"
        new_album.path = dup_album.path
        new_album.mb_album_id = "123"
        dup_album.mb_album_id = None

        tmp_session.merge(dup_album)
        assert new_album.get_existing()

        mock_prompt_choice = moe.cli.PromptChoice("mock", "m", add.add_cli._merge)
        with patch.object(moe.cli, "choice_prompt", return_value=mock_prompt_choice):
            tmp_add_config.plugin_manager.hook.pre_add(
                config=tmp_add_config, item=new_album
            )

        tmp_session.merge(new_album)

        db_album = tmp_session.query(Album).one()
        assert db_album.title == "keep"
        assert db_album.mb_album_id == "123"

    def test_overwrite(self, mock_album_factory, tmp_session, tmp_add_config):
        """Test merging the two albums, overwriting on conflict."""
        new_album = mock_album_factory()
        dup_album = mock_album_factory()

        new_album.title = "keep"
        dup_album.title = "overwrite"
        new_album.path = dup_album.path
        new_album.mb_album_id = "123"
        dup_album.mb_album_id = None

        tmp_session.merge(dup_album)
        assert new_album.get_existing()

        mock_prompt_choice = moe.cli.PromptChoice("mock", "m", add.add_cli._overwrite)
        with patch.object(moe.cli, "choice_prompt", return_value=mock_prompt_choice):
            tmp_add_config.plugin_manager.hook.pre_add(
                config=tmp_add_config, item=new_album
            )

        tmp_session.merge(new_album)

        db_album = tmp_session.query(Album).one()
        assert db_album.title == "keep"
        assert db_album.mb_album_id == "123"

    def test_no_dup_album(self, tmp_session, mock_album, tmp_add_config):
        """Don't do anything if the album does not have a duplicate."""
        with patch.object(moe.cli, "choice_prompt") as mock_choice_prompt:
            tmp_add_config.plugin_manager.hook.pre_add(
                config=tmp_add_config, item=mock_album
            )

            mock_choice_prompt.assert_not_called()

    def test_no_dup_track(self, tmp_session, mock_track, tmp_add_config):
        """Don't do anything if the track does not have a duplicate."""
        with patch.object(moe.cli, "choice_prompt") as mock_choice_prompt:
            tmp_add_config.plugin_manager.hook.pre_add(
                config=tmp_add_config, item=mock_track
            )

            mock_choice_prompt.assert_not_called()

    def test_no_dup_extra(self, tmp_session, mock_extra, tmp_add_config):
        """Don't do anything if the extra does not have a duplicate."""
        with patch.object(moe.cli, "choice_prompt") as mock_choice_prompt:
            tmp_add_config.plugin_manager.hook.pre_add(
                config=tmp_add_config, item=mock_extra
            )

            mock_choice_prompt.assert_not_called()
