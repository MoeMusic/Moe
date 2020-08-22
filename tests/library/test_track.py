"""Test a Track object."""

import pathlib

import pytest

from moe.core.library import Track


class TestInit:
    """Test Track initialization."""

    def test_path_dne(self):
        """Raise an error if the path used to create the Track does not exist."""
        with pytest.raises(FileNotFoundError):
            Track(path=pathlib.Path("this_doesnt_exist"))

    def test_read_tags(self):
        """We should initialize the track with tags from the file if present."""
        track = Track(path=pathlib.Path("tests/resources/audio_files/full.mp3"))

        assert track.artist == "Wu-Tang Clan"
        assert track.albumartist == "Wu-Tang Clan"
        assert track.album == "The Lost Album"
        assert track.title == "Full"

    def test_empty_track(self):
        """If the track's tag doesn't exist, just don't set it. No reason to error."""
        Track(path=pathlib.Path("tests/resources/audio_files/empty.mp3"))
