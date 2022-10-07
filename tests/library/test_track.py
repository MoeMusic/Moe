"""Tests a Track object."""

import datetime

import pytest

import moe
import moe.plugins.write as moe_write
from moe.config import ExtraPlugin
from moe.library import Track, TrackError
from moe.plugins.write import write_tags
from tests.conftest import album_factory, extra_factory, track_factory


class MyTrackPlugin:
    """Plugin that implements the extra hooks for testing."""

    @staticmethod
    @moe.hookimpl
    def create_custom_track_fields():
        """Create a new custom field."""
        return {"no_default": None, "default": "value"}

    @staticmethod
    @moe.hookimpl
    def is_unique_track(track, other):
        """Tracks with the same title aren't unique."""
        if track.title == other.title:
            return False

    @staticmethod
    @moe.hookimpl
    def read_custom_tags(track_path, album_fields, track_fields):
        """Override a new fields for the track and album."""
        album_fields["title"] = "custom album title"
        track_fields["title"] = "custom track title"


class TestHooks:
    """Test track hooks."""

    def test_create_custom_fields(self, tmp_config):
        """Plugins can define new custom fields."""
        tmp_config(extra_plugins=[ExtraPlugin(MyTrackPlugin, "track_plugin")])
        track = track_factory()

        assert not track.no_default
        assert track.default == "value"

    def test_is_unique_track(self, tmp_config):
        """Plugins can add additional unique constraints."""
        tmp_config(extra_plugins=[ExtraPlugin(MyTrackPlugin, "track_plugin")])
        track = track_factory()
        dup_track = track_factory(title=track.title)

        assert not track.is_unique(dup_track)


class TestInit:
    """Test Track initialization."""

    def test_album_init(self):
        """Creating a Track should also create the corresponding Album."""
        assert track_factory().album_obj

    def test_guess_disc_multi_disc(self):
        """Guess the disc if not given."""
        album = album_factory(num_discs=3, exists=True)
        track1 = album.get_track(1, disc=1)
        track2 = album.get_track(1, disc=2)
        track3 = album.get_track(1, disc=3)
        assert track1 and track2 and track3  # noqa: PT018

        new_track1 = Track(album, track1.path, track1.title, track1.track_num)
        new_track2 = Track(album, track2.path, track2.title, track2.track_num)
        new_track3 = Track(album, track3.path, track3.title, track3.track_num)

        assert new_track1.disc == 1
        assert new_track2.disc == 2
        assert new_track3.disc == 3

    def test_guess_disc_single_disc(self):
        """Guess the disc if there are no disc sub directories."""
        track = track_factory()
        assert track.path.parent == track.album_obj.path

        new_track = Track(
            track.album_obj,
            track.path,
            track.title,
            track.track_num,
        )

        assert new_track.disc == 1


class TestAlbumSet:
    """Changing an album attribute will change the value for the current Album.

    Thus, all tracks in the album will reflect the new value.
    """

    def test_album_set(self, tmp_path):
        """Setting an album attribute maintains the same album object."""
        track = track_factory()
        track.album = "TPAB"

        assert track.album_obj.title == track.album


