"""Tests the ``move`` plugin."""

import argparse
from pathlib import Path

import pytest
import sqlalchemy as sa

import moe
from moe.core.library.album import Album
from moe.core.library.session import session_scope
from moe.plugins import move


@pytest.fixture(scope="function")
def tmp_config_lib_path(tmp_config, tmp_path):
    """Creates a configuration with a temporary library path."""
    tmp_settings = f"""
    default_plugins = ["move"]
    [move]
    library_path = '''{tmp_path.resolve()}'''
    """
    return tmp_config(tmp_settings)


########################################################################################
# Test format paths
########################################################################################
class TestFmtAlbumPath:
    """Tests `fmt_item_path(album)`."""

    def test_relative_to_lib_path(self, real_album, tmp_config_lib_path):
        """The album path should be relative to the library path configuration."""
        lib_path = Path(tmp_config_lib_path.settings.move.library_path)

        album_path = move.fmt_item_path(real_album, tmp_config_lib_path)

        assert lib_path in album_path.parents

    def test_album_asciify_paths(self, real_album, tmp_config):
        """Paths should not contain unicode characters if `asciify_paths` is true."""
        tmp_settings = """
        default_plugins = ["move"]
        [move]
        asciify_paths = true
        """
        config = tmp_config(tmp_settings)
        non_ascii_title = "café"

        # assumes that an album's title will be part of the new path
        real_album.title = non_ascii_title
        str(move.fmt_item_path(real_album, config))


class TestFmtExtraPath:
    """Tests `fmt_item_path(extra)`."""

    def test_relative_to_album(self, real_extra, tmp_config_lib_path):
        """The extra path should be relative to its album path."""
        extra_path = move.fmt_item_path(real_extra, tmp_config_lib_path)

        assert real_extra.album_obj.path in extra_path.parents

    def test_extra_asciify_paths(self, real_extra, tmp_config):
        """Paths should not contain unicode characters if `asciify_paths` is true."""
        tmp_settings = """
        default_plugins = ["move"]
        [move]
        asciify_paths = true
        """
        config = tmp_config(tmp_settings)
        non_ascii_title = "café"

        # test assumes that an extra's path name will be part of the new path
        real_extra.path = real_extra.path.with_name(non_ascii_title)
        str(move.fmt_item_path(real_extra, config))


class TestFmtTrackPath:
    """Tests `fmt_item_path(extra)`."""

    def test_relative_to_album(self, real_track, tmp_config_lib_path):
        """The track path should be relative to its album path."""
        track_path = move.fmt_item_path(real_track, tmp_config_lib_path)

        assert real_track.album_obj.path in track_path.parents

    def test_extra_asciify_paths(self, real_track, tmp_config):
        """Paths should not contain unicode characters if `asciify_paths` is true."""
        tmp_settings = """
        default_plugins = ["move"]
        [move]
        asciify_paths = true
        """
        config = tmp_config(tmp_settings)
        non_ascii_title = "café"

        # assumes that a track's title will be part of the new path
        real_track.title = non_ascii_title
        str(move.fmt_item_path(real_track, config))


########################################################################################
# Test copy
########################################################################################
class TestCopyAlbum:
    """Tests `copy_item(album)`."""

    def test_copy_album(self, real_album, tmp_config_lib_path):
        """We can copy an album that was added to the library.

        The album desination should be formatted according to `fmt_item_path()`.
        """
        album_dest = move.fmt_item_path(real_album, tmp_config_lib_path)
        assert real_album.path != album_dest

        og_paths = [track.path for track in real_album.tracks]
        og_paths += [extra.path for extra in real_album.extras]
        og_paths.append(real_album.path)

        move.copy_item(real_album, tmp_config_lib_path)

        assert real_album.path == album_dest
        assert real_album.path.exists()
        for copied_track in real_album.tracks:
            assert copied_track.path == move.fmt_item_path(
                copied_track, tmp_config_lib_path
            )
            assert copied_track.path.is_file()
        for copied_extra in real_album.extras:
            assert copied_extra.path == move.fmt_item_path(
                copied_extra, tmp_config_lib_path
            )
            assert copied_extra.path.is_file()
        for og_path in og_paths:
            assert og_path.exists()

    def test_copy_multi_disc_album(self, real_album, tmp_config_lib_path):
        """We can copy albums containing multiple discs.

        The album desination should be formatted according to `fmt_item_path()`.
        """
        album_dest = move.fmt_item_path(real_album, tmp_config_lib_path)
        assert real_album.path != album_dest

        real_album.tracks[1].disc = 2
        real_album.tracks[1].track_num = 1
        real_album.disc_total = 2

        og_paths = [track.path for track in real_album.tracks]
        og_paths += [extra.path for extra in real_album.extras]
        og_paths.append(real_album.path)

        move.copy_item(real_album, tmp_config_lib_path)

        assert real_album.path == album_dest
        assert real_album.path.exists()
        for copied_track in real_album.tracks:
            assert copied_track.path == move.fmt_item_path(
                copied_track, tmp_config_lib_path
            )
            assert copied_track.path.is_file()
        for copied_extra in real_album.extras:
            assert copied_extra.path == move.fmt_item_path(
                copied_extra, tmp_config_lib_path
            )
            assert copied_extra.path.is_file()
        for og_path in og_paths:
            assert og_path.exists()


