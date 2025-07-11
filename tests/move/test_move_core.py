"""Tests the core api for moving items."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

import moe
from moe import config
from moe import move as moe_move
from moe.config import ExtraPlugin
from moe.library import Album, Extra, LibItem
from tests.conftest import album_factory, extra_factory, track_factory


@pytest.fixture
def _tmp_move_config(tmp_config):
    """Creates a configuration with a temporary library path."""
    tmp_config(settings="default_plugins = ['move', 'write']")


@pytest.fixture
def mock_copy():
    """Mock the `move_item()` api call."""
    with patch("moe.move.move_core.copy_item", autospec=True) as mock_copy:
        yield mock_copy


class MovePlugin:
    """Test plugin that implements the move hookspecs."""

    @staticmethod
    @moe.hookimpl
    def create_path_template_func():
        """Capitalize a string."""
        return [upper]


def upper(text):
    """Test function for MovePlugin."""
    return text.capitalize()


class TestCreatePathTemplateFuncHook:
    """Test the create_path_template_func hook."""

    def test_hook(self, tmp_config):
        """Replace all the defined illegal characters from any paths."""
        tmp_config(
            settings="""
            default_plugins = ["move"]
            [move]
            track_path = "{upper(track.title)}"
            """,
            extra_plugins=[config.ExtraPlugin(MovePlugin, "move_plugin")],
        )
        track = track_factory(title="lower")

        assert moe_move.fmt_item_path(track).name == "Lower"


class TestCustomPathTemplateFuncs:
    """Test any custom path template functions."""

    @pytest.mark.usefixtures("_tmp_move_config")
    def test_e_unique(self):
        """Deconflict any duplicate custom paths."""
        album = album_factory(num_tracks=0, num_extras=0)
        extras = [
            extra_factory(album=album, path=album.path / "cover.jpg"),
            extra_factory(album=album, path=album.path / "cover.jpg"),
            extra_factory(album=album, path=album.path / "cover.jpg"),
        ]
        assert extras[0].path == extras[1].path
        assert extras[0].path == extras[2].path
        assert len(album.extras) == len(extras)

        extras[0].path = moe_move.fmt_item_path(extras[0])
        extras[1].path = moe_move.fmt_item_path(extras[1])
        extras[2].path = moe_move.fmt_item_path(extras[2])

        assert extras[0].path != extras[1].path
        assert extras[0].path != extras[2].path
        assert extras[1].path != extras[2].path


########################################################################################
# Test format paths
########################################################################################
class TestFmtItemPath:
    """Test `fmt_item_path()`."""

    def test_replace_chars(self, tmp_config):
        """Replace all the defined illegal characters from any paths."""
        tmp_config(
            settings="""
            default_plugins = ["move"]
            [move]
            track_path = "{track.title}"
            """
        )
        tracks = []
        replacements = []
        tracks.append(track_factory(title='/ reserved <, >, :, ", ?, *, |, /'))
        replacements.append("_ reserved _, _, _, _, _, _, _, _")
        tracks.append(track_factory(title=".leading dot"))
        replacements.append("_leading dot")
        tracks.append(track_factory(title="trailing dot."))
        replacements.append("trailing dot_")
        tracks.append(track_factory(title="trailing whitespace "))
        replacements.append("trailing whitespace")

        formatted_paths = [moe_move.fmt_item_path(track) for track in tracks]

        for path in formatted_paths:
            assert any(replacement == path.name for replacement in replacements)

    @pytest.mark.usefixtures("_tmp_move_config")
    def test_album_relative_to_lib_path(self):
        """The album path should be relative to the library path configuration."""
        album = album_factory()
        lib_path = Path(config.CONFIG.settings.library_path)

        album_path = moe_move.fmt_item_path(album)

        assert album_path.is_relative_to(lib_path)

    @pytest.mark.usefixtures("_tmp_move_config")
    def test_extra_relative_to_album(self):
        """The extra path should be relative to its album path."""
        extra = extra_factory()
        extra_path = moe_move.fmt_item_path(extra)

        assert extra_path.is_relative_to(moe_move.fmt_item_path(extra.album))

    @pytest.mark.usefixtures("_tmp_move_config")
    def test_track_relative_to_album(self):
        """The track path should be relative to its album path."""
        track = track_factory()
        track_path = moe_move.fmt_item_path(track)

        assert track_path.is_relative_to(track.album.path)

    def test_asciify_paths(self, tmp_config):
        """Paths should not contain unicode characters if `asciify_paths` is true."""
        album = album_factory(title="café")
        tmp_config(
            settings="""
        default_plugins = ["move"]
        [move]
        asciify_paths = true
        """
        )

        # assumes that an album's title will be part of the new path
        assert str(moe_move.fmt_item_path(album)).isascii()

    @pytest.mark.usefixtures("_tmp_move_config")
    def test_given_parent(self, tmp_path):
        """If provided, paths should be relative to ``parent``."""
        track = track_factory()
        track_path = moe_move.fmt_item_path(track, tmp_path)

        assert track_path.is_relative_to(tmp_path)

    def test_not_implemented(self):
        """Raise a NotImplementedError if the item is not a Track, Album, or Extra."""
        with pytest.raises(NotImplementedError):
            moe_move.fmt_item_path(LibItem())


########################################################################################
# Test copy
########################################################################################
@pytest.mark.usefixtures("_tmp_move_config")
class TestCopyAlbum:
    """Tests `copy_item(album)`."""

    def test_copy_album(self, tmp_path):
        """We can copy an album that was added to the library.

        The album desination should be formatted according to `fmt_item_path()`.
        """
        album = album_factory(path=tmp_path, exists=True)
        album_dest = moe_move.fmt_item_path(album)
        assert album.path != album_dest

        og_paths = [track.path for track in album.tracks]
        og_paths += [extra.path for extra in album.extras]
        og_paths.append(album.path)

        moe_move.copy_item(album)

        assert album.path == album_dest
        assert album.path.exists()
        for copied_track in album.tracks:
            assert copied_track.path == moe_move.fmt_item_path(copied_track)
            assert copied_track.path.is_file()
        for copied_extra in album.extras:
            assert copied_extra.path == moe_move.fmt_item_path(copied_extra)
            assert copied_extra.path.is_file()
        for og_path in og_paths:
            assert og_path.exists()

    def test_copy_multi_disc_album(self, tmp_path):
        """We can copy albums containing multiple discs.

        The album desination should be formatted according to `fmt_item_path()`.
        """
        album = album_factory(path=tmp_path, exists=True)
        album_dest = moe_move.fmt_item_path(album)
        assert album.path != album_dest

        album.tracks[1].disc = 2
        album.tracks[1].track_num = 1
        album.disc_total = 2

        og_paths = [track.path for track in album.tracks]
        og_paths += [extra.path for extra in album.extras]
        og_paths.append(album.path)

        moe_move.copy_item(album)

        assert album.path == album_dest
        assert album.path.exists()
        for copied_track in album.tracks:
            assert copied_track.path == moe_move.fmt_item_path(copied_track)
            assert copied_track.path.is_file()
        for copied_extra in album.extras:
            assert copied_extra.path == moe_move.fmt_item_path(copied_extra)
            assert copied_extra.path.is_file()
        for og_path in og_paths:
            assert og_path.exists()


@pytest.mark.usefixtures("_tmp_move_config")
class TestCopyExtra:
    """Tests `copy_item(extra)`."""

    def test_copy_extra(self, tmp_path):
        """We can copy an extra.

        The extra desination should be formatted according to `fmt_item_path()`.
        """
        extra = extra_factory(path=tmp_path / "move me.txt", exists=True)
        extra_dest = moe_move.fmt_item_path(extra)
        og_path = extra.path
        assert og_path != extra_dest

        moe_move.copy_item(extra)

        assert extra.path.exists()
        assert og_path.exists()
        assert og_path != extra.path
        assert extra.path == extra_dest

    def test_same_des(self, tmp_path):
        """Don't do anything if the destination is the same as the current path."""
        extra = extra_factory(path=tmp_path / "in my place.mp3", exists=True)
        og_path = extra.path

        with patch("moe.move.move_core.fmt_item_path", return_value=extra.path):
            moe_move.copy_item(extra)

        assert extra.path == og_path


