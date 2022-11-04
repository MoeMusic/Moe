"""Tests a Track object."""

import pytest

import moe
import moe.plugins.write as moe_write
from moe.config import ExtraPlugin
from moe.library import MetaTrack, Track, TrackError
from moe.library.album import MetaAlbum
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
        other_track = track_factory(title="keep", genres={"keep"})
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

    def test_overwrite(self):
        """Fields are overwritten if the option is given."""
        track = track_factory(title="1")
        other_track = track_factory(title="2")

        track.merge(other_track, overwrite=True)

        assert track.title == "2"


class TestProperties:
    """Test various track properties."""

    def test_genre(self):
        """Genre should concat genres."""
        track = track_factory(genres={"1", "2"})

        assert track.genre == "1;2" or track.genre == "2;1"

    def test_set_genre(self):
        """Setting genre should split into strings."""
        track = track_factory(genre=None)

        assert track.genre is None
        assert track.genres is None

        track.genre = "1; 2"
        assert track.genres == {"1", "2"}

    def test_audio_format(self):
        """We can get the audio format of a track."""
        track = track_factory(exists=True)

        assert track.audio_format == "mp3"

    def test_bit_depth(self):
        """We can get the bit depth of a track."""
        track = track_factory(exists=True)

        # Bit depth is unavailable for MP3.
        assert track.bit_depth == 0

    def test_sample_rate(self):
        """We can get the sample rate of a track."""
        track = track_factory(exists=True)

        assert track.sample_rate == 44100


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


class TestLessThan:
    """Test ``__lt__``."""

    def test_album_sort(self):
        """Sorting by album_obj first."""
        track1 = MetaTrack(album=MetaAlbum(title="a"), track_num=2)
        track2 = MetaTrack(album=MetaAlbum(title="b"), track_num=1)

        assert track1 < track2

    def test_track_num_sort(self):
        """Sorting by track_number if the albums are the same."""
        track1 = MetaTrack(album=MetaAlbum(title="a"), track_num=1)
        track2 = MetaTrack(album=MetaAlbum(title="a"), track_num=2)

        assert track1 < track2

    def test_disc_sort(self):
        """Sorting by disc if the track numbers and albums are the same."""
        track1 = MetaTrack(album=MetaAlbum(title="a"), track_num=1, disc=1)
        track2 = MetaTrack(album=MetaAlbum(title="a"), track_num=1, disc=2)

        assert track1 < track2
