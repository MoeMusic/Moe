"""Test the add plugin."""

import argparse
import pathlib
import shutil
from unittest.mock import Mock, patch

import pytest

from moe import cli
from moe.core.library.session import session_scope
from moe.core.library.track import Album, Track
from moe.plugins import add


class TestParseArgs:
    """Test general functionality of the argument parser."""

    def test_path_not_found(self):
        """Raise SystemExit if the path to add does not exist."""
        args = argparse.Namespace(paths=["does not exist"])

        with pytest.raises(SystemExit) as error:
            add.parse_args(Mock(), Mock(), args)

        assert error.value.code != 0


class TestParseArgsDirectory:
    """Test a directory argument given to add.

    Directories are added as albums.
    """

    def test_dir(self, tmp_session):
        """If a directory given, add to library as an album."""
        album = "tests/resources/album"
        args = argparse.Namespace(paths=[album])

        add.parse_args(Mock(), tmp_session, args)

        assert tmp_session.query(Album).scalar()

    def test_no_valid_tracks(self, tmp_session, tmp_path):
        """Error if given directory does not contain any valid tracks."""
        album = tmp_path / "empty"
        album.mkdir()
        args = argparse.Namespace(paths=[album])

        with pytest.raises(SystemExit) as error:
            add.parse_args(Mock(), tmp_session, args)

        assert error.value.code != 0
        assert not tmp_session.query(Album).scalar()

    def test_different_tracks(self, tmp_path, tmp_session):
        """Raise SystemExit if tracks have different album attributes.

        All tracks in a given directory should belong to the same album.
        """
        tmp_album_path = tmp_path / "tmp_album"
        tmp_album_path.mkdir()
        shutil.copy("tests/resources/album/01.mp3", tmp_album_path)
        shutil.copy("tests/resources/audio_files/full.mp3", tmp_album_path)
        args = argparse.Namespace(paths=[tmp_album_path])

        with pytest.raises(SystemExit) as error:
            add.parse_args(Mock(), tmp_session, args)

        assert error.value.code != 0
        assert not tmp_session.query(Album).scalar()

    def test_duplicate_tracks(self, tmp_session):
        """Don't fail album add if a track (by tags) already exists in the library."""
        album = "tests/resources/album"
        tmp_session.add(Track.from_tags(path=pathlib.Path(album) / "01.mp3"))
        tmp_session.commit()
        args = argparse.Namespace(paths=[album])

        add.parse_args(Mock(), tmp_session, args)

        assert tmp_session.query(Album).scalar()


class TestParseArgsFile:
    """Test a file argument given to add.

    Files are added as Tracks.
    """

    def test_file(self, tmp_session):
        """If a file given, add to library as a Track."""
        file1 = "tests/resources/album/01.mp3"
        args = argparse.Namespace(paths=[file1])

        add.parse_args(Mock(), tmp_session, args)

        assert (
            tmp_session.query(Track.path)
            .filter_by(path=pathlib.Path(file1).resolve())
            .scalar()
        )

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

    def test_multiple_files_exit_error(self, tmp_session):
        """Don't exit after the first failed track if more to be added.

        Still exit with non-zero code if any failures occured.
        """
        file1 = "bad file"
        file2 = "tests/resources/audio_files/full.mp3"
        args = argparse.Namespace(paths=[file1, file2])

        with pytest.raises(SystemExit) as error:
            add.parse_args(Mock(), tmp_session, args)

        assert error.value.code != 0
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

    def test_duplicate_track_path(self, tmp_session):
        """Raise SystemExit if the track already exists in the library."""
        track_path = "tests/resources/audio_files/full.mp3"
        args = argparse.Namespace(paths=[track_path])

        track = Track.from_tags(pathlib.Path(track_path))
        track.track_num = 2
        tmp_session.add(track)
        tmp_session.commit()

        with pytest.raises(SystemExit) as error:
            add.parse_args(Mock(), tmp_session, args)

        assert error.value.code != 0


@pytest.mark.integration
class TestCommand:
    """Test cli integration with the add command."""

    def test_file(self, tmp_config):
        """Tracks are added to the library when a file is passed to `add`."""
        args = ["moe", "add", "tests/resources/audio_files/full.mp3"]

        config = tmp_config(settings='default_plugins = ["add"]')
        with patch("sys.argv", args):
            with patch("moe.cli.Config", return_value=config):
                cli.main()

        with session_scope() as session:
            assert session.query(Track).scalar()

    def test_dir(self, tmp_config):
        """Albums are added to the library when a dir is passed to `add`."""
        args = ["moe", "add", "tests/resources/album/"]

        config = tmp_config(settings='default_plugins = ["add"]')
        with patch("sys.argv", args):
            with patch("moe.cli.Config", return_value=config):
                cli.main()

        with session_scope() as session:
            album = session.query(Album).scalar()
            assert session.query(Album).scalar()

            tracks = session.query(Track)
            for track in tracks:
                assert track in album.tracks

            assert len(album.tracks) > 1
