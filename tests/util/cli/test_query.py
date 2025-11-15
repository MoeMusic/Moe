"""Tests the cli util query module."""

from collections.abc import Iterator
from types import FunctionType
from unittest.mock import MagicMock, patch

import pytest

from moe.query import QueryError, QueryType
from moe.util.cli import cli_query, query_parser


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
            cli_query(mock_session, "bad query", QueryType.TRACK)

        assert error.value.code != 0
        mock_query.assert_called_once_with(mock_session, "bad query", QueryType.TRACK)

    def test_empty_query(self, mock_query):
        """Exit with non-zero code if bad query given."""
        mock_query.return_value = []
        mock_session = MagicMock()

        with pytest.raises(SystemExit) as error:
            cli_query(mock_session, "*", QueryType.TRACK)

        assert error.value.code != 0
        mock_query.assert_called_once_with(mock_session, "*", QueryType.TRACK)

    def test_good_query(self, mock_query):
        """Call a good query if items passed."""
        mock_query.return_value = ["item1", "item2"]
        mock_session = MagicMock()

        items = cli_query(mock_session, "*", QueryType.TRACK)

        assert items == ["item1", "item2"]
        mock_query.assert_called_once_with(mock_session, "*", QueryType.TRACK)


class TestQueryParser:
    """Test `query_parser`."""

    def test_query_arg(self):
        """A query is correctly parsed."""
        args = query_parser.parse_args(["my query"])

        assert args.query == "my query"

    def test_default_query_type(self):
        """The query_type defaults to 'track'."""
        args = query_parser.parse_args(["my query"])

        assert args.query_type == QueryType.TRACK

    @pytest.mark.parametrize("album_flag", ["-a", "--album"])
    def test_album_query_type(self, album_flag):
        """The query_type is 'album' if an album flag is specified."""
        args = query_parser.parse_args([album_flag, "my query"])

        assert args.query_type == QueryType.ALBUM

    @pytest.mark.parametrize("extra_flag", ["-e", "--extra"])
    def test_extra_query_type(self, extra_flag):
        """The query_type is 'extra' if an extra flag is specified."""
        args = query_parser.parse_args([extra_flag, "my query"])

        assert args.query_type == QueryType.EXTRA

    @pytest.mark.parametrize("flags", [("-a", "-e"), ("--album", "--extra")])
    def test_mutually_exclusive(self, flags):
        """We can't have more than one query_type."""
        with pytest.raises(SystemExit):
            query_parser.parse_args([*flags, "my query"])

    def test_no_query(self):
        """A query must be specified."""
        with pytest.raises(SystemExit):
            query_parser.parse_args([])
