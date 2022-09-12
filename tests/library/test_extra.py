"""Tests an Extra object."""

import pytest

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


class TestCustomFields:
    """Test getting and setting operations on custom fields."""

    def test_get_custom_field(self, mock_extra):
        """We can get a custom field like a normal attribute."""
        mock_extra._custom_fields["custom"] = "field"

        assert mock_extra.custom == "field"

    def test_set_custom_field(self, mock_extra):
        """We can set a custom field like a normal attribute."""
        mock_extra._custom_fields["custom_key"] = None
        mock_extra.custom_key = "test"

        assert mock_extra._custom_fields["custom_key"] == "test"

    def test_set_non_key(self, mock_extra):
        """Don't set just any attribute as a custom field if the key doesn't exist."""
        mock_extra.custom_key = 1

        with pytest.raises(KeyError):
            assert mock_extra._custom_fields["custom_key"] == 1

    def test_db_persistence(self, mock_extra, tmp_session):
        """Ensure custom fields persist in the database."""
        mock_extra._custom_fields["db"] = "persist"

        tmp_session.add(mock_extra)
        tmp_session.flush()

        db_extra = tmp_session.query(Extra).one()
        assert db_extra.db == "persist"

    def test_plugin_defined_custom_fields(self, extra_factory, tmp_config):
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
