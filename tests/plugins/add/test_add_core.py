"""Tests the add plugin."""

import copy
import shutil
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

from moe.core.library.album import Album
from moe.core.library.track import Track
from moe.plugins import add
from moe.plugins import write as moe_write


class TestAddItemFromDir:
    """Test a directory given to ``add_item()`` to add as an album."""

    def test_dir_album(self, real_album, tmp_session):
        """If a directory given, add to library as an album."""
        mock_config = MagicMock()
        mock_config.plugin_manager.hook.import_album.return_value = []

        add.add.add_item(mock_config, tmp_session, real_album.path)

        assert tmp_session.query(Album).filter_by(path=real_album.path).one()

    def test_extras(self, real_album, tmp_session):
        """Add any extras that are within the album directory."""
        mock_config = MagicMock()
        mock_config.plugin_manager.hook.import_album.return_value = []
        assert real_album.extras

        add.add.add_item(mock_config, tmp_session, real_album.path)

        db_album = tmp_session.query(Album).one()
        for extra in real_album.extras:
            assert extra in db_album.extras

    def test_no_valid_tracks(self, tmp_session, tmp_path):
        """Error if given directory does not contain any valid tracks."""
        mock_config = MagicMock()
        mock_config.plugin_manager.hook.import_album.return_value = []

        album_path = tmp_path / "empty"
        album_path.mkdir()

        with pytest.raises(add.AddError):
            add.add.add_item(mock_config, tmp_session, album_path)

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
            add.add.add_item(mock_config, tmp_session, tmp_album_path)

        assert not tmp_session.query(Album).scalar()

    def test_duplicate_tracks(self, real_album, tmp_session):
        """Don't fail album add if a track (by tags) already exists in the library."""
        mock_config = MagicMock()
        mock_config.plugin_manager.hook.import_album.return_value = []

        tmp_session.merge(real_album.tracks[0])

        add.add.add_item(mock_config, tmp_session, real_album.path)

        assert tmp_session.query(Album).filter_by(path=real_album.path).one()

    def test_duplicate_album(self, real_album, tmp_session):
        """We merge an existing album by it's path."""
        mock_config = MagicMock()
        mock_config.plugin_manager.hook.import_album.return_value = []

        dup_album = copy.deepcopy(real_album)
        dup_album.title = "diff"
        tmp_session.merge(dup_album)

        add.add.add_item(mock_config, tmp_session, real_album.path)

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
        existing_album.mb_album_id = "1234"
        assert not new_album.is_unique(existing_album)

        for track in new_album.tracks:
            track.title = "new_album"

        for extra_num, extra in enumerate(new_album.extras):
            extra.path = Path(f"{extra_num}.txt")

        assert new_album.mb_album_id != existing_album.mb_album_id
        assert new_album.tracks != existing_album.tracks
        assert new_album.extras != existing_album.extras

        tmp_session.merge(existing_album)
        with patch("moe.plugins.add.add._add_album", return_value=new_album):
            add.add.add_item(mock_config, tmp_session, new_album.path)

        db_album = tmp_session.query(Album).one()
        assert db_album.mb_album_id == existing_album.mb_album_id
        assert sorted(db_album.tracks) == sorted(new_album.tracks)
        assert sorted(db_album.extras) == sorted(new_album.extras)

    def test_add_multi_disc(self, real_album, tmp_session):
        """We can add a multi-disc album."""
        mock_config = MagicMock()
        mock_config.plugin_manager.hook.import_album.return_value = []

        track1 = real_album.tracks[0]
        track2 = real_album.tracks[1]
        track1.disc = 1
        track2.disc = 2
        real_album.disc_total = 2
        moe_write.write_tags(track1)
        moe_write.write_tags(track2)

        track1_path = Path(real_album.path / "disc 01" / track1.path.name)
        track2_path = Path(real_album.path / "disc 02" / track2.path.name)
        track1_path.parent.mkdir()
        track2_path.parent.mkdir()
        track1.path.rename(track1_path)
        track2.path.rename(track2_path)
        track1.path = track1_path
        track2.path = track2_path

        add.add.add_item(mock_config, tmp_session, real_album.path)

        album = tmp_session.query(Album).filter_by(path=real_album.path).one()

        assert album.get_track(track1.track_num, track1.disc)
        assert album.get_track(track2.track_num, track2.disc)


class TestAddItemFromFile:
    """Test a file argument given to add as a track."""

    def test_path_not_found(self):
        """Raise SystemExit if the path to add does not exist."""
        with pytest.raises(add.AddError):
            add.add.add_item(Mock(), Mock(), Path("does not exist"))

    def test_file_track(self, real_track, tmp_session):
        """If a file given, add to library as a Track."""
        mock_config = MagicMock()
        mock_config.plugin_manager.hook.import_album.return_value = []

        add.add.add_item(mock_config, tmp_session, real_track.path)

        assert tmp_session.query(Track.path).filter_by(path=real_track.path).one()

    def test_min_reqd_tags(self, tmp_session, reqd_mp3_path):
        """We can add a track with only a track_num, album, albumartist, and year."""
        mock_config = MagicMock()
        mock_config.plugin_manager.hook.import_album.return_value = []

        add.add.add_item(mock_config, tmp_session, reqd_mp3_path)

        assert tmp_session.query(Track.path).filter_by(path=reqd_mp3_path).one()

    def test_non_track_file(self):
        """Error if the file given is not a valid track."""
        with pytest.raises(add.AddError):
            add.add.add_item(Mock(), Mock(), Path(__file__))

    def test_track_missing_reqd_tags(self, empty_mp3_path):
        """Error if the track doesn't have all the required tags."""
        with pytest.raises(add.AddError):
            add.add.add_item(Mock(), Mock(), empty_mp3_path)

    def test_duplicate_track(self, real_track, tmp_session, tmp_path):
        """Overwrite old track path with the new track if a duplicate is found."""
        mock_config = MagicMock()
        mock_config.plugin_manager.hook.import_album.return_value = []

        new_track_path = tmp_path / "full2"
        shutil.copyfile(real_track.path, new_track_path)
        tmp_session.add(real_track)

        add.add.add_item(mock_config, tmp_session, new_track_path)

        assert tmp_session.query(Track.path).filter_by(path=new_track_path).one()
