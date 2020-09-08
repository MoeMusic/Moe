"""Test the add plugin."""

import argparse
import pathlib
from unittest.mock import Mock, patch

import pytest

from moe import cli
from moe.core.library.session import session_scope
from moe.core.library.track import Track
from moe.plugins import add


class TestParseArgs:
    """Test the plugin argument parser."""

    def test_path_not_found(self):
        """Raise SystemExit if the path to add does not exist."""
        args = argparse.Namespace(path="does not exist")

        with pytest.raises(SystemExit) as error:
            add.parse_args(Mock(), Mock(), args)

        assert error.value.code != 0


class TestAddTrack:
    """Test adding a track."""

    def test_track(self, tmp_session):
        """Tracks are added to the database."""
        music_file = pathlib.Path("tests/resources/audio_files/full.mp3")

        add.add_track(music_file)

        test_path = tmp_session.query(Track.path).scalar()

        assert test_path == music_file.resolve()

    def test_bad_music_file(self, tmp_path):
        """Raise SystemExit if the file given is not a valid music file."""
        bad_file = tmp_path / "a"
        bad_file.touch()

        with pytest.raises(SystemExit) as error:
            add.add_track(bad_file)

        assert error.value.code != 0

    def test_duplicate_file(self, tmp_session):
        """Raise SystemExit if the file already exists in the library."""
        music_file = pathlib.Path("tests/resources/audio_files/full.mp3")
        add.add_track(music_file)

        with pytest.raises(SystemExit) as error:
            add.add_track(music_file)

        assert error.value.code != 0


class TestAddAlbum:
    """Test adding an album."""

    def test_album(self, tmp_session):
        """Test we can add all tracks in a directory."""
        album_path = pathlib.Path("tests/resources/album")
        add.add_album(album_path)

        for track in album_path.rglob("*.mp3"):
            assert tmp_session.query(Track.path).filter_by(path=track.resolve())


@pytest.mark.integration
class TestCommand:
    """Test cli integration with the add command."""

    def test_file(self, tmp_config):
        """Tracks are added to the library when a file is passed to `add`."""
        args = ["moe", "add", "tests/resources/audio_files/full.mp3"]

        with patch("sys.argv", args):
            with patch("moe.cli.Config", return_value=tmp_config):
                cli.main()

        with session_scope() as session:
            assert session.query(Track._id).scalar()

    def test_dir(self, tmp_config):
        """Directories are recursively searched for tracks when passed to `add`."""
        album_path = "tests/resources/album"
        args = ["moe", "add", album_path]

        with patch("sys.argv", args):
            with patch("moe.cli.Config", return_value=tmp_config):
                cli.main()

        with session_scope() as session:
            for track in pathlib.Path(album_path).rglob("*.mp3"):
                assert session.query(Track.path).filter_by(path=track.resolve())
