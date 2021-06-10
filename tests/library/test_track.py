"""Tests a Track object."""

import pathlib
import re
import types

import pytest

from moe.core.library.album import Album
from moe.core.library.session import DbDupTrackPathError, session_scope
from moe.core.library.track import Track


class TestInit:
    """Test Track initialization."""

    def test_album_init(self, mock_track, tmp_session):
        """Creating a Track should also create the corresponding Album."""
        tmp_session.add(mock_track)

        assert mock_track._album_obj

    def test_add_to_album(self, mock_track_factory, tmp_session):
        """Tracks with the same album attributes should be added to the same album.

        Note:
            We must use `session.merge()` here to avoid duplicate albums being added
            to the database.
        """
        track1 = mock_track_factory()
        track2 = mock_track_factory()

        tmp_session.merge(track1)
        tmp_session.merge(track2)

        tracks = tmp_session.query(Track).all()
        album = tmp_session.query(Album).one()

        assert len(tracks) == len(album.tracks)
        assert set(tracks) == album.tracks

    def test_empty(self, tmp_session):
        """Raise TypeError if None value given in argument."""
        with pytest.raises(TypeError):
            Track(
                path=None,
                album=None,
                albumartist=None,
                track_num=None,
                year=None,
                session=None,
            )


class TestAlbumSet:
    """Create a new album when setting an album attribute.

    This will "move" the edited track to a new album rather than editing the
    current album and thus all the other associated tracks.
    """

    def test_album_set(self, mock_track, tmp_session):
        """Setting an album attribute creates a new Album instance."""
        album1 = mock_track._album_obj
        mock_track.album = "TPAB"

        assert mock_track._album_obj.title == mock_track.album
        assert album1 is not mock_track._album_obj
        tmp_session.add(mock_track)  # make sure we still have all the req'd values


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
        assert track.genre == {"hip hop", "rock"}
        assert track.title == "Full"
        assert track.track_num == 1
        assert track.year == 2020


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

    def test_no_sqlalchemy_attrs(self, mock_track):
        """Sqlalchemy attributes are not relevant and should not be included."""
        assert "metadata" not in mock_track.to_dict().keys()
        assert "registry" not in mock_track.to_dict().keys()


class TestWriteTags:
    """Test writing tags to the file."""

    def test_write_tags(self, real_track):
        """We can write track changes to the file."""
        real_track.album = "Bigger, Better, Faster, More!"
        real_track.albumartist = "4 Non Blondes"
        real_track.artist = "4 Non Blondes"
        real_track.genre = {"alternative", "rock"}
        real_track.title = "What's Up"
        real_track.track_num = 3
        real_track.year = 1992

        real_track.write_tags()

        new_track = Track.from_tags(path=real_track.path)
        assert new_track.album == "Bigger, Better, Faster, More!"
        assert new_track.albumartist == "4 Non Blondes"
        assert new_track.artist == "4 Non Blondes"
        assert new_track.genre == {"alternative", "rock"}
        assert new_track.title == "What's Up"
        assert new_track.track_num == 3
        assert new_track.year == 1992


class TestPathSet:
    """Test path set event."""

    def test_path_dne(self, mock_track):
        """Raise an error if setting a path that doesn't exist."""
        with pytest.raises(FileNotFoundError):
            mock_track.path = pathlib.Path("also doesnt exist")


class TestDuplicate:
    """Test behavior when there is an attempt to add a duplicate Track to the db.

    A duplicate Track is defined as a combination of it's album (obj) and track number.
    A duplicate can also be because two Tracks have the same path.
    If a duplicate is found when committing to the database, we should raise a
    DbDupTrackPathError.

    If we use `session.merge()` to add a Track, a duplicate error should only occur
    for duplicate paths, and not because of its tags. This is because a Track's
    primary key is based off of its tags, and `session.merge()` uses an object's
    primary key to merge any existing objects.

    Note:
        This error will only occur upon the session being flushed or committed.
        If you wish to catch this error, then you should use a new session scope
        as shown in `test_dup_path()`. This will allow you to catch the error by
        wrapping the `with` statement with a `try/except`.
    """

    def test_dup_fields_merge(self, mock_track_factory, tmp_session):
        """Duplicate errors should not occur if using `session.merge()`."""
        track1 = mock_track_factory()
        track2 = mock_track_factory()
        track2.track_num = track1.track_num

        tmp_session.merge(track1)
        tmp_session.merge(track2)

    def test_dup_path(self, mock_track_factory, tmp_session):
        """Duplicate tracks can also be defined as having the same path.

        These should also raise the same DbDupTrackError.
        """
        track1 = mock_track_factory()
        track2 = mock_track_factory()
        track2.path = track1.path

        with pytest.raises(DbDupTrackPathError):
            with session_scope() as session:
                session.merge(track1)
                session.merge(track2)
