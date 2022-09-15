"""Tests an Extra object."""

import moe
from moe.config import ExtraPlugin


class MyExtraPlugin:
    """Plugin that implements the extra hooks for testing."""

    @staticmethod
    @moe.hookimpl
    def create_custom_extra_fields(config):
        """Create a new custom field."""
        return {"no_default": None, "default": "value"}


class TestHooks:
    """Test extra hooks."""

    def test_create_custom_fields(self, extra_factory, tmp_config):
        """Plugins can define new custom fields."""
        config = tmp_config(extra_plugins=[ExtraPlugin(MyExtraPlugin, "extra_plugin")])
        extra = extra_factory(config)

        assert not extra.no_default
        assert extra.default == "value"


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
