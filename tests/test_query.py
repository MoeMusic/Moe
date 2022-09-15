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

        assert match["field_type"] == "track"
        assert match["field"] == "field"
        assert match["separator"] == ":"
        assert match["value"] == "value"

    def test_album_field_type(self):
        """Use 'a:' before the rest of the term to specify it's an album field."""
        match = moe.query._parse_term("a:field:value")

        assert match["field_type"] == "album"
        assert match["field"] == "field"
        assert match["separator"] == ":"
        assert match["value"] == "value"

    def test_extra_field_type(self):
        """Use 'a:' before the rest of the term to specify it's an extra field."""
        match = moe.query._parse_term("e:field:value")

        assert match["field_type"] == "extra"
        assert match["field"] == "field"
        assert match["separator"] == ":"
        assert match["value"] == "value"

    def test_track_field_type(self):
        """Optionally use 't:' before the rest of the term to specify a track field."""
        match = moe.query._parse_term("t:field:value")

        assert match["field_type"] == "track"
        assert match["field"] == "field"
        assert match["separator"] == ":"
        assert match["value"] == "value"

    def test_lowercase_field(self):
        """Fields should be case lowercase."""
        match = moe.query._parse_term("t:FIELD:value")

        assert match["field_type"] == "track"
        assert match["field"] == "field"
        assert match["separator"] == ":"
        assert match["value"] == "value"

    def test_value_spaces(self):
        """Values can contain arbitrary whitespace.

        The only exception is immediately after the colon.
        """
        match = moe.query._parse_term("field:val u e")

        assert match["field_type"] == "track"
        assert match["field"] == "field"
        assert match["value"] == "val u e"

    def test_regex_value(self):
        """Regular expression values are indicated by a '::' separator."""
        match = moe.query._parse_term("field::A.*")

        assert match["field_type"] == "track"
        assert match["field"] == "field"
        assert match["separator"] == "::"
        assert match["value"] == "A.*"

    def test_invalid(self):
        """Invalid terms should raise a ValueError."""
        with pytest.raises(QueryError):
            moe.query._parse_term("invalid")


