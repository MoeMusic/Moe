"""Tests the ``edit`` cli plugin."""

from types import FunctionType
from typing import Iterator
from unittest.mock import patch

import pytest

import moe.cli
from moe.config import Config
from moe.plugins.edit import EditError
from moe.query import QueryError


@pytest.fixture
def mock_edit() -> Iterator[FunctionType]:
    """Mock the `edit_item()` api call."""
    with patch("moe.plugins.edit.edit_item", autospec=True) as mock_edit:
        yield mock_edit


@pytest.fixture
def mock_query() -> Iterator[FunctionType]:
    """Mock a database query call.

    Use ``mock_query.return_value` to set the return value of a query.

    Yields:
        Mock query
    """
    with patch("moe.plugins.edit.edit_cli.query", autospec=True) as mock_query:
        yield mock_query


@pytest.fixture
def tmp_edit_config(tmp_config) -> Config:
    """A temporary config for the edit plugin with the cli."""
    return tmp_config('default_plugins = ["cli", "edit"]')


class TestCommand:
    """Test general functionality of the argument parser."""

    def test_track(self, mock_track, mock_query, mock_edit, tmp_edit_config):
        """Tracks are edited."""
        cli_args = ["edit", "*", "track_num=3"]
        mock_query.return_value = [mock_track]

        moe.cli.main(cli_args, tmp_edit_config)

        mock_query.assert_called_once_with("*", query_type="track")
        mock_edit.assert_called_once_with(mock_track, "track_num", "3")

    def test_album(self, mock_album, mock_query, mock_edit, tmp_edit_config):
        """Albums are edited."""
        cli_args = ["edit", "-a", "*", "title=edit"]
        mock_query.return_value = [mock_album]

        moe.cli.main(cli_args, tmp_edit_config)

        mock_query.assert_called_once_with("*", query_type="album")
        mock_edit.assert_called_once_with(mock_album, "title", "edit")

    def test_extra(self, mock_extra, mock_query, mock_edit, tmp_edit_config):
        """Extras are edited."""
        cli_args = ["edit", "-e", "*", "title=edit"]
        mock_query.return_value = [mock_extra]

        moe.cli.main(cli_args, tmp_edit_config)

        mock_query.assert_called_once_with("*", query_type="extra")
        mock_edit.assert_called_once_with(mock_extra, "title", "edit")

    def test_multiple_items(
        self, track_factory, mock_query, mock_edit, tmp_edit_config
    ):
        """All items returned from a query are edited."""
        cli_args = ["edit", "*", "track_num=3"]
        track1 = track_factory()
        track2 = track_factory()
        mock_query.return_value = [track1, track2]

        moe.cli.main(cli_args, tmp_edit_config)

        mock_edit.assert_any_call(track1, "track_num", "3")
        mock_edit.assert_any_call(track2, "track_num", "3")
        assert mock_edit.call_count == 2

    def test_multiple_terms(self, mock_track, mock_query, mock_edit, tmp_edit_config):
        """We can edit multiple terms at once."""
        cli_args = ["edit", "*", "track_num=3", "title=yo"]
        mock_query.return_value = [mock_track]

        moe.cli.main(cli_args, tmp_edit_config)

        mock_edit.assert_any_call(mock_track, "track_num", "3")
        mock_edit.assert_any_call(mock_track, "title", "yo")
        assert mock_edit.call_count == 2

    def test_invalid_fv_term(self, mock_track, mock_query, tmp_edit_config):
        """Raise SystemExit if field/value term is in the wrong format."""
        cli_args = ["edit", "*", "bad_format"]
        mock_query.return_value = [mock_track]

        with pytest.raises(SystemExit) as error:
            moe.cli.main(cli_args, tmp_edit_config)

        assert error.value.code != 0

    def test_single_invalid_term(
        self, mock_track, mock_query, mock_edit, tmp_edit_config
    ):
        """If only one out of multiple fields are invalid, still process the others."""
        cli_args = ["edit", "*", "bad_format", "track_num=3"]
        mock_query.return_value = [mock_track]

        with pytest.raises(SystemExit) as error:
            moe.cli.main(cli_args, tmp_edit_config)

        assert error.value.code != 0
        mock_edit.assert_called_once_with(mock_track, "track_num", "3")

    def test_edit_error(self, mock_track, mock_query, mock_edit, tmp_edit_config):
        """Raise SystemExit if there is an error editing the item."""
        cli_args = ["edit", "*", "track_num=3"]
        mock_query.return_value = [mock_track]
        mock_edit.side_effect = EditError

        with pytest.raises(SystemExit) as error:
            moe.cli.main(cli_args, tmp_edit_config)

        assert error.value.code != 0

    def test_no_items(self, capsys, mock_query, tmp_edit_config):
        """If no items found to edit, exit with non-zero code."""
        cli_args = ["edit", "*", "track_num=3"]
        mock_query.return_value = []

        with pytest.raises(SystemExit) as error:
            moe.cli.main(cli_args, tmp_edit_config)

        assert error.value.code != 0

    def test_bad_query(self, mock_query, tmp_edit_config):
        """Raise SystemExit if given a bad query."""
        cli_args = ["edit", "*", "track_num=3"]
        mock_query.side_effect = QueryError

        with pytest.raises(SystemExit) as error:
            moe.cli.main(cli_args, tmp_edit_config)

        assert error.value.code != 0


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation."""

    def test_no_cli(self, tmp_config):
        """Don't enable the edit cli plugin if the `cli` plugin is not enabled."""
        config = tmp_config(settings='default_plugins = ["edit"]')

        assert not config.pm.has_plugin("edit_cli")

    def test_cli(self, tmp_config):
        """Enable the edit cli plugin if the `cli` plugin is enabled."""
        config = tmp_config(settings='default_plugins = ["edit", "cli"]')

        assert config.pm.has_plugin("edit_cli")
