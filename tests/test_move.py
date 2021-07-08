"""Tests the ``move`` plugin."""

from unittest.mock import patch

import pytest

import moe
from moe.core.library.session import session_scope
from moe.core.library.track import Album
from moe.plugins import move


class TestCopyAlbum:
    """Tests ``_copy_album()``."""

    def test_copy_album(self, real_album, tmp_path):
        """We can copy an album that was added to the library."""
        og_paths = [track.path for track in real_album.tracks]
        og_paths += [extra.path for extra in real_album.extras]
        og_paths.append(real_album.path)
        for og_track in real_album.tracks:
            assert tmp_path not in og_track.path.parents
        for og_extra in real_album.extras:
            assert tmp_path not in og_extra.path.parents

        move._copy_album(real_album, tmp_path)

        for copied_track in real_album.tracks:
            assert tmp_path in copied_track.path.parents
            assert copied_track.path.is_file()
        for copied_extra in real_album.extras:
            assert tmp_path in copied_extra.path.parents
            assert copied_extra.path.is_file()
        for og_path in og_paths:
            assert og_path.exists()

    def test_copy_multi_disc_album(self, real_album, tmp_path):
        """We can copy albums containing multiple discs."""
        real_album.tracks[1].disc = 2
        real_album.tracks[1].track_num = 1
        real_album.disc_total = 2

        og_paths = [track.path for track in real_album.tracks]
        og_paths += [extra.path for extra in real_album.extras]
        og_paths.append(real_album.path)
        for og_track in real_album.tracks:
            assert tmp_path not in og_track.path.parents
        for og_extra in real_album.extras:
            assert tmp_path not in og_extra.path.parents

        move._copy_album(real_album, tmp_path)

        for copied_track in real_album.tracks:
            assert tmp_path in copied_track.path.parents
            assert copied_track.path.is_file()
        for copied_extra in real_album.extras:
            assert tmp_path in copied_extra.path.parents
            assert copied_extra.path.is_file()
        for og_path in og_paths:
            assert og_path.exists()

    def test_file_src_eq_dst(self, real_album, tmp_path):
        """Do nothing if the Track or Extra destination is the same as the source."""
        move._copy_album(real_album, tmp_path)

        with patch("shutil.copyfile") as mock_copy:
            move._copy_album(real_album, tmp_path)

        assert not mock_copy.called


class TestMoveAlbum:
    """Tests ``_move_album()``."""

    def test_move_album(self, real_album, tmp_path):
        """We can move an album that was added to the library."""
        og_paths = [track.path for track in real_album.tracks]
        og_paths += [extra.path for extra in real_album.extras]
        og_paths.append(real_album.path)
        for og_track in real_album.tracks:
            assert tmp_path not in og_track.path.parents
        for og_extra in real_album.extras:
            assert tmp_path not in og_extra.path.parents

        move._move_album(real_album, tmp_path)

        for copied_track in real_album.tracks:
            assert tmp_path in copied_track.path.parents
            assert copied_track.path.is_file()
        for copied_extra in real_album.extras:
            assert tmp_path in copied_extra.path.parents
            assert copied_extra.path.is_file()
        for og_path in og_paths:
            assert not og_path.exists()

    def test_move_multi_disc_album(self, real_album, tmp_path):
        """We can copy albums containing multiple discs."""
        real_album.tracks[1].disc = 2
        real_album.tracks[1].track_num = 1
        real_album.disc_total = 2

        og_paths = [track.path for track in real_album.tracks]
        og_paths += [extra.path for extra in real_album.extras]
        og_paths.append(real_album.path)
        for og_track in real_album.tracks:
            assert tmp_path not in og_track.path.parents
        for og_extra in real_album.extras:
            assert tmp_path not in og_extra.path.parents

        move._move_album(real_album, tmp_path)

        for copied_track in real_album.tracks:
            assert tmp_path in copied_track.path.parents
            assert copied_track.path.is_file()
        for copied_extra in real_album.extras:
            assert tmp_path in copied_extra.path.parents
            assert copied_extra.path.is_file()
        for og_path in og_paths:
            assert not og_path.exists()

    def test_file_src_eq_dst(self, real_album, tmp_path):
        """Do nothing if the Track or Extra destination is the same as the source."""
        move._move_album(real_album, tmp_path)

        with patch("shutil.move") as mock_copy:
            move._move_album(real_album, tmp_path)

        assert not mock_copy.called


@pytest.mark.integration
class TestPreAdd:
    """Test integration with the ``pre_add`` hook entry to the plugin.

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

        og_paths = [track.path for track in real_album.tracks]
        og_paths += [extra.path for extra in real_album.extras]
        og_paths.append(real_album.path)
        for track in real_album.tracks:
            assert tmp_path not in track.path.parents
        for extra in real_album.extras:
            assert tmp_path not in extra.path.parents

        moe.cli.main(cli_args, config)

        with session_scope() as session:
            album = session.query(Album).one()

            for new_track in album.tracks:
                assert tmp_path in new_track.path.parents
            for new_extra in album.extras:
                assert tmp_path in new_extra.path.parents

        for og_path in og_paths:
            assert og_path.exists()


@pytest.mark.integration
class TestPostArgs:
    """Test integration with the ``post_args`` hook entry to the plugin."""

    def test_edit_album(self, real_album, tmp_config, tmp_path):
        """Albums are moved to `library_path` after they are edited."""
        cli_args = ["edit", "*", "album=whatever"]
        tmp_settings = f"""
        default_plugins = ["edit", "move"]
        [move]
        library_path = '''{tmp_path.resolve()}'''
        """
        config = tmp_config(tmp_settings)
        config.init_db()

        og_paths = [track.path for track in real_album.tracks]
        og_paths += [extra.path for extra in real_album.extras]
        og_paths.append(real_album.path)
        for track in real_album.tracks:
            assert tmp_path not in track.path.parents
        for extra in real_album.extras:
            assert tmp_path not in extra.path.parents

        with session_scope() as pre_edit_session:
            pre_edit_session.merge(real_album)

        moe.cli.main(cli_args, config)

        with session_scope() as session:
            album = session.query(Album).one()

            for new_track in album.tracks:
                assert tmp_path in new_track.path.parents
            for new_extra in album.extras:
                assert tmp_path in new_extra.path.parents

        for og_path in og_paths:
            assert not og_path.exists()
