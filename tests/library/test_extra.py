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
