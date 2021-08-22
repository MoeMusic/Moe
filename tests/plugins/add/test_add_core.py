"""Tests the add plugin."""

import copy
import shutil
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

import moe
from moe.config import Config, ExtraPlugin
from moe.library.album import Album
from moe.library.lib_item import LibItem
from moe.library.track import Track
from moe.plugins import add
from moe.plugins import write as moe_write


@pytest.fixture
def tmp_add_config(tmp_config) -> Config:
    """A temporary config for the edit plugin with the cli."""
    return tmp_config('default_plugins = ["add"]', tmp_db=True)


class TestAddItemFromDir:
    """Test a directory given to ``add_item()`` to add as an album."""

    def test_dir_album(self, real_album, tmp_session, tmp_add_config):
        """If a directory given, add to library as an album."""
        add.add_item(tmp_add_config, real_album.path)

        assert tmp_session.query(Album).filter_by(path=real_album.path).one()

    def test_extras(self, real_album, tmp_session, tmp_add_config):
        """Add any extras that are within the album directory."""
        add.add_item(tmp_add_config, real_album.path)

        db_album = tmp_session.query(Album).one()
        for extra in real_album.extras:
            assert extra in db_album.extras

    def test_no_valid_tracks(self, tmp_path, tmp_session, tmp_add_config):
        """Error if given directory does not contain any valid tracks."""
        album_path = tmp_path / "empty"
        album_path.mkdir()

        with pytest.raises(add.AddError):
            add.add_item(tmp_add_config, album_path)

        assert not tmp_session.query(Album).scalar()

    def test_track_error(self, empty_mp3_path, real_album, tmp_session, tmp_add_config):
        """Ignore (just log) any tracks that are unable to be created."""
        new_path = shutil.copyfile(
            empty_mp3_path, real_album.path / empty_mp3_path.name
        )

        add.add_item(tmp_add_config, real_album.path)

        assert not tmp_session.query(Track.path).filter_by(path=new_path).scalar()

    def test_different_tracks(
        self, tmp_path, real_track_factory, tmp_session, tmp_add_config
    ):
        """Error if tracks have different album attributes.

        All tracks in a given directory should belong to the same album.
        """
        tmp_album_path = tmp_path / "tmp_album"
        tmp_album_path.mkdir()
        shutil.copy(real_track_factory(year=1).path, tmp_album_path)
        shutil.copy(real_track_factory(year=2).path, tmp_album_path)

        with pytest.raises(add.AddError):
            add.add_item(tmp_add_config, tmp_album_path)

        assert not tmp_session.query(Album).scalar()

    def test_duplicate_tracks(self, real_album, tmp_session, tmp_add_config):
        """Don't fail album add if a track (by tags) already exists in the library."""
        tmp_session.merge(real_album.tracks[0])

        add.add_item(tmp_add_config, real_album.path)

        assert tmp_session.query(Album).filter_by(path=real_album.path).one()

    def test_duplicate_album(self, real_album, tmp_session, tmp_add_config):
        """We merge an existing album by it's path."""
        dup_album = copy.deepcopy(real_album)
        dup_album.title = "diff"
        tmp_session.merge(dup_album)

        add.add_item(tmp_add_config, real_album.path)

        assert tmp_session.query(Album).filter_by(path=real_album.path).one()

    def test_merge_existing(self, real_album_factory, tmp_session, tmp_add_config):
        """Merge the album to be added with an existing album in the library.

        The album info should be kept (likely to be more accurate), however, any tracks
        or extras should be overwritten.
        """
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
            add.add_item(tmp_add_config, new_album.path)

        db_album = tmp_session.query(Album).one()
        assert db_album.mb_album_id == existing_album.mb_album_id
        assert sorted(db_album.tracks) == sorted(new_album.tracks)
        assert sorted(db_album.extras) == sorted(new_album.extras)

    def test_add_multi_disc(self, real_album, tmp_session, tmp_add_config):
        """We can add a multi-disc album."""
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

        add.add_item(tmp_add_config, real_album.path)

        album = tmp_session.query(Album).filter_by(path=real_album.path).one()

        assert album.get_track(track1.track_num, track1.disc)
        assert album.get_track(track2.track_num, track2.disc)


