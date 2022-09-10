"""Core musicbrainz api.

The ``musicbrainz`` core plugin provides the following functionality:

* Imports metadata from musicbrainz when adding a track or album to the library.
* Optionally updates a musicbrainz collection when items are added or removed from the
  library.

Note:
    This plugin is enabled by default.

See Also:
    * https://musicbrainz.org/doc/MusicBrainz_API/
    * https://python-musicbrainzngs.readthedocs.io/en/latest/api/
"""

import datetime
import logging
from typing import Any, Callable, Dict, List, Optional, Set

import dynaconf
import musicbrainzngs
import pkg_resources

import moe
from moe.config import Config
from moe.library.album import Album
from moe.library.lib_item import LibItem
from moe.library.track import Track

__all__ = [
    "MBAuthError",
    "add_releases_to_collection",
    "get_album_by_id",
    "get_matching_album",
    "rm_releases_from_collection",
    "set_collection",
    "update_album",
]

log = logging.getLogger("moe.mb")

MAX_SEARCH_LIMIT = 100
"""Max number of entries that can be returned from a search to musicbrainz. This limit
is enforced by their api."""


class MBAuthError(Exception):
    """Musicbrainz user authentication error."""


musicbrainzngs.set_useragent(
    "moe",
    pkg_resources.get_distribution("moe").version,
    contact="https://mrmoe.readthedocs.io/en/latest/index.html",
)

