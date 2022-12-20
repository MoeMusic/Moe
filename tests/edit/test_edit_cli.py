"""Tests the ``edit`` cli plugin."""

from types import FunctionType
from typing import Iterator
from unittest.mock import ANY, patch

import pytest

import moe.cli
from moe import config
from moe.edit import EditError
from tests.conftest import album_factory, extra_factory, track_factory


@pytest.fixture
def mock_edit() -> Iterator[FunctionType]:
    """Mock the `edit_item()` api call."""
    with patch("moe.edit.edit_item", autospec=True) as mock_edit:
        yield mock_edit


@pytest.fixture
def mock_query() -> Iterator[FunctionType]:
    """Mock a database query call.

    Use ``mock_query.return_value` to set the return value of a query.

    Yields:
        Mock query
    """
    with patch("moe.edit.edit_cli.cli_query", autospec=True) as mock_query:
        yield mock_query


@pytest.fixture
def _tmp_edit_config(tmp_config):
    """A temporary config for the edit plugin with the cli."""
    tmp_config('default_plugins = ["cli", "edit"]')


@pytest.mark.usefixtures("_tmp_edit_config")
class TestCommand:
    """Test general functionality of the argument parser."""

    def test_track(self, mock_query, mock_edit):
        """Tracks are edited."""
        track = track_factory()
        cli_args = ["edit", "*", "track_num=3"]
        mock_query.return_value = [track]

        moe.cli.main(cli_args)

        mock_query.assert_called_once_with(ANY, "*", query_type="track")
        mock_edit.assert_called_once_with(track, "track_num", "3")

    def test_album(self, mock_query, mock_edit):
        """Albums are edited."""
        album = album_factory()
        cli_args = ["edit", "-a", "*", "title=edit"]
        mock_query.return_value = [album]

        moe.cli.main(cli_args)

        mock_query.assert_called_once_with(ANY, "*", query_type="album")
        mock_edit.assert_called_once_with(album, "title", "edit")

    def test_extra(self, mock_query, mock_edit):
        """Extras are edited."""
        extra = extra_factory()
        cli_args = ["edit", "-e", "*", "title=edit"]
        mock_query.return_value = [extra]

        moe.cli.main(cli_args)

        mock_query.assert_called_once_with(ANY, "*", query_type="extra")
        mock_edit.assert_called_once_with(extra, "title", "edit")

    def test_multiple_items(self, mock_query, mock_edit):
        """All items returned from a query are edited."""
        cli_args = ["edit", "*", "track_num=3"]
        track1 = track_factory()
        track2 = track_factory()
        mock_query.return_value = [track1, track2]

        moe.cli.main(cli_args)

        mock_edit.assert_any_call(track1, "track_num", "3")
        mock_edit.assert_any_call(track2, "track_num", "3")
        assert mock_edit.call_count == 2

    def test_multiple_terms(self, mock_query, mock_edit):
        """We can edit multiple terms at once."""
        track = track_factory()
        cli_args = ["edit", "*", "track_num=3", "title=yo"]
        mock_query.return_value = [track]

        moe.cli.main(cli_args)

        mock_edit.assert_any_call(track, "track_num", "3")
        mock_edit.assert_any_call(track, "title", "yo")
        assert mock_edit.call_count == 2

    def test_invalid_fv_term(self, mock_query):
        """Raise SystemExit if field/value term is in the wrong format."""
        track = track_factory()
        cli_args = ["edit", "*", "bad_format"]
        mock_query.return_value = [track]

        with pytest.raises(SystemExit) as error:
            moe.cli.main(cli_args)

        assert error.value.code != 0

    def test_single_invalid_term(self, mock_query, mock_edit):
        """If only one out of multiple fields are invalid, still process the others."""
        track = track_factory()
        cli_args = ["edit", "*", "bad_format", "track_num=3"]
        mock_query.return_value = [track]

        with pytest.raises(SystemExit) as error:
            moe.cli.main(cli_args)

        assert error.value.code != 0
        mock_edit.assert_called_once_with(track, "track_num", "3")

    def test_edit_error(self, mock_query, mock_edit):
        """Raise SystemExit if there is an error editing the item."""
        track = track_factory()
        cli_args = ["edit", "*", "track_num=3"]
        mock_query.return_value = [track]
        mock_edit.side_effect = EditError

        with pytest.raises(SystemExit) as error:
            moe.cli.main(cli_args)

        assert error.value.code != 0


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation."""

    def test_no_cli(self, tmp_config):
        """Don't enable the edit cli plugin if the `cli` plugin is not enabled."""
        tmp_config(settings='default_plugins = ["edit"]')

        assert not config.CONFIG.pm.has_plugin("edit_cli")

    def test_cli(self, tmp_config):
        """Enable the edit cli plugin if the `cli` plugin is enabled."""
        tmp_config(settings='default_plugins = ["edit", "cli"]')

        assert config.CONFIG.pm.has_plugin("edit_cli")
