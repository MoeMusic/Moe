"""Tests a Track object."""

import datetime
from unittest.mock import MagicMock

import pytest

import moe
import moe.plugins.write as moe_write
from moe.config import ExtraPlugin
from moe.library.track import Track, TrackError
from moe.plugins.write import write_tags


class MyTrackPlugin:
    """Plugin that implements the extra hooks for testing."""

    @staticmethod
    @moe.hookimpl
    def create_custom_track_fields(config):
        """Create a new custom field."""
        return {"no_default": None, "default": "value"}


class TestHooks:
    """Test track hooks."""

    def test_create_custom_fields(self, track_factory, tmp_config):
        """Plugins can define new custom fields."""
        config = tmp_config(extra_plugins=[ExtraPlugin(MyTrackPlugin, "track_plugin")])
        track = track_factory(config)

        assert not track.no_default
        assert track.default == "value"


class TestInit:
    """Test Track initialization."""

    def test_album_init(self, mock_track):
        """Creating a Track should also create the corresponding Album."""
        assert mock_track.album_obj

    def test_guess_disc_multi_disc(self, album_factory):
        """Guess the disc if not given."""
        album = album_factory(num_discs=3, exists=True)
        track1 = album.get_track(1, disc=1)
        track2 = album.get_track(1, disc=2)
        track3 = album.get_track(1, disc=3)

        new_track1 = Track(
            MagicMock(), album, track1.path, track1.title, track1.track_num
        )
        new_track2 = Track(
            MagicMock(), album, track2.path, track2.title, track2.track_num
        )
        new_track3 = Track(
            MagicMock(), album, track3.path, track3.title, track3.track_num
        )

        assert new_track1.disc == 1
        assert new_track2.disc == 2
        assert new_track3.disc == 3

    def test_guess_disc_single_disc(self, real_track):
        """Guess the disc if there are no disc sub directories."""
        assert real_track.path.parent == real_track.album_obj.path

        new_track = Track(
            MagicMock(),
            real_track.album_obj,
            real_track.path,
            real_track.title,
            real_track.track_num,
        )

        assert new_track.disc == 1


class TestAlbumSet:
    """Changing an album attribute will change the value for the current Album.

    Thus, all tracks in the album will reflect the new value.
    """

    def test_album_set(self, mock_track, tmp_path):
        """Setting an album attribute maintains the same album object."""
        album1 = mock_track.album_obj
        mock_track.album = "TPAB"
        mock_track.album_path = tmp_path
        mock_track.albumartist = "Kendrick Lamar"
        mock_track.date = datetime.date(2015, 3, 15)

        assert album1 is mock_track.album_obj


class TestFromFile:
    """Test initialization from given file path."""

    def test_read_tags(self, real_track):
        """We can initialize a track with tags from a file if present."""
        real_track.album = "The Lost Album"
        real_track.albumartist = "Wu-Tang Clan"
        real_track.artist = "Wu-Tang Clan"
        real_track.date = datetime.date(2020, 1, 12)
        real_track.disc = 1
        real_track.disc_total = 2
        real_track.genres = {"hip hop", "rock"}
        real_track.title = "Full"
        real_track.track_num = 1
        write_tags(real_track)

        new_track = Track.from_file(MagicMock(), real_track.path)

        assert new_track.album == real_track.album
        assert new_track.albumartist == real_track.albumartist
        assert new_track.artist == real_track.artist
        assert new_track.date == real_track.date
        assert new_track.disc == real_track.disc
        assert new_track.disc_total == real_track.disc_total
        assert new_track.genres == real_track.genres
        assert new_track.title == real_track.title
        assert new_track.track_num == real_track.track_num

    def test_non_track_file(self, real_extra):
        """Raise `TrackError` if the given path does not correspond to a track file."""
        with pytest.raises(TrackError):
            Track.from_file(MagicMock(), real_extra.path)

    def test_albumartist_backup(self, real_track):
        """Use artist as a backup for albumartist if missing."""
        real_track.albumartist = ""
        real_track.artist = "Backup"
        moe_write.write_tags(real_track)

        track = Track.from_file(MagicMock(), real_track.path)
        assert track.albumartist


class TestEquality:
    """Test equality of tracks."""

    def test_equals(self, track_factory):
        """Tracks with the same metadata are equal."""
        track1 = track_factory(custom="custom")
        track2 = track_factory(dup_track=track1)

        assert track1 == track2

    def test_not_equals(self, track_factory):
        """Tracks with different fields are not equal."""
        track1 = track_factory(title="track1")
        track2 = track_factory(title="track2")

        assert track1 != track2

    def test_not_equals_not_track(self, real_track):
        """Not equal if not comparing two tracks."""
        assert real_track != "test"


class TestMerge:
    """Test merging two tracks."""

    def test_conflict_persists(self, track_factory):
        """Don't overwrite any conflicts."""
        track = track_factory()
        other_track = track_factory()

        track.title = "keep"
        other_track.title = "discard"

        track.merge(other_track)

        assert track.title == "keep"

    def test_merge_non_conflict(self, track_factory):
        """Apply any non-conflicting fields."""
        track = track_factory()
        other_track = track_factory()

        track.title = None
        track.genres = []
        other_track.title = "keep"
        other_track.genres = ["keep"]

        track.merge(other_track)

        assert track.title == "keep"
        assert track.genres == ["keep"]

    def test_none_merge(self, track_factory):
        """Don't merge in any null values."""
        track = track_factory()
        other_track = track_factory()

        track.title = "keep"
        other_track.title = None

        track.merge(other_track)

        assert track.title == "keep"

    def test_db_delete(self, track_factory, tmp_session):
        """Remove the other track from the db if it exists."""
        track = track_factory()
        other_track = track_factory()
        tmp_session.add(other_track)
        tmp_session.flush()

        track.merge(other_track)

        assert tmp_session.query(Track).one()


class TestDupListField:
    """Ensure duplicate list fields can be assigned/created without error."""

    def test_genre(self, track_factory, tmp_session):
        """Duplicate genres don't error."""
        track1 = track_factory(genre="pop")
        track2 = track_factory(genre="pop")

        tmp_session.add(track1)
        tmp_session.merge(track2)

        tracks = tmp_session.query(Track).all()
        for track in tracks:
            track.genre = "new genre"
