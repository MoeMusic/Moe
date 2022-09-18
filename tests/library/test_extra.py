"""Tests an Extra object."""

import moe
from moe.config import ExtraPlugin
from moe.library.extra import Extra


class MyExtraPlugin:
    """Plugin that implements the extra hooks for testing."""

    @staticmethod
    @moe.hookimpl
    def create_custom_extra_fields(config):
        """Create a new custom field."""
        return {"no_default": None, "default": "value"}

    @staticmethod
    @moe.hookimpl
    def is_unique_extra(extra, other):
        """Extras with the same title aren't unique."""
        print(extra.custom)
        if extra.custom == other.custom:
            return False


class TestHooks:
    """Test extra hooks."""

    def test_create_custom_fields(self, extra_factory, tmp_config):
        """Plugins can define new custom fields."""
        config = tmp_config(extra_plugins=[ExtraPlugin(MyExtraPlugin, "extra_plugin")])
        extra = extra_factory(config)

        assert not extra.no_default
        assert extra.default == "value"

    def test_is_unique_extra(self, extra_factory, tmp_config):
        """Plugins can add additional unique constraints."""
        config = tmp_config(extra_plugins=[ExtraPlugin(MyExtraPlugin, "extra_plugin")])
        extra1 = extra_factory(config=config)
        extra2 = extra_factory(config=config)
        extra1.custom_fields = ["custom"]
        extra2.custom_fields = extra1.custom_fields
        extra1.custom = "dup_extra"
        extra2.custom = extra1.custom

        assert not extra1.is_unique(extra2)


class TestIsUnique:
    """Test `is_unique()`."""

    def test_non_extra(self, mock_extra):
        """Non-extras are unique."""
        assert mock_extra.is_unique(None)

    def test_same_path(self, extra_factory):
        """Extras with the same path are not unique."""
        extra = extra_factory()
        dup_extra = extra_factory(path=extra.path)

        assert not extra.is_unique(dup_extra)

    def test_default(self, extra_factory):
        """Extras with no matching parameters are unique."""
        extra1 = extra_factory()
        extra2 = extra_factory()

        assert extra1.is_unique(extra2)


class TestMerge:
    """Test merging two extras."""

    def test_conflict_persists(self, extra_factory):
        """Don't overwrite any conflicts."""
        extra = extra_factory(path="keep")
        other_extra = extra_factory(path="discard")

        extra.merge(other_extra)

        assert extra.path == "keep"

    def test_merge_non_conflict(self, extra_factory):
        """Apply any non-conflicting fields."""
        extra = extra_factory()
        other_extra = extra_factory(path="keep")
        extra.path = None

        extra.merge(other_extra)

        assert extra.path == "keep"

    def test_none_merge(self, extra_factory):
        """Don't merge in any null values."""
        extra = extra_factory(path="keep")
        other_extra = extra_factory()
        other_extra.path = None

        extra.merge(other_extra)

        assert extra.path == "keep"

    def test_db_delete(self, extra_factory, tmp_session):
        """Remove the other extra from the db if it exists."""
        extra = extra_factory()
        other_extra = extra_factory()
        tmp_session.add(other_extra)
        tmp_session.flush()

        extra.merge(other_extra)

        assert tmp_session.query(Extra).one()


class TestEquality:
    """Test equality of extras."""

    def test_equals(self, extra_factory):
        """Extras with the same fields are equal."""
        extra1 = extra_factory(custom="custom")
        extra2 = extra_factory(dup_extra=extra1)

        assert extra1 == extra2

    def test_not_equals(self, extra_factory):
        """Extras with different designated unique fields are not equal."""
        extra1 = extra_factory()
        extra2 = extra_factory()
        assert extra1.path != extra2.path

        assert extra1 != extra2

    def test_not_equals_not_extra(self, real_extra):
        """Not equal if not comparing two extras."""
        assert real_extra != "test"
