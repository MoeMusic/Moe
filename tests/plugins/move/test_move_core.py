"""Tests the core api for moving items."""
from pathlib import Path
from unittest.mock import patch

import pytest

from moe.plugins import move as moe_move


@pytest.fixture(scope="function")
def tmp_move_config(tmp_config, tmp_path):
    """Creates a configuration with a temporary library path."""
    return tmp_config(
        f"""
    default_plugins = ["move"]
    [move]
    library_path = '''{tmp_path.resolve()}'''
    """
    )


@pytest.fixture
def mock_copy():
    """Mock the `move_item()` api call."""
    with patch("moe.plugins.move.move_core.copy_item", autospec=True) as mock_edit:
        yield mock_edit


########################################################################################
# Test format paths
########################################################################################
class TestFmtAlbumPath:
    """Tests `fmt_item_path(album)`."""

    def test_relative_to_lib_path(self, real_album, tmp_move_config):
        """The album path should be relative to the library path configuration."""
        lib_path = Path(tmp_move_config.settings.move.library_path)

        album_path = moe_move.fmt_item_path(tmp_move_config, real_album)

        assert lib_path in album_path.parents

    def test_album_asciify_paths(self, real_album, tmp_config):
        """Paths should not contain unicode characters if `asciify_paths` is true."""
        tmp_settings = """
        default_plugins = ["move"]
        [move]
        asciify_paths = true
        """
        config = tmp_config(tmp_settings)
        ascii_title = "café"

        # assumes that an album's title will be part of the new path
        real_album.title = ascii_title
        assert str(moe_move.fmt_item_path(config, real_album)).isascii()


class TestFmtExtraPath:
    """Tests `fmt_item_path(extra)`."""

    def test_relative_to_album(self, real_extra, tmp_move_config):
        """The extra path should be relative to its album path."""
        extra_path = moe_move.fmt_item_path(tmp_move_config, real_extra)

        assert real_extra.album_obj.path in extra_path.parents

    def test_extra_asciify_paths(self, real_extra, tmp_config):
        """Paths should not contain unicode characters if `asciify_paths` is true."""
        tmp_settings = """
        default_plugins = ["move"]
        [move]
        asciify_paths = true
        """
        config = tmp_config(tmp_settings)
        ascii_title = "café"

        # test assumes that an extra's path name will be part of the new path
        real_extra.path = real_extra.path.with_name(ascii_title)
        assert str(moe_move.fmt_item_path(config, real_extra)).isascii()


class TestFmtTrackPath:
    """Tests `fmt_item_path(extra)`."""

    def test_relative_to_album(self, real_track, tmp_move_config):
        """The track path should be relative to its album path."""
        track_path = moe_move.fmt_item_path(tmp_move_config, real_track)

        assert real_track.album_obj.path in track_path.parents

    def test_extra_asciify_paths(self, real_track, tmp_config):
        """Paths should not contain unicode characters if `asciify_paths` is true."""
        tmp_settings = """
        default_plugins = ["move"]
        [move]
        asciify_paths = true
        """
        config = tmp_config(tmp_settings)
        ascii_title = "café"

        # assumes that a track's title will be part of the new path
        real_track.title = ascii_title
        assert str(moe_move.fmt_item_path(config, real_track)).isascii()