@pytest.mark.usefixtures("_tmp_move_config")
class TestCopyTrack:
    """Tests `copy_item(track)`."""

    def test_copy_track(self, tmp_path):
        """We can copy a track.

        The track desination should be formatted according to `fmt_item_path()`.
        """
        track = track_factory(path=tmp_path / "move me.mp3", exists=True)
        track_dest = moe_move.fmt_item_path(track)
        og_path = track.path
        assert og_path != track_dest

        moe_move.copy_item(track)

        assert track.path.exists()
        assert og_path.exists()
        assert og_path != track.path
        assert track.path == track_dest

    def test_same_des(self, tmp_path):
        """Don't do anything if the destination is the same as the current path."""
        track = track_factory(path=tmp_path / "in my place.txt", exists=True)
        og_path = track.path

        with patch("moe.move.move_core.fmt_item_path", return_value=track.path):
            moe_move.copy_item(track)

        assert track.path == og_path


########################################################################################
# Test move
########################################################################################
@pytest.mark.usefixtures("_tmp_move_config")
class TestMoveAlbum:
    """Tests `move_item(album)`."""

    def test_move_album(self, tmp_path):
        """We can move an album that was added to the library."""
        album = album_factory(path=tmp_path, exists=True)
        album_dest = moe_move.fmt_item_path(album)
        assert album.path != album_dest

        og_paths = [track.path for track in album.tracks]
        og_paths += [extra.path for extra in album.extras]
        og_paths.append(album.path)

        moe_move.move_item(album)

        assert album.path == album_dest
        assert album.path.exists()
        for copied_track in album.tracks:
            assert copied_track.path == moe_move.fmt_item_path(copied_track)
            assert copied_track.path.is_file()
        for copied_extra in album.extras:
            assert copied_extra.path == moe_move.fmt_item_path(copied_extra)
            assert copied_extra.path.is_file()
        for og_path in og_paths:
            assert not og_path.exists()

    def test_move_multi_disc_album(self, tmp_path):
        """We can copy albums containing multiple discs."""
        album = album_factory(path=tmp_path, exists=True)
        album_dest = moe_move.fmt_item_path(album)
        assert album.path != album_dest

        album.tracks[1].disc = 2
        album.tracks[1].track_num = 1
        album.disc_total = 2

        og_paths = [track.path for track in album.tracks]
        og_paths += [extra.path for extra in album.extras]
        og_paths.append(album.path)

        moe_move.move_item(album)

        assert album.path == album_dest
        assert album.path.exists()
        for copied_track in album.tracks:
            assert copied_track.path == moe_move.fmt_item_path(copied_track)
            assert copied_track.path.is_file()
        for copied_extra in album.extras:
            assert copied_extra.path == moe_move.fmt_item_path(copied_extra)
            assert copied_extra.path.is_file()
        for og_path in og_paths:
            assert not og_path.exists()

    def test_rm_empty_leftover_dirs(self, tmp_path):
        """Remove any leftover empty directories after a move."""
        lib_path = Path(config.CONFIG.settings.library_path)
        album = album_factory(num_discs=2, exists=True, path=lib_path / "empty/album")
        og_path = album.path
        assert any(path.is_dir() for path in album.path.rglob("*"))

        # move the item to it's final directory
        config.CONFIG.settings.library_path = tmp_path
        moe_move.move_item(album)

        assert not og_path.exists()  # original path and subdirs should be removed
        assert not og_path.parent.exists()  # removed 'empty' dir

    def test_dont_rm_full_leftover_dirs(self, tmp_path):
        """Don't remove any leftover dirs that still have leftover items."""
        lib_path = Path(config.CONFIG.settings.library_path)
        album = album_factory(num_discs=2, exists=True, path=lib_path / "empty/album")
        og_path = album.path
        assert any(path.is_dir() for path in album.path.rglob("*"))
        (og_path / "leftover_file.txt").touch()
        (og_path.parent / "leftover_file.txt").touch()

        # move the item to it's final directory
        config.CONFIG.settings.library_path = tmp_path
        moe_move.move_item(album)

        assert og_path.exists()  # original path and subdirs should be removed
        assert og_path.parent.exists()  # removed 'empty' dir


