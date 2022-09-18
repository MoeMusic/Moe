"""Test the duplicate plugin cli."""

from unittest.mock import patch

import pytest

from moe.library.track import Track
from moe.plugins.duplicate import dup_cli


@pytest.fixture
def tmp_dup_config(tmp_config):
    """Tempory config enabling the cli and duplicate plugins."""
    return tmp_config('default_plugins = ["cli", "duplicate"]')


class TestPrompt:
    """Test the duplicate prompt for tracks used in the `resolve_dup_items()` hook."""

    def test_choices_called(self, track_factory, tmp_dup_config):
        """The proper choices get called.."""
        track_a = track_factory()
        track_b = track_factory()

        with patch(
            "moe.plugins.duplicate.dup_cli.choice_prompt",
            autospec=True,
        ) as mock_prompt_choice:
            tmp_dup_config.pm.hook.resolve_dup_items(
                config=tmp_dup_config, item_a=track_a, item_b=track_b
            )

        mock_prompt_choice.return_value.func.assert_called_once_with(
            tmp_dup_config, track_a, track_b
        )

    def test_keep_a(self, tmp_session, track_factory, tmp_dup_config):
        """When keeping item a."""
        track_a = track_factory(title="a")
        track_b = track_factory(title="b")
        tmp_session.add_all([track_a, track_b])
        tmp_session.flush()

        dup_cli._keep_a(tmp_dup_config, track_a, track_b)

        db_track = tmp_session.query(Track).one()
        assert db_track.title == "a"

    def test_keep_b(self, tmp_session, track_factory, tmp_dup_config):
        """When keeping item a."""
        track_a = track_factory(title="a")
        track_b = track_factory(title="b")
        tmp_session.add_all([track_a, track_b])
        tmp_session.flush()

        dup_cli._keep_b(tmp_dup_config, track_a, track_b)

        db_track = tmp_session.query(Track).one()
        assert db_track.title == "b"

    def test_merge(self, tmp_session, track_factory, tmp_dup_config):
        """Merging item_a into item_b without overwriting."""
        track_a = track_factory(title="a", genres={"merge"})
        track_b = track_factory(title="b")
        track_b.genres = None
        tmp_session.add_all([track_a, track_b])
        tmp_session.flush()

        dup_cli._merge(tmp_dup_config, track_a, track_b)

        db_track = tmp_session.query(Track).one()
        assert db_track.title == "b"
        assert db_track.genre == "merge"

    def test_overwrite(self, tmp_session, track_factory, tmp_dup_config):
        """Merging item_a into item_b with overwriting."""
        track_a = track_factory(title="a", genres={"merge"})
        track_b = track_factory(title="b")
        track_b.genres = None
        tmp_session.add_all([track_a, track_b])
        tmp_session.flush()

        dup_cli._overwrite(tmp_dup_config, track_a, track_b)

        db_track = tmp_session.query(Track).one()
        assert db_track.title == "a"
        assert db_track.genre == "merge"
