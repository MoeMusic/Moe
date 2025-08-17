"""A Track in the database and any related logic."""

from __future__ import annotations

import logging
import sys
from typing import TYPE_CHECKING, Any, Optional

import mediafile
from sqlalchemy import Integer
from sqlalchemy.ext.mutable import MutableSet
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKey, UniqueConstraint

import moe
from moe import config
from moe.library.album import Album, MetaAlbum
from moe.library.lib_item import LibItem, LibraryError, MetaLibItem, SABase, SetType

if sys.version_info < (3, 11):
    from typing_extensions import Self
else:
    from typing import Self

if TYPE_CHECKING:
    from pathlib import Path

    import pluggy

__all__ = ["MetaTrack", "Track", "TrackError"]

log = logging.getLogger("moe.track")


class Hooks:
    """Track hook specifications."""

    @staticmethod
    @moe.hookspec
    def is_unique_track(track: Track, other: Track) -> bool:  # type: ignore[reportReturnType]
        """Add new conditions to determine whether two tracks are unique.

        "Uniqueness" is meant in terms of whether the two tracks should be considered
        duplicates in the library. These additional conditions will be applied inside a
        track's :meth:`is_unique` method.
        """

    @staticmethod
    @moe.hookspec
    def read_custom_tags(
        track_path: Path, album_fields: dict[str, Any], track_fields: dict[str, Any]
    ) -> None:
        """Read and set any fields from a track_path.

        How you read the file and assign tags is up to each individual plugin.
        Internally, Moe uses the `mediafile <https://github.com/beetbox/mediafile>`_
        library to read tags.

        Args:
            track_path: Path of the track file to read.
            album_fields: Dictionary of album fields to read from the given track file's
                tags. The dictionary may contain existing fields and values, and you
                can choose to either override the existing fields, or to provide new
                fields.
            track_fields: Dictionary of track fields to read from the given track file's
                tags. The dictionary may contain existing fields and values, and you
                can choose to either override the existing fields, or to provide new
                fields.

        Example:
            .. code:: python

                audio_file = mediafile.MediaFile(track_path)
                album_fields["title"] = audio_file.album
                track_fields["title"] = audio_file.title

        See Also:
            * :ref:`Album and track fields <fields:Fields>`
            * `Mediafile docs <https://mediafile.readthedocs.io/en/latest/>`_
            * The :meth:`~moe.write.Hooks.write_custom_tags` hook for writing
              tags.
        """


@moe.hookimpl
def add_hooks(pm: pluggy._manager.PluginManager) -> None:
    """Registers `track` hookspecs to Moe."""
    from moe.library.track import Hooks  # noqa: PLC0415

    pm.add_hookspecs(Hooks)


@moe.hookimpl(tryfirst=True)
def read_custom_tags(
    track_path: Path, album_fields: dict[str, Any], track_fields: dict[str, Any]
) -> None:
    """Read and set internally tracked fields."""
    audio_file = mediafile.MediaFile(track_path)

    album_fields["artist"] = audio_file.albumartist or audio_file.artist
    album_fields["barcode"] = audio_file.barcode
    if audio_file.catalognums is not None:
        album_fields["catalog_nums"] = set(audio_file.catalognums)
    album_fields["country"] = audio_file.country
    album_fields["date"] = audio_file.date
    album_fields["disc_total"] = audio_file.disctotal
    album_fields["label"] = audio_file.label
    album_fields["media"] = audio_file.media
    album_fields["original_date"] = audio_file.original_date
    album_fields["title"] = audio_file.album
    album_fields["track_total"] = audio_file.tracktotal

    track_fields["artist"] = audio_file.artist
    if audio_file.artists is not None:
        track_fields["artists"] = set(audio_file.artists)
    track_fields["composer"] = audio_file.composer
    track_fields["composer_sort"] = audio_file.composer_sort
    track_fields["disc"] = audio_file.disc
    if audio_file.genres is not None:
        track_fields["genres"] = set(audio_file.genres)
    track_fields["title"] = audio_file.title
    track_fields["track_num"] = audio_file.track


