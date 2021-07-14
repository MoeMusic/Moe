"""Tests the ``move`` plugin."""

from unittest.mock import patch

import pytest
import sqlalchemy

import moe
from moe.core.library.album import Album
from moe.core.library.session import session_scope
from moe.core.library.track import Track
from moe.plugins import move


class TestCopyAlbum:
    """Tests ``_copy_album()``."""

    def test_copy_album(self, real_album, tmp_config, tmp_path):
        """We can copy an album that was added to the library."""
        og_paths = [track.path for track in real_album.tracks]
        og_paths += [extra.path for extra in real_album.extras]
        og_paths.append(real_album.path)
        for og_track in real_album.tracks:
            assert tmp_path not in og_track.path.parents
        for og_extra in real_album.extras:
            assert tmp_path not in og_extra.path.parents

        move._copy_album(real_album, tmp_path, tmp_config())

        for copied_track in real_album.tracks:
            assert tmp_path in copied_track.path.parents
            assert copied_track.path.is_file()
        for copied_extra in real_album.extras:
            assert tmp_path in copied_extra.path.parents
            assert copied_extra.path.is_file()
        for og_path in og_paths:
            assert og_path.exists()

    def test_copy_multi_disc_album(self, real_album, tmp_config, tmp_path):
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

        move._copy_album(real_album, tmp_path, tmp_config())

        for copied_track in real_album.tracks:
            assert tmp_path in copied_track.path.parents
            assert copied_track.path.is_file()
        for copied_extra in real_album.extras:
            assert tmp_path in copied_extra.path.parents
            assert copied_extra.path.is_file()
        for og_path in og_paths:
            assert og_path.exists()

    def test_file_src_eq_dst(self, real_album, tmp_config, tmp_path):
        """Do nothing if the Track or Extra destination is the same as the source."""
        move._copy_album(real_album, tmp_path, tmp_config())

        with patch("shutil.copyfile") as mock_copy:
            move._copy_album(real_album, tmp_path, tmp_config())

        assert not mock_copy.called


class TestCopyTrack:
    """Tests ``_copy_track()``."""

    def test_copy_track(self, real_track, tmp_path):
        """We can copy a track."""
        og_path = real_track.path
        dest = tmp_path / real_track.path.name
        assert og_path != dest

        move._copy_track(real_track, dest)

        assert og_path.exists()
        assert real_track.path.exists()
        assert og_path != real_track.path
        assert real_track.path == dest


class TestCopyExtra:
    """Tests ``_copy_extra()``."""

    def test_copy_extra(self, real_track, tmp_path):
        """We can copy an extra."""
        og_path = real_track.path
        dest = tmp_path / real_track.path.name
        assert og_path != dest

        move._copy_track(real_track, dest)

        assert og_path.exists()
        assert real_track.path.exists()
        assert og_path != real_track.path
        assert real_track.path == dest


class TestMoveAlbum:
    """Tests ``_move_album()``."""

    def test_move_album(self, real_album, tmp_config, tmp_path):
        """We can move an album that was added to the library."""
        og_paths = [track.path for track in real_album.tracks]
        og_paths += [extra.path for extra in real_album.extras]
        og_paths.append(real_album.path)
        for og_track in real_album.tracks:
            assert tmp_path not in og_track.path.parents
        for og_extra in real_album.extras:
            assert tmp_path not in og_extra.path.parents

        move._move_album(real_album, tmp_path, tmp_config())

        for copied_track in real_album.tracks:
            assert tmp_path in copied_track.path.parents
            assert copied_track.path.is_file()
        for copied_extra in real_album.extras:
            assert tmp_path in copied_extra.path.parents
            assert copied_extra.path.is_file()
        for og_path in og_paths:
            assert not og_path.exists()

    def test_move_multi_disc_album(self, real_album, tmp_config, tmp_path):
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

        move._move_album(real_album, tmp_path, tmp_config())

        for copied_track in real_album.tracks:
            assert tmp_path in copied_track.path.parents
            assert copied_track.path.is_file()
        for copied_extra in real_album.extras:
            assert tmp_path in copied_extra.path.parents
            assert copied_extra.path.is_file()
        for og_path in og_paths:
            assert not og_path.exists()

    def test_file_src_eq_dst(self, real_album, tmp_config, tmp_path):
        """Do nothing if the Track or Extra destination is the same as the source."""
        move._move_album(real_album, tmp_path, tmp_config())

        with patch("shutil.move") as mock_copy:
            move._move_album(real_album, tmp_path, tmp_config())

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

            assert tmp_path in album.path.parents
            assert album.path.exists()
            for new_track in album.tracks:
                assert tmp_path in new_track.path.parents
                assert new_track.path.exists()
            for new_extra in album.extras:
                assert tmp_path in new_extra.path.parents
                assert new_extra.path.exists()

        for og_path in og_paths:
            assert og_path.exists()


@pytest.mark.integration
class TestDBListener:
    """Test registered database listeners.

    Items are moved before they are flushed to the database.
    """

    def test_edit_album(self, real_album, tmp_config, tmp_path):
        """Albums are moved to `library_path` after they are edited."""
        cli_args = ["edit", "-a", "*", "title=whatever"]
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

            assert album.path.exists()
            for new_track in album.tracks:
                assert tmp_path in new_track.path.parents
                assert new_track.path.exists()
            for new_extra in album.extras:
                assert tmp_path in new_extra.path.parents
                assert new_extra.path.exists()

        for og_path in og_paths:
            assert not og_path.exists()

    def test_edit_track(self, real_track, tmp_config):
        """Tracks are moved after they are edited."""
        new_title = "whatever"
        cli_args = ["edit", "*", f"title={new_title}"]
        tmp_settings = """
        default_plugins = ["edit", "move"]
        """
        config = tmp_config(tmp_settings)
        config.init_db()

        og_path = real_track.path

        with session_scope() as pre_edit_session:
            pre_edit_session.merge(real_track)

        moe.cli.main(cli_args, config)

        with session_scope() as session:
            track = session.query(Track).one()

            assert track.path.exists()
            assert new_title in track.path.name

        assert not og_path.exists()

    def test_db_error(self, real_album, tmp_config, tmp_path):
        """Don't move the item if it isn't added to the database due to an error."""
        cli_args = ["edit", "*", "track_num=1"]  # dup track_nums will cause a rollback
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

        with pytest.raises(sqlalchemy.exc.IntegrityError):
            moe.cli.main(cli_args, config)

        with session_scope() as session:
            album = session.query(Album).one()

            for new_track in album.tracks:
                assert new_track.path in og_paths  # path not updated in db
                assert new_track.path.exists()  # old path still exists
            for new_extra in album.extras:
                assert new_extra.path in og_paths  # path not updated in db
                assert new_extra.path.exists()  # old path still exists


class TestItemPaths:
    """Test various configuration options with creating item paths."""

    def test_asciify_paths(self, real_album, tmp_config):
        """Paths should not contain unicode characters if `asciify_paths` is true."""
        tmp_settings = """
        default_plugins = ["move"]
        [move]
        asciify_paths = true
        """
        config = tmp_config(tmp_settings)
        non_ascii_title = "café"

        real_album.title = non_ascii_title
        str(move._fmt_album_path(real_album, config))

        for track in real_album.tracks:
            track.title = non_ascii_title
            str(move._fmt_track_path(track, config))
        for extra in real_album.extras:
            extra.path = extra.path.parent / f"{non_ascii_title}"
            str(move._fmt_extra_path(extra, config))
