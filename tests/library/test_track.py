"""Tests a Track object."""

import datetime

import pytest

import moe.plugins.write
from moe.library.track import Track, TrackError


class TestInit:
    """Test Track initialization."""

    def test_album_init(self, mock_track, tmp_session):
        """Creating a Track should also create the corresponding Album."""
        tmp_session.add(mock_track)

        assert mock_track.album_obj


class TestAlbumSet:
    """Changing an album attribute will change the value for the current Album.

    Thus, all tracks in the album will reflect the new value.
    """

    def test_album_set(self, mock_track, tmp_path):
        """Setting an album attribute maintains the same album object."""
        album1 = mock_track.album_obj
        mock_track.album = "TPAB"
        mock_track.album_path = tmp_path
        mock_track.albumartist = "Kendrick Lamar"
        mock_track.date = datetime.date(2015, 3, 15)

        assert album1 is mock_track.album_obj


class TestFromTags:
    """Test initialization from tags."""

    def test_read_tags(self, full_mp3_path):
        """We can initialize a track with tags from a file if present."""
        track = Track.from_path(full_mp3_path)

        assert track.album == "The Lost Album"
        assert track.albumartist == "Wu-Tang Clan"
        assert track.artist == "Wu-Tang Clan"
        assert track.date == datetime.date(2020, 1, 12)
        assert track.disc == 1
        assert track.disc_total == 2
        assert set(track.genres) == {"hip hop", "rock"}
        assert track.mb_album_id == "1234"
        assert track.mb_track_id == "123"
        assert track.title == "Full"
        assert track.track_num == 1

    def test_no_reqd_tags(self, empty_mp3_path):
        """Raise `TrackError` if missing required tags."""
        with pytest.raises(TrackError):
            Track.from_path(empty_mp3_path)

    def test_albumartist_backup(self, real_track):
        """Use artist as a backup for albumartist if missing."""
        real_track.albumartist = ""
        real_track.artist = "Backup"
        moe.plugins.write.write_tags(real_track)

        track = Track.from_path(real_track.path)
        assert track.albumartist


class TestGetExisting:
    """Test `get_existing()`."""

    def test_path(self, mock_track_factory, tmp_session):
        """We match an existing track by it's path."""
        track1 = mock_track_factory()
        track2 = mock_track_factory()
        track1.path = track2.path

        tmp_session.merge(track1)

        assert track1.get_existing()

    def test_mb_track_id(self, mock_track_factory, tmp_session):
        """We match an existing track by it's mb_track_id."""
        track1 = mock_track_factory()
        track2 = mock_track_factory()
        track1.mb_track_id = "123"
        track1.mb_track_id = track2.mb_track_id

        tmp_session.merge(track1)

        assert track1.get_existing()

    def test_null_match(self, mock_track_factory, tmp_session):
        """Don't match off of null values."""
        track1 = mock_track_factory()
        track2 = mock_track_factory()
        assert not track1.mb_track_id
        assert not track2.mb_track_id
        assert track1.path != track2.path

        tmp_session.merge(track1)

        assert not track2.get_existing()


class TestEquality:
    """Test equality of tracks."""

    def test_equals_mb_track_id(self, real_track_factory):
        """Tracks with the same `mb_track_id` are equal."""
        track1 = real_track_factory()
        track2 = real_track_factory()
        track1.mb_track_id = "1"
        assert track1 != track2

        track2.mb_track_id = track1.mb_track_id
        assert track1 == track2

    def test_equals_path(self, real_track_factory):
        """Tracks with the same `path` are equal."""
        track1 = real_track_factory()
        track2 = real_track_factory()
        assert track1 != track2

        track1.path = track2.path
        assert track1 == track2

    def test_not_equals(self, real_track_factory):
        """Tracks with different designated unique fields are not equal."""
        track1 = real_track_factory()
        track2 = real_track_factory()
        track1.mb_track_id = "1"

        assert track1.mb_track_id != track2.mb_track_id
        assert track1.path != track2.path

        assert track1 != track2

    def test_not_equals_not_track(self, real_track):
        """Not equal if not comparing two tracks."""
        assert real_track != "test"


class TestMerge:
    """Test merging two tracks."""

    def test_conflict_persists(self, mock_track_factory):
        """Don't overwrite any conflicts."""
        track = mock_track_factory()
        other_track = mock_track_factory()

        track.title = "keep"
        other_track.title = "discard"

        track.merge(other_track)

        assert track.title == "keep"

    def test_merge_non_conflict(self, mock_track_factory):
        """Apply any non-conflicting fields."""
        track = mock_track_factory()
        other_track = mock_track_factory()

        track.title = None
        track.genres = []
        other_track.title = "keep"
        other_track.genres = ["keep"]

        track.merge(other_track)

        assert track.title == "keep"
        assert track.genres == ["keep"]

    def test_none_merge(self, mock_track_factory):
        """Don't merge in any null values."""
        track = mock_track_factory()
        other_track = mock_track_factory()

        track.title = "keep"
        other_track.title = None

        track.merge(other_track)

        assert track.title == "keep"

    def test_db_delete(self, mock_track_factory, tmp_session):
        """Remove the other track from the db if it exists."""
        track = mock_track_factory()
        other_track = mock_track_factory()
        tmp_session.add(other_track)
        tmp_session.flush()

        track.merge(other_track)

        assert not track.get_existing()


class TestDupListField:
    """Ensure duplicate list fields can be assigned/created without error."""

    def test_genre(self, mock_track_factory, tmp_session):
        """Duplicate genres don't error."""
        track1 = mock_track_factory()
        track2 = mock_track_factory()
        track1.genre = "pop"
        track2.genre = "pop"

        tmp_session.add(track1)
        tmp_session.merge(track2)

        tracks = tmp_session.query(Track).all()
        for track in tracks:
            track.genre = "new genre"
