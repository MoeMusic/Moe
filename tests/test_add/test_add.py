"""Tests the add plugin."""

import argparse
import shutil
from pathlib import Path
from unittest.mock import MagicMock, Mock, call, patch

import pytest
from sqlalchemy.orm.session import Session

import moe
from moe.core.config import Config
from moe.core.library.album import Album
from moe.core.library.session import session_scope
from moe.core.library.track import Track
from moe.plugins.add import add


class ImportPlugin:
    """Test plugin that implements the ``import_metadata`` hook for testing."""

    @staticmethod
    @moe.hookimpl
    def import_album(config: Config, session: Session, album: Album) -> Album:
        """Changes the album title."""
        album.title = "pre-add plugin"
        return album


class TestParseArgs:
    """Test general functionality of the argument parser."""

    def test_multiple_item_exit_error(self, real_track, tmp_session):
        """Don't exit after the first failed item if more to be added.

        Still exit with non-zero code if any failures occured.
        """
        args = argparse.Namespace(paths=["bad file", str(real_track.path)])

        with patch("moe.plugins.add.add.add_item") as add_item_mock:
            add_item_mock.side_effect = [add.AddError, tmp_session.add(real_track)]
            with pytest.raises(SystemExit) as error:
                add.parse_args(Mock(), tmp_session, args)

        assert error.value.code != 0
        assert tmp_session.query(Track).one()

    def test_multiple_paths(self, real_track_factory, tmp_session):
        """Add all paths given."""
        mock_config = Mock()
        mock_session = Mock()

        track_path1 = real_track_factory().path
        track_path2 = real_track_factory().path
        args = argparse.Namespace(paths=[str(track_path1), str(track_path2)])

        with patch("moe.plugins.add.add.add_item") as add_item_mock:
            add.parse_args(mock_config, mock_session, args)

        calls = [
            call(mock_config, mock_session, track_path1),
            call(mock_config, mock_session, track_path2),
        ]
        add_item_mock.assert_has_calls(calls)
        assert add_item_mock.call_count == 2


class TestAddItemFromDir:
    """Test a directory given to ``add_item()`` to add as an album."""

    def test_dir_album(self, real_album, tmp_session):
        """If a directory given, add to library as an album."""
        mock_config = MagicMock()
        mock_config.plugin_manager.hook.import_album.return_value = []

        add.add_item(mock_config, tmp_session, real_album.path)

        assert tmp_session.query(Album).filter_by(path=real_album.path).one()

    def test_extras(self, real_album, tmp_session):
        """Add any extras that are within the album directory."""
        mock_config = MagicMock()
        mock_config.plugin_manager.hook.import_album.return_value = []

        cue_file = real_album.path / ".cue"
        cue_file.touch()
        playlist_file = real_album.path / ".m3u"
        playlist_file.touch()

        add.add_item(mock_config, tmp_session, real_album.path)

        album = tmp_session.query(Album).one()
        extra_paths = [extra.path for extra in album.extras]
        assert cue_file in extra_paths
        assert playlist_file in extra_paths
        assert len(album.extras) == 3  # accounts for log file added in fixture

    def test_no_valid_tracks(self, tmp_session, tmp_path):
        """Error if given directory does not contain any valid tracks."""
        mock_config = MagicMock()
        mock_config.plugin_manager.hook.import_album.return_value = []

        album_path = tmp_path / "empty"
        album_path.mkdir()

        with pytest.raises(add.AddError):
            add.add_item(mock_config, tmp_session, album_path)

        assert not tmp_session.query(Album).scalar()

    def test_different_tracks(self, real_track_factory, tmp_path, tmp_session):
        """Error if tracks have different album attributes.

        All tracks in a given directory should belong to the same album.
        """
        mock_config = MagicMock()
        mock_config.plugin_manager.hook.import_album.return_value = []

        tmp_album_path = tmp_path / "tmp_album"
        tmp_album_path.mkdir()
        shutil.copy(real_track_factory(year=1).path, tmp_album_path)
        shutil.copy(real_track_factory(year=2).path, tmp_album_path)

        with pytest.raises(add.AddError):
            add.add_item(mock_config, tmp_session, tmp_album_path)

        assert not tmp_session.query(Album).scalar()

    def test_duplicate_tracks(self, real_album, tmp_session):
        """Don't fail album add if a track (by tags) already exists in the library."""
        mock_config = MagicMock()
        mock_config.plugin_manager.hook.import_album.return_value = []

        tmp_session.merge(real_album.tracks[0])

        add.add_item(mock_config, tmp_session, real_album.path)

        assert tmp_session.query(Album).filter_by(path=real_album.path).one()

    def test_merge_existing(self, real_album_factory, tmp_session):
        """Merge the album to be added with an existing album in the library.

        The album info should be kept (likely to be more accurate), however, any tracks
        or extras should be overwritten.
        """
        mock_config = MagicMock()
        mock_config.plugin_manager.hook.import_album.return_value = []

        new_album = real_album_factory()
        existing_album = real_album_factory()
        new_album.date = existing_album.date
        new_album.path = existing_album.path
        existing_album.mb_id = "1234"
        assert not new_album.is_unique(existing_album)

        for track in new_album.tracks:
            track.title = "new_album"

        for extra_num, extra in enumerate(new_album.extras):
            extra.filename = f"{extra_num} new_album"

        assert new_album.mb_id != existing_album.mb_id
        assert new_album.tracks != existing_album.tracks
        assert new_album.extras != existing_album.extras

        tmp_session.merge(existing_album)
        with patch("moe.plugins.add.add._add_album", return_value=new_album):
            add.add_item(mock_config, tmp_session, new_album.path)

        db_album = tmp_session.query(Album).one()
        assert db_album.mb_id == existing_album.mb_id
        assert sorted(db_album.tracks) == sorted(new_album.tracks)
        assert sorted(db_album.extras) == sorted(new_album.extras)


