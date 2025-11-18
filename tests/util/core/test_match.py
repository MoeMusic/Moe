"""Tests the logic regarding matching albums and tracks against each other."""

from unittest.mock import patch

import pytest

from moe.util.core import get_match_value, get_matching_tracks
from moe.util.core.match import MatchType, get_field_match_penalty
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


class TestGetFieldMatchPenalty:
    """Test ``get_field_match_penalty()``."""

    @pytest.mark.parametrize(
        ("str_a", "str_b", "assertion"),
        [
            ("test", "test", lambda p: p == 0.0),  # same has 0 penalty
            ("test", "xyz", lambda p: p == 1.0),  # entirely dissimilar as full penalty
            ("test", "tst", lambda p: 0.0 < p < 1.0),  # similar is in between
        ],
    )
    def test_string_match_type(self, str_a, str_b, assertion):
        """Identical strings should have zero penalty."""
        penalty = get_field_match_penalty(str_a, str_b, MatchType.STRING)

        assert assertion(penalty)

    @pytest.mark.parametrize(
        ("bool_a", "bool_b", "penalty"),
        [
            (7, 7, 0.0),  # no penalty for same value
            (7, 6, 1.0),  # full penalty for different value
        ],
    )
    def test_bool_match_type(self, bool_a, bool_b, penalty):
        """MatchType.BOOL should return 0 if the two values are equal."""
        assert get_field_match_penalty(bool_a, bool_b, MatchType.BOOL) == penalty

    @pytest.mark.parametrize(
        ("duration_b_multiplier", "assertion"),
        [
            (1.0, lambda p: p == 0.0),  # identical
            (1.02, lambda p: p == 0.0),  # within tolerance
            (1.06, lambda p: 0.0 < p < 1.0),  # moderate mismatch
            (1.15, lambda p: p == 1.0),  # large mismatch
        ],
    )
    def test_duration_match_type(self, duration_b_multiplier, assertion):
        """Tests duration penalty scenarios."""
        base_duration = 180.0
        duration_b = base_duration * duration_b_multiplier

        penalty = get_field_match_penalty(base_duration, duration_b, MatchType.DURATION)

        assert assertion(penalty)

    @pytest.mark.parametrize(
        "match_type", [MatchType.STRING, MatchType.BOOL, MatchType.DURATION]
    )
    def test_both_values_missing_penalty(self, match_type):
        """A 0.2 penalty is returned when both values are missing."""
        both_missing_penalty = 0.2

        assert get_field_match_penalty(None, None, match_type) == both_missing_penalty

    @pytest.mark.parametrize(
        ("value_a", "value_b", "match_type"),
        [
            ("test", None, MatchType.STRING),
            (None, "test", MatchType.STRING),
            ("", "test", MatchType.STRING),  # empty string counts as missing
            ("test", "", MatchType.STRING),  # empty string counts as missing
            (1, None, MatchType.BOOL),
            (1, 0, MatchType.BOOL),  # falsey values are considered missing
            (None, 1, MatchType.BOOL),
            (0.0, 1.0, MatchType.DURATION),  # falsey values are considered missing
            (1.0, None, MatchType.DURATION),
        ],
    )
    def test_one_value_missing_penalty(self, value_a, value_b, match_type):
        """A 0.1 penalty is returned when one value is missing."""
        one_missing_penalty = 0.1

        assert (
            get_field_match_penalty(value_a, value_b, match_type) == one_missing_penalty
        )
