"""Tests a Track object."""

import pytest

import moe
import moe.write as moe_write
from moe.config import ExtraPlugin
from moe.library import MetaTrack, Track, TrackError
from moe.library.album import MetaAlbum
from tests.conftest import album_factory, extra_factory, track_factory


class MyTrackPlugin:
    """Plugin that implements the extra hooks for testing."""

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
        assert track_factory().album

    def test_guess_disc_multi_disc(self):
        """Guess the disc if not given."""
        album = album_factory(num_discs=3, exists=True)
        track1 = album.get_track(1, disc=1)
        track2 = album.get_track(1, disc=2)
        track3 = album.get_track(1, disc=3)
        track1_disc = 1
        track2_disc = 2
        track3_disc = 3
        assert track1
        assert track2
        assert track3

        new_track1 = Track(album, track1.path, track1.title, track1.track_num)
        new_track2 = Track(album, track2.path, track2.title, track2.track_num)
        new_track3 = Track(album, track3.path, track3.title, track3.track_num)

        assert new_track1.disc == track1_disc
        assert new_track2.disc == track2_disc
        assert new_track3.disc == track3_disc

    def test_guess_disc_single_disc(self):
        """Guess the disc if there are no disc sub directories."""
        track = track_factory()
        assert track.path.parent == track.album.path

        new_track = Track(
            track.album,
            track.path,
            track.title,
            track.track_num,
        )

        assert new_track.disc == 1

    def test_default_artist(self):
        """Use the album artist if an artist is not given."""
        album = album_factory(artist="use me")
        track = track_factory(album=album, artist=None)

        assert track.artist == "use me"

    def test_use_given_artist(self):
        """Don't use the album artist if an artist is given."""
        album = album_factory(artist="dont use me")
        track = track_factory(album=album, artist="use me")

        assert track.artist == "use me"

    def test_custom_fields(self):
        """Custom fields can be assigned using kwargs."""
        track = track_factory()

        new_track = Track(
            track.album,
            track.path,
            track.title,
            track.track_num,
            custom="custom",
        )

        assert new_track.custom["custom"] == "custom"

    def test_composer_field(self):
        """Composer field can be assigned during initialization."""
        track = track_factory()

        new_track = Track(
            track.album,
            track.path,
            track.title,
            track.track_num,
            composer="Antonín Leopold Dvořák",
        )

        assert new_track.composer == "Antonín Leopold Dvořák"

    def test_composer_sort_field(self):
        """Composer sort field can be assigned during initialization."""
        track = track_factory()

        new_track = Track(
            track.album,
            track.path,
            track.title,
            track.track_num,
            composer_sort="Dvořák, Antonín Leopold",
        )

        assert new_track.composer_sort == "Dvořák, Antonín Leopold"


