"""Tests the ``move`` plugin."""

import argparse
from unittest.mock import patch

import pytest
import sqlalchemy as sa

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

    def test_copy_extra(self, real_extra, tmp_path):
        """We can copy an extra."""
        og_path = real_extra.path
        dest = tmp_path / real_extra.path.name
        assert og_path != dest

        move._copy_extra(real_extra, dest)

        assert og_path.exists()
        assert real_extra.path.exists()
        assert og_path != real_extra.path
        assert real_extra.path == dest


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

    def test_rm_empty_leftover_dirs(self, real_album, tmp_config, tmp_path):
        """Remove any leftover empty directories after a move."""
        nested_album_dir = tmp_path / "should" / "be" / "removed"
        real_album.disc_total = 2  # also remove empty child directories

        move._move_album(real_album, nested_album_dir, tmp_config())
        move._move_album(real_album, tmp_path, tmp_config())

        for parent in nested_album_dir.parents:
            if tmp_path in parent.parents and parent != tmp_path:
                assert not parent.exists()


class TestMoveTrack:
    """Tests ``_move_track()``."""

    def test_move_track(self, real_track, tmp_path):
        """We can move a track."""
        og_path = real_track.path
        dest = tmp_path / real_track.path.name
        assert og_path != dest

        move._move_track(real_track, dest)

        assert not og_path.exists()
        assert real_track.path.exists()
        assert og_path != real_track.path
        assert real_track.path == dest


class TestMoveExtra:
    """Tests ``_move_extra()``."""

    def test_move_extra(self, real_extra, tmp_path):
        """We can move an extra."""
        og_path = real_extra.path
        dest = tmp_path / real_extra.path.name
        assert og_path != dest

        move._move_extra(real_extra, dest)

        assert not og_path.exists()
        assert real_extra.path.exists()
        assert og_path != real_extra.path
        assert real_extra.path == dest


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

        with pytest.raises(sa.exc.IntegrityError):
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


class TestMoveCmd:
    """Test the ``move`` cli command."""

    @pytest.mark.integration
    def test_move(self, real_album_factory, tmp_config, tmp_path):
        """Test all items in the library are moved when the command is invoked."""
        cli_args = ["move"]
        tmp_settings = f"""
        default_plugins = ["move"]
        [move]
        library_path = '''{tmp_path.resolve()}'''
        """
        config = tmp_config(tmp_settings)
        config.init_db()

        album1 = real_album_factory()
        album2 = real_album_factory()

        with session_scope() as session:
            session.merge(album1)
            session.merge(album2)

        moe.cli.main(cli_args, config)

        with session_scope() as new_session:
            with new_session.no_autoflush:
                albums = new_session.execute(sa.select(Album)).scalars().all()

                for album in albums:
                    assert tmp_path in album.path.parents

                    for track in album.tracks:
                        assert tmp_path in track.path.parents

                    for extra in album.extras:
                        assert tmp_path in extra.path.parents

    def test_dry_run(self, real_album, tmp_config, tmp_path, tmp_session):
        """If `dry-run` is specified, don't actually move the items."""
        tmp_settings = f"""
        default_plugins = ["move"]
        [move]
        library_path = '''{tmp_path.resolve()}'''
        """
        real_album = tmp_session.merge(real_album)

        args = argparse.Namespace(dry_run=True)
        move._parse_args(tmp_config(tmp_settings), tmp_session, args)
        tmp_session.commit()

        db_album = tmp_session.execute(sa.select(Album)).scalar()

        assert tmp_path not in db_album.path.parents
        for track in db_album.tracks:
            assert tmp_path not in track.path.parents
        for extra in db_album.extras:
            assert tmp_path not in extra.path.parents
