"""Test a Track object."""

import pathlib
import re
import types

import pytest

from moe.core.library.session import DbDupTrackError, session_scope
from moe.core.library.track import Track


class TestInit:
    """Test Track initialization."""

    def test_add_to_album(self, mock_track_factory, tmp_session):
        """Tracks with the same album attributes should be added to the same album."""
        track1 = mock_track_factory()
        track2 = mock_track_factory()

        tmp_session.add(track1)
        tmp_session.add(track2)

        assert track1._album_obj is track2._album_obj


class TestFromTags:
    """Test initialization from tags."""

    def test_read_tags(self, tmp_session):
        """We should initialize the track with tags from the file if present."""
        track = Track.from_tags(
            path=pathlib.Path("tests/resources/audio_files/full.mp3"),
            session=tmp_session,
        )

        assert track.album == "The Lost Album"
        assert track.albumartist == "Wu-Tang Clan"
        assert track.artist == "Wu-Tang Clan"
        assert track.title == "Full"
        assert track.year == 2020
        assert track.track_num == 1


class TestToDict:
    """Test dict representation of a track."""

    def test_no_private_attributes(self, mock_track):
        """Private attributes should not be included."""
        private_re = "^_.*"
        for key in mock_track.to_dict().keys():
            assert not re.match(private_re, key)

    def test_no_methods(self, mock_track):
        """Methods should not be included."""
        for key in mock_track.to_dict().keys():
            assert not isinstance(getattr(mock_track, key), types.MethodType)

    def test_no_metadata(self, mock_track):
        """Metadata is a sqlalchemy-ism and should not be included."""
        assert "metadata" not in mock_track.to_dict().keys()


class TestPathSet:
    """Test path set event."""

    def test_path_dne(self, mock_track):
        """Raise an error if setting a path that doesn't exist."""
        with pytest.raises(FileNotFoundError):
            mock_track.path = pathlib.Path("also doesnt exist")


class TestDuplicate:
    """Test behavior when there is an attempt to add a duplicate Track to the db.

    A duplicate Track is defined as a combination of it's album (obj) and track number.
    If a duplicate is found when committing to the database, we should raise a
    DbDupTrackError.

    Note:
        This error will only occur upon the session being flushed or committed.
        If you wish to catch this error, then you should use a new session scope
        as shown in the test methods. This will allow you to catch the error by wrapping
        the `with` statement with a `try/except`. In this case, be sure not to create
        the Track with one session, and then attempt to add it with a different
        session. The same session should be used throughout as shown in the tests
        below.
    """

    def test_dup_fields(self, mock_track_factory):
        """Duplicate tracks by fields should raise a DbDupTrackError."""
        with pytest.raises(DbDupTrackError):
            with session_scope() as session:
                track1 = mock_track_factory(session)
                track2 = mock_track_factory(session)
                track2._album_obj = track1._album_obj
                track2.track_num = track1.track_num

                session.add(track1)
                session.add(track2)

    def test_dup_path(self, mock_track_factory):
        """Duplicate tracks can also be defined as having the same path.

        These should also raise the same DbDupTrackError.
        """
        with pytest.raises(DbDupTrackError):
            with session_scope() as session:
                track1 = mock_track_factory(session)
                track2 = mock_track_factory(session)
                track2.path = track1.path

                session.add(track1)
                session.add(track2)
