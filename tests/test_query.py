"""Test the core query module."""

from unittest.mock import Mock

import pytest

from moe.core import query
from moe.core.library.album import Album
from moe.core.library.track import Track


class TestParseTerm:
    """Test the query term parsing _parse_term()."""

    def test_basic(self):
        """Simplest case field:value test."""
        match = query._parse_term("field:value")

        assert match["field"] == "field"
        assert match["separator"] == ":"
        assert match["value"] == "value"

    def test_value_spaces(self):
        """Values can contain arbitrary whitespace.

        The only exception is immediately after the colon.
        """
        match = query._parse_term(r"field:val u e")

        assert match["field"] == "field"
        assert match["value"] == "val u e"

    def test_regex_value(self):
        """Regular expression values are indicated by a '::' separator."""
        match = query._parse_term(r"field::A.*")

        assert match["field"] == "field"
        assert match["separator"] == "::"
        assert match["value"] == "A.*"

    def test_invalid(self):
        """Invalid terms should raise a ValueError."""
        with pytest.raises(ValueError):
            query._parse_term(r"invalid")


class TestQuery:
    """Test actual query."""

    def test_empty_query_str(self):
        """Empty queries should return an empty list."""
        assert not query.query(r"", Mock())

    def test_invalid_query_str(self):
        """Invalid queries should return an empty list."""
        assert not query.query(r"invalid", Mock())  # invalid pattern

    def test_invalid_query_field(self):
        """Invalid queries should return an empty list."""
        assert not query.query(r"invalid:a", Mock())  # invalid field

    def test_valid_query(self, tmp_session, mock_track):
        """Simplest query."""
        tmp_session.add(mock_track)

        assert query.query("_id:1", tmp_session)

    def test_space_value(self, tmp_session, mock_track):
        """If a value has whitespace, it must be encolsed by quotes."""
        mock_track.title = "Holy cow"
        tmp_session.add(mock_track)

        assert query.query("'title:Holy cow'", tmp_session)

    def test_multiple_terms(self, tmp_session, mock_track):
        """We should be able to query for multiple terms at once."""
        mock_track.title = "C.R.E.A.M."
        tmp_session.add(mock_track)

        assert query.query("_id:1 title:C.R.E.A.M.", tmp_session)

    def test_track_album_field_query(self, tmp_session, mock_track):
        """We should be able to query tracks that match album-related fields.

        These fields belong to the Album table and thus aren't normally exposed
        through a track.
        """
        mock_track.albumartist = "2Pac"
        mock_track.album = "All Eyez on Me"
        tmp_session.add(mock_track)

        assert query.query("'album:All Eyez on Me'", tmp_session)
        assert query.query("albumartist:2Pac", tmp_session)  # Album field

    def test_case_insensitive_value(self, tmp_session, mock_track):
        """Query values should be case-insensitive."""
        mock_track.title = "TMP"
        mock_track.album = "TMP"
        tmp_session.add(mock_track)

        assert query.query("title:tmp", tmp_session)
        assert query.query("album:tmp", tmp_session)  # Album field

    def test_case_insensitive_field(self, tmp_session, mock_track):
        """Fields should be able to be specified case-insensitive."""
        mock_track.title = "tmp"
        mock_track.album = "tmp"
        tmp_session.add(mock_track)

        assert query.query("Title:tmp", tmp_session)
        assert query.query("Album:tmp", tmp_session)  # Album field

    def test_regex(self, tmp_session, mock_track):
        """Queries can use regular expression matching."""
        tmp_session.add(mock_track)

        assert query.query(r"title::.*", tmp_session)
        assert query.query(r"album::.*", tmp_session)  # Album field

    def test_regex_non_str(self, tmp_session, mock_track):
        """Non string fields should be converted to strings for matching."""
        tmp_session.add(mock_track)

        assert query.query(r"track_num::.*", tmp_session)
        assert query.query(r"year::.*", tmp_session)  # Album field

    def test_invalid_regex(self, tmp_session, mock_track):
        """Invalid regex queries should return an empty list."""
        tmp_session.add(mock_track)

        assert not query.query(r"_id::[", tmp_session)

    def test_regex_case_insensitive(self, tmp_session, mock_track):
        """Regex queries should be case-insensitive."""
        mock_track.title = "TMP"
        mock_track.album = "TMP"
        tmp_session.add(mock_track)

        assert query.query(r"title::tmp", tmp_session)
        assert query.query(r"album::tmp", tmp_session)  # Album field

    def test_track_query(self, tmp_session, mock_track):
        """A track query should return track objects."""
        tmp_session.add(mock_track)

        tracks = query.query("_id:1", tmp_session, album_query=False)

        assert tracks
        for track in tracks:
            assert isinstance(track, Track)

    def test_album_query(self, tmp_session, mock_track):
        """An album query should return album objects."""
        tmp_session.add(mock_track)

        albums = query.query("_id:1", tmp_session, album_query=True)

        assert albums
        for album in albums:
            assert isinstance(album, Album)

    def test_album_query_track_fields(self, tmp_session, mock_track):
        """Album queries should still be filtered based off Track fields."""
        mock_track.album = "ATLiens"
        tmp_session.add(mock_track)

        albums = query.query("album:ATLiens", tmp_session, album_query=True)

        assert albums
        for album in albums:
            assert isinstance(album, Album)

    def test_like_query(self, tmp_session, mock_track):
        """Test sql LIKE queries. '%' and '_' are wildcard characters."""
        tmp_session.add(mock_track)

        assert query.query("_id:_", tmp_session)
        assert query.query("_id:%", tmp_session)

    def test_like_escape_query(self, tmp_session, mock_track_factory):
        r"""We should be able to escape the LIKE wildcard characters with '/'.

        Note, I think '\' would be the preferred backslash character, but for
        some reason it doesn't work.
        """
        track1 = mock_track_factory()
        track2 = mock_track_factory()
        track1.title = "_"
        track2.title = "b"
        tmp_session.add(track1)
        tmp_session.add(track2)

        assert len(query.query(r"title:/_", tmp_session)) == 1

    def test_genres_query(self, tmp_session, mock_track):
        """We should be able to query genres transparently.

        `genres` is a list of genres for a Track.
        """
        mock_track.genres = ["hip hop", "rock"]

        assert query.query("'genre:hip hop'", tmp_session)
        assert query.query("genre:rock", tmp_session)
