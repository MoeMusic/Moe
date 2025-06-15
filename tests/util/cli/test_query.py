"""Tests the cli util query module."""

from collections.abc import Iterator
from types import FunctionType
from unittest.mock import MagicMock, patch

import pytest

from moe.query import QueryError
from moe.util.cli import cli_query


@pytest.fixture
def mock_query() -> Iterator[FunctionType]:
    """Mock a database query call.

    Use ``mock_query.return_value` to set the return value of a query.

    Yields:
        Mock query
    """
    with patch("moe.util.cli.query.query", autospec=True) as mock_query:
        yield mock_query


class TestCLIQuery:
    """Test `cli_query`."""

    def test_bad_query(self, mock_query):
        """Exit with non-zero code if bad query given."""
        mock_query.side_effect = QueryError
        mock_session = MagicMock()

        with pytest.raises(SystemExit) as error:
            cli_query(mock_session, "bad query", "track")

        assert error.value.code != 0
        mock_query.assert_called_once_with(mock_session, "bad query", "track")

    def test_empty_query(self, mock_query):
        """Exit with non-zero code if bad query given."""
        mock_query.return_value = []
        mock_session = MagicMock()

        with pytest.raises(SystemExit) as error:
            cli_query(mock_session, "*", "track")

        assert error.value.code != 0
        mock_query.assert_called_once_with(mock_session, "*", "track")
