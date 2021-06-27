"""Tests the ``write`` plugin."""

import datetime

import pytest

import moe
from moe.core.library.session import session_scope
from moe.core.library.track import Track
from moe.plugins import write as moe_write


class TestWriteTags:
    """Tests the ability to write tags to a track file."""

    def test_write_tags(self, real_track):
        """We can write track changes to the file."""
        real_track.album = "Bigger, Better, Faster, More!"
        real_track.albumartist = "4 Non Blondes"
        real_track.artist = "4 Non Blondes"
        real_track.mb_album_id = "123"
        real_track.mb_id = "1234"
        real_track.genre = {"alternative", "rock"}
        real_track.title = "What's Up"
        real_track.track_num = 3
        real_track.date = datetime.date(1992, 1, 1)

        moe_write._write_tags(real_track)

        new_track = Track.from_tags(path=real_track.path)
        assert new_track.album == "Bigger, Better, Faster, More!"
        assert new_track.albumartist == "4 Non Blondes"
        assert new_track.artist == "4 Non Blondes"
        assert set(new_track.genre) == {"alternative", "rock"}
        assert new_track.mb_album_id == "123"
        assert new_track.mb_id == "1234"
        assert new_track.title == "What's Up"
        assert new_track.track_num == 3
        assert new_track.date == datetime.date(1992, 1, 1)


@pytest.mark.integration
class TestPostArgs:
    """Test integration with the ``post_args`` hook entry to the plugin."""

    def test_edit_track(self, real_track, tmp_config):
        """Any altered Tracks have their tags written."""
        new_title = "Summertime"
        cli_args = ["edit", "*", f"title={new_title}"]

        tmp_settings = """
        default_plugins = ["edit", "write"]
        """
        config = tmp_config(tmp_settings)
        config.init_db()
        with session_scope() as session:
            session.add(real_track)

        moe.cli.main(cli_args, config)

        with session_scope() as post_session:
            track = post_session.query(Track).one()
            assert track.title == new_title
