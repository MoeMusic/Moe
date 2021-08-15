"""Tests an Album object."""

import pytest

from moe.core.library.album import Album
from moe.core.library.extra import Extra
from moe.core.library.session import DbDupAlbumError, session_scope


class TestMerge:
    """Test merging two albums together."""

    def test_merge_extras(self, real_album_factory, tmp_session):
        """Any extra conflicts should be overwritten by the current album."""
        album1 = real_album_factory()
        album2 = real_album_factory()
        album1.date = album2.date
        album1.path = album2.path
        assert not album1.is_unique(album2)

        # should merge `mutual_extra`
        mutual_extra1 = album1.path / "log.txt"
        mutual_extra2 = album2.path / "log.txt"
        Extra(mutual_extra1, album1)
        Extra(mutual_extra2, album2)

        assert album1.extras != album2.extras

        tmp_session.merge(album1)
        album2.merge(album2.get_existing(tmp_session))
        tmp_session.merge(album2)

        db_album = tmp_session.query(Album).one()

        assert mutual_extra1 not in db_album.extras

    def test_merge_tracks(self, mock_album_factory, mock_track, tmp_session):
        """Any track conflicts should be overwritten by the current album."""
        album1 = mock_album_factory()
        album2 = mock_album_factory()
        album1.date = album2.date
        album1.path = album2.path
        assert not album1.is_unique(album2)

        album1.tracks.append(mock_track)
        for track in album1.tracks:
            if album2.get_track(track.track_num):
                track.title = "overwrite me"

        assert album1.tracks != album2.tracks

        tmp_session.merge(album1)
        existing_album = album2.get_existing(tmp_session)
        album2.merge(existing_album)
        tmp_session.merge(album2)

        db_album = tmp_session.query(Album).one()

        assert len(db_album.tracks) == len(album1.tracks)
        for db_track in db_album.tracks:
            assert db_track.title != "overwrite me"

    def test_overwrite_album_info(self, mock_album_factory, tmp_session):
        """If overwriting, the current album's data should be kept if conflict."""
        album1 = mock_album_factory()
        album2 = mock_album_factory()
        album1.date = album2.date
        album1.path = album2.path
        album1.mb_album_id = "1234"  # conflict field; should overwrite on album2
        assert not album1.is_unique(album2)
        assert album1.mb_album_id != album2.mb_album_id

        tmp_session.merge(album1)
        album2.merge(album2.get_existing(tmp_session), overwrite_album_info=True)
        tmp_session.merge(album2)

        db_album = tmp_session.query(Album).one()
        assert db_album.mb_album_id == album2.mb_album_id

    def test_keep_album_info(self, mock_album_factory, tmp_session):
        """If ``overwrite_album_info=False`` don't overwrite the album info."""
        album1 = mock_album_factory()
        album2 = mock_album_factory()
        album1.date = album2.date
        album1.path = album2.path
        album1.mb_album_id = "1234"
        assert not album1.is_unique(album2)
        assert album1.mb_album_id != album2.mb_album_id

        tmp_session.merge(album1)
        album2.merge(album2.get_existing(tmp_session), overwrite_album_info=False)
        tmp_session.merge(album2)

        db_album = tmp_session.query(Album).one()
        assert db_album.mb_album_id == album1.mb_album_id


class TestDuplicate:
    """Test behavior when there is an attempt to add a duplicate Album to the db.

    A duplicate Album can be defined as a combination of the artist, title, and date.
    If a duplicate is found when committing to the database, we should raise a
    ``DbDupAlbumError``.

    A duplicate can also be because two Albums have the same path.
    If a duplicate is found when committing to the database, we should raise a
    ``DbDupAlbumPathError``.

    To handle duplicates by tags, you should use ``album.get_existing(session)`` to get
    the existing album. At this point, you can either delete the existing album from the
    session using ``session.delete()``, or you can merge it with the current album
    using ``album.merge()``. Finally, to add the current album into the session,
    make sure to use ``session.merge()``.

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

    def test_dup_deleted(self, real_album_factory, tmp_session):
        """Duplicate errors should not occur if the existing album is deleted."""
        album1 = real_album_factory()
        album2 = real_album_factory()
        album1.date = album2.date
        album1.path = album2.path

        album1.tracks.pop(0)
        album1.extras.pop(0)

        with session_scope() as session:
            session.add(album1)
            session.delete(album2.get_existing(session))
            session.merge(album2)

            db_album = session.query(Album).one()
            assert sorted(db_album.tracks) == sorted(album2.tracks)
            assert sorted(db_album.extras) == sorted(album2.extras)

    def test_dup_merge(self, real_album_factory, tmp_session):
        """Duplicate errors should not occur if the existing album is merged."""
        album1 = real_album_factory()
        album2 = real_album_factory()
        album1.date = album2.date
        album1.path = album2.path

        album1.tracks.pop(0)
        album1.extras.pop(0)

        with session_scope() as session:
            session.add(album1)
            album2.merge(album2.get_existing(session))
            session.merge(album2)

            db_album = session.query(Album).one()
            assert sorted(db_album.tracks) == sorted(album2.tracks)
            assert sorted(db_album.extras) == sorted(album2.extras)

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
