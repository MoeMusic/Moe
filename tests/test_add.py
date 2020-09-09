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
        args = argparse.Namespace(paths=["does not exist"])

        with pytest.raises(SystemExit) as error:
            add.parse_args(Mock(), Mock(), args)

        assert error.value.code != 0

    def test_file(self, tmp_session):
        """If a file given, add to library as a Track."""
        music_file = pathlib.Path("tests/resources/audio_files/full.mp3")

        add._add_track(music_file)

        assert tmp_session.query(Track.path).scalar() == music_file.resolve()

    def test_multiple_files(self, tmp_session):
        """Add all files given."""
        file1 = "tests/resources/album/01.mp3"
        file2 = "tests/resources/album/02.mp3"
        args = argparse.Namespace(paths=[file1, file2])

        add.parse_args(Mock(), Mock(), args)

        assert (
            tmp_session.query(Track.path)
            .filter_by(path=pathlib.Path(file1).resolve())
            .scalar()
        )
        assert (
            tmp_session.query(Track.path)
            .filter_by(path=pathlib.Path(file2).resolve())
            .scalar()
        )

    def test_non_track_file(self, tmp_session):
        """Raise SystemExit if the file given is not a valid track."""
        args = argparse.Namespace(paths=["tests/resources/album/log.txt"])

        with pytest.raises(SystemExit) as error:
            add.parse_args(Mock(), tmp_session, args)

        assert error.value.code != 0

    def test_track_missing_reqd_tags(self, tmp_session):
        """Raise SystemExit if the track doesn't have all the required tags."""
        args = argparse.Namespace(paths=["tests/resources/audio_files/empty.mp3"])

        with pytest.raises(SystemExit) as error:
            add.parse_args(Mock(), tmp_session, args)

        assert error.value.code != 0

    def test_duplicate_track(self, tmp_session):
        """Raise SystemExit if the track already exists in the library."""
        args = argparse.Namespace(paths=["tests/resources/audio_files/full.mp3"])

        add.parse_args(Mock(), tmp_session, args)

        with pytest.raises(SystemExit) as error:
            add.parse_args(Mock(), tmp_session, args)

        assert error.value.code != 0


class TestAddTrack:
    """Test `_add_track()`."""

    def test_track(self, tmp_session):
        """Tracks are added to the database."""
        music_file = pathlib.Path("tests/resources/audio_files/full.mp3")

        add._add_track(music_file)

        assert tmp_session.query(Track.path).scalar() == music_file.resolve()


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
