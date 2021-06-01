"""Tests the ``move`` plugin."""

import os
import pathlib
from unittest.mock import Mock, patch

import pytest

from moe import cli
from moe.core.library.session import session_scope
from moe.core.library.track import Album, Track
from moe.plugins import move


class TestPostAdd:
    """Test functionality of the post-add hook."""

    def test_copy_track(self, real_track, tmp_config, tmp_path):
        """Test we can copy a Track that was added to the library.

        The track's path should refer to the destination.
        """
        config = tmp_config(f"library_path = '''{tmp_path.resolve()}'''")
        origin_track_path = real_track.path

        move.post_add(config=config, session=Mock(), item=real_track)

        assert tmp_path in real_track.path.parents  # accounts for track path formatting
        assert origin_track_path.is_file()
        assert real_track.path.is_file()

    def test_copy_album(self, real_album, tmp_config, tmp_path):
        """Test we can copy an Album that was added to the library.

        Copying an album is just copying each item belonging to that album.
        """
        config = tmp_config(f"library_path = '''{tmp_path.resolve()}'''")
        for track in real_album.tracks:
            origin_track_paths = []
            origin_track_paths.append(track.path)

        move.post_add(config=config, session=Mock(), item=real_album)

        for copied_track in real_album.tracks:
            assert tmp_path in copied_track.path.parents
            assert copied_track.path.is_file()

        for origin_track_path in origin_track_paths:
            assert origin_track_path.is_file()

    def test_home_dir(self, mock_track, tmp_config, tmp_path):
        """Home directories are allowed to be shortened with '~' in the config."""
        config = tmp_config("library_path = '''~'''")

        move.post_add(config=config, session=Mock(), item=mock_track)

        assert pathlib.Path.home() in mock_track.path.parents

    def test_path_updated_in_db(self, real_track, tmp_config, tmp_path, tmp_session):
        """Make sure the path updates are being reflected in the DB."""
        config = tmp_config(f"library_path = '''{tmp_path.resolve()}'''")
        move.post_add(config=config, session=tmp_session, item=real_track)

        db_track = tmp_session.query(Track).one()
        assert db_track.path == real_track.path

    def test_duplicate(self, real_track_factory, tmp_config, tmp_path, tmp_session):
        """Overwrite duplicate tracks that already exist in the db."""
        track1 = real_track_factory()
        track2 = real_track_factory()
        track1.genre = ["rap"]
        track2.genre = ["hip hop"]
        track2.track_num = track1.track_num
        config = tmp_config(f"library_path = '''{tmp_path.resolve()}'''")

        move.post_add(config=config, session=tmp_session, item=track1)
        move.post_add(config=config, session=tmp_session, item=track2)

        db_track = tmp_session.query(Track).one()
        assert db_track.genre == track2.genre


@pytest.mark.integration
class TestAddEntry:
    """Test integration with the `add` command entry of `move`."""

    def test_move_track(self, tmp_config, tmp_path):
        """Tracks are copied to `library_path` after they are added."""
        args = ["moe", "add", "tests/resources/audio_files/full.mp3"]
        library_path = tmp_path / "Music"
        os.environ["MOE_CONFIG_DIR"] = str(tmp_path)
        os.environ["MOE_LIBRARY_PATH"] = str(library_path)
        os.environ["MOE_DEFAULT_PLUGINS"] = '["add", "move"]'

        with patch("sys.argv", args):
            cli.main()

        with session_scope() as session:
            track = session.query(Track).one()
            assert (
                library_path in track.path.parents
            )  # accounts for track path formatting

    def test_move_album(self, tmp_path):
        """Albums are copied to `library_path` after they are added."""
        cli_args = ["moe", "add", "tests/resources/album/"]
        library_path = tmp_path / "Music"
        os.environ["MOE_CONFIG_DIR"] = str(tmp_path)
        os.environ["MOE_LIBRARY_PATH"] = str(library_path)
        os.environ["MOE_DEFAULT_PLUGINS"] = '["add", "move"]'

        with patch("sys.argv", cli_args):
            cli.main()

        with session_scope() as session:
            album = session.query(Album).one()
            for track in album.tracks:
                assert (
                    library_path in track.path.parents
                )  # accounts for track path formatting
