"""Tests the logic regarding matching albums and tracks against each other."""

from unittest.mock import patch

import pytest

from moe.library import MetaAlbum, MetaTrack
from moe.util.core import get_match_value, get_matching_tracks
from moe.util.core.match import FieldType, get_field_match_value
from tests.conftest import album_factory, track_factory


class TestGetMatchingTracks:
    """Test ``get_track_matches()``."""

    def test_full_match(self):
        """All tracks have matches."""
        album_a = album_factory(exists=True)
        album_b = album_factory(dup_album=album_a)

        track_matches = get_matching_tracks(album_a, album_b)

        for track_match in track_matches:
            assert None not in track_match

        for a_track in album_a.tracks:
            assert any(a_track == track_match[0] for track_match in track_matches)
        for b_track in album_b.tracks:
            assert any(b_track == track_match[1] for track_match in track_matches)

        assert len(track_matches) == len(album_a.tracks)

    def test_low_threshold(self):
        """A threshold above 1 should never return a match.

        Any non-matched tracks should be paired with ``None``.
        """
        album_a = album_factory(exists=True)
        album_b = album_factory(dup_album=album_a)

        track_matches = get_matching_tracks(album_a, album_b, match_threshold=1.1)

        for track_match in track_matches:
            assert None in track_match

        for track in album_a.tracks:
            assert (track, None) in track_matches
            assert (None, track) in track_matches

        assert len(track_matches) == len(album_a.tracks) + len(album_b.tracks)

    def test_high_threshold(self):
        """A zero threshold should always return a match."""
        track1 = track_factory(track_num=1, exists=True)
        track2 = track_factory(track_num=2, exists=True)
        assert track1.track_num != track2.track_num

        track_matches = get_matching_tracks(
            track1.album, track2.album, match_threshold=0
        )

        for track_match in track_matches:
            assert None not in track_match

        assert len(track_matches) == 1

    def test_a_longer_than_b(self):
        """Any unmatched tracks should be paired with ``None``."""
        album_a = album_factory(exists=True)
        album_b = album_factory(exists=True)
        track = track_factory(album=album_a, exists=True)

        track_matches = get_matching_tracks(album_a, album_b)

        assert (track, None) in track_matches

    def test_b_longer_than_a(self):
        """Any unmatched tracks should be paired with ``None``."""
        album_a = album_factory(exists=True)
        album_b = album_factory(exists=True)
        track = track_factory(album=album_b, exists=True)

        track_matches = get_matching_tracks(album_a, album_b)

        assert (None, track) in track_matches

    def test_multiple_same_match(self):
        """Any track should not have more than one match."""
        track1 = track_factory(track_num=1, exists=True)
        track2 = track_factory(track_num=2, exists=True)
        track1.album = track2.album

        track3 = track_factory(track_num=3, exists=True)
        track4 = track_factory(track_num=4, exists=True)
        track3.album = track4.album

        track3.title = "not a match"
        assert track2.title != track3.title
        assert track2.title == track1.title
        assert track2.title == track4.title

        def mock_get_value(track_a, track_b):
            if track_a.title == track_b.title:
                return 1
            return 0

        with patch("moe.util.core.match.get_match_value", wraps=mock_get_value):
            track_matches = get_matching_tracks(track1.album, track3.album)

        album1_tracks = [track_match[0] for track_match in track_matches]
        assert album1_tracks.count(track1) == 1
        assert album1_tracks.count(track2) == 1

        album2_tracks = [track_match[1] for track_match in track_matches]
        assert album2_tracks.count(track3) == 1
        assert album2_tracks.count(track4) == 1


