"""Tests an Album object."""

import copy

from moe.library.album import Album
from moe.library.extra import Extra


class TestGetExisting:
    """Test we can match an existing album based on unique attributes."""

    def test_by_path(self, real_album_factory, tmp_session):
        """Get an exisiting album from a matching path."""
        album1 = real_album_factory()
        album2 = real_album_factory()

        tmp_session.merge(album2)
        album1.path = album2.path

        assert album1.get_existing()

    def test_by_mb_album_id(self, real_album_factory, tmp_session):
        """Get an exisiting album from a matching mb_album_id."""
        album1 = real_album_factory()
        album2 = real_album_factory()

        tmp_session.merge(album2)
        album1.mb_album_id = album2.mb_album_id

        assert album1.get_existing()


class TestIsUnique:
    """Test determing if an album is unique based on its tags."""

    def test_mb_album_id(self, real_album):
        """Albums with different mb_album_ids are unique."""
        dup_album = copy.deepcopy(real_album)

        real_album.mb_album_id = "1"
        assert real_album != dup_album

        assert real_album.is_unique(dup_album)


class TestMerge:
    """Test merging two albums together."""

    def test_merge_extras(self, real_album_factory, tmp_session):
        """Any extra conflicts should be overwritten by the current album."""
        album1 = real_album_factory()
        album2 = real_album_factory()
        album1.date = album2.date
        album1.path = album2.path
        assert not album1.is_unique(album2)

        mutual_extra = Extra(album1.path / "log.txt", album1)
        Extra(album2.path / "log.txt", album2)  # should get overwritten
        new_extra = Extra(album2.path / "new.txt", album2)  # should persist

        assert album1.extras != album2.extras

        tmp_session.merge(album1)
        album2.merge(album2.get_existing())
        tmp_session.merge(album2)

        db_album = tmp_session.query(Album).one()

        assert mutual_extra in db_album.extras
        assert new_extra in db_album.extras

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
        existing_album = album2.get_existing()
        album2.merge(existing_album)
        tmp_session.merge(album2)

        db_album = tmp_session.query(Album).one()

        assert len(db_album.tracks) == len(album1.tracks)
        for db_track in db_album.tracks:
            assert db_track.title != "overwrite me"

    def test_overwrite_album_info(self, mock_album, tmp_session):
        """If overwriting, the current album's data should be kept if conflict."""
        dup_album = copy.deepcopy(mock_album)

        mock_album.artist = "conflict"  # conflict field; should overwrite on album2
        assert not mock_album.is_unique(dup_album)

        tmp_session.merge(dup_album)
        mock_album.merge(mock_album.get_existing(), overwrite_album_info=True)
        tmp_session.merge(mock_album)

        db_album = tmp_session.query(Album).one()
        assert db_album.artist == "conflict"

    def test_keep_album_info(self, mock_album, tmp_session):
        """If ``overwrite_album_info=False`` don't overwrite the album info."""
        dup_album = copy.deepcopy(mock_album)

        mock_album.artist = "conflict"  # conflict field; don't overwrite
        assert not mock_album.is_unique(dup_album)

        tmp_session.merge(dup_album)
        mock_album.merge(mock_album.get_existing(), overwrite_album_info=False)
        tmp_session.merge(mock_album)

        db_album = tmp_session.query(Album).one()
        assert db_album.artist != "conflict"


class TestDuplicate:
    """Test behavior when there is an attempt to add a duplicate Album to the db.

    A duplicate Album is defined as having any of the same unique attributes: path, or
    mb_album_id.

    To handle duplicates by tags, you should use ``album.get_existing(session)`` to get
    the existing album. At this point, you can either delete the existing album from the
    session using ``session.delete()``, or you can merge it with the current album
    using ``album.merge()``. Finally, to add the current album into the session,
    make sure to use ``session.merge()``.

    Note:
        This error will only occur upon the session being flushed or committed.
        If you wish to catch this error, then you should use a new session scope. This
        will allow you to catch the error by wrapping the `with` statement with a
        `try/except`.
    """

    def test_dup_deleted(self, real_album_factory, tmp_session):
        """Duplicate errors should not occur if the existing album is deleted."""
        album1 = real_album_factory()
        album2 = real_album_factory()
        album1.date = album2.date
        album1.path = album2.path

        album1.tracks.pop(0)
        album1.extras.pop(0)

        tmp_session.add(album1)
        tmp_session.delete(album2.get_existing())
        tmp_session.merge(album2)

        db_album = tmp_session.query(Album).one()
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

        tmp_session.add(album1)
        album2.merge(album2.get_existing())
        tmp_session.merge(album2)

        db_album = tmp_session.query(Album).one()
        assert sorted(db_album.tracks) == sorted(album2.tracks)
        assert sorted(db_album.extras) == sorted(album2.extras)
