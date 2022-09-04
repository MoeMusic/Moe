"""Tests an Extra object."""


class TestGetExisting:
    """Test we can match an existing extra based on unique attributes."""

    def test_by_path(self, mock_extra_factory, tmp_session):
        """Get an exisiting extra from a matching path."""
        extra1 = mock_extra_factory()
        extra2 = mock_extra_factory()
        extra1.path = extra2.path

        tmp_session.merge(extra2)

        assert extra1.get_existing()


class TestEquality:
    """Test equality of extras."""

    def test_equals_path(self, real_extra_factory):
        """Extras with the same `path` are equal."""
        extra1 = real_extra_factory()
        extra2 = real_extra_factory()
        assert extra1 != extra2

        extra1.path = extra2.path
        assert extra1 == extra2

    def test_not_equals(self, real_extra_factory):
        """Extras with different designated unique fields are not equal."""
        extra1 = real_extra_factory()
        extra2 = real_extra_factory()
        assert extra1.path != extra2.path

        assert extra1 != extra2

    def test_not_equals_not_extra(self, real_extra):
        """Not equal if not comparing two extras."""
        assert real_extra != "test"
