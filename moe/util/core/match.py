"""All logic regarding matching albums and tracks against each other."""

import difflib
import logging
from typing import Optional

from moe.library import Album, Track

log = logging.getLogger("moe")

__all__ = ["get_match_value", "get_matching_tracks"]

TrackMatch = tuple[Optional[Track], Optional[Track]]
TrackCoord = tuple[
    tuple[int, int], tuple[int, int]
]  # ((a.disc, a.track_num), (b.disc, b.track_num))

MATCH_FIELD_WEIGHTS = {
    "disc": 0.3,
    "title": 0.7,
    "track_num": 0.9,
}  # how much to weigh matches of various fields


def get_matching_tracks(  # noqa: C901 (I don't see benefit from splitting)
    album_a: Album, album_b: Album, match_threshold: float = 0.7
) -> list[TrackMatch]:
    """Returns a list of tuples of track match pairs.

    Args:
        album_a: Album tracks will be matched against ``album_b``.
        album_b: Album tracks will be matched against ``album_a``.
        match_threshold: Threshold match value to consider a track a match with
            another. See ``get_match_value()`` for more info.

    Returns:
        A list of tuples of track match pairs. Each track in ``album_a`` and
        ``album_b`` will appear with its respective track match or ``None`` if no match
        was found. Each tuple represents a match and will be in the form
        ``(album_a_track, album_b_track)``.
    """
    log.debug(
        f"Finding matching tracks. [{album_a=!r}, {album_b=!r}, {match_threshold=!r}]"
    )

    # get all match values for every pair of tracks between both albums
    track_match_values: dict[TrackCoord, float] = {}
    for a_track in album_a.tracks:
        for b_track in album_b.tracks:
            track_match_values[
                ((a_track.disc, a_track.track_num), (b_track.disc, b_track.track_num))
            ] = get_match_value(a_track, b_track, MATCH_FIELD_WEIGHTS)

    # Greedy algorithm that assigns a match to each track pair in order of greatest
    # match value.
    #
    # Potential issues:
    # 1. Consider the following match_value matrix:
    #    a1 a2
    # b1 .8 .9
    # b2  0 .8
    # In this case, a2 will match with b1, while both a1 and b2 will be left with no
    # match. A better solution may be to have (a1, b1) and (a2, b2) as matches.
    #
    # Potential improvements:
    # 1. Solve for greatest sum of match values between all row/col pairs?
    #     a. Not sure if this would actually produce a more desireable solution.
    track_match_values = dict(
        sorted(track_match_values.items(), reverse=True, key=lambda match: match[1])
    )  # sort by match value (descending)
    track_matches: list[TrackMatch] = []  # [(a_track, b_track)]
    for track_pair, match_value in track_match_values.items():
        if match_value < match_threshold:
            continue

        track_matches.append(
            (
                album_a.get_track(track_num=track_pair[0][1], disc=track_pair[0][0]),
                album_b.get_track(track_num=track_pair[1][1], disc=track_pair[1][0]),
            )
        )

        # prevent subsequent matches
        for track_pair2 in track_match_values.keys():
            if track_pair[0] == track_pair2[0] or track_pair[1] == track_pair2[1]:
                track_match_values[track_pair2] = -1

    # pair unmatched tracks with `None`
    for a_track in album_a.tracks:
        if not any(a_track == track_match[0] for track_match in track_matches):
            track_matches.append((a_track, None))
    for b_track in album_b.tracks:
        if not any(b_track == track_match[1] for track_match in track_matches):
            track_matches.append((None, b_track))

    log.debug(f"Found matching tracks. [matches={track_matches!r}]")
    return track_matches


def get_match_value(
    track_a: Track,
    track_b: Track,
    field_weights: dict[str, float] = MATCH_FIELD_WEIGHTS,
) -> float:
    """Returns a similarity "match value" between two tracks on a scale of 0 to 1.

    Args:
        track_a: First Track to compare.
        track_b: Second Track to compare.
        field_weights: Mapping of track fields to weights for how much to value the
            field when considering it for matching two tracks.

    Returns:
        The match value is a weighted sum according to the defined weights for each
        applicable field.
    """
    log.debug(f"Determining match value between tracks. [{track_a=!r}, {track_b=!r}]")

    match_values = []
    for field, weight in field_weights.items():
        value_a = getattr(track_a, field)
        value_b = getattr(track_b, field)

        if field == "title":
            match_value = difflib.SequenceMatcher(None, value_a, value_b).ratio()
        else:
            if value_a == value_b:
                match_value = 1
            else:
                match_value = 0

        match_values.append(match_value * weight)

    match_value = sum(match_values) / sum(field_weights.values())

    log.debug(f"Determined match value between tracks. [{match_value=!r}]")
    return match_value
