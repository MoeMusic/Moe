"""Test an Album object."""

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


class TestGetOrCreate:
    """Test `get_or_create()`."""

    def test_album_dne(self, tmp_session):
        """We should return a new Album() if a match doesn't exist."""
        album = Album.get_or_create(
            tmp_session, artist="this doesnt", title="exist", year=1
        )

        assert isinstance(album, Album)

    def test_album_exists(self, tmp_session):
        """Return the matching album if it exists in the database."""
        artist = "this does"
        title = "exist"
        year = 1

        old_album = Album(artist=artist, title=title, year=year)
        tmp_session.add(old_album)

        new_album = Album.get_or_create(
            tmp_session, artist=artist, title=title, year=year
        )
        assert new_album is old_album


class TestDuplicate:
    """Test behavior when there is an attempt to add a duplicate Album to the db.

    A duplicate Album is defined as a combination of the artist, title, and year.
    If a duplicate is found when committing to the database, we should raise a
    DbDupAlbumError.

    Note:
        This error will only occur upon the session being flushed or committed.
        If you wish to catch this error, then you should use a new session scope
        as shown in `test_dup()`. This will allow you to catch the error by wrapping
        the `with` statement with a `try/except`.
    """

    def test_dup(self, mock_track_factory):
        """Duplicate albums should raise a DbDupAlbumError."""
        artist = "Dup"
        title = "licate"
        year = 9999

        album1 = Album(artist=artist, title=title, year=year)
        album2 = Album(artist=artist, title=title, year=year)

        with pytest.raises(DbDupAlbumError):
            with session_scope() as session:
                session.add(album1)
                session.add(album2)
