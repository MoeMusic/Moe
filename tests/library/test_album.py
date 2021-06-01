"""Tests an Album object."""

import pytest

from moe.core.library.album import Album
from moe.core.library.session import DbDupAlbumError, session_scope


class TestToDict:
    """Test dict representation of an album."""

    def test_single_track(self, mock_track):
        """If only one track, just return the track's dict."""
        assert mock_track._album_obj.to_dict() == mock_track.to_dict()

    def test_second_track_attribute_dne(self, mock_track_factory):
        """If varying existence of fields between tracks, set field to Various.

        For example, if track 1 has a year, but track 2 doesn't. The album should
        display `year: Various`.
        """
        track1 = mock_track_factory()
        track2 = mock_track_factory()

        track1.title = "don't show this"
        track2.title = ""
        track1._album_obj = track2._album_obj

        assert track1._album_obj.to_dict()["title"] == "Various"

    def test_second_track_attribute_different(self, mock_track_factory):
        """If varying field values between tracks, set field to Various."""
        track1 = mock_track_factory()
        track2 = mock_track_factory()

        track1.title = "don't show this"
        track2.title = "different"
        track1._album_obj = track2._album_obj

        assert track1._album_obj.to_dict()["title"] == "Various"


class TestEquals:
    """Equality based on primary key."""

    def test_equals(self):
        """Equal if two albums share the same primary key attributes."""
        album1 = Album(artist="this", title="is equal", year=1111)
        album2 = Album(artist="this", title="is equal", year=1111)

        assert album1 == album2

    def test_not_equals(self):
        """Not equal if two albums don't share the same primary key attributes."""
        album1 = Album(artist="this", title="is not equal", year=1111)
        album2 = Album(artist="this", title="is equal", year=1111)

        assert album1 != album2


class TestDuplicate:
    """Test behavior when there is an attempt to add a duplicate Album to the db.

    A duplicate Album is defined as a combination of the artist, title, and year.
    If a duplicate is found when committing to the database, we should raise a
    DbDupAlbumError.

    Duplicates should not error if using `session.merge()`

    Note:
        This error will only occur upon the session being flushed or committed.
        If you wish to catch this error, then you should use a new session scope
        as shown in `test_dup()`. This will allow you to catch the error by wrapping
        the `with` statement with a `try/except`.
    """

    def test_dup(self, tmp_session):
        """Duplicate albums should raise a DbDupAlbumError."""
        album1 = Album(artist="Dup", title="licate", year=1999)
        album2 = Album(artist="Dup", title="licate", year=1999)

        with pytest.raises(DbDupAlbumError):
            with session_scope() as session:
                session.add(album1)
                session.add(album2)

    def test_dup_merge(self, mock_track_factory, tmp_session):
        """Duplicate errors should not occur if using `session.merge()`."""
        album1 = Album(artist="Dup", title="licate", year=1999)
        album2 = Album(artist="Dup", title="licate", year=1999)

        with session_scope() as session:
            session.merge(album1)
            session.merge(album2)
