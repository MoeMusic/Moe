"""Tests the core query module."""


from datetime import date
from unittest.mock import MagicMock

import pytest

import moe.query
from moe.library import Album, Extra, Track
from moe.query import QueryError, query
from tests.conftest import album_factory, extra_factory, track_factory


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
            query(MagicMock(), "", "track")

    def test_empty_query(self, tmp_session):
        """Empty queries should return an empty list."""
        assert not query(tmp_session, "title:nope", "track")

    def test_invalid_query_str(self, tmp_session):
        """Invalid queries should raise a QueryError."""
        with pytest.raises(QueryError):
            query(tmp_session, "invalid", "track")

    def test_return_type(self, tmp_session):
        """Queries return the appropriate type."""
        album = album_factory()
        tmp_session.add(album)
        tmp_session.flush()

        albums = query(tmp_session, f"a:title:'{album.title}'", "album")
        extras = query(tmp_session, f"a:title:'{album.title}'", "extra")
        tracks = query(tmp_session, f"a:title:'{album.title}'", "track")

        assert albums
        for album in albums:
            assert isinstance(album, Album)
        assert extras
        for extra in extras:
            assert isinstance(extra, Extra)
        assert tracks
        for track in tracks:
            assert isinstance(track, Track)

    def test_years(self, tmp_session):
        """We can query an album's year and original year directly."""
        album = album_factory(date=date(1999, 1, 2), original_date=date(1998, 1, 1))
        tmp_session.add(album)
        tmp_session.flush()

        assert query(tmp_session, f"a:year:{album.year}", "album")
        assert query(tmp_session, f"a:original_year:{album.original_year}", "album")

    def test_multiple_terms(self, tmp_session):
        """We should be able to query for multiple terms at once."""
        album = album_factory()
        tmp_session.add(album)
        tmp_session.flush()

        assert query(tmp_session, f"a:year:{album.year} a:title:{album.title}", "album")

    def test_regex(self, tmp_session):
        """Queries can use regular expression matching."""
        tmp_session.add(track_factory())
        tmp_session.flush()

        assert query(tmp_session, "title::.*", "track")

    def test_path_query(self, tmp_config, tmp_session):
        """We can query for paths."""
        tmp_config(settings="default_plugins = ['write']")
        album = album_factory(exists=True)
        tmp_session.add(album)
        tmp_session.flush()

        assert query(tmp_session, f"'a:path:{str(album.path.resolve())}'", "album")
        assert query(tmp_session, "'a:path::.*'", "album")

    def test_case_insensitive_value(self, tmp_session):
        """Query values should be case-insensitive."""
        tmp_session.add(album_factory(title="TMP"))
        tmp_session.flush()

        assert query(tmp_session, "a:title:tmp", "album")

    def test_regex_non_str(self, tmp_session):
        """Non string fields should be converted to strings for matching."""
        tmp_session.add(album_factory())
        tmp_session.flush()

        assert query(tmp_session, "a:year::.*", "album")

    def test_invalid_regex(self, tmp_session):
        """Invalid regex queries should raise a QueryError."""
        tmp_session.add(album_factory())
        tmp_session.flush()

        with pytest.raises(QueryError):
            query(tmp_session, "title::[", "album")

    def test_regex_case_insensitive(self, tmp_session):
        """Regex queries should be case-insensitive."""
        tmp_session.add(album_factory(title="TMP"))
        tmp_session.flush()

        assert query(tmp_session, "a:title::tmp", "album")

    def test_like_query(self, tmp_session):
        """Test sql LIKE queries. '%' and '_' are wildcard characters."""
        tmp_session.add(track_factory(track_num=1))
        tmp_session.flush()

        assert query(tmp_session, "track_num:_", "track")
        assert query(tmp_session, "track_num:%", "track")

    def test_like_escape_query(self, tmp_session):
        r"""We should be able to escape the LIKE wildcard characters with '/'.

        Note, I think '\' would be the preferred backslash character, but shlex
        removes them from strings.
        """
        tmp_session.add(album_factory(title="a"))
        tmp_session.add(album_factory(title="_"))
        tmp_session.flush()

        assert len(query(tmp_session, "a:title:/_", "album")) == 1

    def test_track_genre_query(self, tmp_session):
        """Querying 'genre' should use the 'genres' field."""
        tmp_session.add(track_factory(genres={"hip hop", "rock"}))
        tmp_session.flush()

        assert query(tmp_session, "'genre::.*'", "track")
        assert query(tmp_session, "'genre:hip hop'", "track")

    def test_album_catalog_num_query(self, tmp_session):
        """Querying 'catalog_num' should use the 'catalog_nums' field."""
        tmp_session.add(album_factory(catalog_nums={"1", "2"}))
        tmp_session.flush()

        assert query(tmp_session, "a:catalog_num:1 a:catalog_num:2", "album")

    def test_wildcard_query(self, tmp_session):
        """'*' as a query should return all items."""
        tmp_session.add(album_factory())
        tmp_session.flush()

        assert len(query(tmp_session, "*", "album")) == 1

    def test_missing_extras_tracks(self, tmp_session):
        """Ensure albums without extras or tracks."""
        album = album_factory(num_extras=0, num_tracks=0)

        tmp_session.add(album)
        tmp_session.flush()

        assert len(query(tmp_session, "*", "album")) == 1

    def test_custom_fields(self, tmp_session):
        """We can query a custom field."""
        album = album_factory(blah="album")
        extra_factory(album=album, blah="extra")
        track_factory(album=album, blah="track")

        tmp_session.add(album)
        tmp_session.flush()

        assert query(tmp_session, "a:blah:album t:blah:track e:blah:extra", "album")

    def test_custom_field_regex(self, tmp_session):
        """We can regex query a custom field."""
        album = album_factory(blah="album")
        extra_factory(album=album, blah=3)
        track_factory(album=album, blah="track")

        tmp_session.add(album)
        tmp_session.flush()

        assert query(tmp_session, "a:blah::albu. t:blah::trac. e:blah::3", "album")

    def test_custom_list_field(self, tmp_session):
        """We can query custom list fields."""
        album = album_factory(blah=["album", 1])
        extra_factory(album=album, blah=["extra", 2])
        track_factory(album=album, blah=["track", 3])

        tmp_session.add(album)
        tmp_session.flush()

        assert query(tmp_session, "a:blah:album t:blah:track e:blah:extra", "album")
        assert query(tmp_session, "a:blah:1 e:blah:2 t:blah:3", "album")
        assert query(tmp_session, "t:blah:3 t:blah:track", "album")

    def test_numeric_query_range(self, tmp_session):
        """We can query for a range."""
        tmp_session.add(track_factory(track_num=2))
        tmp_session.flush()

        assert query(tmp_session, "t:track_num:1..3", "track")

    def test_numeric_lt(self, tmp_session):
        """Numeric queries without a lower bound test less than the upper bound."""
        tmp_session.add(track_factory(track_num=1))
        tmp_session.flush()

        assert query(tmp_session, "t:track_num:..3", "track")

    def test_numeric_gt(self, tmp_session):
        """Numeric queries without an upper bound test greater than the lower bound."""
        tmp_session.add(track_factory(track_num=2))
        tmp_session.flush()

        assert query(tmp_session, "t:track_num:1..", "track")

    def test_numeric_query_inclusive(self, tmp_session):
        """Numeric queries should be inclusive of their upper or lower bounds."""
        tmp_session.add(track_factory(track_num=1))
        tmp_session.add(track_factory(track_num=3))
        tmp_session.flush()

        assert len(query(tmp_session, "t:track_num:1..3", "track")) == 2
        assert len(query(tmp_session, "t:track_num:1..", "track")) == 2
        assert len(query(tmp_session, "t:track_num:..3", "track")) == 2
