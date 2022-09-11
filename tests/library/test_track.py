"""Tests a Track object."""

import datetime
from pathlib import Path
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


class TestCustomFields:
    """Test getting and setting operations on custom fields."""

    def test_get_custom_field(self, mock_track):
        """We can get a custom field like a normal attribute."""
        mock_track._custom_fields["custom"] = "field"

        assert mock_track.custom == "field"

    def test_set_custom_field(self, mock_track):
        """We can set a custom field like a normal attribute."""
        mock_track._custom_fields["custom_key"] = None
        mock_track.custom_key = "test"

        assert mock_track._custom_fields["custom_key"] == "test"

    def test_set_non_key(self, mock_track):
        """Don't set just any attribute as a custom field if the key doesn't exist."""
        mock_track.custom_key = 1

        with pytest.raises(KeyError):
            assert mock_track._custom_fields["custom_key"] == 1

    def test_db_persistence(self, mock_track, tmp_session):
        """Ensure custom fields persist in the database."""
        mock_track._custom_fields["db"] = "persist"

        tmp_session.add(mock_track)
        tmp_session.flush()

        db_track = tmp_session.query(Track).one()
        assert db_track.db == "persist"

    def test_plugin_defined_custom_fields(self, track_factory, tmp_config):
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

    def test_guess_disc_multi_disc(self, real_album):
        """Guess the disc if not given."""
        track1 = real_album.tracks[0]
        track2 = real_album.tracks[1]
        track1.track_num = track2.track_num
        track1.disc = 1
        track2.disc = 1  # should be 2!
        real_album.disc_total = 2
        moe_write.write_tags(track1)
        moe_write.write_tags(track2)
        assert track1 == track2

        track1_path = Path(real_album.path / "disc 01" / track1.path.name)
        track2_path = Path(real_album.path / "disc 02" / track2.path.name)
        Path(real_album.path / "artwork (1996)").mkdir()
        track1_path.parent.mkdir()
        track2_path.parent.mkdir()
        track1.path.rename(track1_path)
        track2.path.rename(track2_path)
        track1.path = track1_path
        track2.path = track2_path

        new_track1 = Track(
            MagicMock(), real_album, track1.path, track1.title, track1.track_num
        )
        new_track2 = Track(
            MagicMock(), real_album, track2.path, track2.title, track2.track_num
        )

        assert new_track1.disc == 1
        assert new_track2.disc == 2

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
        real_track.mb_album_id = "1234"
        real_track.mb_track_id = "123"
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
        assert new_track.mb_album_id == real_track.mb_album_id
        assert new_track.mb_track_id == real_track.mb_track_id
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


class TestGetExisting:
    """Test `get_existing()`."""

    def test_path(self, track_factory, tmp_session):
        """We match an existing track by it's path."""
        track1 = track_factory()
        track2 = track_factory()
        track1.path = track2.path

        tmp_session.merge(track1)

        assert track1.get_existing()

    def test_mb_track_id(self, track_factory, tmp_session):
        """We match an existing track by it's mb_track_id."""
        track1 = track_factory()
        track2 = track_factory()
        track1.mb_track_id = "123"
        track1.mb_track_id = track2.mb_track_id

        tmp_session.merge(track1)

        assert track1.get_existing()

    def test_null_match(self, track_factory, tmp_session):
        """Don't match off of null values."""
        track1 = track_factory()
        track2 = track_factory()
        assert not track1.mb_track_id
        assert not track2.mb_track_id
        assert track1.path != track2.path

        tmp_session.merge(track1)

        assert not track2.get_existing()


class TestEquality:
    """Test equality of tracks."""

    def test_equals_mb_track_id(self, track_factory):
        """Tracks with the same `mb_track_id` are equal."""
        track1 = track_factory()
        track2 = track_factory()
        track1.mb_track_id = "1"
        assert track1 != track2

        track2.mb_track_id = track1.mb_track_id
        assert track1 == track2

    def test_equals_path(self, track_factory):
        """Tracks with the same `path` are equal."""
        track1 = track_factory()
        track2 = track_factory()
        assert track1 != track2

        track1.path = track2.path
        assert track1 == track2

    def test_not_equals(self, track_factory):
        """Tracks with different designated unique fields are not equal."""
        track1 = track_factory()
        track2 = track_factory()
        track1.mb_track_id = "1"

        assert track1.mb_track_id != track2.mb_track_id
        assert track1.path != track2.path

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

        assert not track.get_existing()


class TestDupListField:
    """Ensure duplicate list fields can be assigned/created without error."""

    def test_genre(self, track_factory, tmp_session):
        """Duplicate genres don't error."""
        track1 = track_factory()
        track2 = track_factory()
        track1.genre = "pop"
        track2.genre = "pop"

        tmp_session.add(track1)
        tmp_session.merge(track2)

        tracks = tmp_session.query(Track).all()
        for track in tracks:
            track.genre = "new genre"