class TestCopyExtra:
    """Tests `copy_item(extra)`."""

    def test_copy_extra(self, real_extra, tmp_config_lib_path):
        """We can copy an extra.

        The extra desination should be formatted according to `fmt_item_path()`.
        """
        # we need to set the album's path since extra paths are based off their albums
        real_extra.album_obj.path = move.fmt_item_path(
            real_extra.album_obj, tmp_config_lib_path
        )

        extra_dest = move.fmt_item_path(real_extra, tmp_config_lib_path)
        og_path = real_extra.path
        assert og_path != extra_dest

        move.copy_item(real_extra, tmp_config_lib_path)

        assert real_extra.path.exists()
        assert og_path.exists()
        assert og_path != real_extra.path
        assert real_extra.path == extra_dest


class TestCopyTrack:
    """Tests `copy_item(track)`."""

    def test_copy_track(self, real_track, tmp_config_lib_path):
        """We can copy a track.

        The track desination should be formatted according to `fmt_item_path()`.
        """
        # we need to set the album's path since track paths are based off their albums
        real_track.album_obj.path = move.fmt_item_path(
            real_track.album_obj, tmp_config_lib_path
        )

        track_dest = move.fmt_item_path(real_track, tmp_config_lib_path)
        og_path = real_track.path
        assert og_path != track_dest

        move.copy_item(real_track, tmp_config_lib_path)

        assert real_track.path.exists()
        assert og_path.exists()
        assert og_path != real_track.path
        assert real_track.path == track_dest


########################################################################################
# Test move
########################################################################################
class TestMoveAlbum:
    """Tests `move_item(album)`."""

    def test_move_album(self, real_album, tmp_config_lib_path):
        """We can move an album that was added to the library."""
        album_dest = move.fmt_item_path(real_album, tmp_config_lib_path)
        assert real_album.path != album_dest

        og_paths = [track.path for track in real_album.tracks]
        og_paths += [extra.path for extra in real_album.extras]
        og_paths.append(real_album.path)

        move.move_item(real_album, tmp_config_lib_path)

        assert real_album.path == album_dest
        assert real_album.path.exists()
        for copied_track in real_album.tracks:
            assert copied_track.path == move.fmt_item_path(
                copied_track, tmp_config_lib_path
            )
            assert copied_track.path.is_file()
        for copied_extra in real_album.extras:
            assert copied_extra.path == move.fmt_item_path(
                copied_extra, tmp_config_lib_path
            )
            assert copied_extra.path.is_file()
        for og_path in og_paths:
            assert not og_path.exists()

    def test_move_multi_disc_album(self, real_album, tmp_config_lib_path):
        """We can copy albums containing multiple discs."""
        album_dest = move.fmt_item_path(real_album, tmp_config_lib_path)
        assert real_album.path != album_dest

        real_album.tracks[1].disc = 2
        real_album.tracks[1].track_num = 1
        real_album.disc_total = 2

        og_paths = [track.path for track in real_album.tracks]
        og_paths += [extra.path for extra in real_album.extras]
        og_paths.append(real_album.path)

        move.move_item(real_album, tmp_config_lib_path)

        assert real_album.path == album_dest
        assert real_album.path.exists()
        for copied_track in real_album.tracks:
            assert copied_track.path == move.fmt_item_path(
                copied_track, tmp_config_lib_path
            )
            assert copied_track.path.is_file()
        for copied_extra in real_album.extras:
            assert copied_extra.path == move.fmt_item_path(
                copied_extra, tmp_config_lib_path
            )
            assert copied_extra.path.is_file()
        for og_path in og_paths:
            assert not og_path.exists()

    def test_rm_empty_leftover_dirs(self, real_album, tmp_config_lib_path):
        """Remove any leftover empty directories after a move."""
        real_album.disc_total = 2  # also remove empty child directories
        lib_path = tmp_config_lib_path.settings.move.library_path

        # first move the album to a nested sub directory
        nested_lib_path = lib_path + "/should/be/deleted"
        tmp_config_lib_path.settings.move.library_path = nested_lib_path
        move.move_item(real_album, tmp_config_lib_path)

        # now move the item to it's final directory
        tmp_config_lib_path.settings.move.library_path = lib_path
        move.move_item(real_album, tmp_config_lib_path)

        # all the original nestesd sub dirs of the first album path should be deleted
        nested_lib_path = Path(nested_lib_path)
        assert not nested_lib_path.exists()
        for parent in nested_lib_path.parents:
            if parent == Path(lib_path):
                break

            assert not parent.exists()


