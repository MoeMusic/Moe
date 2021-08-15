"""Tests the ``move`` plugin."""

import argparse

import pytest
import sqlalchemy as sa

import moe
from moe.config import MoeSession
from moe.library.album import Album
from moe.plugins import move as moe_move


@pytest.fixture(scope="function")
def tmp_config_lib_path(tmp_config, tmp_path):
    """Creates a configuration with a temporary library path."""
    tmp_settings = f"""
    default_plugins = ["cli", "move"]
    [move]
    library_path = '''{tmp_path.resolve()}'''
    """
    return tmp_config(tmp_settings)


class TestParseArgs:
    """Test the `move` command argument parser."""

    def test_dry_run(self, real_album, tmp_config_lib_path, tmp_config):
        """If `dry-run` is specified, don't actually move the items."""
        tmp_config(tmp_db=True)
        session = MoeSession()
        with session.begin():
            album_dest = moe_move.fmt_item_path(real_album, tmp_config_lib_path)
            real_album = session.merge(real_album)
        MoeSession.remove()

        args = argparse.Namespace(dry_run=True)
        moe_move.move_cli._parse_args(tmp_config_lib_path, args)

        with session.begin():
            db_album = session.execute(sa.select(Album)).scalar_one()

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
        tmp_config_lib_path._init_db()
        session = MoeSession()

        album1 = real_album_factory()
        album2 = real_album_factory()

        with session.begin():
            session.merge(album1)
            session.merge(album2)

        og_paths = [track.path for track in album1.tracks]
        og_paths += [extra.path for extra in album1.extras]
        og_paths.append(album1.path)
        og_paths = [track.path for track in album2.tracks]
        og_paths += [extra.path for extra in album2.extras]
        og_paths.append(album2.path)

        moe.cli.main(cli_args, tmp_config_lib_path)

        with session.begin():
            albums = session.execute(sa.select(Album)).scalars().all()

            for album in albums:
                assert album.path == moe_move.fmt_item_path(album, tmp_config_lib_path)
                assert album.path.exists()
                for track in album.tracks:
                    assert track.path == moe_move.fmt_item_path(
                        track, tmp_config_lib_path
                    )
                    assert track.path.exists()
                for extra in album.extras:
                    assert extra.path == moe_move.fmt_item_path(
                        extra, tmp_config_lib_path
                    )
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
        default_plugins = ["add", "cli", "move"]
        [move]
        library_path = '''{tmp_path.resolve()}'''
        """
        config = tmp_config(tmp_settings, init_db=True)
        album_dest = moe_move.fmt_item_path(real_album, config)
        assert real_album.path != album_dest

        og_paths = [track.path for track in real_album.tracks]
        og_paths += [extra.path for extra in real_album.extras]
        og_paths.append(real_album.path)

        moe.cli.main(cli_args, config)

        session = MoeSession()
        with session.begin():
            album = session.query(Album).one()

            assert album.path == album_dest
            assert album.path.exists()
            for new_track in album.tracks:
                assert new_track.path == moe_move.fmt_item_path(new_track, config)
                assert new_track.path.exists()
            for new_extra in album.extras:
                assert new_extra.path == moe_move.fmt_item_path(new_extra, config)
                assert new_extra.path.exists()

        for og_path in og_paths:
            assert og_path.exists()
