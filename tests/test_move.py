"""Tests the ``move`` plugin."""

from unittest.mock import Mock, patch

import pytest

from moe import cli
from moe.core.library.session import session_scope
from moe.core.library.track import Album, Track
from moe.plugins import move


class TestPostAdd:
    """Test functionality of the post-add hook."""

    def test_default_copy(self, mock_track, tmp_config):
        """Items are copied by default."""
        mock_session = Mock()
        config = tmp_config()
        with patch("moe.plugins.move._copy_item") as mock_copy_item:
            move.post_add(config=config, session=mock_session, item=mock_track)

            mock_copy_item.assert_called_once()

    def test_path_updated_in_db(self, real_track, tmp_config, tmp_path, tmp_session):
        """Make sure the path updates are being reflected in the db."""
        tmp_settings = f"""
        [move]
        library_path = '''{tmp_path.resolve()}'''
        """
        move.post_add(
            config=tmp_config(tmp_settings), session=tmp_session, item=real_track
        )

        db_track = tmp_session.query(Track).one()
        assert db_track.path == real_track.path

    def test_duplicate(self, real_track_factory, tmp_config, tmp_path, tmp_session):
        """Overwrite duplicate tracks that already exist in the db."""
        tmp_settings = f"""
        [move]
        library_path = '''{tmp_path.resolve()}'''
        """
        config = tmp_config(tmp_settings)
        track1 = real_track_factory()
        track2 = real_track_factory()
        track1.genre = ["rap"]
        track2.genre = ["hip hop"]
        track2.track_num = track1.track_num

        move.post_add(config, session=tmp_session, item=track1)
        move.post_add(config, session=tmp_session, item=track2)

        db_track = tmp_session.query(Track).one()
        assert db_track.genre == track2.genre


class TestCopy:
    """Tests ``_copy_item()``."""

    def test_copy_track(self, real_track, tmp_path):
        """Test we can copy a Track that was added to the library.

        The new track's path should refer to the destination i.e. only one copy of the
        item will remain in the library.
        """
        origin_track_path = real_track.path

        move._copy_item(item=real_track, album_dir=tmp_path)

        assert tmp_path / real_track.filename == real_track.path
        assert origin_track_path.is_file()
        assert real_track.path.is_file()

    def test_copy_album(self, real_album, tmp_path):
        """Test we can copy an Album that was added to the library.

        Copying an album is just copying each item belonging to that album.
        """
        origin_track_paths = []
        for track in real_album.tracks:
            origin_track_paths.append(track.path)

        move._copy_item(item=real_album, album_dir=tmp_path)

        for copied_track in real_album.tracks:
            assert tmp_path / copied_track.filename == copied_track.path
            assert copied_track.path.is_file()

        for origin_track_path in origin_track_paths:
            assert origin_track_path.is_file()

    def test_file_src_eq_dst(self, real_album, tmp_path):
        """Do nothing if the Track or Extra destination is the same as the source."""
        move._copy_item(item=real_album, album_dir=tmp_path)
        move._copy_item(item=real_album, album_dir=tmp_path)


@pytest.mark.integration
class TestAddEntry:
    """Test integration with the `add` command entry of `move`."""

    def test_add_track(self, real_track, tmp_config, tmp_path):
        """Tracks are copied to `library_path` after they are added."""
        args = ["moe", "add", str(real_track.path)]

        tmp_settings = f"""
        default_plugins = ["add", "move"]
        [move]
        library_path = '''{tmp_path.resolve()}'''
        """
        config = tmp_config(tmp_settings)
        with patch("sys.argv", args):
            with patch("moe.cli.Config", return_value=config):
                cli.main()

        with session_scope() as session:
            track = session.query(Track).one()
            assert tmp_path in track.path.parents  # accounts for track path formatting

    def test_add_album(self, real_album, tmp_config, tmp_path):
        """Albums are copied to `library_path` after they are added."""
        cli_args = ["moe", "add", str(real_album.path)]

        tmp_settings = f"""
        default_plugins = ["add", "move"]
        [move]
        library_path = '''{tmp_path.resolve()}'''
        """
        config = tmp_config(tmp_settings)
        with patch("sys.argv", cli_args):
            with patch("moe.cli.Config", return_value=config):
                cli.main()

        with session_scope() as session:
            album = session.query(Album).one()
            for track in album.tracks:
                assert tmp_path / album.path / track.filename == track.path

            for extra in album.extras:
                assert tmp_path / album.path / extra.filename == extra.path