class TrackError(LibraryError):
    """Error performing some operation on a Track."""


class MetaTrack(MetaLibItem):  # noqa: PLW1641 MetaTracks are unhashable
    """A track containing only metadata.

    It does not exist on the filesystem nor in the library. It can be used
    to represent information about a track to later be merged into a full ``Track``
    instance.

    Attributes:
        album (Album | None): Corresponding Album object.
        artist (str | None)
        artists (set[str] | None): Set of all artists.
        composer (str | None): Track composer.
        composer_sort (str | None): Composer sort field.
        custom (dict[str, Any]): Dictionary of custom fields.
        disc (int | None): Disc number the track is on.
        duration (float | None): Duration of the track in seconds.
        genres (set[str] | None): Set of all genres.
        title (str | None)
        track_num (int | None)
    """

    def __init__(  # noqa: PLR0913
        self,
        album: MetaAlbum,
        track_num: int,
        artist: str | None = None,
        artists: set[str] | None = None,
        composer: str | None = None,
        composer_sort: str | None = None,
        disc: int = 1,
        duration: float | None = None,
        genres: set[str] | None = None,
        title: str | None = None,
        **kwargs: object,
    ) -> None:
        """Creates a MetaTrack object with any additional custom fields as kwargs."""
        self.custom = kwargs

        self.album = album
        album.tracks.append(self)

        self.track_num = track_num
        self.artist = artist or self.album.artist
        self.artists = artists
        self.composer = composer
        self.composer_sort = composer_sort
        self.disc = disc
        self.duration = duration
        self.genres = genres
        self.title = title

        log.debug(f"MetaTrack created. [track={self!r}]")

    @property
    def genre(self) -> str | None:
        """Returns a string of all genres concatenated with ';'."""
        if self.genres is None:
            return None

        return ";".join(self.genres)

    @genre.setter
    def genre(self, genre_str: str | None) -> None:
        """Sets a track's genre from a string.

        Args:
            genre_str: For more than one genre, they should be split with ';'.
        """
        if genre_str is None:
            self.genres = None
        else:
            self.genres = {genre.strip() for genre in genre_str.split(";")}

    @property
    def fields(self) -> set[str]:
        """Returns any editable, track-specific fields."""
        return {
            "album",
            "artist",
            "artists",
            "composer",
            "composer_sort",
            "disc",
            "duration",
            "genres",
            "title",
            "track_num",
        }

    def merge(self, other: MetaTrack | Track, overwrite: bool = False) -> None:  # noqa: FBT001, FBT002 breaking change
        """Merges another track into this one.

        Args:
            other: Other track to be merged with the current track.
            overwrite: Whether or not to overwrite self if a conflict exists.
        """
        log.debug(
            f"Merging tracks. [track_a={self!r}, track_b={other!r}, {overwrite=}]"
        )

        omit_fields = {"album"}
        for field in self.fields - omit_fields:
            other_value = getattr(other, field, None)
            self_value = getattr(self, field, None)
            if other_value and (overwrite or (not overwrite and not self_value)):
                setattr(self, field, other_value)

        for custom_field in self.custom:
            other_value = other.custom.get(custom_field)
            if other_value and (
                overwrite or (not overwrite and not self.custom[custom_field])
            ):
                self.custom[custom_field] = other_value

        log.debug(f"Tracks merged. [track_a={self!r}, track_b={other!r}, {overwrite=}]")

    def __eq__(self, other: object) -> bool:
        """Compares Tracks by their fields."""
        if not isinstance(other, MetaTrack):
            return False

        for field in self.fields:
            if not hasattr(other, field) or (
                getattr(self, field) != getattr(other, field)
            ):
                return False

        return True

    def __lt__(self, other: Self) -> bool:
        """Sort based on album, then disc, then track number."""
        if self.album == other.album:
            if self.disc == other.disc:
                return self.track_num < other.track_num

            return self.disc < other.disc

        return self.album < other.album

    def __repr__(self) -> str:
        """Represents a Track using track-specific and relevant album fields."""
        field_reprs = [
            f"{field}={getattr(self, field)!r}"
            for field in self.fields - {"album"}  # don't display album repr
            if hasattr(self, field)
        ]

        repr_str = (
            f"{type(self).__name__}("
            + ", ".join(field_reprs)
            + f", album='{self.album}'"
        )

        custom_field_reprs = []
        for custom_field, value in self.custom.items():
            custom_field_reprs.append(f"{custom_field}={value}")
        if custom_field_reprs:
            repr_str += ", custom_fields=[" + ", ".join(custom_field_reprs) + "]"

        repr_str += ")"
        return repr_str

    def __str__(self) -> str:
        """String representation of a track."""
        return f"{self.artist} - {self.title}"


