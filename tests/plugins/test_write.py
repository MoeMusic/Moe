"""Tests the ``write`` plugin."""

import datetime

import pytest

import moe
from moe.config import MoeSession
from moe.library.track import Track
from moe.plugins import write as moe_write


class TestWriteTags:
    """Tests `write_tags()`."""

    def test_write_tags(self, real_track):
        """We can write track changes to the file."""
        album = "Bigger, Better, Faster, More!"
        albumartist = "4 Non Blondes"
        artist = "4 Non Blondes"
        date = datetime.date(1996, 10, 13)
        disc = 2
        disc_total = 2
        mb_album_id = "123"
        mb_track_id = "1234"
        genres = ["alternative", "rock"]
        title = "What's Up"
        track_num = 3

        real_track.album = album
        real_track.albumartist = albumartist
        real_track.artist = artist
        real_track.date = date
        real_track.disc = disc
        real_track.disc_total = disc_total
        real_track.mb_album_id = mb_album_id
        real_track.mb_track_id = mb_track_id
        real_track.genres = genres
        real_track.title = title
        real_track.track_num = track_num

        moe_write.write_tags(real_track)

        new_track = Track.from_tags(path=real_track.path)
        assert new_track.album == album
        assert new_track.albumartist == albumartist
        assert new_track.artist == artist
        assert new_track.date == date
        assert new_track.disc == disc
        assert new_track.disc_total == disc_total
        assert set(new_track.genres) == set(genres)
        assert new_track.mb_album_id == mb_album_id
        assert new_track.mb_track_id == mb_track_id
        assert new_track.title == title
        assert new_track.track_num == track_num


@pytest.mark.integration
class TestDBListener:
    """Test integration with the `process_items` hook entry to the plugin."""

    def test_edit_track(self, real_track, tmp_config):
        """Any altered Tracks have their tags written."""
        new_title = "Summertime"
        cli_args = ["edit", "*", f"title={new_title}"]

        tmp_settings = """
        default_plugins = ["cli", "edit", "write"]
        """
        config = tmp_config(tmp_settings, init_db=True)
        og_path = real_track.path

        session = MoeSession()
        with session.begin():
            session.add(real_track)

        moe.cli.main(cli_args, config)

        new_track = Track.from_tags(og_path)
        assert new_track.title == new_title

    def test_write_through_flush(self, real_album, tmp_config):
        """If a flush occurs, ensure we still write all items that changed.

        A database "flush" will occur if querying, or if editing an association
        attribute. This test ensures we aren't just naively checking `session.dirty` to
        get a list of all edited items.
        """
        new_genre = "new genre"
        cli_args = ["edit", "*", f"genre={new_genre}"]

        tmp_settings = """
        default_plugins = ["cli", "edit", "write"]
        """
        config = tmp_config(tmp_settings, init_db=True)
        og_paths = [track.path for track in real_album.tracks]

        session = MoeSession()
        with session.begin():
            session.merge(real_album)

        moe.cli.main(cli_args, config)

        new_tracks = [Track.from_tags(path) for path in og_paths]
        for track in new_tracks:
            assert track.genre == new_genre
