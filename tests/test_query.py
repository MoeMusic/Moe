"""Tests the core query module."""


import pytest

import moe.query
from moe.library.album import Album
from moe.library.extra import Extra
from moe.library.track import Track
from moe.query import QueryError, query


class TestParseTerm:
    """Test the query term parsing _parse_term()."""

    def test_basic(self):
        """Simplest case field:value test."""
        match = moe.query._parse_term("field:value")

        assert match["field"] == "field"
        assert match["separator"] == ":"
        assert match["value"] == "value"

    def test_value_spaces(self):
        """Values can contain arbitrary whitespace.

        The only exception is immediately after the colon.
        """
        match = moe.query._parse_term("field:val u e")

        assert match["field"] == "field"
        assert match["value"] == "val u e"

    def test_regex_value(self):
        """Regular expression values are indicated by a '::' separator."""
        match = moe.query._parse_term("field::A.*")

        assert match["field"] == "field"
        assert match["separator"] == "::"
        assert match["value"] == "A.*"

    def test_invalid(self):
        """Invalid terms should raise a ValueError."""
        with pytest.raises(QueryError):
            moe.query._parse_term("invalid")


class TestQuery:
    """Test actual query."""

    def test_empty_query_str(self):
        """Empty queries strings should raise a QueryError."""
        with pytest.raises(QueryError):
            query("")

    def test_empty_query(self, tmp_session):
        """Empty queries should return an empty list."""
        assert not query("title:nope")

    def test_invalid_query_str(self, tmp_session):
        """Invalid queries should raise a QueryError."""
        with pytest.raises(QueryError):
            query("invalid")

    def test_invalid_query_type(self, tmp_session):
        """A query type should be one of: 'extra', 'track', or 'album'."""
        with pytest.raises(QueryError):
            query("title:a", "invalid")

    def test_valid_query(self, mock_track, tmp_session):
        """Simplest query."""
        tmp_session.add(mock_track)

        assert query(f"title:'{mock_track.title}'")

    def test_space_value(self, mock_track, tmp_session):
        """If a value has whitespace, it must be encolsed by quotes."""
        mock_track.title = "Holy cow"
        tmp_session.add(mock_track)

        assert query("'title:Holy cow'")

    def test_multiple_terms(self, mock_track, tmp_session):
        """We should be able to query for multiple terms at once."""
        mock_track.title = "C.R.E.A.M."
        tmp_session.add(mock_track)

        assert query(f"track_num:{mock_track.track_num} title:{mock_track.title}")

    def test_regex(self, mock_track, tmp_session):
        """Queries can use regular expression matching."""
        tmp_session.add(mock_track)

        assert query("title::.*")

    def test_track_path(self, real_track, tmp_session):
        """We can query a track's path."""
        tmp_session.add(real_track)

        assert query(f"'path:{str(real_track.path.resolve())}'")
        assert query("'path::.*'")

    def test_extra_path(self, real_album, tmp_session):
        """We can query for Extra paths."""
        tmp_session.merge(real_album)

        extra_path_str = str(real_album.extras.pop().path.resolve())
        assert query(f"'extra_path:{extra_path_str}'")
        assert query("'extra_path::.*'")

    def test_album_path(self, real_album, tmp_session):
        """We can query for Extra paths."""
        tmp_session.merge(real_album)

        assert query(f"'album_path:{str(real_album.path.resolve())}'")
        assert query("'album_path::.*'")

    def test_date(self, mock_track, tmp_session):
        """We can query an album's date."""
        tmp_session.add(mock_track)

        assert query(f"'date:{str(mock_track.date)}'")
        assert query("'date::.*'")

    def test_track_album_field(self, real_track, tmp_session):
        """We should be able to query tracks that match album-related fields.

        These fields belong to the Album table and thus aren't normally exposed
        through a track.
        """
        tmp_session.add(real_track)

        assert query(f"'album:{real_track.album}'")
        assert query(f"'albumartist:{real_track.albumartist}'")
        assert query(f"year:{real_track.year}")

    def test_case_insensitive_value(self, mock_track, tmp_session):
        """Query values should be case-insensitive."""
        mock_track.title = "TMP"
        mock_track.album = "TMP"
        tmp_session.add(mock_track)

        assert query("title:tmp")

    def test_case_insensitive_field(self, mock_track, tmp_session):
        """Fields should be able to be specified case-insensitive."""
        mock_track.title = "tmp"
        mock_track.album = "tmp"
        tmp_session.add(mock_track)

        assert query("Title:tmp")

    def test_regex_non_str(self, mock_track, tmp_session):
        """Non string fields should be converted to strings for matching."""
        tmp_session.add(mock_track)

        assert query("track_num::.*")

    def test_invalid_regex(self, tmp_session, mock_track):
        """Invalid regex queries should return an empty list."""
        tmp_session.add(mock_track)

        with pytest.raises(QueryError):
            query("title::[")

    def test_regex_case_insensitive(self, mock_track, tmp_session):
        """Regex queries should be case-insensitive."""
        mock_track.title = "TMP"
        mock_track.album = "TMP"
        tmp_session.add(mock_track)

        assert query("title::tmp")

    def test_track_query(self, mock_track, tmp_session):
        """A track query should return Track objects."""
        tmp_session.add(mock_track)

        tracks = query(f"title:'{mock_track.title}'", query_type="track")

        assert tracks
        for track in tracks:
            assert isinstance(track, Track)

    def test_album_query(self, mock_track, tmp_session):
        """An album query should return Album objects."""
        tmp_session.add(mock_track)

        albums = query(f"title:'{mock_track.title}'", query_type="album")

        assert albums
        for album in albums:
            assert isinstance(album, Album)

    def test_extra_query(self, mock_album, tmp_session):
        """An extra query should return Extra objects."""
        tmp_session.merge(mock_album)

        extras = query(f"album:'{mock_album.title}'", query_type="extra")

        assert extras
        for extra in extras:
            assert isinstance(extra, Extra)

    def test_album_query_track_fields(self, mock_track, tmp_session):
        """Album queries should still be filtered based off Track fields."""
        mock_track.album = "ATLiens"
        tmp_session.add(mock_track)

        albums = query("album:ATLiens", query_type="album")

        assert albums
        for album in albums:
            assert isinstance(album, Album)

    def test_like_query(self, mock_track, tmp_session):
        """Test sql LIKE queries. '%' and '_' are wildcard characters."""
        tmp_session.add(mock_track)
        mock_track.track_num = 1

        assert query("track_num:_")
        assert query("track_num:%")

    def test_like_escape_query(self, track_factory, tmp_session):
        r"""We should be able to escape the LIKE wildcard characters with '/'.

        Note, I think '\' would be the preferred backslash character, but for
        some reason it doesn't work.
        """
        track1 = track_factory()
        track2 = track_factory()
        track1.title = "_"
        track2.title = "b"
        tmp_session.merge(track1)
        tmp_session.merge(track2)

        assert len(query("title:/_")) == 1

    def test_multi_value_query(self, mock_track, tmp_session):
        """We should be able to query multi-value fields transparently.

        ``genre`` is a list of genres for a Track.
        """
        mock_track.genres = ["hip hop", "rock"]
        tmp_session.add(mock_track)

        assert query("'genre::.*'")
        assert query("'genre:hip hop'")
        assert query("genre:rock")
        assert query("genre:rock 'genre:hip hop'")

    def test_wildcard_query(self, track_factory, tmp_session):
        """'*' as a query should return all items."""
        track1 = track_factory()
        track2 = track_factory()

        tmp_session.merge(track1)
        tmp_session.merge(track2)

        assert len(query("*")) == 2

    def test_missing_extras(self, album_factory, tmp_session):
        """Ensure albums without extras are still returned by a valid query."""
        album1 = album_factory()
        album2 = album_factory()
        album2.extras = []
        assert album1.extras
        assert not album2.extras

        tmp_session.merge(album1)
        tmp_session.merge(album2)

        assert len(query("*", "album")) == 2

    def test_custom_field(self, mock_track, tmp_session):
        """Test querying a custom field."""
        mock_track._custom_fields["custom"] = "query"

        tmp_session.add(mock_track)

        assert query("custom:query")