@pytest.mark.usefixtures("_tmp_move_config")
class TestMoveExtra:
    """Tests `move_item(extra)`."""

    def test_move_extra(self, tmp_path):
        """We can move an extra.

        The extra desination should be formatted according to `fmt_item_path()`.
        """
        extra = extra_factory(path=tmp_path / "move me.txt", exists=True)
        extra_dest = moe_move.fmt_item_path(extra)
        og_path = extra.path
        assert og_path != extra_dest

        moe_move.move_item(extra)

        assert extra.path.exists()
        assert not og_path.exists()
        assert og_path != extra.path
        assert extra.path == extra_dest

    def test_same_des(self, tmp_path):
        """Don't do anything if the destination is the same as the current path."""
        extra = extra_factory(path=tmp_path / "in my place.txt", exists=True)
        og_path = extra.path

        with patch("moe.move.move_core.fmt_item_path", return_value=extra.path):
            moe_move.move_item(extra)

        assert extra.path == og_path


@pytest.mark.usefixtures("_tmp_move_config")
class TestMoveTrack:
    """Tests `move_item(track)`."""

    def test_move_track(self, tmp_path):
        """We can move a track.

        The track desination should be formatted according to `fmt_item_path()`.
        """
        track = track_factory(path=tmp_path / "move me.mp3", exists=True)
        track_dest = moe_move.fmt_item_path(track)
        og_path = track.path
        assert og_path != track_dest

        moe_move.move_item(track)

        assert track.path.exists()
        assert not og_path.exists()
        assert og_path != track.path
        assert track.path == track_dest

    def test_same_des(self, tmp_path):
        """Don't do anything if the destination is the same as the current path."""
        track = track_factory(path=tmp_path / "in my place.mp3", exists=True)
        og_path = track.path

        with patch("moe.move.move_core.fmt_item_path", return_value=track.path):
            moe_move.move_item(track)

        assert track.path == og_path