########################################################################################
# Test copy
########################################################################################
class TestCopyAlbum:
    """Tests `copy_item(album)`."""

    def test_copy_album(self, real_album, tmp_move_config):
        """We can copy an album that was added to the library.

        The album desination should be formatted according to `fmt_item_path()`.
        """
        album_dest = moe_move.fmt_item_path(tmp_move_config, real_album)
        assert real_album.path != album_dest

        og_paths = [track.path for track in real_album.tracks]
        og_paths += [extra.path for extra in real_album.extras]
        og_paths.append(real_album.path)

        moe_move.copy_item(tmp_move_config, real_album)

        assert real_album.path == album_dest
        assert real_album.path.exists()
        for copied_track in real_album.tracks:
            assert copied_track.path == moe_move.fmt_item_path(
                tmp_move_config, copied_track
            )
            assert copied_track.path.is_file()
        for copied_extra in real_album.extras:
            assert copied_extra.path == moe_move.fmt_item_path(
                tmp_move_config, copied_extra
            )
            assert copied_extra.path.is_file()
        for og_path in og_paths:
            assert og_path.exists()

    def test_copy_multi_disc_album(self, real_album, tmp_move_config):
        """We can copy albums containing multiple discs.

        The album desination should be formatted according to `fmt_item_path()`.
        """
        album_dest = moe_move.fmt_item_path(tmp_move_config, real_album)
        assert real_album.path != album_dest

        real_album.tracks[1].disc = 2
        real_album.tracks[1].track_num = 1
        real_album.disc_total = 2

        og_paths = [track.path for track in real_album.tracks]
        og_paths += [extra.path for extra in real_album.extras]
        og_paths.append(real_album.path)

        moe_move.copy_item(tmp_move_config, real_album)

        assert real_album.path == album_dest
        assert real_album.path.exists()
        for copied_track in real_album.tracks:
            assert copied_track.path == moe_move.fmt_item_path(
                tmp_move_config, copied_track
            )
            assert copied_track.path.is_file()
        for copied_extra in real_album.extras:
            assert copied_extra.path == moe_move.fmt_item_path(
                tmp_move_config, copied_extra
            )
            assert copied_extra.path.is_file()
        for og_path in og_paths:
            assert og_path.exists()


class TestCopyExtra:
    """Tests `copy_item(extra)`."""

    def test_copy_extra(self, real_extra, tmp_move_config):
        """We can copy an extra.

        The extra desination should be formatted according to `fmt_item_path()`.
        """
        # we need to set the album's path since extra paths are based off their albums
        real_extra.album_obj.path = moe_move.fmt_item_path(
            tmp_move_config, real_extra.album_obj
        )

        extra_dest = moe_move.fmt_item_path(tmp_move_config, real_extra)
        og_path = real_extra.path
        assert og_path != extra_dest

        moe_move.copy_item(tmp_move_config, real_extra)

        assert real_extra.path.exists()
        assert og_path.exists()
        assert og_path != real_extra.path
        assert real_extra.path == extra_dest


class TestCopyTrack:
    """Tests `copy_item(track)`."""

    def test_copy_track(self, real_track, tmp_move_config):
        """We can copy a track.

        The track desination should be formatted according to `fmt_item_path()`.
        """
        # we need to set the album's path since track paths are based off their albums
        real_track.album_obj.path = moe_move.fmt_item_path(
            tmp_move_config, real_track.album_obj
        )

        track_dest = moe_move.fmt_item_path(tmp_move_config, real_track)
        og_path = real_track.path
        assert og_path != track_dest

        moe_move.copy_item(tmp_move_config, real_track)

        assert real_track.path.exists()
        assert og_path.exists()
        assert og_path != real_track.path
        assert real_track.path == track_dest


########################################################################################
# Test move
########################################################################################
class TestMoveAlbum:
    """Tests `move_item(album)`."""

    def test_move_album(self, real_album, tmp_move_config):
        """We can move an album that was added to the library."""
        album_dest = moe_move.fmt_item_path(tmp_move_config, real_album)
        assert real_album.path != album_dest

        og_paths = [track.path for track in real_album.tracks]
        og_paths += [extra.path for extra in real_album.extras]
        og_paths.append(real_album.path)

        moe_move.move_item(tmp_move_config, real_album)

        assert real_album.path == album_dest
        assert real_album.path.exists()
        for copied_track in real_album.tracks:
            assert copied_track.path == moe_move.fmt_item_path(
                tmp_move_config, copied_track
            )
            assert copied_track.path.is_file()
        for copied_extra in real_album.extras:
            assert copied_extra.path == moe_move.fmt_item_path(
                tmp_move_config, copied_extra
            )
            assert copied_extra.path.is_file()
        for og_path in og_paths:
            assert not og_path.exists()

    def test_move_multi_disc_album(self, real_album, tmp_move_config):
        """We can copy albums containing multiple discs."""
        album_dest = moe_move.fmt_item_path(tmp_move_config, real_album)
        assert real_album.path != album_dest

        real_album.tracks[1].disc = 2
        real_album.tracks[1].track_num = 1
        real_album.disc_total = 2

        og_paths = [track.path for track in real_album.tracks]
        og_paths += [extra.path for extra in real_album.extras]
        og_paths.append(real_album.path)

        moe_move.move_item(tmp_move_config, real_album)

        assert real_album.path == album_dest
        assert real_album.path.exists()
        for copied_track in real_album.tracks:
            assert copied_track.path == moe_move.fmt_item_path(
                tmp_move_config, copied_track
            )
            assert copied_track.path.is_file()
        for copied_extra in real_album.extras:
            assert copied_extra.path == moe_move.fmt_item_path(
                tmp_move_config, copied_extra
            )
            assert copied_extra.path.is_file()
        for og_path in og_paths:
            assert not og_path.exists()

    def test_rm_empty_leftover_dirs(self, real_album, tmp_move_config):
        """Remove any leftover empty directories after a move."""
        real_album.disc_total = 2  # also remove empty child directories
        lib_path = tmp_move_config.settings.move.library_path

        # first move the album to a nested sub directory
        nested_lib_path = lib_path + "/should/be/deleted"
        tmp_move_config.settings.move.library_path = nested_lib_path
        moe_move.move_item(tmp_move_config, real_album)

        # now move the item to it's final directory
        tmp_move_config.settings.move.library_path = lib_path
        moe_move.move_item(tmp_move_config, real_album)

        # all the original nestesd sub dirs of the first album path should be deleted
        nested_lib_path = Path(nested_lib_path)
        assert not nested_lib_path.exists()
        for parent in nested_lib_path.parents:
            if parent == Path(lib_path):
                break

            assert not parent.exists()


