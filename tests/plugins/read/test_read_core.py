"""Test read_core."""

import pytest

from moe.library import Album, Track
from moe.plugins import read
from tests.conftest import album_factory, track_factory


@pytest.fixture
def _tmp_read_config(tmp_config):
    """A temporary config for the read plugin with the cli."""
    tmp_config('default_plugins = ["read", "write"]')


@pytest.mark.usefixtures("_tmp_read_config")
class TestReadItem:
    """Test read_item()."""

    def test_track(self):
        """We can read updates from a track file."""
        track = track_factory(title="file", exists=True)

        track.title = "changed"
        assert Track.from_file(track.path).title == "file"

        read.read_item(track)
        assert track.title == "file"

    def test_album(self):
        """We can read updates from an album directory."""
        album = album_factory(title="file", exists=True)

        album.title = "changed"
        assert Album.from_dir(album.path).title == "file"

        read.read_item(album)
        assert album.title == "file"

    def test_path_dne(self):
        """Raise FileNotFoundError if the item's path does not exist."""
        with pytest.raises(FileNotFoundError):
            read.read_item(track_factory())
