"""Test the duplicate plugin core."""
import shutil
from pathlib import Path

import pytest

import moe
from moe.config import ExtraPlugin, MoeSession
from moe.library import Album, Extra, Track
from moe.plugins.remove import remove_item
from tests.conftest import album_factory, extra_factory, track_factory


class DuplicatePlugin:
    """Test duplicate plugin."""

    @staticmethod
    @moe.hookimpl
    def resolve_dup_items(item_a, item_b):
        """Resolve duplicates."""
        if isinstance(item_a, (Track, Album)):
            if item_a.title == "remove me":
                remove_item(item_a)
            if item_b.title == "remove me":
                remove_item(item_b)
            if item_a.title == "change me":
                dest = item_a.path.parent / "new.mp3"
                shutil.copyfile(item_a.path, dest)
                item_a.path = dest
        elif isinstance(item_a, Extra):
            item_a.path = Path("/")


@pytest.fixture
def _tmp_dup_config(tmp_config):
    """Tempory config enabling the cli and duplicate plugins."""
    tmp_config(
        "default_plugins = ['duplicate', 'write']",
        extra_plugins=[ExtraPlugin(DuplicatePlugin, "dup_test")],
        tmp_db=True,
    )


@pytest.mark.usefixtures("_tmp_dup_config")
class TestResolveDupItems:
    """Test ``resolve_dup_items()``."""

    def test_remove_a(self):
        """Remove a track."""
        track_a = track_factory(exists=True, title="remove me")
        track_b = track_factory(exists=True, path=track_a.path)

        session = MoeSession()
        session.add(track_a)
        session.add(track_b)
        session.flush()

        db_track = session.query(Track).one()
        assert db_track == track_b

    def test_remove_b(self):
        """Remove b track."""
        track_a = track_factory(exists=True)
        track_b = track_factory(exists=True, path=track_a.path, title="remove me")

        session = MoeSession()
        session.add(track_a)
        session.add(track_b)
        session.flush()

        db_track = session.query(Track).one()
        assert db_track == track_a

    def test_rm_existing_track(self):
        """Remove b track."""
        track_a = track_factory(exists=True, title="remove me")
        track_b = track_factory(exists=True, path=track_a.path)

        session = MoeSession()
        session.add(track_a)
        session.flush()
        session.add(track_b)
        session.flush()

        db_track = session.query(Track).one()
        assert db_track == track_b

    def test_changing_fields(self):
        """Duplicates can be avoided by changing conflicting fields."""
        track_a = track_factory(exists=True, title="change me")
        track_b = track_factory(exists=True, path=track_a.path)

        session = MoeSession()
        session.add(track_a)
        session.add(track_b)
        session.flush()

        db_tracks = session.query(Track).all()
        assert track_a in db_tracks
        assert track_b in db_tracks

    def test_change_extra(self):
        """Duplicate extras can be avoided."""
        extra_a = extra_factory(exists=True)
        extra_b = extra_factory(exists=True, path=extra_a.path)

        session = MoeSession()
        session.add(extra_a)
        session.add(extra_b)
        session.flush()

        db_extras = session.query(Extra).all()
        assert extra_a in db_extras
        assert extra_b in db_extras

    def test_remove_album(self):
        """Remove an album."""
        album_a = album_factory(exists=True, title="remove me")
        album_b = album_factory(exists=True, path=album_a.path)

        session = MoeSession()
        session.add(album_a)
        session.add(album_b)
        session.flush()

        db_album = session.query(Album).one()
        assert db_album == album_b

    def test_album_first(self):
        """Albums should be processed first as they may resolve tracks or extras too."""
        album_a = album_factory(exists=True, title="remove me")
        album_b = album_factory(exists=True, path=album_a.path)
        album_b.tracks[0].path = album_a.tracks[0].path
        album_a.tracks[0].title = "change me"  # shouldn't get changed as

        session = MoeSession()
        session.add(album_a.tracks[0])
        session.add(album_b.tracks[0])
        session.add(album_a)
        session.add(album_b)
        session.flush()

        db_album = session.query(Album).one()
        assert db_album == album_b
        db_tracks = session.query(Track).all()
        for track in db_tracks:
            assert track.title != "changed"