class TestMoveExtra:
    """Tests `move_item(extra)`."""

    def test_move_extra(self, real_extra, tmp_move_config):
        """We can move an extra.

        The extra desination should be formatted according to `fmt_item_path()`.
        """
        # we need to set the album's path since extra paths are based off their albums
        real_extra.album_obj.path = moe_move.fmt_item_path(
            tmp_move_config, real_extra.album_obj
        )

        extra_dest = moe_move.fmt_item_path(tmp_move_config, real_extra)
        og_path = real_extra.path
        assert og_path != extra_dest

        moe_move.move_item(tmp_move_config, real_extra)

        assert real_extra.path.exists()
        assert not og_path.exists()
        assert og_path != real_extra.path
        assert real_extra.path == extra_dest


class TestMoveTrack:
    """Tests `move_item(track)`."""

    def test_move_track(self, real_track, tmp_move_config):
        """We can move a track.

        The track desination should be formatted according to `fmt_item_path()`.
        """
        # we need to set the album's path since track paths are based off their albums
        real_track.album_obj.path = moe_move.fmt_item_path(
            tmp_move_config, real_track.album_obj
        )

        track_dest = moe_move.fmt_item_path(tmp_move_config, real_track)
        og_path = real_track.path
        assert og_path != track_dest

        moe_move.move_item(tmp_move_config, real_track)

        assert real_track.path.exists()
        assert not og_path.exists()
        assert og_path != real_track.path
        assert real_track.path == track_dest


class TestPostAdd:
    """Test the `post_add` hook implementation.

    The hook should copy all items after they are added to the library. Track and extra
    albums are copied in case album attributes have changed.
    """

    def test_post_add_album(self, mock_album, tmp_config, mock_copy):
        """Albums are copied after they are added to the library."""
        config = tmp_config("default_plugins = ['add', 'move']")

        config.plugin_manager.hook.post_add(config=config, item=mock_album)

        mock_copy.assert_called_once_with(config, mock_album)

    def test_post_add_track(self, mock_track, tmp_config, mock_copy):
        """Tracks are copied after they are added to the library."""
        config = tmp_config("default_plugins = ['add', 'move']")

        config.plugin_manager.hook.post_add(config=config, item=mock_track)

        mock_copy.assert_called_once_with(config, mock_track.album_obj)

    def test_post_add_extra(self, mock_extra, tmp_config, mock_copy):
        """Extras are copied after they are added to the library."""
        config = tmp_config("default_plugins = ['add', 'move']")

        config.plugin_manager.hook.post_add(config=config, item=mock_extra)

        mock_copy.assert_called_once_with(config, mock_extra.album_obj)


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation."""

    def test_move_core(self, tmp_config):
        """Enable the move core plugin if specified in the config."""
        config = tmp_config(settings='default_plugins = ["move"]')

        assert config.plugin_manager.has_plugin("move_core")