class TestQueries:
    """Test queries."""

    def test_empty_query_str(self):
        """Empty queries strings should raise a QueryError."""
        with pytest.raises(QueryError):
            query("", "track")

    def test_empty_query(self, tmp_session):
        """Empty queries should return an empty list."""
        assert not query("title:nope", "track")

    def test_invalid_query_str(self, tmp_session):
        """Invalid queries should raise a QueryError."""
        with pytest.raises(QueryError):
            query("invalid", "track")

    def test_return_type(self, mock_album, tmp_session):
        """Queries return the appropriate type."""
        tmp_session.add(mock_album)

        albums = query(f"a:title:'{mock_album.title}'", "album")
        extras = query(f"a:title:'{mock_album.title}'", "extra")
        tracks = query(f"a:title:'{mock_album.title}'", "track")

        assert albums
        for album in albums:
            assert isinstance(album, Album)
        assert extras
        for extra in extras:
            assert isinstance(extra, Extra)
        assert tracks
        for track in tracks:
            assert isinstance(track, Track)

    def test_multiple_terms(self, mock_album, tmp_session):
        """We should be able to query for multiple terms at once."""
        tmp_session.add(mock_album)

        assert query(f"a:year:{mock_album.year} album:{mock_album.title}", "album")

    def test_regex(self, mock_track, tmp_session):
        """Queries can use regular expression matching."""
        tmp_session.add(mock_track)

        assert query("title::.*", "track")

    def test_path_query(self, real_album, tmp_session):
        """We can query for paths."""
        tmp_session.add(real_album)

        assert query(f"'a:path:{str(real_album.path.resolve())}'", "album")
        assert query("'a:path::.*'", "album")

    def test_case_insensitive_value(self, mock_album, tmp_session):
        """Query values should be case-insensitive."""
        mock_album.title = "TMP"
        tmp_session.add(mock_album)

        assert query("a:title:tmp", "album")

    def test_regex_non_str(self, mock_album, tmp_session):
        """Non string fields should be converted to strings for matching."""
        tmp_session.add(mock_album)

        assert query("a:year::.*", "album")

    def test_invalid_regex(self, tmp_session, mock_album):
        """Invalid regex queries should raise a QueryError."""
        tmp_session.add(mock_album)

        with pytest.raises(QueryError):
            query("title::[", "album")

    def test_regex_case_insensitive(self, mock_album, tmp_session):
        """Regex queries should be case-insensitive."""
        mock_album.title = "TMP"
        tmp_session.add(mock_album)

        assert query("a:title::tmp", "album")

    def test_track_album_field(self, mock_album, tmp_session):
        """We should be able to query tracks that match album-related fields.

        These fields belong to the Album table and thus aren't normally exposed
        through a track.
        """
        tmp_session.add(mock_album)

        assert query(f"'album:{mock_album.title}'", "track")

    def test_like_query(self, mock_track, tmp_session):
        """Test sql LIKE queries. '%' and '_' are wildcard characters."""
        mock_track.track_num = 1
        tmp_session.add(mock_track)

        assert query("track_num:_", "track")
        assert query("track_num:%", "track")

    def test_like_escape_query(self, album_factory, tmp_session):
        r"""We should be able to escape the LIKE wildcard characters with '/'.

        Note, I think '\' would be the preferred backslash character, but shlex
        removes them from strings.
        """
        album1 = album_factory(title="a")
        album2 = album_factory(title="_")
        tmp_session.add(album1)
        tmp_session.add(album2)

        assert len(query("a:title:/_", "album")) == 1

    def test_multi_value_query(self, mock_album, tmp_session):
        """We should be able to query multi-value fields transparently.

        ``genre`` is a list of genres for a Track.
        """
        mock_album.tracks[0].genres = ["hip hop", "rock"]
        tmp_session.add(mock_album)

        assert query("'genre::.*'", "track")
        assert query("'genre:hip hop'", "track")

    def test_wildcard_query(self, mock_album, tmp_session):
        """'*' as a query should return all items."""
        tmp_session.add(mock_album)

        assert len(query("*", "album")) == 1

    def test_missing_extras(self, album_factory, tmp_session):
        """Ensure albums without extras are still returned by a valid query."""
        album = album_factory(num_extras=0)

        tmp_session.add(album)

        assert len(query("*", "album")) == 1

    def test_custom_fields(self, mock_album, tmp_session):
        """We can query a custom field."""
        track = mock_album.tracks[0]
        extra = mock_album.extras[0]

        mock_album.custom_fields = ["custom"]
        mock_album._custom_fields["custom"] = "album"
        extra.custom_fields = ["custom"]
        extra._custom_fields["custom"] = "extra"
        track.custom_fields = ["custom"]
        track._custom_fields["custom"] = "track"

        tmp_session.add(mock_album)

        assert query("a:custom:album t:custom:track e:custom:extra", "album")

    def test_custom_field_regex(self, mock_album, tmp_session):
        """We can regex query a custom field."""
        track = mock_album.tracks[0]
        extra = mock_album.extras[0]

        mock_album.custom_fields = ["custom"]
        mock_album._custom_fields["custom"] = "album"
        extra.custom_fields = ["custom"]
        extra._custom_fields["custom"] = 3
        track.custom_fields = ["custom"]
        track._custom_fields["custom"] = "track"

        tmp_session.add(mock_album)

        assert query("a:custom::albu. t:custom::trac. e:custom::3", "album")

    def test_custom_list_field(self, mock_album, tmp_session):
        """We can query custom list fields."""
        track = mock_album.tracks[0]
        extra = mock_album.extras[0]

        mock_album.custom_fields = ["custom"]
        mock_album._custom_fields["custom"] = ["album", 1]
        extra.custom_fields = ["custom"]
        extra._custom_fields["custom"] = ["extra", 2]
        track.custom_fields = ["custom"]
        track._custom_fields["custom"] = ["track", 3]

        tmp_session.add(mock_album)

        import sqlalchemy as sa

        field = "custom"
        custom_func = sa.func.json_each(
            Album._custom_fields, f"$.{field}"
        ).table_valued("value", joins_implicitly=True)
        tmp_session.query(Album).filter(custom_func.c.value.ilike(1)).one()

        assert query("a:custom:album t:custom:track e:custom:extra", "album")
        assert query("a:custom:1 e:custom:2 t:custom:3", "album")
        assert query("t:custom:3 t:custom:track", "album")
