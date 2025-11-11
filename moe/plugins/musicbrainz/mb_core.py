"""Core musicbrainz API.

See Also:
    * https://musicbrainz.org/doc/MusicBrainz_API/
    * https://python-musicbrainzngs.readthedocs.io/en/latest/api/
"""

from __future__ import annotations

import datetime
import importlib.metadata
import logging
from typing import TYPE_CHECKING, Any, Callable, cast

import dynaconf.base
import mediafile
import musicbrainzngs

import moe
from moe import config
from moe.library import Album, LibItem, MergeStrategy, MetaAlbum, MetaTrack, Track
from moe.moe_import import CandidateAlbum
from moe.util.core import match

if TYPE_CHECKING:
    from pathlib import Path

    from sqlalchemy.orm.session import Session

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
    importlib.metadata.version("moe"),
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
def add_config_validator(settings: dynaconf.base.LazySettings) -> None:
    """Validates musicbrainz plugin configuration settings."""
    login_required = False

    settings.validators.register(  # type: ignore[reportCallIssue]
        dynaconf.Validator("musicbrainz.search_limit", default=5, gte=1)
    )

    settings.validators.register(  # type: ignore[reportCallIssue]
        dynaconf.Validator(
            "musicbrainz.collection.auto_add",
            "musicbrainz.collection.auto_remove",
            default=False,
        )
    )

    if settings.get("musicbrainz.collection.auto_add", False) or settings.get(  # type: ignore[reportCallIssue]
        "musicbrainz.collection.auto_remove", False
    ):  # type: ignore[reportCallIssue]
        login_required = True
        settings.validators.register(  # type: ignore[reportCallIssue]
            dynaconf.Validator("musicbrainz.collection.collection_id", must_exist=True)
        )

    if login_required:
        settings.validators.register(  # type: ignore[reportCallIssue]
            dynaconf.Validator(
                "musicbrainz.username", "musicbrainz.password", must_exist=True
            )
        )


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
    if album.custom.get("mb_album_id"):
        search_criteria["reid"] = album.custom["mb_album_id"]
    if album.media:
        search_criteria["format"] = album.media
    if album.track_total:
        search_criteria["tracks"] = album.track_total

    search_limit = config.CONFIG.settings.get("musicbrainz.search_limit")
    releases = musicbrainzngs.search_releases(limit=search_limit, **search_criteria)

    candidates = [
        get_candidate_by_id(album, release["id"])
        for release in releases["release-list"]
    ]

    if not candidates:
        log.warning("No candidate albums found.")
    else:
        log.info(f"Found candidate albums. [{candidates=!r}]")

    return candidates


@moe.hookimpl
def process_removed_items(session: Session, items: list[LibItem]) -> None:  # noqa: ARG001
    """Removes a release from a collection when removed from the library."""
    if not config.CONFIG.settings.musicbrainz.collection.auto_remove:
        return

    mb_ids = [
        item.custom["mb_album_id"]
        for item in items
        if isinstance(item, Album) and item.custom.get("mb_album_id")
    ]

    if mb_ids:
        try:
            rm_releases_from_collection(set(mb_ids))
        except MBAuthError:
            log.exception("Error authenticating Musicbrainz")


@moe.hookimpl
def process_new_items(session: Session, items: list[LibItem]) -> None:  # noqa: ARG001
    """Updates a user collection in musicbrainz with new releases."""
    if not config.CONFIG.settings.musicbrainz.collection.auto_add:
        return

    releases = set()
    for item in items:
        if isinstance(item, Album) and item.custom.get("mb_album_id"):
            releases.add(item.custom["mb_album_id"])

    if releases:
        try:
            add_releases_to_collection(releases)
        except MBAuthError:
            log.exception("Error authenticating Musicbrainz.")


@moe.hookimpl
def read_custom_tags(
    track_path: Path, album_fields: dict[str, Any], track_fields: dict[str, Any]
) -> None:
    """Read and set musicbrainz release IDs from a track file."""
    audio_file = mediafile.MediaFile(track_path)

    album_fields["mb_album_id"] = audio_file.mb_albumid
    track_fields["mb_track_id"] = audio_file.mb_releasetrackid


@moe.hookimpl
def sync_metadata(item: LibItem) -> None:
    """Sync musibrainz metadata for associated items."""
    if isinstance(item, Album) and item.custom.get("mb_album_id"):
        item.merge(
            get_album_by_id(item.custom["mb_album_id"]),
            merge_strategy=MergeStrategy.OVERWRITE,
        )
    elif isinstance(item, Track) and item.custom.get("mb_track_id"):
        item = cast("Track", item)
        item.merge(
            get_track_by_id(
                item.custom["mb_track_id"], item.album.custom["mb_album_id"]
            ),
            merge_strategy=MergeStrategy.OVERWRITE,
        )


@moe.hookimpl
def write_custom_tags(track: Track) -> None:
    """Write musicbrainz ID fields as tags."""
    audio_file = mediafile.MediaFile(track.path)

    audio_file.mb_albumid = track.album.custom.get("mb_album_id")
    audio_file.mb_releasetrackid = track.custom.get("mb_track_id")

    audio_file.save()


def add_releases_to_collection(
    releases: set[str], collection: str | None = None
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
    releases: set[str], collection: str | None = None
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


def _mb_auth_call(api_func: Callable, **kwargs: object) -> Any:  # noqa: ANN401 musicbrainzngs doesn't have type stubs
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
        err_msg = "User authentication with musicbrainz failed."
        raise MBAuthError(err_msg) from err


def set_collection(releases: set[str], collection: str | None = None) -> None:
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

    log.debug(f"Setting musicbrainz collection. [{releases=!r}, {collection=!r}]")

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
        current_releases.extend(
            [release["id"] for release in result["collection"]["release-list"]]
        )

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

    mb_disambigs = []
    if date := _get_release_date(release):
        mb_disambigs.append(str(date.year))
    if disambiguation := release.get("disambiguation"):
        mb_disambigs.append(disambiguation)

    return CandidateAlbum(
        album=candidate_album,
        match_value=match.get_match_value(album, candidate_album),
        plugin_source="musicbrainz",
        source_id=release_id,
        disambigs=mb_disambigs,
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
    elif catalog_nums == {"[none]"}:
        catalog_nums = set()

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


def _get_release_date(release: dict) -> datetime.date | None:
    """Gets the release date from a given musicbrainz release."""
    date = release.get("date")
    if date:
        return _parse_date(date)

    return _get_original_date(release)


def _get_original_date(release: dict) -> datetime.date | None:
    """Gets the original release date from a given musicbrainz release."""
    release_group = release.get("release-group", {})
    first_release_date = release_group.get("first-release-date")
    return _parse_date(first_release_date)


def _parse_date(date: str | None) -> datetime.date | None:
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
        if track.custom.get("mb_track_id") == track_id:
            log.info(f"Fetched track from musicbrainz. [{track=!r}]")
            return track

    err_msg = (
        f"Given track or album id could not be found. [{track_id=!r}, {album_id=!r}]"
    )
    raise ValueError(err_msg)