class TestMetaInit:
    """Test MetaTrack initialization."""

    def test_default_artist(self):
        """Use the album artist if an artist is not given."""
        album = MetaAlbum(artist="use me")
        track = MetaTrack(album, 1, artist=None)

        assert track.artist == "use me"

    def test_use_given_artist(self):
        """Don't use the album artist if an artist is given."""
        album = MetaAlbum(artist="dont use me")
        track = MetaTrack(album, 1, artist="use me")

        assert track.artist == "use me"

    def test_composer_field(self):
        """Composer field can be assigned during MetaTrack initialization."""
        album = MetaAlbum(artist="test_artist")
        track = MetaTrack(
            album,
            1,
            composer="Jane Melody",
        )

        assert track.composer == "Jane Melody"

    def test_composer_sort_field(self):
        """Composer sort field can be assigned during MetaTrack initialization."""
        album = MetaAlbum(artist="test_artist")
        track = MetaTrack(
            album,
            1,
            composer_sort="Melody, Jane",
        )

        assert track.composer_sort == "Melody, Jane"


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
        track.album.artist = ""
        track.artist = "Backup"
        moe_write.write_tags(track)

        track = Track.from_file(track.path)
        assert track.album.artist

    def test_read_custom_tags(self, tmp_config):
        """Plugins can add additional track and album fields via `read_custom_tags`."""
        tmp_config(extra_plugins=[ExtraPlugin(MyTrackPlugin, "track_plugin")])
        track = track_factory(exists=True)
        new_track = Track.from_file(track.path)

        assert new_track.album.title == "custom album title"
        assert new_track.title == "custom track title"

    def test_missing_artist(self, tmp_config):
        """Raise ValueError if track is missing both an artist and albumartist."""
        tmp_config()
        track = track_factory(exists=True)
        track.album.artist = None
        track.artist = None
        moe_write.write_tags(track)

        with pytest.raises(ValueError, match="missing"):
            Track.from_file(track.path)

    def test_missing_album_title(self, tmp_config):
        """Raise ValueError if track is missing the album title."""
        tmp_config()
        track = track_factory(exists=True)
        track.album.title = None
        moe_write.write_tags(track)

        with pytest.raises(ValueError, match="missing"):
            Track.from_file(track.path)

    def test_missing_date(self, tmp_config):
        """Raise ValueError if track is missing the date."""
        tmp_config()
        track = track_factory(exists=True)
        track.album.date = None
        moe_write.write_tags(track)

        with pytest.raises(ValueError, match="missing"):
            Track.from_file(track.path)

    def test_missing_title(self, tmp_config):
        """Raise ValueError if track is missing the title."""
        tmp_config()
        track = track_factory(exists=True)
        track.title = None
        moe_write.write_tags(track)

        with pytest.raises(ValueError, match="missing"):
            Track.from_file(track.path)

    def test_missing_track_num(self, tmp_config):
        """Raise ValueError if track is missing the track number."""
        tmp_config()
        track = track_factory(exists=True)
        track.track_num = None
        moe_write.write_tags(track)

        with pytest.raises(ValueError, match="missing"):
            Track.from_file(track.path)

    def test_missing_disc_total(self, tmp_config):
        """Use the default disc total if missing from tags."""
        tmp_config()
        track = track_factory(exists=True)
        track.album.disc_total = None
        moe_write.write_tags(track)

        Track.from_file(track.path).album.disc_total = 1

    def test_init_album_defaults(self, tmp_config):
        """If an album is not given, we will create it with the track's parent path."""
        tmp_config()
        track = track_factory(exists=True)

        new_track = Track.from_file(track.path)
        assert new_track.album.path == new_track.path.parent

    def test_init_album_with_album_path(self, tmp_config):
        """If an album is not given, we will create it with a specified album_path."""
        tmp_config()
        track = track_factory(exists=True)
        album_path = track.path.parent.parent

        new_track = Track.from_file(track.path, None, album_path)
        assert new_track.album.path == album_path


class TestEquality:
    """Test equality of tracks."""

    def test_meta_equals(self):
        """Meta Tracks with the same metadata are equal."""
        album = MetaAlbum(artist="meta_artist")
        track1 = MetaTrack(album, 1)
        track2 = MetaTrack(album, 1)

        assert track1 == track2

    def test_meta_not_equals(self):
        """Meta Tracks with different metadata are not equal."""
        album = MetaAlbum(artist="meta_artist")
        track1 = MetaTrack(album, 1)
        track2 = MetaTrack(album, 2)

        assert track1 != track2

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
            album=track.album, track_num=track.track_num, disc=track.disc
        )

        assert not track.is_unique(dup_track)

    def test_default(self):
        """Tracks with no matching parameters are unique."""
        track1 = track_factory()
        track2 = track_factory()

        assert track1.is_unique(track2)

    def test_non_track(self):
        """Other library items that aren't tracks are unique."""
        assert track_factory().is_unique(album_factory())


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

    def test_custom_fields(self):
        """Merge custom fields too."""
        track = track_factory(custom="")
        other_track = track_factory(custom="new")

        track.merge(other_track)

        assert track.custom["custom"] == "new"


class TestProperties:
    """Test various track properties."""

    def test_genre(self):
        """Genre should concat genres."""
        track = track_factory(genres={"1", "2"})

        assert track.genre in {"1;2", "2;1"}

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

        assert track.sample_rate == 44100  # noqa: PLR2004

    def test_duration_property_access(self):
        """We can get the duration of a track."""
        track = track_factory(exists=True)
        assert isinstance(track.duration, float)


class TestListDuplicates:
    """List fields should not cause duplicate errors (just merge silently)."""

    def test_genre(self, tmp_session):
        """Duplicate genres don't error."""
        track1 = track_factory(genres={"pop"})
        track2 = track_factory(genres={"pop"})

        tmp_session.add(track1)
        tmp_session.add(track2)
        tmp_session.flush()

        tracks = tmp_session.query(Track).all()
        for track in tracks:
            assert track.genre == "pop"


class TestLessThan:
    """Test ``__lt__``."""

    def test_album_sort(self):
        """Sorting by album first."""
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