class TestAddItemFromFile:
    """Test a file argument given to add as a track."""

    def test_file_track(self, real_track, tmp_session, tmp_add_config):
        """If a file given, add to library as a Track."""
        add.add_item(tmp_add_config, real_track.path)

        assert tmp_session.query(Track.path).filter_by(path=real_track.path).one()

    def test_min_reqd_tags(self, reqd_mp3_path, tmp_session, tmp_add_config):
        """We can add a track with only a track_num, album, albumartist, and year."""
        add.add_item(tmp_add_config, reqd_mp3_path)

        assert tmp_session.query(Track.path).filter_by(path=reqd_mp3_path).one()

    def test_non_track_file(self):
        """Error if the file given is not a valid track."""
        with pytest.raises(add.AddError):
            add.add_item(Mock(), Path(__file__))

    def test_track_missing_reqd_tags(self, empty_mp3_path, tmp_add_config):
        """Error if the track doesn't have all the required tags."""
        with pytest.raises(add.AddError):
            add.add_item(tmp_add_config, empty_mp3_path)

    def test_duplicate_track(self, tmp_path, real_track, tmp_session, tmp_add_config):
        """Overwrite old track path with the new track if a duplicate is found."""
        new_track_path = tmp_path / "full2"
        shutil.copyfile(real_track.path, new_track_path)
        tmp_session.add(real_track)

        add.add_item(tmp_add_config, new_track_path)

        assert tmp_session.query(Track.path).filter_by(path=new_track_path).one()


class AddPlugin:
    """Test plugin that implements the add hookspecs."""

    @staticmethod
    @moe.hookimpl
    def pre_add(config: Config, item: LibItem):
        """Changes the album title."""
        if isinstance(item, Track):
            item.title = "pre_add"

    @staticmethod
    @moe.hookimpl
    def post_add(config: Config, item: LibItem):
        """Apply the new title onto the old album."""
        if isinstance(item, Track):
            item.genre = "post_add"


class TestAddItem:
    """General functionality of `add_item`."""

    def test_hooks(self, real_track, tmp_config, tmp_session):
        """The pre and post add hooks are called when adding an item."""
        config = tmp_config(
            "default_plugins = ['add']",
            extra_plugins=[ExtraPlugin(AddPlugin, "add_plugin")],
            tmp_db=True,
        )

        add.add_item(config, real_track.path)

        db_track = tmp_session.query(Track).one()

        assert db_track.title == "pre_add"
        assert db_track.genre == "post_add"

    def test_path_not_found(self):
        """Raise SystemExit if the path to add does not exist."""
        with pytest.raises(add.AddError):
            add.add_item(Mock(), Path("does not exist"))


class TestHookSpecs:
    """Test the various hook specifications."""

    def test_pre_add(self, mock_track, tmp_config):
        """Ensure plugins can implement the `pre_add` hook."""
        config = tmp_config(
            "default_plugins = ['add']",
            extra_plugins=[ExtraPlugin(AddPlugin, "add_plugin")],
        )

        config.plugin_manager.hook.pre_add(config=config, item=mock_track)

        assert mock_track.title == "pre_add"

    def test_post_add(self, mock_track, tmp_config):
        """Ensure plugins can implement the `pre_add` hook."""
        config = tmp_config(
            "default_plugins = ['add']",
            extra_plugins=[ExtraPlugin(AddPlugin, "add_plugin")],
        )

        config.plugin_manager.hook.post_add(config=config, item=mock_track)

        assert mock_track.genre == "post_add"


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation."""

    def test_add_core(self, tmp_config):
        """Enable the add core plugin if specified in the config."""
        config = tmp_config(settings='default_plugins = ["add"]')

        assert config.plugin_manager.has_plugin("add_core")