class TestMoveExtra:
    """Tests `move_item(extra)`."""

    def test_move_extra(self, real_extra, tmp_config_lib_path):
        """We can move an extra.

        The extra desination should be formatted according to `fmt_item_path()`.
        """
        # we need to set the album's path since extra paths are based off their albums
        real_extra.album_obj.path = move.fmt_item_path(
            real_extra.album_obj, tmp_config_lib_path
        )

        extra_dest = move.fmt_item_path(real_extra, tmp_config_lib_path)
        og_path = real_extra.path
        assert og_path != extra_dest

        move.move_item(real_extra, tmp_config_lib_path)

        assert real_extra.path.exists()
        assert not og_path.exists()
        assert og_path != real_extra.path
        assert real_extra.path == extra_dest


class TestMoveTrack:
    """Tests `move_item(track)`."""

    def test_move_track(self, real_track, tmp_config_lib_path):
        """We can move a track.

        The track desination should be formatted according to `fmt_item_path()`.
        """
        # we need to set the album's path since track paths are based off their albums
        real_track.album_obj.path = move.fmt_item_path(
            real_track.album_obj, tmp_config_lib_path
        )

        track_dest = move.fmt_item_path(real_track, tmp_config_lib_path)
        og_path = real_track.path
        assert og_path != track_dest

        move.move_item(real_track, tmp_config_lib_path)

        assert real_track.path.exists()
        assert not og_path.exists()
        assert og_path != real_track.path
        assert real_track.path == track_dest


class TestParseArgs:
    """Test the `move` command argument parser."""

    def test_dry_run(self, real_album, tmp_config_lib_path, tmp_session):
        """If `dry-run` is specified, don't actually move the items."""
        album_dest = move.fmt_item_path(real_album, tmp_config_lib_path)
        real_album = tmp_session.merge(real_album)

        args = argparse.Namespace(dry_run=True)
        move._parse_args(tmp_config_lib_path, tmp_session, args)
        tmp_session.commit()

        db_album = tmp_session.execute(sa.select(Album)).scalar_one()

        assert db_album.path != album_dest
        for track in db_album.tracks:
            assert album_dest not in track.path.parents
        for extra in db_album.extras:
            assert album_dest not in extra.path.parents


@pytest.mark.integration
class TestMoveCmd:
    """Test the `move` cli command."""

    def test_move(self, real_album_factory, tmp_config_lib_path):
        """Test all items in the library are moved when the command is invoked."""
        cli_args = ["move"]
        tmp_config_lib_path.init_db()

        album1 = real_album_factory()
        album2 = real_album_factory()

        with session_scope() as session:
            session.merge(album1)
            session.merge(album2)

        og_paths = [track.path for track in album1.tracks]
        og_paths += [extra.path for extra in album1.extras]
        og_paths.append(album1.path)
        og_paths = [track.path for track in album2.tracks]
        og_paths += [extra.path for extra in album2.extras]
        og_paths.append(album2.path)

        moe.cli.main(cli_args, tmp_config_lib_path)

        with session_scope() as new_session:
            albums = new_session.execute(sa.select(Album)).scalars().all()

            for album in albums:
                assert album.path == move.fmt_item_path(album, tmp_config_lib_path)
                assert album.path.exists()
                for track in album.tracks:
                    assert track.path == move.fmt_item_path(track, tmp_config_lib_path)
                    assert track.path.exists()
                for extra in album.extras:
                    assert extra.path == move.fmt_item_path(extra, tmp_config_lib_path)
                    assert extra.path.exists()

        for og_path in og_paths:
            assert not og_path.exists()


@pytest.mark.integration
class TestPreAdd:
    """Test integration with the `pre_add` hook entry to the plugin.

    By default, items are copied after they are added.
    """

    def test_add_album(self, real_album, tmp_config, tmp_path):
        """Albums are copied to `library_path` after they are added."""
        cli_args = ["add", str(real_album.path)]
        tmp_settings = f"""
        default_plugins = ["add", "move"]
        [move]
        library_path = '''{tmp_path.resolve()}'''
        """
        config = tmp_config(tmp_settings)
        album_dest = move.fmt_item_path(real_album, config)
        assert real_album.path != album_dest

        og_paths = [track.path for track in real_album.tracks]
        og_paths += [extra.path for extra in real_album.extras]
        og_paths.append(real_album.path)

        moe.cli.main(cli_args, config)

        with session_scope() as session:
            album = session.query(Album).one()

            assert album.path == album_dest
            assert album.path.exists()
            for new_track in album.tracks:
                assert new_track.path == move.fmt_item_path(new_track, config)
                assert new_track.path.exists()
            for new_extra in album.extras:
                assert new_extra.path == move.fmt_item_path(new_extra, config)
                assert new_extra.path.exists()

        for og_path in og_paths:
            assert og_path.exists()
