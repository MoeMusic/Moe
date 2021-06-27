"""Tests a Track object."""

import datetime
import pathlib

import pytest

from moe.core.library.album import Album
from moe.core.library.session import DbDupAlbumError, session_scope
from moe.core.library.track import Track


class TestInit:
    """Test Track initialization."""

    def test_album_init(self, mock_track, tmp_session):
        """Creating a Track should also create the corresponding Album."""
        tmp_session.add(mock_track)

        assert mock_track.album_obj

    def test_add_to_album(self, mock_track_factory, tmp_session):
        """Tracks with the same album attributes should be added to the same album."""
        track1 = mock_track_factory()
        track2 = mock_track_factory()

        tmp_session.merge(track1)
        track2.album_obj.merge_existing(tmp_session)

        tracks = tmp_session.query(Track).all()
        album = tmp_session.query(Album).one()

        for track in tracks:
            assert track in album.tracks

        assert len(tracks) == len(album.tracks)
        assert tracks == album.tracks


class TestAlbumSet:
    """Changing an album attribute will change the value for the current Album.

    Thus, all tracks in the album will reflect the new value.
    """

    def test_album_set(self, mock_track, tmp_path, tmp_session):
        """Setting an album attribute maintains the same album object."""
        album1 = mock_track.album_obj
        mock_track.album = "TPAB"
        mock_track.album_path = tmp_path
        mock_track.albumartist = "Kendrick Lamar"
        mock_track.date = datetime.date(2015, 3, 15)

        assert album1 is mock_track.album_obj


class TestFromTags:
    """Test initialization from tags."""

    def test_read_tags(self, tmp_session):
        """We should initialize the track with tags from the file if present."""
        track = Track.from_tags(
            path=pathlib.Path("tests/resources/full.mp3"),
        )

        assert track.album == "The Lost Album"
        assert track.albumartist == "Wu-Tang Clan"
        assert track.artist == "Wu-Tang Clan"
        assert track.file_ext == "mp3"
        assert set(track.genre) == {"hip hop", "rock"}
        assert track.title == "Full"
        assert track.track_num == 1
        assert track.year == 2020


class TestDuplicate:
    """Test behavior when there is an attempt to add a duplicate Track to the db.

    A duplicate Track is defined as a combination of it's album (obj) and track number.
    If a duplicate is found when committing to the database, we should raise a
    ``DbDupAlbumError``.

    The reason a DbDupAlbumError is raised instead of a track-related error, is because
    a duplicate Track must have a duplicate Album by definition of a Track's uniqueness
    being defined by the album it belongs to.

    Duplicates should not error if using ``track.album_obj.merge_existing(session)``.

    Note:
        This error will only occur upon the session being flushed or committed.
        If you wish to catch this error, then you should use a new session scope
        as shown in `test_dup_path()`. This will allow you to catch the error by
        wrapping the `with` statement with a `try/except`.
    """

    def test_dup(self, mock_track_factory, tmp_session):
        """Duplicate tracks should raise a DbDupAlbumError."""
        track1 = mock_track_factory()
        track2 = mock_track_factory()
        track2.track_num = track1.track_num

        with pytest.raises(DbDupAlbumError):
            with session_scope() as session:
                session.add(track1)
                session.add(track2)

    def test_dup_fields_merge(self, mock_track_factory, tmp_session):
        """Duplicate errors should not occur if using `Album.merge_existing()`."""
        track1 = mock_track_factory()
        track2 = mock_track_factory()
        track2.track_num = track1.track_num

        tmp_session.add(track1)
        track2.album_obj.merge_existing(tmp_session)
