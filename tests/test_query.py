"""Tests the core query module."""

from datetime import date
from unittest.mock import MagicMock

import pytest

from moe.library import Album, Extra, Track
from moe.query import QueryError, QueryType, query
from tests.conftest import album_factory, extra_factory, track_factory


class TestQueries:
    """Test queries."""

    def test_empty_query_str(self):
        """Empty queries strings should raise a QueryError."""
        with pytest.raises(QueryError):
            query(MagicMock(), "", QueryType.TRACK)

    def test_empty_query(self, tmp_session):
        """Empty queries should return an empty list."""
        assert not query(tmp_session, "title:nope", QueryType.TRACK)

    def test_invalid_query_str(self):
        """Invalid queries should raise a QueryError."""
        with pytest.raises(QueryError):
            query(MagicMock(), "invalid", QueryType.TRACK)

    def test_invalid_querty_type_separate(self):
        """Queries can have either a : or :: separator, otherwise throw QuerError."""
        with pytest.raises(QueryError):
            query(MagicMock(), "title$nope", QueryType.TRACK)

    def test_return_type(self, tmp_session):
        """Queries return the appropriate type."""
        album = album_factory()
        tmp_session.add(album)
        tmp_session.flush()

        albums = query(tmp_session, f"a:title:'{album.title}'", QueryType.ALBUM)
        extras = query(tmp_session, f"a:title:'{album.title}'", QueryType.EXTRA)
        tracks = query(tmp_session, f"a:title:'{album.title}'", QueryType.TRACK)

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

        assert query(tmp_session, f"a:year:{album.year}", QueryType.ALBUM)
        assert query(
            tmp_session, f"a:original_year:{album.original_year}", QueryType.ALBUM
        )

    def test_multiple_terms(self, tmp_session):
        """We should be able to query for multiple terms at once."""
        album = album_factory()
        tmp_session.add(album)
        tmp_session.flush()

        assert query(
            tmp_session, f"a:year:{album.year} a:title:{album.title}", QueryType.ALBUM
        )

    def test_regex(self, tmp_session):
        """Queries can use regular expression matching."""
        tmp_session.add(track_factory())
        tmp_session.flush()

        assert query(tmp_session, "title::.*", QueryType.TRACK)

    def test_path_query(self, tmp_config, tmp_session):
        """We can query for paths."""
        tmp_config(settings="default_plugins = ['write']")
        album = album_factory(exists=True)
        tmp_session.add(album)
        tmp_session.flush()

        assert query(tmp_session, f"'a:path:{album.path.resolve()}'", QueryType.ALBUM)
        assert query(tmp_session, "'a:path::.*'", QueryType.ALBUM)

    def test_case_insensitive_value(self, tmp_session):
        """Query values should be case-insensitive."""
        tmp_session.add(album_factory(title="TMP"))
        tmp_session.flush()

        assert query(tmp_session, "a:title:tmp", QueryType.ALBUM)

    def test_regex_non_str(self, tmp_session):
        """Non string fields should be converted to strings for matching."""
        tmp_session.add(album_factory())
        tmp_session.flush()

        assert query(tmp_session, "a:year::.*", QueryType.ALBUM)

    def test_invalid_regex(self, tmp_session):
        """Invalid regex queries should raise a QueryError."""
        tmp_session.add(album_factory())
        tmp_session.flush()

        with pytest.raises(QueryError):
            query(tmp_session, "title::[", QueryType.ALBUM)

    def test_regex_case_insensitive(self, tmp_session):
        """Regex queries should be case-insensitive."""
        tmp_session.add(album_factory(title="TMP"))
        tmp_session.flush()

        assert query(tmp_session, "a:title::tmp", QueryType.ALBUM)

    def test_like_query(self, tmp_session):
        """Test sql LIKE queries. '%' and '_' are wildcard characters."""
        tmp_session.add(track_factory(track_num=1))
        tmp_session.flush()

        assert query(tmp_session, "track_num:_", QueryType.TRACK)
        assert query(tmp_session, "track_num:%", QueryType.TRACK)

    def test_like_escape_query(self, tmp_session):
        r"""We should be able to escape the LIKE wildcard characters with '/'.

        Note, I think '\' would be the preferred backslash character, but shlex
        removes them from strings.
        """
        tmp_session.add(album_factory(title="a"))
        tmp_session.add(album_factory(title="_"))
        tmp_session.flush()

        assert len(query(tmp_session, "a:title:/_", QueryType.ALBUM)) == 1

    def test_track_genre_query(self, tmp_session):
        """Querying 'genre' should use the 'genres' field."""
        tmp_session.add(track_factory(genres={"hip hop", "rock"}))
        tmp_session.flush()

        assert query(tmp_session, "'genre::.*'", QueryType.TRACK)
        assert query(tmp_session, "'genre:hip hop'", QueryType.TRACK)

    def test_album_catalog_num_query(self, tmp_session):
        """Querying 'catalog_num' should use the 'catalog_nums' field."""
        tmp_session.add(album_factory(catalog_nums={"1", "2"}))
        tmp_session.flush()

        assert query(tmp_session, "a:catalog_num:1 a:catalog_num:2", QueryType.ALBUM)

    def test_wildcard_query(self, tmp_session):
        """'*' as a query should return all items."""
        tmp_session.add(album_factory())
        tmp_session.flush()

        assert len(query(tmp_session, "*", QueryType.ALBUM)) == 1

    def test_missing_extras_tracks(self, tmp_session):
        """Ensure albums without extras or tracks."""
        album = album_factory(num_extras=0, num_tracks=0)

        tmp_session.add(album)
        tmp_session.flush()

        assert len(query(tmp_session, "*", QueryType.ALBUM)) == 1

    def test_custom_fields(self, tmp_session):
        """We can query a custom field."""
        album = album_factory(blah="album")
        extra_factory(album=album, blah="extra")
        track_factory(album=album, blah="track")

        tmp_session.add(album)
        tmp_session.flush()

        assert query(
            tmp_session, "a:blah:album t:blah:track e:blah:extra", QueryType.ALBUM
        )

    def test_custom_field_regex(self, tmp_session):
        """We can regex query a custom field."""
        album = album_factory(blah="album")
        extra_factory(album=album, blah=3)
        track_factory(album=album, blah="track")

        tmp_session.add(album)
        tmp_session.flush()

        assert query(
            tmp_session, "a:blah::albu. t:blah::trac. e:blah::3", QueryType.ALBUM
        )

    def test_custom_list_field(self, tmp_session):
        """We can query custom list fields."""
        album = album_factory(blah=["album", 1])
        extra_factory(album=album, blah=["extra", 2])
        track_factory(album=album, blah=["track", 3])

        tmp_session.add(album)
        tmp_session.flush()

        assert query(
            tmp_session, "a:blah:album t:blah:track e:blah:extra", QueryType.ALBUM
        )
        assert query(tmp_session, "a:blah:1 e:blah:2 t:blah:3", QueryType.ALBUM)
        assert query(tmp_session, "t:blah:3 t:blah:track", QueryType.ALBUM)

    def test_numeric_query_range(self, tmp_session):
        """We can query for a range."""
        tmp_session.add(track_factory(track_num=2))
        tmp_session.flush()

        assert query(tmp_session, "t:track_num:1..3", QueryType.TRACK)

    def test_numeric_lt(self, tmp_session):
        """Numeric queries without a lower bound test less than the upper bound."""
        tmp_session.add(track_factory(track_num=1))
        tmp_session.flush()

        assert query(tmp_session, "t:track_num:..3", QueryType.TRACK)

    def test_numeric_gt(self, tmp_session):
        """Numeric queries without an upper bound test greater than the lower bound."""
        tmp_session.add(track_factory(track_num=2))
        tmp_session.flush()

        assert query(tmp_session, "t:track_num:1..", QueryType.TRACK)

    def test_numeric_query_inclusive(self, tmp_session):
        """Numeric queries should be inclusive of their upper or lower bounds."""
        tracks = [track_factory(track_num=1), track_factory(track_num=3)]
        tmp_session.add_all(tracks)
        tmp_session.flush()

        assert len(query(tmp_session, "t:track_num:1..3", QueryType.TRACK)) == len(
            tracks
        )
        assert len(query(tmp_session, "t:track_num:1..", QueryType.TRACK)) == len(
            tracks
        )
        assert len(query(tmp_session, "t:track_num:..3", QueryType.TRACK)) == len(
            tracks
        )
