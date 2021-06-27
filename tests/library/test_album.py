"""Tests an Album object."""

import pytest

from moe.core.library.session import DbDupAlbumError, session_scope


class TestDuplicate:
    """Test behavior when there is an attempt to add a duplicate Album to the db.

    A duplicate Album is defined as a combination of the artist, title, and year.
    If a duplicate is found when committing to the database, we should raise a
    ``DbDupAlbumError``.

    A duplicate can also be because two Albums have the same path.
    If a duplicate is found when committing to the database, we should raise a
    ``DbDupAlbumPathError``.

    Duplicates should not error if using ``album.merge_existing(session)``.

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
        album1.date = album2.date

        with pytest.raises(DbDupAlbumError):
            with session_scope() as session:
                session.add(album1)
                session.add(album2)

    def test_dup_merge(self, mock_album_factory, tmp_session):
        """Duplicate errors should not occur if using `Album.merge_existing()`."""
        album1 = mock_album_factory()
        album2 = mock_album_factory()
        album1.date = album2.date
        album1.path = album2.path

        with session_scope() as session:
            session.add(album1)
            album2.merge_existing(session)

    def test_dup_path(self, mock_album_factory, tmp_session):
        """Duplicate albums can also be defined as having the same path.

        These should also raise the same DbDupTrackError.
        """
        album1 = mock_album_factory()
        album2 = mock_album_factory()
        album2.path = album1.path

        with pytest.raises(DbDupAlbumError):
            with session_scope() as session:
                session.add(album1)
                session.add(album2)
