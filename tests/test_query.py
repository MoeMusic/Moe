"""Test the core query module."""

import pathlib
from unittest.mock import Mock

from moe.core import library, query


class TestParseQuery:
    """Test the query string parsing _parse_query()."""

    def test_basic(self):
        """Simplest case field:value test."""
        matches = query._parse_query("field:value")

        assert matches[0]["field"] == "field"
        assert matches[0]["separator"] == ":"
        assert matches[0]["value"] == "value"
        assert len(matches) == 1

    def test_escaped_colon(self):
        """Values can contain escaped colons."""
        matches = query._parse_query(r"field:val\:ue")

        assert matches[0]["field"] == "field"
        assert matches[0]["value"] == "val:ue"
        assert len(matches) == 1

    def test_multiple(self):
        """Queries can contain more than one field:value."""
        matches = query._parse_query(r"field:value field2:value2")

        assert matches[0]["field"] == "field"
        assert matches[0]["value"] == "value"
        assert matches[1]["field"] == "field2"
        assert matches[1]["value"] == "value2"
        assert len(matches) == 2

    def test_value_spaces(self):
        """Values can contain arbitrary whitespace.

        The only exception is immediately after the colon.
        """
        matches = query._parse_query(r"field:val u e")

        assert matches[0]["field"] == "field"
        assert matches[0]["value"] == "val u e"
        assert len(matches) == 1

    def test_value_spaces_multiple(self):
        """Values shouldn't match the next field if it exists.

        This can become tricky to match if the value also contains whitespace.
        """
        matches = query._parse_query(r"field:val u e field2:value2")

        assert matches[0]["field"] == "field"
        assert matches[0]["value"] == "val u e"
        assert matches[1]["field"] == "field2"
        assert matches[1]["value"] == "value2"
        assert len(matches) == 2

    def test_unescaped_colons(self):
        """Unescaped colons are fine as long as they don't look like 'field:value'."""
        matches = query._parse_query(r"field:Vol 1: field2:Vol: 1")

        assert matches[0]["field"] == "field"
        assert matches[0]["value"] == "Vol 1:"
        assert matches[1]["field"] == "field2"
        assert matches[1]["value"] == "Vol: 1"
        assert len(matches) == 2

    def test_regex_value(self):
        """Regular expression values are indicated by a '::' separator."""
        matches = query._parse_query(r"field::A.*")

        assert matches[0]["field"] == "field"
        assert matches[0]["separator"] == "::"
        assert matches[0]["value"] == "A.*"
        assert len(matches) == 1


class TestQuery:
    """Test actual query."""

    def test_invalid_query(self):
        """Invalid queries should return an empty list."""
        matches = query.query(r"invalid", Mock())

        assert matches == []

    def test_valid_query(self, tmp_session):
        """Simplest query."""
        tmp_session.add(library.Track(path=pathlib.Path("/path")))

        tracks = query.query("path:/path", tmp_session)

        assert tracks

    def test_case_insensitive(self, tmp_session):
        """Queries should be case-insensitive."""
        tmp_session.add(library.Track(path=pathlib.Path("/PATH")))

        tracks = query.query("path:/path", tmp_session)

        assert tracks

    def test_regex(self, tmp_session):
        """Queries can use regular expression matching."""
        tmp_session.add(library.Track(path=pathlib.Path("/path")))

        tracks = query.query("path::path", tmp_session)

        assert tracks
