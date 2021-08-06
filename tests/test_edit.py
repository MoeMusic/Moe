"""Tests the ``edit`` plugin."""

import argparse
import datetime
from unittest.mock import Mock, patch

import pytest

import moe
from moe.core.library.session import session_scope
from moe.core.library.track import Track
from moe.plugins import edit


class TestParseArgs:
    """Test general functionality of the argument parser."""

    def test_multiple_items(self, mock_track_factory):
        """All items returned from a query are edited."""
        args = argparse.Namespace(
            fv_terms=["track_num=3"], query="", album=False, extra=False
        )

        track1 = mock_track_factory()
        track2 = mock_track_factory()
        with patch("moe.core.query.query", return_value=[track1, track2]) as mock_query:
            mock_session = Mock()

            edit._parse_args(config=Mock(), session=mock_session, args=args)

            mock_query.assert_called_once_with("", mock_session, query_type="track")

        assert track1.track_num == 3
        assert track2.track_num == 3

    def test_multiple_terms(self, mock_track):
        """We can edit multiple terms at once."""
        args = argparse.Namespace(
            fv_terms=["track_num=3", "title=yo"], query="", album=False, extra=False
        )

        with patch("moe.core.query.query", return_value=[mock_track]) as mock_query:
            mock_session = Mock()

            edit._parse_args(config=Mock(), session=mock_session, args=args)

            mock_query.assert_called_with("", mock_session, query_type="track")

        assert mock_track.track_num == 3
        assert mock_track.title == "yo"

    def test_invalid_fv_term(self, mock_track):
        """Raise SystemExit if field/value term is in the wrong format."""
        args = argparse.Namespace(
            fv_terms=["bad_format"], query="", album=False, extra=False
        )

        with pytest.raises(SystemExit) as error:
            with patch("moe.core.query.query", return_value=[mock_track]):
                edit._parse_args(config=Mock(), session=Mock(), args=args)

        assert error.value.code != 0

    def test_single_invalid_field(self, mock_track):
        """If only one out of multiple fields are invalid, still process the others."""
        args = argparse.Namespace(
            fv_terms=["lol=3", "track_num=3"], query="", album=False, extra=False
        )

        with pytest.raises(SystemExit) as error:
            with patch("moe.core.query.query", return_value=[mock_track]) as mock_query:
                mock_session = Mock()

                edit._parse_args(config=Mock(), session=mock_session, args=args)

                mock_query.assert_called_once_with("", mock_session, query_type="track")

        assert error.value.code != 0
        assert mock_track.track_num == 3


class TestEditItem:
    """Test `edit_item()`."""

    def test_track(self, mock_track):
        """We can edit a track's field."""
        edit.edit_item(mock_track, "title", "new title")

        assert mock_track.title == "new title"

    def test_album(self, mock_album):
        """We can edit an album's field."""
        edit.edit_item(mock_album, "title", "new title")

        assert mock_album.title == "new title"

    def test_int_field(self, mock_track):
        """We can edit integer fields."""
        edit.edit_item(mock_track, "track_num", "3")

        assert mock_track.track_num == 3

    def test_date_field(self, mock_track):
        """We can edit the date."""
        edit.edit_item(mock_track, "date", "2020-11-01")

        assert mock_track.date == datetime.date(2020, 11, 1)

    def test_invalid_date_field(self, mock_track):
        """Invalid dates should raise an EditError."""
        with pytest.raises(edit.EditError):
            edit.edit_item(mock_track, "date", "2020")

    def test_list_field(self, mock_track):
        """We can edit list fields."""
        edit.edit_item(mock_track, "genre", "a; b")

        assert set(mock_track.genres) == {"a", "b"}

    def test_non_editable_fields(self, mock_track):
        """Editing paths is not currently supported."""
        with pytest.raises(edit.EditError):
            edit.edit_item(mock_track, "path", "~")

    def test_invalid_track_field(self, mock_track):
        """Raise EditError if attempting to edit an invalid field."""
        with pytest.raises(edit.EditError):
            edit.edit_item(mock_track, "lol", "bad field")

    def test_invalid_album_field(self, mock_album):
        """Raise SystemExit if attempting to edit an invalid field."""
        with pytest.raises(edit.EditError):
            edit.edit_item(mock_album, "lol", "bad field")


@pytest.mark.integration
class TestCommand:
    """Test cli integration with the `edit` command."""

    def test_parse_args(self, real_track, tmp_config):
        """Music is edited when the `edit` command is invoked."""
        new_title = "Lovely Day"
        assert real_track.title != new_title
        cli_args = ["edit", "*", f"title={new_title}"]

        config = tmp_config(settings='default_plugins = ["edit"]')
        config.init_db()
        with session_scope() as pre_edit_session:
            pre_edit_session.add(real_track)

        moe.cli.main(cli_args, config)

        with session_scope() as post_edit_session:
            edited_track = post_edit_session.query(Track).one()

            assert edited_track.title == new_title
