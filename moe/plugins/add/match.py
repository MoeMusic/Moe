"""All logic regarding matching albums and tracks against each other."""

from typing import Dict, List, Optional, Tuple

from moe.core.library.album import Album
from moe.core.library.track import Track

__all__: List[str] = []

TrackMatch = Tuple[Optional[Track], Optional[Track]]
TrackCoord = Tuple[
    Tuple[int, int], Tuple[int, int]
]  # ((a.disc, a.track_num), (b.disc, b.track_num))


def get_matching_tracks(
    album_a: Album, album_b: Album, match_threshold: int = 1
) -> List[TrackMatch]:
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
    # get all match values for every pair of tracks between both albums
    track_match_values: Dict[TrackCoord, int] = {}
    for a_track in album_a.tracks:
        for b_track in album_b.tracks:
            track_match_values[
                ((a_track.disc, a_track.track_num), (b_track.disc, b_track.track_num))
            ] = get_match_value(a_track, b_track)

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
    track_matches: List[TrackMatch] = []  # [(a_track, b_track)]
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
    for a_track in album_a.tracks:  # noqa: WPS440
        if not any(a_track == track_match[0] for track_match in track_matches):
            track_matches.append((a_track, None))
    for b_track in album_b.tracks:  # noqa: WPS440
        if not any(b_track == track_match[1] for track_match in track_matches):
            track_matches.append((None, b_track))

    return track_matches


def get_match_value(track_a: Track, track_b: Track) -> int:
    """Returns a similarity "match value" between two tracks on a scale of 0 to 1."""
    if track_a.track_num == track_b.track_num and track_a.disc == track_b.disc:
        return 1

    return 0
