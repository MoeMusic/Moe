"""Tests an Extra object."""

from pathlib import Path

import moe
from moe.config import ExtraPlugin
from moe.library import Extra, MergeStrategy
from tests.conftest import extra_factory, track_factory


class MyExtraPlugin:
    """Plugin that implements the extra hooks for testing."""

    @staticmethod
    @moe.hookimpl
    def is_unique_extra(extra, other):
        """Extras with the same title aren't unique."""
        if extra.custom == other.custom:
            return False


class TestHooks:
    """Test extra hooks."""

    def test_is_unique_extra(self, tmp_config):
        """Plugins can add additional unique constraints."""
        tmp_config(extra_plugins=[ExtraPlugin(MyExtraPlugin, "extra_plugin")])
        extra1 = extra_factory(custom_fields={"custom": "dup_extra"})
        extra2 = extra_factory(custom_fields={"custom": "dup_extra"})

        assert not extra1.is_unique(extra2)


class TestIsUnique:
    """Test `is_unique()`."""

    def test_same_path(self):
        """Extras with the same path are not unique."""
        extra = extra_factory()
        dup_extra = extra_factory(path=extra.path)

        assert not extra.is_unique(dup_extra)

    def test_default(self):
        """Extras with no matching parameters are unique."""
        extra1 = extra_factory()
        extra2 = extra_factory()

        assert extra1.is_unique(extra2)

    def test_non_extra(self):
        """Other library items that aren't extras are unique."""
        assert extra_factory().is_unique(track_factory())


class TestMerge:
    """Test merging two extras."""

    def test_conflict_persists(self):
        """Don't overwrite any conflicts."""
        extra = extra_factory(path=Path("keep"))
        other_extra = extra_factory(path=Path("discard"))

        extra.merge(other_extra, MergeStrategy.KEEP_EXISTING)

        assert extra.path == Path("keep")

    def test_merge_non_conflict(self):
        """Apply any non-conflicting fields."""
        extra = extra_factory(custom=None)
        other_extra = extra_factory(custom="keep")

        extra.merge(other_extra, MergeStrategy.KEEP_EXISTING)

        assert extra.custom["custom"] == "keep"

    def test_none_merge(self):
        """Don't merge in any null values."""
        extra = extra_factory(custom="keep")
        other_extra = extra_factory(custom=None)

        extra.merge(other_extra, MergeStrategy.OVERWRITE)

        assert extra.custom["custom"] == "keep"

    def test_custom_overwrite(self):
        """Custom fields overwrite merge strategy."""
        extra = extra_factory(custom="old")
        other_extra = extra_factory(custom="new")

        extra.merge(other_extra, MergeStrategy.OVERWRITE)

        assert extra.custom["custom"] == "new"

    def test_custom_keep_existing(self):
        """Custom fields keep existing merge strategy."""
        extra = extra_factory(custom="old")
        other_extra = extra_factory(custom="new")

        extra.merge(other_extra, MergeStrategy.KEEP_EXISTING)

        assert extra.custom["custom"] == "old"

    def test_db_delete(self, tmp_session):
        """Remove the other extra from the db if it exists."""
        extra = extra_factory()
        other_extra = extra_factory()
        tmp_session.add(other_extra)
        tmp_session.flush()

        extra.merge(other_extra)

        assert tmp_session.query(Extra).one()


class TestEquality:
    """Test equality of extras."""

    def test_equals(self):
        """Extras with the same fields are equal."""
        extra1 = extra_factory(custom="custom")
        extra2 = extra_factory(dup_extra=extra1)

        assert extra1 == extra2

    def test_not_equals(self):
        """Extras with different designated unique fields are not equal."""
        extra1 = extra_factory()
        extra2 = extra_factory()
        assert extra1.path != extra2.path

        assert extra1 != extra2

    def test_not_equals_not_extra(self):
        """Not equal if not comparing two extras."""
        assert extra_factory() != "test"