# information to include in the release api query
RELEASE_INCLUDES = [
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
def add_config_validator(settings: dynaconf.base.LazySettings):
    """Validates musicbrainz plugin configuration settings."""
    login_required = False

    settings.validators.register(
        dynaconf.Validator(
            "musicbrainz.collection.auto_add",
            "musicbrainz.collection.auto_remove",
            default=False,
        )
    )

    if settings.get("musicbrainz.collection.auto_add", False) or settings.get(
        "musicbrainz.collection.auto_remove", False
    ):
        login_required = True
        settings.validators.register(
            dynaconf.Validator("musicbrainz.collection.collection_id", must_exist=True)
        )

    if login_required:
        settings.validators.register(
            dynaconf.Validator(
                "musicbrainz.username", "musicbrainz.password", must_exist=True
            )
        )


@moe.hookimpl
def import_candidates(config: Config, album: Album) -> Album:
    """Applies musicbrainz metadata changes to a given album.

    Args:
        config: Moe config.
        album: Original album used to search musicbrainz for a matching album.

    Returns:
        A new album containing all the corrected metadata from musicbrainz. Note, this
        album is not complete, as it will not contain any references to the filesystem.
    """
    return get_matching_album(album)


@moe.hookimpl
def post_remove(config: Config, item: LibItem):
    """Removes a release from a collection when removed from the library."""
    if not config.settings.musicbrainz.collection.auto_remove:
        return

    if isinstance(item, Album) and item.mb_album_id:
        try:
            rm_releases_from_collection(config, {item.mb_album_id})
        except MBAuthError as err:
            log.error(err)


@moe.hookimpl
def process_new_items(config: Config, items: List[LibItem]):
    """Updates a user collection in musicbrainz with new releases."""
    if not config.settings.musicbrainz.collection.auto_add:
        return

    releases = set()
    for item in items:
        if isinstance(item, Album) and item.mb_album_id:
            releases.add(item.mb_album_id)

    if releases:
        try:
            add_releases_to_collection(config, releases)
        except MBAuthError as err:
            log.error(err)


def add_releases_to_collection(
    config: Config, releases: Set[str], collection: Optional[str] = None
) -> None:
    """Adds releases to a musicbrainz collection.

    Args:
        config: Moe config.
        releases: Musicbrainz release IDs to add to the collection.
        collection: Musicbrainz collection ID to add the releases to.
            If not given, defaults to the ``musicbrainz.collection.collection_id``
            config option.

    Raises:
        MBAuthError: Invalid musicbrainz user credentials in the configuration.
    """
    collection = collection or config.settings.musicbrainz.collection.collection_id

    log.debug(
        f"Adding releases to musicbrainz collection. [{releases=!r}, {collection=!r}]"
    )

    _mb_auth_call(
        config,
        musicbrainzngs.add_releases_to_collection,
        collection=collection,
        releases=releases,
    )

    log.info(
        f"Added releases to musicbrainz collection. [{releases=!r}, {collection=!r}]"
    )


def rm_releases_from_collection(
    config: Config, releases: Set[str], collection: Optional[str] = None
) -> None:
    """Removes releases from a musicbrainz collection.

    Args:
        config: Moe config.
        releases: Musicbrainz release IDs to remove from the collection.
        collection: Musicbrainz collection ID to remove the releases from.
            If not given, defaults to the ``musicbrainz.collection.collection_id``
            config option.

    Raises:
        MBAuthError: Invalid musicbrainz user credentials in the configuration.
    """
    collection = collection or config.settings.musicbrainz.collection.collection_id

    log.debug(
        "Removing releases from musicbrainz collection. "
        f"[{releases=!r}, {collection=!r}]"
    )

    _mb_auth_call(
        config,
        musicbrainzngs.remove_releases_from_collection,
        collection=collection,
        releases=releases,
    )

    log.info(
        "Removed releases from musicbrainz collection. "
        f"[{releases=!r}, {collection=!r}]"
    )


def _mb_auth_call(config: Config, api_func: Callable, **kwargs) -> Any:
    """Call a musicbrainz API function that requires user authentication.

    Args:
        config: Moe config. Used to access credentials for user authentication.
        api_func: Musicbrainz API function to call.
        **kwargs: Keyword arguments to pass to the API function call.

    Returns:
        The return value of the API function called.

    Raises:
        MBAuthError: Invalid user credentials in the configuration.
    """
    if config:
        musicbrainzngs.auth(
            config.settings.musicbrainz.username, config.settings.musicbrainz.password
        )

    try:
        return api_func(**kwargs)
    except musicbrainzngs.AuthenticationError as err:
        raise MBAuthError("User authentication with musicbrainz failed.") from err


def set_collection(
    config: Config, releases: Set[str], collection: Optional[str] = None
) -> None:
    """Sets a musicbrainz collection with the given releases.

    The releases in the collection will be set to ``releases``, adding any releases not
    present in the collection, as well as removing any extraneous releases.

    Args:
        config: Moe config.
        releases: Musicbrainz releases to set the collection to.
        collection: Musicbrainz collection ID for the collection to set.
            If not given, defaults to the ``musicbrainz.collection.collection_id``
            config option.

    Raises:
        MBAuthError: Invalid user credentials in the configuration.
    """
    collection = collection or config.settings.musicbrainz.collection.collection_id

    log.debug("Setting musicbrainz collection. " f"[{releases=!r}, {collection=!r}]")

    current_releases = []
    num_searches = 0
    limit = MAX_SEARCH_LIMIT
    while len(current_releases) == limit * num_searches:  # hitting the search limit
        result = _mb_auth_call(
            config,
            musicbrainzngs.get_releases_in_collection,
            collection=collection,
            limit=limit,
            offset=limit * num_searches,
        )
        for release in result["collection"]["release-list"]:
            current_releases.append(release["id"])

        num_searches += 1
    current_releases = set(current_releases)

    stale_releases = current_releases.difference(releases)
    rm_releases_from_collection(config, stale_releases, collection)

    new_releases = releases.difference(current_releases)
    add_releases_to_collection(config, new_releases, collection)


def get_matching_album(album: Album) -> Album:
    """Gets a matching musicbrainz album for a given album.

    Args:
        album: Album used to search for the release.

    Returns:
        Dictionary of release information. See the ``tests/musicbrainz/resources``
        directory for an idea of what this contains.
    """
    if album.mb_album_id:
        return get_album_by_id(album.mb_album_id)

    log.debug(f"Determing matching releases from musicbrainz. [{album=!r}]")

    search_criteria: Dict = {}
    search_criteria["artist"] = album.artist
    search_criteria["release"] = album.title
    search_criteria["date"] = album.date.isoformat()

    releases = musicbrainzngs.search_releases(limit=1, **search_criteria)

    release = releases["release-list"][0]
    release_id = release["id"]

    log.info(f"Determined matching release from musicbrainz. [match={release_id!r}]")

    return get_album_by_id(release_id)  # searching by id provides more info


def get_album_by_id(release_id: str) -> Album:
    """Gets a musicbrainz album from a release ID.

    Args:
        release_id: Musicbrainz release ID to search.

    Returns:
        Dictionary of release information. See ``tests/resources/musicbrainz`` for
        an idea of what this contains. Note this is a different dictionary that what
        is returned from searching by fields for a release. Notably, searching by an id
        results in more information including track information.
    """
    log.debug(f"Fetching release from musicbrainz. [release={release_id!r}]")

    release = musicbrainzngs.get_release_by_id(release_id, includes=RELEASE_INCLUDES)

    log.info(f"Fetched release from musicbrainz. [release={release_id!r}]")

    return _create_album(release["release"])


def _create_album(release: Dict) -> Album:
    """Creates an album from a given musicbrainz release."""
    log.debug(f"Creating album from musicbrainz release. [release={release['id']!r}]")

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

    log.debug(f"Created album from musicbrainz release. [{album=!r}]")
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


def update_album(album: Album):
    """Updates an album with metadata from musicbrainz.

    Args:
        album: Album to update.

    Raises:
        ValueError: ``album`` has no ``mb_album_id``.
    """
    log.debug(f"Updating album with musicbrainz metadata. [{album=!r}]")

    if not album.mb_album_id:
        raise ValueError(
            "Unable to update album, no musicbrainz id found. [{album=!r}]"
        )

    album.merge(get_album_by_id(album.mb_album_id), overwrite=True)
