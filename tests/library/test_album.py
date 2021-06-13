"""Tests an Album object."""

import pathlib

import pytest

from moe.core.library.session import DbDupAlbumError, DbDupAlbumPathError, session_scope


class TestToDict:
    """Test dict representation of an album."""

    def test_second_track_attribute_dne(self, mock_track_factory):
        """If varying existence of fields between tracks, set field to Various.

        For example, if track 1 has a year, but track 2 doesn't. The album should
        display `year: Various`.
        """
        track1 = mock_track_factory()
        track2 = mock_track_factory()

        track1.artist = "don't show this"
        track2.artist = ""
        track1.album_obj = track2.album_obj

        assert track1.album_obj.to_dict()["artist"] == "Various"

    def test_second_track_attribute_different(self, mock_track_factory):
        """If varying field values between tracks, set field to Various."""
        track1 = mock_track_factory()
        track2 = mock_track_factory()

        track1.artist = "don't show this"
        track2.artist = "different"
        track1.album_obj = track2.album_obj

        assert track1.album_obj.to_dict()["artist"] == "Various"


class TestEquals:
    """Equality based on primary key."""

    def test_equals(self, mock_album_factory):
        """Equal if two albums share the same primary key attributes."""
        album1 = mock_album_factory()
        album2 = mock_album_factory()

        album1.artist = album2.artist
        album1.title = album2.title
        album1.year = album2.year

        assert album1 == album2

    def test_not_equals(self, mock_album_factory):
        """Not equal if two albums don't share the same primary key attributes."""
        album1 = mock_album_factory()
        album2 = mock_album_factory()

        assert album1 != album2


class TestPathSet:
    """Test path set event."""

    def test_path_dne(self, mock_album):
        """Raise an error if setting a path that doesn't exist."""
        with pytest.raises(NotADirectoryError):
            mock_album.path = pathlib.Path("also doesnt exist")


class TestDuplicate:
    """Test behavior when there is an attempt to add a duplicate Album to the db.

    A duplicate Album is defined as a combination of the artist, title, and year.
    If a duplicate is found when committing to the database, we should raise a
    ``DbDupAlbumError``.

    A duplicate can also be because two Albums have the same path.
    If a duplicate is found when committing to the database, we should raise a
    ``DbDupAlbumPathError``.

    If we use `session.merge()` to add an Album, a duplicate error should only occur
    for duplicate paths, and not because of its tags. This is because an Album's
    primary key is based off of its tags, and `session.merge()` uses an object's
    primary key to merge any existing objects.

    Note:
        This error will only occur upon the session being flushed or committed.
        If you wish to catch this error, then you should use a new session scope
        as shown in `test_dup()`. This will allow you to catch the error by wrapping
        the `with` statement with a `try/except`.
    """

    def test_dup(self, mock_album_factory, tmp_session):
        """Duplicate albums should raise a DbDupAlbumError."""
        album1 = mock_album_factory()
        album2 = mock_album_factory()
        album1.year = album2.year

        with pytest.raises(DbDupAlbumError):
            with session_scope() as session:
                session.add(album1)
                session.add(album2)

    def test_dup_merge(self, mock_album_factory, tmp_session):
        """Duplicate errors should not occur if using `session.merge()`."""
        album1 = mock_album_factory()
        album2 = mock_album_factory()
        album1.year = album2.year

        with session_scope() as session:
            session.merge(album1)
            session.merge(album2)

    def test_dup_path(self, mock_album_factory, tmp_session):
        """Duplicate tracks can also be defined as having the same path.

        These should also raise the same DbDupTrackError.
        """
        album1 = mock_album_factory()
        album2 = mock_album_factory()
        album2.path = album1.path

        with pytest.raises(DbDupAlbumPathError):
            with session_scope() as session:
                session.merge(album1)
                session.merge(album2)
