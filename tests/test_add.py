"""Tests the add plugin."""

import argparse
import pathlib
import shutil
from unittest.mock import Mock, patch

import pytest

from moe import cli
from moe.core.library.album import Album
from moe.core.library.session import session_scope
from moe.core.library.track import Track
from moe.plugins import add


class TestParseArgs:
    """Test general functionality of the argument parser."""

    def test_path_not_found(self):
        """Raise SystemExit if the path to add does not exist."""
        args = argparse.Namespace(paths=["does not exist"])

        with pytest.raises(SystemExit) as error:
            add.parse_args(config=Mock(), session=Mock(), args=args)

        assert error.value.code != 0

    def test_multiple_item_exit_error(self, real_track, tmp_session):
        """Don't exit after the first failed item if more to be added.

        Still exit with non-zero code if any failures occured.
        """
        args = argparse.Namespace(paths=["bad file", str(real_track.path)])

        with pytest.raises(SystemExit) as error:
            add.parse_args(config=Mock(), session=tmp_session, args=args)

        assert error.value.code != 0
        assert (
            tmp_session.query(Track.path)
            .filter_by(path=real_track.path.resolve())
            .one()
        )


class TestParseArgsDirectory:
    """Test a directory argument given to add.

    Directories are added as albums.
    """

    def test_dir(self, real_album, tmp_session):
        """If a directory given, add to library as an album."""
        args = argparse.Namespace(paths=[real_album.path])

        add.parse_args(config=Mock(), session=tmp_session, args=args)

        assert tmp_session.query(Album).one()

    def test_extras(self, real_album, tmp_session):
        """Add any extras that are within the album directory."""
        cue_file = real_album.path / ".cue"
        cue_file.touch()
        playlist_file = real_album.path / ".m3u"
        playlist_file.touch()
        args = argparse.Namespace(paths=[real_album.path])

        add.parse_args(config=Mock(), session=tmp_session, args=args)

        album = tmp_session.query(Album).one()
        extra_paths = [extra.path for extra in album.extras]

        assert cue_file in extra_paths
        assert playlist_file in extra_paths
        assert len(album.extras) == 3  # accounts for log file added in fixture

    def test_no_valid_tracks(self, tmp_session, tmp_path):
        """Error if given directory does not contain any valid tracks."""
        album = tmp_path / "empty"
        album.mkdir()
        args = argparse.Namespace(paths=[album])

        with pytest.raises(SystemExit) as error:
            add.parse_args(config=Mock(), session=tmp_session, args=args)

        assert error.value.code != 0
        assert not tmp_session.query(Album).scalar()

    def test_different_tracks(self, real_track_factory, tmp_path, tmp_session):
        """Raise SystemExit if tracks have different album attributes.

        All tracks in a given directory should belong to the same album.
        """
        tmp_album_path = tmp_path / "tmp_album"
        tmp_album_path.mkdir()
        shutil.copy(real_track_factory(year=1).path, tmp_album_path)
        shutil.copy(real_track_factory(year=2).path, tmp_album_path)
        args = argparse.Namespace(paths=[tmp_album_path])

        with pytest.raises(SystemExit) as error:
            add.parse_args(config=Mock(), session=tmp_session, args=args)

        assert error.value.code != 0
        assert not tmp_session.query(Album).scalar()

    def test_duplicate_tracks(self, real_album, tmp_session):
        """Don't fail album add if a track (by tags) already exists in the library."""
        tmp_session.merge(list(real_album.tracks)[0])
        tmp_session.commit()
        args = argparse.Namespace(paths=[real_album.path])

        add.parse_args(config=Mock(), session=tmp_session, args=args)

        assert tmp_session.query(Album).one()


class TestParseArgsFile:
    """Test a file argument given to add.

    Files are added as Tracks.
    """

    def test_file(self, real_track, tmp_session):
        """If a file given, add to library as a Track."""
        args = argparse.Namespace(paths=[str(real_track.path)])

        add.parse_args(config=Mock(), session=tmp_session, args=args)

        assert (
            tmp_session.query(Track.path)
            .filter_by(path=real_track.path.resolve())
            .one()
        )

    def test_multiple_files(self, real_track_factory, tmp_session):
        """Add all files given."""
        track_path1 = real_track_factory().path
        track_path2 = real_track_factory().path
        args = argparse.Namespace(paths=[str(track_path1), str(track_path2)])

        add.parse_args(config=Mock(), session=tmp_session, args=args)

        assert tmp_session.query(Track.path).filter_by(path=track_path1.resolve()).one()
        assert tmp_session.query(Track.path).filter_by(path=track_path2.resolve()).one()

    def test_min_reqd_tags(self, tmp_session):
        """We can add a track with only a track_num, album, albumartist, and year."""
        reqd_track_path = "tests/resources/reqd.mp3"
        args = argparse.Namespace(paths=[reqd_track_path])

        add.parse_args(config=Mock(), session=tmp_session, args=args)

        assert (
            tmp_session.query(Track.path)
            .filter_by(path=pathlib.Path(reqd_track_path).resolve())
            .one()
        )

    def test_non_track_file(self):
        """Raise SystemExit if the file given is not a valid track."""
        args = argparse.Namespace(paths=["tests/resources/log.txt"])

        with pytest.raises(SystemExit) as error:
            add.parse_args(config=Mock(), session=Mock(), args=args)

        assert error.value.code != 0

    def test_track_missing_reqd_tags(self):
        """Raise SystemExit if the track doesn't have all the required tags."""
        args = argparse.Namespace(paths=["tests/resources/empty.mp3"])

        with pytest.raises(SystemExit) as error:
            add.parse_args(config=Mock(), session=Mock(), args=args)

        assert error.value.code != 0

    def test_duplicate_track(self, real_track, tmp_session, tmp_path):
        """Overwrite old track path with the new track if a duplicate is found."""
        new_track_path = tmp_path / "full2"
        args = argparse.Namespace(paths=[str(new_track_path)])
        shutil.copyfile(real_track.path, new_track_path)

        tmp_session.add(real_track)
        tmp_session.commit()

        add.parse_args(config=Mock(), session=tmp_session, args=args)

        new_track = tmp_session.query(Track).one()

        assert new_track.path == new_track_path.resolve()


@pytest.mark.integration
class TestCommand:
    """Test cli integration with the add command."""

    def test_file(self, real_track, tmp_config):
        """Tracks are added to the library when a file is passed to `add`."""
        cli_args = ["moe", "add", str(real_track.path)]
        config = tmp_config(settings='default_plugins = ["add"]')

        with patch("sys.argv", cli_args):
            with patch("moe.cli.Config", return_value=config):
                cli.main()

        with session_scope() as session:
            assert session.query(Track).one()

    def test_dir(self, real_album, tmp_config):
        """Albums are added to the library when a dir is passed to `add`."""
        cli_args = ["moe", "add", str(real_album.path)]
        config = tmp_config(settings='default_plugins = ["add"]')

        with patch("sys.argv", cli_args):
            with patch("moe.cli.Config", return_value=config):
                cli.main()

        with session_scope() as session:
            album = session.query(Album).one()

            tracks = session.query(Track)
            for track in tracks:
                assert track in album.tracks

            assert len(album.tracks) > 1
            assert album.extras
