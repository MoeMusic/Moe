"""Tests an Album object."""

import copy

from moe.library.album import Album
from moe.library.extra import Extra


class TestGetExisting:
    """Test we can match an existing album based on unique attributes."""

    def test_by_path(self, mock_album_factory, tmp_session):
        """Get an exisiting album from a matching path."""
        album1 = mock_album_factory()
        album2 = mock_album_factory()
        album1.path = album2.path

        tmp_session.merge(album2)

        assert album1.get_existing()

    def test_by_mb_album_id(self, mock_album_factory, tmp_session):
        """Get an exisiting album from a matching mb_album_id."""
        album1 = mock_album_factory()
        album2 = mock_album_factory()
        album1.mb_album_id = "123"
        album2.mb_album_id = album1.mb_album_id

        tmp_session.merge(album2)

        assert album1.get_existing()

    def test_null_match(self, mock_album_factory, tmp_session):
        """Don't match off of null values."""
        album1 = mock_album_factory()
        album2 = mock_album_factory()
        assert not album1.mb_album_id
        assert not album2.mb_album_id
        assert album1.path != album2.path

        tmp_session.merge(album1)

        assert not album2.get_existing()


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

    def test_conflict_persists(self, mock_album_factory):
        """Don't overwrite any conflicts."""
        album = mock_album_factory()
        other_album = mock_album_factory()
        album.mb_album_id = "123"
        other_album.mb_album_id = "456"
        assert album.mb_album_id and other_album.mb_album_id
        keep_mb_album_id = album.mb_album_id

        album.merge(other_album)

        assert album.mb_album_id == keep_mb_album_id

    def test_merge_non_conflict(self, mock_album_factory):
        """Apply any non-conflicting fields."""
        album = mock_album_factory()
        other_album = mock_album_factory()
        album.mb_album_id = None
        other_album.mb_album_id = "456"

        album.merge(other_album)

        assert album.mb_album_id == "456"

    def test_none_merge(self, mock_album_factory):
        """Don't merge in any null values."""
        album = mock_album_factory()
        other_album = mock_album_factory()
        album.mb_album_id = "123"
        other_album.mb_album_id = None

        album.merge(other_album)

        assert album.mb_album_id == "123"

    def test_overwrite_field(self, mock_album_factory):
        """Overwrite fields if the option is given."""
        album = mock_album_factory()
        other_album = mock_album_factory()
        album.mb_album_id = "123"
        other_album.mb_album_id = "456"
        assert album.mb_album_id and other_album.mb_album_id
        keep_mb_album_id = other_album.mb_album_id

        album.merge(other_album, overwrite=True)

        assert album.mb_album_id == keep_mb_album_id

    def test_merge_extras(self, mock_album_factory):
        """Merge in any new extras."""
        album1 = mock_album_factory()
        album2 = mock_album_factory()
        new_extra = Extra(album2.path / "new.txt", album2)
        assert album1.extras != album2.extras
        extras_count = len(album1.extras) + len(album2.extras)

        album1.merge(album2)

        assert new_extra in album1.extras
        assert len(album1.extras) == extras_count

    def test_overwrite_extras(self, real_album_factory):
        """Replace conflicting extras if told to overwrite."""
        album1 = real_album_factory()
        album2 = real_album_factory()

        conflict_extra = Extra(album2.path / album1.extras[0].filename, album2)
        overwrite_extra = album1.get_extra(conflict_extra.filename)
        overwrite_extra.path.write_text("overwrite")
        assert overwrite_extra.path.exists()

        album1.merge(album2, overwrite=True)

        for extra in album1.extras:
            if extra.path.exists():
                assert extra.path.read_text() != "overwrite"

    def test_merge_tracks(self, mock_album_factory, mock_track_factory):
        """Tracks should merge with the same behavior as fields."""
        album1 = mock_album_factory()
        album2 = mock_album_factory()

        new_track = mock_track_factory(album=album2)
        conflict_track = album2.tracks[0]
        keep_track = album1.get_track(conflict_track.track_num)
        keep_track.title = "keep"
        assert conflict_track.title != keep_track.title
        assert album1.tracks != album2.tracks

        album1.merge(album2)

        assert new_track in album1.tracks
        assert keep_track.title == "keep"

    def test_overwrite_tracks(self, mock_album_factory, mock_track_factory):
        """Tracks should overwrite the same as fields if option given."""
        album1 = mock_album_factory()
        album2 = mock_album_factory()

        conflict_track = album2.tracks[0]
        overwrite_track = album1.get_track(conflict_track.track_num)
        conflict_track.title = "conflict"
        assert conflict_track.title != overwrite_track.title
        assert album1.tracks != album2.tracks

        album1.merge(album2, overwrite=True)

        assert overwrite_track.title == "conflict"


class TestDuplicate:
    """Test behavior when there is an attempt to add a duplicate Album to the db.

    A duplicate Album is defined as having any of the same unique attributes: path, or
    mb_album_id.

    To handle duplicates by tags, you should use ``album.get_existing(session)`` to get
    the existing album. At this point, you can either delete the existing album from the
    session using ``session.delete()``, or you can merge it with the current album
    using ``album.merge()``. For examples on how to resolve duplicates, check out the
    ``pre_add()`` hook of the ``add_cli`` plugin.


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
