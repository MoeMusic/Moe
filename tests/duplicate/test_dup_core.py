"""Test the duplicate plugin core."""

import shutil
from collections.abc import Iterator
from pathlib import Path
from types import FunctionType
from unittest.mock import MagicMock, patch

import pytest

import moe
from moe import config, remove
from moe.config import ExtraPlugin
from moe.library import Album, Extra, Track
from tests.conftest import album_factory, extra_factory, track_factory


class DuplicatePlugin:
    """Test duplicate plugin."""

    @staticmethod
    @moe.hookimpl
    def resolve_dup_items(session, item_a, item_b):
        """Resolve duplicates."""
        if isinstance(item_a, (Track, Album)):
            if item_a.title == "remove me":
                remove.remove_item(session, item_a)
            if item_b.title == "remove me":
                remove.remove_item(session, item_b)
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


@pytest.fixture
def mock_resolve_duplicates() -> Iterator[FunctionType]:
    """Mock the `resolve_duplicates` function."""
    with patch(
        "moe.duplicate.dup_core.resolve_duplicates", autospec=True
    ) as mock_resolve_dups:
        yield mock_resolve_dups


@pytest.mark.usefixtures("_tmp_dup_config")
class TestResolveDupItems:
    """Test ``resolve_dup_items()``."""

    def test_remove_a(self, tmp_session):
        """Remove a track."""
        track_a = track_factory(exists=True, title="remove me")
        track_b = track_factory(exists=True, path=track_a.path)

        tmp_session.add(track_a)
        tmp_session.add(track_b)
        tmp_session.flush()

        db_track = tmp_session.query(Track).one()
        assert db_track == track_b

    def test_remove_b(self, tmp_session):
        """Remove b track."""
        track_a = track_factory(exists=True)
        track_b = track_factory(exists=True, path=track_a.path, title="remove me")

        tmp_session.add(track_a)
        tmp_session.add(track_b)
        tmp_session.flush()

        db_track = tmp_session.query(Track).one()
        assert db_track == track_a

    def test_rm_existing_track(self, tmp_session):
        """Remove b track."""
        track_a = track_factory(exists=True, title="remove me")
        track_b = track_factory(exists=True, path=track_a.path)

        tmp_session.add(track_a)
        tmp_session.flush()
        tmp_session.add(track_b)
        tmp_session.flush()

        db_track = tmp_session.query(Track).one()
        assert db_track == track_b

    def test_changing_fields(self, tmp_session):
        """Duplicates can be avoided by changing conflicting fields."""
        track_a = track_factory(exists=True, title="change me")
        track_b = track_factory(exists=True, path=track_a.path)

        tmp_session.add(track_a)
        tmp_session.add(track_b)
        tmp_session.flush()

        db_tracks = tmp_session.query(Track).all()
        assert track_a in db_tracks
        assert track_b in db_tracks

    def test_change_extra(self, tmp_session):
        """Duplicate extras can be avoided."""
        extra_a = extra_factory(exists=True)
        extra_b = extra_factory(exists=True, path=extra_a.path)

        tmp_session.add(extra_a)
        tmp_session.add(extra_b)
        tmp_session.flush()

        db_extras = tmp_session.query(Extra).all()
        assert extra_a in db_extras
        assert extra_b in db_extras

    def test_remove_album(self, tmp_session):
        """Remove an album."""
        album_a = album_factory(exists=True, title="remove me")
        album_b = album_factory(exists=True, path=album_a.path)

        tmp_session.add(album_a)
        tmp_session.add(album_b)
        tmp_session.flush()

        db_album = tmp_session.query(Album).one()
        assert db_album == album_b

    def test_album_first(self, tmp_session):
        """Albums should be processed first as they may resolve tracks or extras too."""
        album_a = album_factory(exists=True, title="remove me")
        album_b = album_factory(exists=True, path=album_a.path)
        album_b.tracks[0].path = album_a.tracks[0].path
        album_a.tracks[0].title = "change me"  # shouldn't get changed as

        tmp_session.add(album_a.tracks[0])
        tmp_session.add(album_b.tracks[0])
        tmp_session.add(album_a)
        tmp_session.add(album_b)
        tmp_session.flush()

        db_album = tmp_session.query(Album).one()
        assert db_album == album_b
        db_tracks = tmp_session.query(Track).all()
        for track in db_tracks:
            assert track.title != "changed"


@pytest.mark.usefixtures("_tmp_dup_config")
class TestEditChangedItems:
    """Test the `edit_changed_items` hook."""

    def test_dup_items(self, mock_resolve_duplicates):
        """Resolve any duplicate albums when they're edited."""
        album = album_factory()
        extra = extra_factory()
        track = track_factory()
        num_dup_albums = 3
        mock_session = MagicMock()

        config.CONFIG.pm.hook.edit_changed_items(
            session=mock_session, items=[album, extra, track]
        )

        mock_resolve_duplicates.assert_any_call(mock_session, [album])
        mock_resolve_duplicates.assert_any_call(mock_session, [extra])
        mock_resolve_duplicates.assert_any_call(mock_session, [track])
        assert mock_resolve_duplicates.call_count == num_dup_albums


@pytest.mark.usefixtures("_tmp_dup_config")
class TestEditNewItems:
    """Test the `edit_new_items` hook."""

    def test_dup_items(self, mock_resolve_duplicates):
        """Resolve any duplicate albums when they're edited."""
        album = album_factory()
        extra = extra_factory()
        track = track_factory()
        num_dup_albums = 3
        mock_session = MagicMock()

        config.CONFIG.pm.hook.edit_new_items(
            session=mock_session, items=[album, extra, track]
        )

        mock_resolve_duplicates.assert_any_call(mock_session, [album])
        mock_resolve_duplicates.assert_any_call(mock_session, [extra])
        mock_resolve_duplicates.assert_any_call(mock_session, [track])
        assert mock_resolve_duplicates.call_count == num_dup_albums
