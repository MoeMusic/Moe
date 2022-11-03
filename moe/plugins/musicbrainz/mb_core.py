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
from pathlib import Path
from typing import Any, Callable, Optional, cast

import dynaconf
import mediafile
import musicbrainzngs
import pkg_resources

import moe
from moe import config
from moe.library import Album, LibItem, MetaAlbum, MetaTrack, Track
from moe.plugins.moe_import.import_core import CandidateAlbum
from moe.util.core import match

__all__ = [
    "MBAuthError",
    "add_releases_to_collection",
    "get_album_by_id",
    "get_candidate_by_id",
    "get_track_by_id",
    "rm_releases_from_collection",
    "set_collection",
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
    "annotation",
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
def create_custom_album_fields() -> dict[str, Any]:  # type: ignore
    """Adds relevant musicbrainz fields to an album."""
    return {"mb_album_id": None}


@moe.hookimpl
def create_custom_track_fields() -> dict[str, Any]:  # type: ignore
    """Adds relevant musicbrainz fields to a track."""
    return {"mb_track_id": None}


@moe.hookimpl
def get_candidates(album: Album) -> list[CandidateAlbum]:
    """Applies musicbrainz metadata changes to a given album.

    Args:
        album: Original album used to search musicbrainz for a matching album.

    Returns:
        A new album containing all the corrected metadata from musicbrainz. Note, this
        album is not complete, as it will not contain any references to the filesystem.
    """
    log.debug(f"Getting candidate albums from musicbrainz. [{album=!r}]")

    search_criteria: dict = {}
    search_criteria["artist"] = album.artist
    search_criteria["release"] = album.title
    search_criteria["date"] = album.date.isoformat()
    search_criteria["mediums"] = album.disc_total
    if album.barcode:
        search_criteria["barcode"] = album.barcode
    if album.catalog_nums:
        search_criteria["catno"] = next(iter(album.catalog_nums))  # get any cat_num
    if album.label:
        search_criteria["label"] = album.label
    if album.mb_album_id:
        search_criteria["reid"] = album.mb_album_id
    if album.media:
        search_criteria["format"] = album.media
    if album.track_total:
        search_criteria["tracks"] = album.track_total

    releases = musicbrainzngs.search_releases(limit=5, **search_criteria)

    candidates = []
    for release in releases["release-list"]:
        candidates.append(get_candidate_by_id(album, release["id"]))

    if not candidates:
        log.warning("No candidate albums found.")
    else:
        log.info(f"Found candidate albums. [{candidates=!r}]")

    return candidates


@moe.hookimpl
def process_removed_items(items: list[LibItem]):
    """Removes a release from a collection when removed from the library."""
    if not config.CONFIG.settings.musicbrainz.collection.auto_remove:
        return

    mb_ids = []
    for item in items:
        if isinstance(item, Album) and item.mb_album_id:
            mb_ids.append(item.mb_album_id)

    if mb_ids:
        try:
            rm_releases_from_collection(set(mb_ids))
        except MBAuthError as err:
            log.error(err)


@moe.hookimpl
def process_new_items(items: list[LibItem]):
    """Updates a user collection in musicbrainz with new releases."""
    if not config.CONFIG.settings.musicbrainz.collection.auto_add:
        return

    releases = set()
    for item in items:
        if isinstance(item, Album) and item.mb_album_id:
            releases.add(item.mb_album_id)

    if releases:
        try:
            add_releases_to_collection(releases)
        except MBAuthError as err:
            log.error(err)


@moe.hookimpl
def read_custom_tags(
    track_path: Path, album_fields: dict[str, Any], track_fields: dict[str, Any]
) -> None:
    """Read and set musicbrainz release IDs from a track file."""
    audio_file = mediafile.MediaFile(track_path)

    album_fields["mb_album_id"] = audio_file.mb_albumid
    track_fields["mb_track_id"] = audio_file.mb_releasetrackid


@moe.hookimpl
def sync_metadata(item: LibItem):
    """Sync musibrainz metadata for associated items."""
    if isinstance(item, Album) and hasattr(item, "mb_album_id"):
        item.merge(get_album_by_id(item.mb_album_id), overwrite=True)
    elif isinstance(item, Track) and hasattr(item, "mb_track_id"):
        item = cast(Track, item)
        item.merge(
            get_track_by_id(item.mb_track_id, item.album_obj.mb_album_id),
            overwrite=True,
        )


@moe.hookimpl
def write_custom_tags(track: Track):
    """Write musicbrainz ID fields as tags."""
    audio_file = mediafile.MediaFile(track.path)

    audio_file.mb_albumid = track.album_obj.mb_album_id
    audio_file.mb_releasetrackid = track.mb_track_id

    audio_file.save()


def add_releases_to_collection(
    releases: set[str], collection: Optional[str] = None
) -> None:
    """Adds releases to a musicbrainz collection.

    Args:
        releases: Musicbrainz release IDs to add to the collection.
        collection: Musicbrainz collection ID to add the releases to.
            If not given, defaults to the ``musicbrainz.collection.collection_id``
            config option.

    Raises:
        MBAuthError: Invalid musicbrainz user credentials in the configuration.
    """
    collection = (
        collection or config.CONFIG.settings.musicbrainz.collection.collection_id
    )

    log.debug(
        f"Adding releases to musicbrainz collection. [{releases=!r}, {collection=!r}]"
    )

    _mb_auth_call(
        musicbrainzngs.add_releases_to_collection,
        collection=collection,
        releases=releases,
    )

    log.info(
        f"Added releases to musicbrainz collection. [{releases=!r}, {collection=!r}]"
    )


def rm_releases_from_collection(
    releases: set[str], collection: Optional[str] = None
) -> None:
    """Removes releases from a musicbrainz collection.

    Args:
        releases: Musicbrainz release IDs to remove from the collection.
        collection: Musicbrainz collection ID to remove the releases from.
            If not given, defaults to the ``musicbrainz.collection.collection_id``
            config option.

    Raises:
        MBAuthError: Invalid musicbrainz user credentials in the configuration.
    """
    collection = (
        collection or config.CONFIG.settings.musicbrainz.collection.collection_id
    )

    log.debug(
        "Removing releases from musicbrainz collection. "
        f"[{releases=!r}, {collection=!r}]"
    )

    _mb_auth_call(
        musicbrainzngs.remove_releases_from_collection,
        collection=collection,
        releases=releases,
    )

    log.info(
        "Removed releases from musicbrainz collection. "
        f"[{releases=!r}, {collection=!r}]"
    )


def _mb_auth_call(api_func: Callable, **kwargs) -> Any:
    """Call a musicbrainz API function that requires user authentication.

    Args:
        api_func: Musicbrainz API function to call.
        **kwargs: Keyword arguments to pass to the API function call.

    Returns:
        The return value of the API function called.

    Raises:
        MBAuthError: Invalid user credentials in the configuration.
    """
    musicbrainzngs.auth(
        config.CONFIG.settings.musicbrainz.username,
        config.CONFIG.settings.musicbrainz.password,
    )

    try:
        return api_func(**kwargs)
    except musicbrainzngs.AuthenticationError as err:
        raise MBAuthError("User authentication with musicbrainz failed.") from err


def set_collection(releases: set[str], collection: Optional[str] = None) -> None:
    """Sets a musicbrainz collection with the given releases.

    The releases in the collection will be set to ``releases``, adding any releases not
    present in the collection, as well as removing any extraneous releases.

    Args:
        releases: Musicbrainz releases to set the collection to.
        collection: Musicbrainz collection ID for the collection to set.
            If not given, defaults to the ``musicbrainz.collection.collection_id``
            config option.

    Raises:
        MBAuthError: Invalid user credentials in the configuration.
    """
    collection = (
        collection or config.CONFIG.settings.musicbrainz.collection.collection_id
    )

    log.debug("Setting musicbrainz collection. " f"[{releases=!r}, {collection=!r}]")

    current_releases = []
    num_searches = 0
    limit = MAX_SEARCH_LIMIT
    while len(current_releases) == limit * num_searches:  # hitting the search limit
        result = _mb_auth_call(
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
    rm_releases_from_collection(stale_releases, collection)

    new_releases = releases.difference(current_releases)
    add_releases_to_collection(new_releases, collection)


def get_album_by_id(release_id: str) -> MetaAlbum:
    """Returns an album from musicbrainz with the given release ID."""
    log.debug(f"Fetching release from musicbrainz. [release={release_id!r}]")

    release = musicbrainzngs.get_release_by_id(release_id, includes=RELEASE_INCLUDES)

    log.info(f"Fetched release from musicbrainz. [release={release_id!r}]")

    return _create_album(release["release"])


def get_candidate_by_id(album: Album, release_id: str) -> CandidateAlbum:
    """Returns a candidate for ``album`` from the given ``release_id``."""
    log.debug(f"Fetching release from musicbrainz. [release={release_id!r}]")
    release = musicbrainzngs.get_release_by_id(release_id, includes=RELEASE_INCLUDES)[
        "release"
    ]
    log.info(f"Fetched release from musicbrainz. [release={release_id!r}]")

    candidate_album = _create_album(release)

    sub_header_info = []
    if date := _get_release_date(release):
        sub_header_info.append(str(date.year))
    if disambiguation := release.get("disambiguation"):
        sub_header_info.append(disambiguation)

    return CandidateAlbum(
        album=candidate_album,
        match_value=match.get_match_value(album, candidate_album),
        source_str=f"Musicbrainz: {release_id}",
        sub_header_info=sub_header_info,
    )


def _create_album(release: dict) -> MetaAlbum:
    """Creates an album from a given musicbrainz release."""
    log.debug(f"Creating album from musicbrainz release. [release={release['id']!r}]")

    catalog_nums = set()
    if release["label-info-list"]:
        label = release["label-info-list"][0]["label"]["name"]
        for label_info in release["label-info-list"]:
            if label_info.get("catalog-number"):
                catalog_nums.add(label_info["catalog-number"])
    else:
        label = None
    if not catalog_nums:
        catalog_nums = None

    album = MetaAlbum(
        artist=_flatten_artist_credit(release["artist-credit"]),
        barcode=release.get("barcode"),
        catalog_nums=catalog_nums,
        country=release.get("country"),
        date=_get_release_date(release),
        disc_total=int(release["medium-count"]),
        label=label,
        mb_album_id=release["id"],
        media=release["medium-list"][0].get("format"),
        original_date=_get_original_date(release),
        title=release["title"],
    )
    for medium in release["medium-list"]:
        for track in medium["track-list"]:
            MetaTrack(
                album=album,
                track_num=int(track["position"]),
                artist=_flatten_artist_credit(track["recording"]["artist-credit"]),
                disc=int(medium["position"]),
                mb_track_id=track["id"],
                title=track["recording"]["title"],
            )
    album.track_total = len(album.tracks)

    log.debug(f"Created album from musicbrainz release. [{album=!r}]")
    return album


def _flatten_artist_credit(artist_credit: list[dict]) -> str:
    """Given a musicbrainz formatted artist-credit, return the full artist name."""
    full_artist = ""
    for artist in artist_credit:
        if isinstance(artist, str):
            full_artist += artist
        else:
            full_artist += artist["artist"]["name"]

    return full_artist


def _get_release_date(release: dict) -> Optional[datetime.date]:
    """Gets the release date from a given musicbrainz release."""
    date = release.get("date")
    if date:
        return _parse_date(date)

    return _get_original_date(release)


def _get_original_date(release: dict) -> Optional[datetime.date]:
    """Gets the original release date from a given musicbrainz release."""
    return _parse_date(release["release-group"]["first-release-date"])


def _parse_date(date: Optional[str]) -> Optional[datetime.date]:
    """Parses a date from a musicbrainz release."""
    if not date:
        return None

    date_parts = date.split("-")

    year = int(date_parts[0])
    try:
        month = int(date_parts[1])
    except IndexError:
        month = 1
    try:
        day = int(date_parts[2])
    except IndexError:
        day = 1

    return datetime.date(year, month, day)


def get_track_by_id(track_id: str, album_id: str) -> MetaTrack:
    """Gets a musicbrainz track from a given track and release id.

    Args:
        track_id: Musicbrainz track ID to match.
        album_id: Release album ID the track belongs to.

    Returns:
        A track containing all metadata associated with the given IDs.

    Raises:
        ValueError: Couldn't find track based on given ``track_id`` and ``album_id``.
    """
    log.debug(f"Fetching track from musicbrainz. [{track_id=!r}, {album_id=!r}]")

    album = get_album_by_id(album_id)
    for track in album.tracks:
        if track.mb_track_id == track_id:
            log.info(f"Fetched track from musicbrainz. [{track=!r}]")
            return track

    raise ValueError(
        f"Given track or album id could not be found. [{track_id=!r}, {album_id=!r}]"
    )
