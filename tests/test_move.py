"""Tests the ``move`` plugin."""

import pathlib
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

            mock_copy_item.assert_called_once_with(
                mock_session,
                mock_track,
                pathlib.Path(config.settings.move.library_path),
            )


class TestCopy:
    """Tests ``_copy_item()``."""

    def test_copy_track(self, real_track, tmp_path):
        """Test we can copy a Track that was added to the library.

        The new track's path should refer to the destination i.e. only one copy of the
        item will remain in the library.
        """
        origin_track_path = real_track.path

        move._copy_item(session=Mock(), item=real_track, root=tmp_path)

        assert tmp_path in real_track.path.parents  # accounts for track path formatting
        assert origin_track_path.is_file()
        assert real_track.path.is_file()

    def test_copy_album(self, real_album, tmp_path):
        """Test we can copy an Album that was added to the library.

        Copying an album is just copying each item belonging to that album.
        """
        origin_track_paths = []
        for track in real_album.tracks:
            origin_track_paths.append(track.path)

        move._copy_item(session=Mock(), item=real_album, root=tmp_path)

        for copied_track in real_album.tracks:
            assert tmp_path in copied_track.path.parents
            assert copied_track.path.is_file()

        for origin_track_path in origin_track_paths:
            assert origin_track_path.is_file()

    def test_path_updated_in_db(self, real_track, tmp_path, tmp_session):
        """Make sure the path updates are being reflected in the db."""
        move._copy_item(session=tmp_session, item=real_track, root=tmp_path)

        db_track = tmp_session.query(Track).one()
        assert db_track.path == real_track.path

    def test_duplicate(self, real_track_factory, tmp_config, tmp_path, tmp_session):
        """Overwrite duplicate tracks that already exist in the db."""
        track1 = real_track_factory()
        track2 = real_track_factory()
        track1.genre = ["rap"]
        track2.genre = ["hip hop"]
        track2.track_num = track1.track_num

        move._copy_item(session=tmp_session, item=track1, root=tmp_path)
        move._copy_item(session=tmp_session, item=track2, root=tmp_path)

        db_track = tmp_session.query(Track).one()
        assert db_track.genre == track2.genre


@pytest.mark.integration
class TestAddEntry:
    """Test integration with the `add` command entry of `move`."""

    def test_add_track(self, tmp_config, tmp_path):
        """Tracks are copied to `library_path` after they are added."""
        args = ["moe", "add", "tests/resources/audio_files/full.mp3"]

        tmp_settings = f"""
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

    def test_add_album(self, tmp_config, tmp_path):
        """Albums are copied to `library_path` after they are added."""
        cli_args = ["moe", "add", "tests/resources/album/"]

        tmp_settings = f"""
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
                assert (
                    tmp_path in track.path.parents
                )  # accounts for track path formatting
