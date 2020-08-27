"""Test a Track object."""

import pathlib
import re
import types
from unittest.mock import Mock

import pytest
from sqlalchemy import exc

from moe.core.library import Track


class TestInit:
    """Test Track initialization."""

    def test_path_dne(self):
        """Raise an error if the path used to create the Track does not exist."""
        with pytest.raises(FileNotFoundError):
            Track(
                path=pathlib.Path("this_doesnt_exist"),
                session=Mock(),
                album="tmp",
                albumartist="tmp",
                track_num=1,
                year=1,
            )

    # TODO: we should have better checking so we don't hit the integrity error
    def test_dup(self, mock_track_factory, tmp_session):
        """Duplicate tracks should not be added to the database.

        A duplicate is defined as a combination of it's album (obj) and track number.
        """
        track1 = mock_track_factory()
        track2 = mock_track_factory()
        track2._album_obj = track1._album_obj

        tmp_session.add(track1)
        tmp_session.add(track2)

        with pytest.raises(exc.IntegrityError):
            tmp_session.commit()

        tmp_session.rollback()


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