class TestFromFile:
    """Test initialization from given file path."""

    def test_read_tags(self, tmp_config):
        """We can initialize a track with tags from a file if present."""
        tmp_config()
        track = track_factory(exists=True)
        album = track.album_obj

        track.album = "The Lost Album"
        track.albumartist = "Wu-Tang Clan"
        track.artist = "Wu-Tang Clan"
        track.artists = {"Wu-Tang Clan", "Me"}
        track.disc = 1
        track.genres = {"hip hop", "rock"}
        track.title = "Full"
        track.track_num = 1

        album.country = "US"
        album.date = datetime.date(2020, 1, 12)
        album.disc_total = 2
        album.media = "CD"
        write_tags(track)

        new_track = Track.from_file(track.path)
        new_album = new_track.album_obj

        assert new_track.album == track.album
        assert new_track.albumartist == track.albumartist
        assert new_track.artist == track.artist
        assert new_track.artists == track.artists
        assert new_track.disc == track.disc
        assert new_track.genres == track.genres
        assert new_track.title == track.title
        assert new_track.track_num == track.track_num

        assert new_album.country == album.country
        assert new_album.disc_total == album.disc_total
        assert new_album.date == album.date
        assert new_album.media == album.media

    def test_non_track_file(self):
        """Raise `TrackError` if the given path does not correspond to a track file."""
        with pytest.raises(TrackError):
            Track.from_file(extra_factory().path)

    def test_albumartist_backup(self, tmp_config):
        """Use artist as a backup for albumartist if missing."""
        tmp_config()
        track = track_factory(exists=True)
        track.albumartist = ""
        track.artist = "Backup"
        moe_write.write_tags(track)

        track = Track.from_file(track.path)
        assert track.albumartist

    def test_read_custom_tags(self, tmp_config):
        """Plugins can add additional track and album fields via `read_custom_tags`."""
        tmp_config(extra_plugins=[ExtraPlugin(MyTrackPlugin, "track_plugin")])
        track = track_factory(exists=True)
        new_track = Track.from_file(track.path)

        assert new_track.album == "custom album title"
        assert new_track.title == "custom track title"

    def test_read_track_fields(self, tmp_config):
        """Plugins can add additional album fields via the `read_album_fields` hook."""
        tmp_config(extra_plugins=[ExtraPlugin(MyTrackPlugin, "track_plugin")])
        track = track_factory(exists=True)
        new_track = Track.from_file(track.path)

        assert new_track.title == "custom track title"


class TestEquality:
    """Test equality of tracks."""

    def test_equals(self):
        """Tracks with the same metadata are equal."""
        track1 = track_factory()
        track2 = track_factory(dup_track=track1)

        assert track1 == track2

    def test_not_equals(self):
        """Tracks with different fields are not equal."""
        track1 = track_factory(title="track1")
        track2 = track_factory(title="track2")

        assert track1 != track2

    def test_not_equals_not_track(self):
        """Not equal if not comparing two tracks."""
        assert track_factory() != "test"


class TestIsUnique:
    """Test `is_unique()`."""

    def test_same_path(self):
        """Tracks with the same path are not unique."""
        track = track_factory()
        dup_track = track_factory(path=track.path)

        assert not track.is_unique(dup_track)

    def test_same_track_disc_num(self):
        """Tracks with the same album, track #, and disc # are not unique."""
        track = track_factory()
        dup_track = track_factory(
            album=track.album_obj, track_num=track.track_num, disc=track.disc
        )

        assert not track.is_unique(dup_track)

    def test_default(self):
        """Tracks with no matching parameters are unique."""
        track1 = track_factory()
        track2 = track_factory()

        assert track1.is_unique(track2)


class TestMerge:
    """Test merging two tracks."""

    def test_conflict_persists(self):
        """Don't overwrite any conflicts."""
        track = track_factory(title="keep")
        other_track = track_factory(title="discard")

        track.merge(other_track)

        assert track.title == "keep"

    def test_merge_non_conflict(self):
        """Apply any non-conflicting fields."""
        track = track_factory()
        other_track = track_factory(title="keep", genres=["keep"])
        track.title = ""
        track.genres = set()

        track.merge(other_track)

        assert track.title == "keep"
        assert track.genres == {"keep"}

    def test_none_merge(self):
        """Don't merge in any null values."""
        track = track_factory(title="keep")
        other_track = track_factory()
        other_track.title = ""

        track.merge(other_track)

        assert track.title == "keep"

    def test_db_delete(self, tmp_session):
        """Remove the other track from the db if it exists."""
        track = track_factory()
        other_track = track_factory()
        tmp_session.add(other_track)
        tmp_session.flush()

        track.merge(other_track)

        assert tmp_session.query(Track).one()


class TestListDuplicates:
    """List fields should not cause duplicate errors (just merge silently)."""

    def test_genre(self, tmp_session):
        """Duplicate genres don't error."""
        track1 = track_factory(genre="pop")
        track2 = track_factory(genre="pop")

        tmp_session.add(track1)
        tmp_session.add(track2)
        tmp_session.flush()

        tracks = tmp_session.query(Track).all()
        for track in tracks:
            assert track.genre == "pop"
