"""Musicbrainz integration plugin.

For more information on the Musicbrainz API see the following:
https://musicbrainz.org/doc/MusicBrainz_API/
https://python-musicbrainzngs.readthedocs.io/en/latest/api/
"""

import datetime
from typing import Dict, List, Optional

import musicbrainzngs
import pkg_resources
import questionary
from sqlalchemy.orm.session import Session

import moe
from moe.core.config import Config
from moe.core.library.album import Album
from moe.core.library.track import Track
from moe.plugins import add

__all__: List[str] = []

musicbrainzngs.set_useragent(
    "moe",
    pkg_resources.get_distribution("moe").version,
    contact="https://mrmoe.readthedocs.io/en/latest/index.html",
)

# information to include in the release api query
RELEASE_INCLUDES = [  # noqa: WPS407
    "aliases",
    "artists",
    "artist-credits",
    "artist-rels",
    "labels",
    "media",
    "recordings",
    "recording-level-rels",
    "release-groups",
    "work-level-rels",
    "work-rels",
]


@moe.hookimpl
def add_prompt_choice(prompt_choices: List[add.PromptChoice]):
    """Adds the ``apply`` and ``abort`` prompt choices to the user prompt."""
    prompt_choices.append(
        add.PromptChoice(
            title="Enter Musicbrainz ID",
            shortcut_key="m",
            func=_enter_id,
        )
    )


@moe.hookimpl
def import_album(config: Config, session: Session, album: Album) -> Album:
    """Applies musicbrainz metadata changes to a given album.

    Args:
        config: Moe config.
        session: Current db session.
        album: Original album used to search musicbrainz for a matching album.

    Returns:
        A new album containing all the corrected metadata from musicbrainz. This album
        is not complete, as it will not contain any references to the filesystem.
    """
    release = _get_matching_release(album)

    return _create_album(release)


def _get_matching_release(album: Album) -> Dict:
    """Gets a matching musicbrainz release for a given album.

    Args:
        album: Album used to search for the release.

    Returns:
        Dictionary of release information. See ``tests/resources/musicbrainz`` for
        an idea of what this contains.
    """
    if album.mb_album_id:
        return _get_release_by_id(album.mb_album_id)

    search_criteria: Dict = {}
    search_criteria["artist"] = album.artist
    search_criteria["release"] = album.title
    search_criteria["date"] = album.date.isoformat()

    releases = musicbrainzngs.search_releases(limit=1, **search_criteria)

    release = releases["release-list"][0]
    return _get_release_by_id(release["id"])  # searching by id provides more info


def _get_release_by_id(release_id: str) -> Dict:
    """Gets a musicbrainz release from it's ID.

    Args:
        release_id: Musicbrainz release ID to search.

    Returns:
        Dictionary of release information. See ``tests/resources/musicbrainz`` for
        an idea of what this contains. Note this is a different dictionary that what
        is returned from searching by fields for a release. Notably, searching by an id
        results in more information including track information.
    """
    # https://python-musicbrainzngs.readthedocs.io/en/latest/api/#musicbrainzngs.get_release_by_id

    release = musicbrainzngs.get_release_by_id(release_id, includes=RELEASE_INCLUDES)
    return release["release"]


def _create_album(release: Dict) -> Album:
    """Creates an album from a given musicbrainz release."""
    date = release["date"].split("-")
    year = int(date[0])
    try:
        month = int(date[1])
    except IndexError:
        month = 1
    try:
        day = int(date[2])
    except IndexError:
        day = 1

    album = Album(
        artist=_flatten_artist_credit(release["artist-credit"]),
        date=datetime.date(year, month, day),
        disc_total=int(release["medium-count"]),
        mb_album_id=release["id"],
        title=release["title"],
        path=None,  # type: ignore # this will get set in `add_prompt`
    )
    for medium in release["medium-list"]:
        for track in medium["track-list"]:
            Track(
                album=album,
                track_num=int(track["position"]),
                path=None,  # type: ignore # this will get set in `add_prompt`
                artist=_flatten_artist_credit(track["recording"]["artist-credit"]),
                disc=int(medium["position"]),
                mb_track_id=track["id"],
                title=track["recording"]["title"],
            )
    return album


def _flatten_artist_credit(artist_credit: List[Dict]) -> str:
    """Given a musicbrainz formatted artist-credit, return the full artist name."""
    full_artist = ""
    for artist in artist_credit:
        if isinstance(artist, str):
            full_artist += artist
        else:
            full_artist += artist["artist"]["name"]

    return full_artist


def _enter_id(
    config: Config,
    session: Session,
    old_album: Album,
    new_album: Album,
) -> Optional[Album]:
    """Re-run the add prompt with the inputted Musibrainz release."""
    mb_id = questionary.text("Enter Musicbrainz ID: ").ask()

    release = _get_release_by_id(mb_id)
    album = _create_album(release)

    return add.run_prompt(config, session, old_album, album)