class TestMatchValue:
    """Test ``get_match_value()``."""

    HIGH_MATCH_THRESHOLD = 0.9
    LOW_MATCH_THRESHOLD = 0.7  # default match threshold used in `get_matching_tracks`

    def test_same_album(self):
        """Albums with the same values for all used fields should be a perfect match."""
        album1 = album_factory()
        album2 = album_factory(dup_album=album1)

        assert get_match_value(album1, album2) > self.HIGH_MATCH_THRESHOLD

    def test_diff_album(self):
        """Albums with different values for each field should not match."""
        album1 = album_factory()
        album2 = album_factory()
        album1.title = "a"
        album2.title = "b"
        album1.disc_total = 2
        assert album1.title != album2.title
        assert album1.disc_total != album2.disc_total

        assert get_match_value(album1, album2) < self.LOW_MATCH_THRESHOLD

    def test_same_track(self):
        """Tracks with the same values for all used fields should be a perfect match."""
        track1 = track_factory(exists=True)
        track2 = track_factory(dup_track=track1)

        assert get_match_value(track1, track2) > self.HIGH_MATCH_THRESHOLD

    def test_diff_track(self):
        """Tracks with different values for each field should not match."""
        track1 = track_factory(exists=True)
        track2 = track_factory(exists=True)
        track1.title = "a"
        track2.title = "b"
        track1.disc = 2
        assert track1.title != track2.title
        assert track1.disc != track2.disc
        assert track1.track_num != track2.track_num

        assert get_match_value(track1, track2) < self.LOW_MATCH_THRESHOLD

    def test_duration_tolerance_thresholds(self):
        """Test duration matching tolerance thresholds."""
        album = MetaAlbum(title="Test Album", artist="Test Artist")
        track1 = MetaTrack(album=album, title="Test Track", track_num=1, disc=1)
        track2 = MetaTrack(album=album, title="Test Track", track_num=1, disc=1)

        base_duration = 180.0
        track1.duration = base_duration

        # Perfect match: same duration should have no penalty
        track2.duration = base_duration
        perfect_match = get_match_value(track1, track2)

        # Within tolerance: <= 2.5% mismatch should have no penalty
        track2.duration = base_duration * 1.02
        within_tolerance = get_match_value(track1, track2)

        # Moderate mismatch: 6% difference should receive partial penalty
        track2.duration = base_duration * 1.06
        moderate_mismatch = get_match_value(track1, track2)

        # Large mismatch: >= 10% difference should receive full duration penalty
        track2.duration = base_duration * 1.15
        large_mismatch = get_match_value(track1, track2)

        assert within_tolerance == perfect_match
        assert large_mismatch < moderate_mismatch < within_tolerance

    def test_duration_missing_data_penalties(self):
        """Test penalty differences for missing duration data."""
        album = MetaAlbum(title="Test Album", artist="Test Artist")
        track1 = MetaTrack(album=album, title="Test Track", track_num=1, disc=1)
        track2 = MetaTrack(album=album, title="Test Track", track_num=1, disc=1)

        track1.duration = None
        track2.duration = None
        match_with_both_missing = get_match_value(track1, track2)

        track1.duration = 180.0
        track2.duration = None
        match_with_one_missing = get_match_value(track1, track2)

        assert match_with_one_missing < match_with_both_missing

    def test_duration_zero_treated_as_missing(self):
        """Non-positive Duration values should be treated as missing data."""
        album = MetaAlbum(title="Test Album", artist="Test Artist")
        track1 = MetaTrack(album=album, title="Test Track", track_num=1, disc=1)
        track2 = MetaTrack(album=album, title="Test Track", track_num=1, disc=1)

        track1.duration = 0.0
        track2.duration = 180.0
        zero_match = get_match_value(track1, track2)

        track1.duration = None
        track2.duration = 180.0
        none_match = get_match_value(track1, track2)

        assert zero_match == none_match


class TestGetFieldMatchValue:
    """Test ``get_field_match_value()``."""

    def test_string_field_perfect_match(self):
        """Identical strings should have zero penalty."""
        penalty = get_field_match_value("test", "test", FieldType.STRING)
        assert penalty == 0.0

    def test_string_field_complete_mismatch(self):
        """Completely different strings should have a high penalty."""
        penalty = get_field_match_value("test", "xyz", FieldType.STRING)
        assert penalty > 0.9

    def test_string_field_partial_match(self):
        """Partially matching strings should have penalty between 0 and 1."""
        penalty = get_field_match_value("test string", "test", FieldType.STRING)
        assert 0.0 < penalty < 1.0

    def test_integer_field_equal(self):
        """Equal integers should have zero penalty."""
        penalty = get_field_match_value(7, 7, FieldType.INTEGER)
        assert penalty == 0.0

    def test_integer_field_different(self):
        """Different integers should have penalty of 1.0."""
        penalty = get_field_match_value(7, 11, FieldType.INTEGER)
        assert penalty == 1.0

    def test_duration_field_identical(self):
        """Identical durations should have zero penalty."""
        penalty = get_field_match_value(180.0, 180.0, FieldType.DURATION)
        assert penalty == 0.0

    def test_duration_field_within_tolerance(self):
        """Duration within 2.5% tolerance should have zero penalty."""
        base_duration = 180.0
        tolerance_duration = base_duration * 1.02
        penalty = get_field_match_value(
            base_duration, tolerance_duration, FieldType.DURATION
        )
        assert penalty == 0.0

    def test_duration_field_moderate_mismatch(self):
        """Duration with moderate mismatch should have partial penalty."""
        base_duration = 180.0
        moderate_duration = base_duration * 1.06
        penalty = get_field_match_value(
            base_duration, moderate_duration, FieldType.DURATION
        )
        assert 0.0 < penalty < 1.0

    def test_duration_field_large_mismatch(self):
        """Duration with large mismatch (>= 10%) should have penalty of 1.0."""
        base_duration = 180.0
        large_duration = base_duration * 1.15
        penalty = get_field_match_value(
            base_duration, large_duration, FieldType.DURATION
        )
        assert penalty == 1.0

    def test_both_missing_data(self):
        """Both missing values should have consistent penalty for all field types."""
        string_penalty = get_field_match_value(None, None, FieldType.STRING)
        integer_penalty = get_field_match_value(None, None, FieldType.INTEGER)
        duration_penalty = get_field_match_value(None, None, FieldType.DURATION)

        assert string_penalty == integer_penalty == duration_penalty == 0.1

    def test_one_missing_data(self):
        """One missing value should have consistent penalty for all field types."""
        string_penalty = get_field_match_value("test", None, FieldType.STRING)
        integer_penalty = get_field_match_value(42, None, FieldType.INTEGER)
        duration_penalty = get_field_match_value(180.0, None, FieldType.DURATION)

        assert string_penalty == integer_penalty == duration_penalty == 0.2