class Track(LibItem, SABase, MetaTrack):
    """A single track in the library.

    Attributes:
        album (Album): Corresponding Album object.
        artist (str)
        artists (set[str] | None): Set of all artists.
        composer (str | None): Track composer.
        composer_sort (str | None): Composer sort field.
        custom (dict[str, Any]): Dictionary of custom fields.
        disc (int): Disc number the track is on.
        genres (set[str] | None): Set of all genres.
        path (Path): Filesystem path of the track file.
        title (str)
        track_num (int)

    Note:
        Altering any album-related property attributes, will result in changing the
        album field and thus all other tracks in the album as well.
    """

    __tablename__ = "track"

    artist: Mapped[str]
    artists: Mapped[Optional[set[str]]] = mapped_column(  # noqa: UP045 sqlalchemy does not support
        MutableSet.as_mutable(SetType()), nullable=True
    )
    composer: Mapped[Optional[str]]  # noqa: UP045 sqlalchemy does not support
    composer_sort: Mapped[Optional[str]]  # noqa: UP045 sqlalchemy does not support
    disc: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    genres: Mapped[Optional[set[str]]] = mapped_column(  # noqa: UP045 sqlalchemy does not support
        MutableSet.as_mutable(SetType()), nullable=True
    )
    title: Mapped[str]
    track_num: Mapped[int]

    _album_id: Mapped[int] = mapped_column(Integer, ForeignKey("album._id"))
    album: Mapped[Album] = relationship(back_populates="tracks")

    __table_args__ = (UniqueConstraint("disc", "track_num", "_album_id"),)

    def __init__(  # noqa: PLR0913
        self,
        album: Album,
        path: Path,
        title: str,
        track_num: int,
        artist: str | None = None,
        artists: set[str] | None = None,
        composer: str | None = None,
        composer_sort: str | None = None,
        disc: int | None = None,
        genres: set[str] | None = None,
        **kwargs: object,
    ) -> None:
        """Creates a Track.

        Args:
            album: Album the track belongs to.
            path: Filesystem path of the track file.
            title: Title of the track.
            track_num: Track number.
            artist: Track artist. Defaults to the album artist if not given.
            artists: Set of all artists.
            composer: Track composer.
            composer_sort: Composer sort field.
            disc: Disc the track belongs to. If not given, will try to guess the disc
                based on the ``path`` of the track.
            genres (Optional[set[str]]): Set of all genres.
            **kwargs: Any custom fields to assign to the track.
        """
        self.custom = kwargs

        album.tracks.append(self)

        self.path = path
        self.artist = artist or self.album.artist
        self.artists = artists
        self.composer = composer
        self.composer_sort = composer_sort
        self.disc = disc or self._guess_disc()
        self.genres = genres
        self.title = title
        self.track_num = track_num

        log.debug(f"Track created. [track={self!r}]")

    def _guess_disc(self) -> int:
        """Attempts to guess the disc of a track based on it's path."""
        log.debug(f"Guessing track disc number. [track={self!r}]")

        if self.path.parent == self.album.path:
            return 1

        # The track is in a subdirectory of the album - most likely disc directories.
        disc_dirs: list[Path] = []
        for path in self.album.path.iterdir():
            if not path.is_dir():
                continue

            contains_tracks = False
            for album_track in self.album.tracks:
                if album_track.path.is_relative_to(path):
                    contains_tracks = True

            if contains_tracks:
                disc_dirs.append(path)

        # Guess the disc by the order of the disc directory it appears in.
        for disc_num, disc_dir in enumerate(sorted(disc_dirs), start=1):
            if self.path.is_relative_to(disc_dir):
                return disc_num

        return 1

    @classmethod
    def from_file(
        cls,
        track_path: Path,
        album: Album | None = None,
        album_path: Path | None = None,
    ) -> Track:
        """Alternate initializer that creates a Track from a track file.

        Will read any tags from the given path and save them to the Track.

        Args:
            track_path: Filesystem path of the track.
            album: Corresponding album for the track. If ``None``, the album will be
                created using the parent directory of ``track_path``, unless
                ``album_path`` is also given.
            album_path: When ``album`` is ``None``, this is the path of the created
                album. If ``None`` it defaults to the parent directory of
                ``track_path``.

        Returns:
            Track instance.

        Raises:
            TrackError: Given ``path`` does not correspond to a track file.
            ValueError: Track is missing required fields.
        """
        log.debug(f"Creating track from path. [path={track_path}, {album=}]")

        try:
            mediafile.MediaFile(track_path)
        except mediafile.UnreadableFileError as err:
            err_msg = (
                "Unable to create track; given path is not a track file. "
                f"[path={track_path}]"
            )
            raise TrackError(err_msg) from err

        album_fields: dict[str, Any] = {}
        track_fields: dict[str, Any] = {}
        config.CONFIG.pm.hook.read_custom_tags(
            track_path=track_path, album_fields=album_fields, track_fields=track_fields
        )

        title = track_fields.pop("title")
        track_num = track_fields.pop("track_num")

        album_artist = album_fields.pop("artist")
        album_title = album_fields.pop("title")
        date = album_fields.pop("date")
        disc_total = album_fields.pop("disc_total") or 1

        missing_reqd_fields = []
        if not title:
            missing_reqd_fields.append("title")
        if not track_num:
            missing_reqd_fields.append("track_num")
        if not album_artist and not album:
            missing_reqd_fields.append("album_artist")
        if not album_title and not album:
            missing_reqd_fields.append("album_title")
        if not date and not album:
            missing_reqd_fields.append("date")
        if missing_reqd_fields:
            err_msg = f"Track is missing required fields. [{missing_reqd_fields=}]"
            raise ValueError(err_msg)

        if not album:
            album = Album(
                path=album_path or track_path.parent,
                artist=album_artist,
                title=album_title,
                date=date,
                disc_total=disc_total,
                **album_fields,
            )

        return cls(
            album=album,
            path=track_path,
            title=title,
            track_num=track_num,
            **track_fields,
        )

    @property
    def audio_format(self) -> str:
        """Returns the audio format of the track.

        One of ['aac', 'aiff', 'alac', 'ape', 'asf', 'dsf', 'flac', 'ogg', 'opus',
            'mp3', 'mpc', 'wav', 'wv'].
        """
        return mediafile.MediaFile(self.path).type

    @property
    def bit_depth(self) -> int:
        """Returns the number of bits per sample in the audio encoding.

        The bit depth is an integer and zero when unavailable or when the file format
        does not support bit depth.
        """
        return mediafile.MediaFile(self.path).bitdepth

    @property
    def duration(self) -> float:
        """Returns the duration of the track in seconds."""
        return mediafile.MediaFile(self.path).length

    @property
    def fields(self) -> set[str]:
        """Returns any editable, track-specific fields."""
        return super().fields.union({"path"}) - {"duration"}

    @property
    def sample_rate(self) -> int:
        """Returns the sampling rate of the track.

        The sampling rate is in Hertz (Hz) as an integer and zero when unavailable.
        """
        return mediafile.MediaFile(self.path).samplerate

    def is_unique(self, other: LibItem) -> bool:
        """Returns whether a track is unique in the library from ``other``."""
        if not isinstance(other, Track):
            return True

        if self.path == other.path:
            return False
        if (
            self.track_num == other.track_num
            and self.disc == other.disc
            and self.album == other.album
        ):
            return False

        custom_uniqueness = config.CONFIG.pm.hook.is_unique_track(
            track=self, other=other
        )

        return False not in custom_uniqueness