class TestAddItemFromFile:
    """Test a file argument given to add as a track."""

    def test_path_not_found(self):
        """Raise SystemExit if the path to add does not exist."""
        with pytest.raises(add.AddError):
            add.add_item(Mock(), Mock(), Path("does not exist"))

    def test_file_track(self, real_track, tmp_session):
        """If a file given, add to library as a Track."""
        mock_config = MagicMock()
        mock_config.plugin_manager.hook.import_album.return_value = []

        add.add_item(mock_config, tmp_session, real_track.path)

        assert tmp_session.query(Track.path).filter_by(path=real_track.path).one()

    def test_min_reqd_tags(self, tmp_session):
        """We can add a track with only a track_num, album, albumartist, and year."""
        mock_config = MagicMock()
        mock_config.plugin_manager.hook.import_album.return_value = []

        reqd_track_path = Path("tests/resources/reqd.mp3")

        add.add_item(mock_config, tmp_session, reqd_track_path)

        assert tmp_session.query(Track.path).filter_by(path=reqd_track_path).one()

    def test_non_track_file(self):
        """Error if the file given is not a valid track."""
        with pytest.raises(add.AddError):
            add.add_item(Mock(), Mock(), Path("tests/resources/log.txt"))

    def test_track_missing_reqd_tags(self):
        """Error if the track doesn't have all the required tags."""
        with pytest.raises(add.AddError):
            add.add_item(Mock(), Mock(), Path("tests/resources/empty.mp3"))

    def test_duplicate_track(self, real_track, tmp_session, tmp_path):
        """Overwrite old track path with the new track if a duplicate is found."""
        mock_config = MagicMock()
        mock_config.plugin_manager.hook.import_album.return_value = []

        new_track_path = tmp_path / "full2"
        shutil.copyfile(real_track.path, new_track_path)
        tmp_session.add(real_track)

        add.add_item(mock_config, tmp_session, new_track_path)

        assert tmp_session.query(Track.path).filter_by(path=new_track_path).one()


@pytest.mark.integration
class TestPreAdd:
    """Test integration with the ``import_album`` hook and thus the add prompt."""

    def test_album(self, real_album, tmp_config):
        """Prompt is run with a plugin implementing the ``import_album`` hook."""
        cli_args = ["add", str(real_album.path)]
        config = tmp_config(settings='default_plugins = ["add"]')
        config.plugin_manager.register(ImportPlugin)

        with patch("builtins.input", lambda _: "a"):  # apply changes
            moe.cli.main(cli_args, config)

        with session_scope() as session:
            album = session.query(Album).one()
            assert album.title == "pre-add plugin"


@pytest.mark.integration
class TestCommand:
    """Test cli integration with the add command."""

    def test_file(self, real_track, tmp_config):
        """Tracks are added to the library when a file is passed to `add`."""
        cli_args = ["add", str(real_track.path)]
        config = tmp_config(settings='default_plugins = ["add"]')

        moe.cli.main(cli_args, config)

        with session_scope() as session:
            assert session.query(Track).one()
