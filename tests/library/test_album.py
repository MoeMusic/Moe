"""Tests an Album object."""

from pathlib import Path

import pytest

import moe
from moe.config import ExtraPlugin
from moe.library import Album, AlbumError, Extra
from moe.plugins import write as moe_write
from tests.conftest import album_factory, track_factory


class MyAlbumPlugin:
    """Plugin that implements the extra hooks for testing."""

    @staticmethod
    @moe.hookimpl
    def create_custom_album_fields():
        """Create a new custom field."""
        return {"no_default": None, "default": "value"}

    @staticmethod
    @moe.hookimpl
    def is_unique_album(album, other):
        """Albums with the same title aren't unique."""
        if album.title == other.title:
            return False


class TestHooks:
    """Test album hooks."""

    def test_create_custom_fields(self, tmp_config):
        """Plugins can define new custom fields."""
        tmp_config(extra_plugins=[ExtraPlugin(MyAlbumPlugin, "album_plugin")])
        album = album_factory()

        assert not album.no_default
        assert album.default == "value"

    def test_is_unique_album(self, tmp_config):
        """Plugins can add additional unique constraints."""
        tmp_config(extra_plugins=[ExtraPlugin(MyAlbumPlugin, "album_plugin")])
        album = album_factory()
        dup_album = album_factory(title=album.title)

        assert not album.is_unique(dup_album)


class TestFromDir:
    """Test a creating an album from a directory."""

    def test_dir_album(self, tmp_config):
        """If a directory given, add to library as an album."""
        tmp_config()
        album = album_factory(exists=True)
        assert Album.from_dir(album.path) == album

    def test_extras(self, tmp_config):
        """Add any extras that are within the album directory."""
        tmp_config()
        album = album_factory(exists=True)
        new_album = Album.from_dir(album.path)

        for extra in album.extras:
            assert extra in new_album.extras

    def test_no_valid_tracks(self, tmp_path):
        """Error if given directory does not contain any valid tracks."""
        empty_path = tmp_path / "empty"
        empty_path.mkdir()

        with pytest.raises(AlbumError):
            Album.from_dir(empty_path)

    def test_add_multi_disc(self, tmp_config):
        """We can add a multi-disc album."""
        tmp_config()
        album = album_factory(exists=True)
        track1 = album.tracks[0]
        track2 = album.tracks[1]
        track1.disc = 1
        track2.disc = 2
        album.disc_total = 2
        moe_write.write_tags(track1)
        moe_write.write_tags(track2)

        track1_path = Path(album.path / "disc 01" / track1.path.name)
        track2_path = Path(album.path / "disc 02" / track2.path.name)
        track1_path.parent.mkdir()
        track2_path.parent.mkdir()
        track1.path.rename(track1_path)
        track2.path.rename(track2_path)
        track1.path = track1_path
        track2.path = track2_path

        album = Album.from_dir(album.path)

        assert album.get_track(track1.track_num, track1.disc)
        assert album.get_track(track2.track_num, track2.disc)


class TestIsUnique:
    """Test `is_unique()`."""

    def test_same_path(self):
        """Albums with the same path are not unique."""
        album = album_factory()
        dup_album = album_factory(path=album.path)

        assert not album.is_unique(dup_album)

    def test_default(self):
        """Albums with no matching parameters are unique."""
        album1 = album_factory()
        album2 = album_factory()

        assert album1.is_unique(album2)


class TestMerge:
    """Test merging two albums together."""

    def test_conflict_persists(self):
        """Don't overwrite any conflicts."""
        album = album_factory(title="123")
        other_album = album_factory(title="456")
        keep_title = album.title

        album.merge(other_album)

        assert album.title == keep_title

    def test_merge_non_conflict(self):
        """Apply any non-conflicting fields."""
        album = album_factory(title="")
        other_album = album_factory(title="new")

        album.merge(other_album)

        assert album.title == "new"

    def test_none_merge(self):
        """Don't merge in any null values."""
        album = album_factory(title="123")
        other_album = album_factory(title="")

        album.merge(other_album)

        assert album.title == "123"

    def test_overwrite_field(self):
        """Overwrite fields if the option is given."""
        album = album_factory(title="123")
        other_album = album_factory(title="456")
        keep_title = other_album.title

        album.merge(other_album, overwrite=True)

        assert album.title == keep_title

    def test_merge_extras(self):
        """Merge in any new extras."""
        album1 = album_factory()
        album2 = album_factory()
        new_extra = Extra(album2, album2.path / "new.txt")
        assert album1.extras != album2.extras
        extras_count = len(album1.extras) + len(album2.extras)

        album1.merge(album2)

        assert new_extra in album1.extras
        assert len(album1.extras) == extras_count

    def test_overwrite_extras(self):
        """Replace conflicting extras if told to overwrite."""
        album1 = album_factory(exists=True, title="album1")
        album2 = album_factory(exists=True, title="album2")

        Extra(album2, album2.path / album1.extras[0].path.name)  # conflict
        overwrite_extra = album1.extras[0]
        overwrite_extra.path.write_text("overwrite")
        assert overwrite_extra.path.exists()

        album1.merge(album2, overwrite=True)

        for extra in album1.extras:
            if extra.path.exists():
                assert extra.path.read_text() != "overwrite"

    def test_merge_tracks(self):
        """Tracks should merge with the same behavior as fields."""
        album1 = album_factory()
        album2 = album_factory()

        new_track = track_factory(album=album2)
        conflict_track = album2.tracks[0]
        keep_track = album1.get_track(conflict_track.track_num)
        assert keep_track
        keep_track.title = "keep"
        assert conflict_track.title != keep_track.title
        assert album1.tracks != album2.tracks

        album1.merge(album2)

        assert new_track in album1.tracks
        assert keep_track.title == "keep"

    def test_overwrite_tracks(self):
        """Tracks should overwrite the same as fields if option given."""
        album1 = album_factory()
        album2 = album_factory()

        conflict_track = album2.tracks[0]
        overwrite_track = album1.get_track(conflict_track.track_num)
        assert overwrite_track
        conflict_track.title = "conflict"
        assert conflict_track.title != overwrite_track.title

        album1.merge(album2, overwrite=True)

        assert overwrite_track.title == "conflict"


class TestEquality:
    """Test equality of albums."""

    def test_equals(self):
        """Albums with the same fields are equal."""
        album1 = album_factory()
        album2 = album_factory(dup_album=album1)

        assert album1 == album2

    def test_not_equals(self):
        """Albums with different fields are not equal."""
        album1 = album_factory(title="diff")
        album2 = album_factory(title="erent")

        assert album1 != album2

    def test_not_equals_not_album(self):
        """Not equal if not comparing two albums."""
        assert album_factory() != "test"
