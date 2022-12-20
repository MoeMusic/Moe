"""Test the duplicate plugin cli."""

import datetime
from unittest.mock import MagicMock, patch

import pytest

from moe import config
from moe.cli import console
from moe.duplicate import dup_cli
from moe.library import Track
from tests.conftest import album_factory, extra_factory, track_factory


@pytest.fixture
def _tmp_dup_config(tmp_config):
    """Tempory config enabling the cli and duplicate plugins."""
    tmp_config('default_plugins = ["cli", "duplicate"]')


@pytest.mark.usefixtures("_tmp_dup_config")
class TestPrompt:
    """Test the duplicate prompt for tracks used in the `resolve_dup_items()` hook."""

    def test_choices_called(self):
        """The proper choices get called.."""
        track_a = track_factory()
        track_b = track_factory()

        mock_session = MagicMock()
        with patch(
            "moe.duplicate.dup_cli.choice_prompt",
            autospec=True,
        ) as mock_prompt_choice:
            config.CONFIG.pm.hook.resolve_dup_items(
                session=mock_session, item_a=track_a, item_b=track_b
            )

        mock_prompt_choice.return_value.func.assert_called_once_with(
            mock_session, track_a, track_b
        )

    def test_keep_a(self, tmp_session):
        """When keeping item a."""
        track_a = track_factory(title="a")
        track_b = track_factory(title="b")
        tmp_session.add_all([track_a, track_b])
        tmp_session.flush()

        dup_cli._keep_a(tmp_session, track_a, track_b)

        db_track = tmp_session.query(Track).one()
        assert db_track.title == "a"

    def test_keep_b(self, tmp_session):
        """When keeping item a."""
        track_a = track_factory(title="a")
        track_b = track_factory(title="b")
        tmp_session.add_all([track_a, track_b])
        tmp_session.flush()

        dup_cli._keep_b(tmp_session, track_a, track_b)

        db_track = tmp_session.query(Track).one()
        assert db_track.title == "b"

    def test_merge(self, tmp_session):
        """Merging item_a into item_b without overwriting."""
        track_a = track_factory(title="a", genres={"merge"})
        track_b = track_factory(title="b")
        track_b.genres = set()
        tmp_session.add_all([track_a, track_b])
        tmp_session.flush()

        dup_cli._merge(tmp_session, track_a, track_b)

        db_track = tmp_session.query(Track).one()
        assert db_track.title == "b"
        assert db_track.genre == "merge"

    def test_overwrite(self, tmp_session):
        """Merging item_a into item_b with overwriting."""
        track_a = track_factory(title="a", genres={"merge"})
        track_b = track_factory(title="b")
        track_b.genres = set()
        tmp_session.add_all([track_a, track_b])
        tmp_session.flush()

        dup_cli._overwrite(tmp_session, track_a, track_b)

        db_track = tmp_session.query(Track).one()
        assert db_track.title == "a"
        assert db_track.genre == "merge"


class TestUI:
    """These tests exist as a convenience to view different changes to the duplicate UI.

    To view the output from any of the tests, simply append an `assert 0` to the end of
    the test.

    Note:
        You will not see rich color with this approach unless you set
        `force_terminal=True` on the Console constructor in `cli.py`.
    """

    def test_full_diff_album(self):
        """Print prompt for fully different albums."""
        old_album = album_factory(num_tracks=6, num_discs=2, artist="outkist")
        new_album = album_factory(
            title=old_album.title,
            date=datetime.date(1999, 12, 31),
            num_tracks=6,
            num_discs=2,
        )
        old_album.tracks[0].title = "really really long old title"
        old_album.tracks[0].custom["custom_field"] = "custom field!"

        assert old_album is not new_album

        console.print(dup_cli._fmt_item_vs(old_album, new_album))

    def test_track(self):
        """Duplicate prompt for two tracks."""
        track_a = track_factory()
        track_b = track_factory(path=track_a.path)

        console.print(dup_cli._fmt_item_vs(track_a, track_b))

    def test_extra(self):
        """Duplicate prompt for two extras."""
        extra_a = extra_factory(custom_fields={"custom": "diff A"})
        extra_b = extra_factory(custom_fields={"custom": "diff B"})

        console.print(dup_cli._fmt_item_vs(extra_a, extra_b))

    def test_dup_tracks(self):
        """Album with the same tracks."""
        album_a = album_factory()
        album_b = album_factory(dup_album=album_a)
        album_a.title = "diff"

        console.print(dup_cli._fmt_item_vs(album_a, album_b))