########################################################################################
# Test hooks
########################################################################################
@pytest.mark.usefixtures("_tmp_move_config")
class TestConfigOptions:
    """Test adding options and validation to the configuration."""

    def test_asciify_paths(self):
        """`asciify_paths` is not required and defaults to 'False'."""
        assert not config.CONFIG.settings.move.asciify_paths

    def test_album_path(self):
        """`album_path` is not required and has a default."""
        assert config.CONFIG.settings.move.album_path

    def test_extra_path(self):
        """`extra_path` is not required and has a default."""
        assert config.CONFIG.settings.move.extra_path

    def test_track_path(self):
        """`track_path` is not required and has a default."""
        assert config.CONFIG.settings.move.track_path


@pytest.mark.usefixtures("_tmp_move_config")
class TestEditNewItems:
    """Test the `edit_new_items` hook implementation.

    The hook should copy all items after they are added to the library. Track and extra
    albums are copied in case album attributes have changed.
    """

    def test_album(self, mock_copy):
        """Albums are copied after they are added to the library."""
        album = album_factory()
        mock_session = MagicMock()

        config.CONFIG.pm.hook.edit_new_items(session=mock_session, items=[album])

        mock_copy.assert_called_once_with(album)

    def test_track(self, mock_copy):
        """Tracks are copied after they are added to the library."""
        track = track_factory()
        mock_session = MagicMock()

        config.CONFIG.pm.hook.edit_new_items(session=mock_session, items=[track])

        mock_copy.assert_called_once_with(track)

    def test_extra(self, mock_copy):
        """Extras are copied after they are added to the library."""
        extra = extra_factory()
        mock_session = MagicMock()

        config.CONFIG.pm.hook.edit_new_items(session=mock_session, items=[extra])

        mock_copy.assert_called_once_with(extra)

    def test_album_with_tracks_and_extras_no_duplicate_copy(self, mock_copy):
        """Avoid duplicate copying when album and its items are batched."""
        album = album_factory(num_tracks=2, num_extras=2)
        mock_session = MagicMock()

        items = [album, *album.tracks, *album.extras]

        config.CONFIG.pm.hook.edit_new_items(session=mock_session, items=items)

        mock_copy.assert_called_once_with(album)


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation."""

    def test_move_core(self, tmp_config):
        """Enable the move core plugin if specified in the config."""
        tmp_config(settings='default_plugins = ["move"]')

        assert config.CONFIG.pm.has_plugin("move_core")


class TestPluginOverrideAlbumPathConfig:
    """Test plugin that implements the override_album_path_config hook."""

    @staticmethod
    @moe.hookimpl
    def override_album_path_config(album: Album) -> str | None:
        """Override the `album_path` for classical music albums."""
        if "Classical" in album.title:
            return "Classical/{album.artist}/{album.title}"


class TestOverrideAlbumPathConfig:
    """Test the `override_album_path_config` hook implementation."""

    @pytest.fixture
    def _tmp_album_path_config(self, tmp_config):
        """Create a temporary configuration with the test plugin."""
        tmp_config(
            settings="""
            default_plugins = ["move"]
            [move]
            album_path = "{album.artist}/{album.title}"
            """,
            extra_plugins=[
                ExtraPlugin(
                    TestPluginOverrideAlbumPathConfig, "override_album_path_plugin"
                )
            ],
        )

    @pytest.mark.usefixtures("_tmp_album_path_config")
    def test_classical_album(self):
        """Test that classical albums use the artist in the path."""
        album = album_factory(
            artist="Antonín Dvořák",
            title="Classical Symphony No. 6",
        )

        path = moe_move.fmt_item_path(album)
        expected_path = (
            Path(moe.config.CONFIG.settings.library_path).expanduser()
            / "Classical"
            / "Antonín Dvořák"
            / "Classical Symphony No. 6"
        )

        assert path == expected_path

    @pytest.mark.usefixtures("_tmp_album_path_config")
    def test_other_genre_album(self):
        """Test that other albums use the default path configuration."""
        album = album_factory(artist="Foreigner", title="Double Vision")

        path = moe_move.fmt_item_path(album)
        expected_path = (
            Path(moe.config.CONFIG.settings.library_path).expanduser()
            / "Foreigner"
            / "Double Vision"
        )

        assert path == expected_path

    def test_no_plugin(self, tmp_config):
        """Test that the default configuration is used when no plugin is active."""
        tmp_config(
            settings="""
            default_plugins = ["move"]
            [move]
            album_path = "{album.artist}/{album.title}"
            """
        )

        album = album_factory(artist="Antonín Dvořák", title="Classical Symphony No. 6")

        path = moe_move.fmt_item_path(album)
        expected_path = (
            Path(moe.config.CONFIG.settings.library_path).expanduser()
            / "Antonín Dvořák"
            / "Classical Symphony No. 6"
        )

        assert path == expected_path


class TestPluginOverrideExtraPathConfig:
    """Test plugin that implements the override_extra_path_config hook."""

    @staticmethod
    @moe.hookimpl
    def override_extra_path_config(extra: Extra) -> str | None:
        """Override the `extra_path` for specific extra file types."""
        if "cover" in extra.path.name.lower():
            return f"{extra.album.title}.jpg"


class TestOverrideExtraPathConfig:
    """Test the `override_extra_path_config` hook implementation."""

    @pytest.fixture
    def _tmp_extra_path_config(self, tmp_config):
        """Create a temporary configuration with the test plugin."""
        tmp_config(
            settings="""
            default_plugins = ["move"]
            [move]
            extra_path = "{extra.path.name}"
            """,
            extra_plugins=[
                ExtraPlugin(
                    TestPluginOverrideExtraPathConfig, "override_extra_path_plugin"
                )
            ],
        )

    @pytest.mark.usefixtures("_tmp_extra_path_config")
    def test_cover_extra(self):
        """Test that cover files get renamed to use the album title."""
        album = album_factory(title="Test Album")
        extra = extra_factory(album=album, path=album.path / "cover.jpg")

        path = moe_move.fmt_item_path(extra)
        expected_path = moe_move.fmt_item_path(album) / "Test Album.jpg"

        assert path == expected_path

    @pytest.mark.usefixtures("_tmp_extra_path_config")
    def test_other_extra(self):
        """Test that other extras use the default path configuration."""
        album = album_factory(title="Test Album")
        extra = extra_factory(album=album, path=album.path / "playlist.m3u")

        path = moe_move.fmt_item_path(extra)
        expected_path = moe_move.fmt_item_path(album) / "playlist.m3u"

        assert path == expected_path

    def test_no_plugin(self, tmp_config):
        """Test that the default configuration is used when no plugin is active."""
        tmp_config(
            settings="""
            default_plugins = ["move"]
            [move]
            extra_path = "{extra.path.name}"
            """
        )

        album = album_factory(title="Test Album")
        extra = extra_factory(album=album, path=album.path / "cover.jpg")

        path = moe_move.fmt_item_path(extra)
        expected_path = moe_move.fmt_item_path(album) / "cover.jpg"

        assert path == expected_path
