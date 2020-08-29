"""Test the core query module."""

from unittest.mock import Mock

from moe.core import query
from moe.core.library import Album, Track


class TestParseQuery:
    """Test the query string parsing _parse_query()."""

    def test_basic(self):
        """Simplest case field:value test."""
        matches = query._parse_query("field:value")

        assert matches[0]["field"] == "field"
        assert matches[0]["separator"] == ":"
        assert matches[0]["value"] == "value"
        assert len(matches) == 1

    def test_escaped_colon(self):
        """Values can contain escaped colons."""
        matches = query._parse_query(r"field:val\:ue")

        assert matches[0]["field"] == "field"
        assert matches[0]["value"] == "val:ue"
        assert len(matches) == 1

    def test_multiple(self):
        """Queries can contain more than one field:value."""
        matches = query._parse_query(r"field:value field2:value2")

        assert matches[0]["field"] == "field"
        assert matches[0]["value"] == "value"
        assert matches[1]["field"] == "field2"
        assert matches[1]["value"] == "value2"
        assert len(matches) == 2

    def test_value_spaces(self):
        """Values can contain arbitrary whitespace.

        The only exception is immediately after the colon.
        """
        matches = query._parse_query(r"field:val u e")

        assert matches[0]["field"] == "field"
        assert matches[0]["value"] == "val u e"
        assert len(matches) == 1

    def test_value_spaces_multiple(self):
        """Values shouldn't match the next field if it exists.

        This can become tricky to match if the value also contains whitespace.
        """
        matches = query._parse_query(r"field:val u e field2:value2")

        assert matches[0]["field"] == "field"
        assert matches[0]["value"] == "val u e"
        assert matches[1]["field"] == "field2"
        assert matches[1]["value"] == "value2"
        assert len(matches) == 2

    def test_unescaped_colons(self):
        """Unescaped colons are fine as long as they don't look like 'field:value'."""
        matches = query._parse_query(r"field:Vol 1: field2:Vol: 1")

        assert matches[0]["field"] == "field"
        assert matches[0]["value"] == "Vol 1:"
        assert matches[1]["field"] == "field2"
        assert matches[1]["value"] == "Vol: 1"
        assert len(matches) == 2

    def test_regex_value(self):
        """Regular expression values are indicated by a '::' separator."""
        matches = query._parse_query(r"field::A.*")

        assert matches[0]["field"] == "field"
        assert matches[0]["separator"] == "::"
        assert matches[0]["value"] == "A.*"
        assert len(matches) == 1


class TestQuery:
    """Test actual query."""

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

    def test_track_album_field_query(self, tmp_session, mock_track):
        """We should be able to query tracks that match album-related fields.

        These fields belong to the Album table and thus aren't normally exposed
        through a track.
        """
        mock_track.albumartist = "2Pac"
        mock_track.album = "All Eyez on Me"
        tmp_session.add(mock_track)

        assert query.query("album:All Eyez on Me", tmp_session)
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
