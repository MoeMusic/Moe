"""Transcode music."""

from __future__ import annotations

import logging
import multiprocessing
import shlex
import subprocess
from pathlib import Path
from typing import Literal, TypeVar

import dynaconf.base

import moe
from moe import config
from moe.library import Album, Track
from moe.move import fmt_item_path

__all__ = ["I", "TranscodeFormat", "transcode"]

log = logging.getLogger("moe.transcode")

TranscodeFormat = Literal["mp3 v2", "mp3 v0", "mp3 320"]
FFMPEG_MP3_ARG = {
    "mp3 v0": "-qscale:a 0",
    "mp3 v2": "-qscale:a 2",
    "mp3 320": "-b:a 320k",
}


@moe.hookimpl
def add_config_validator(settings: dynaconf.base.LazySettings) -> None:
    """Validate move plugin configuration settings."""
    settings.validators.register(  # type: ignore[reportCallIssue]
        dynaconf.Validator(
            "TRANSCODE.TRANSCODE_PATH",
            default=Path(settings.library_path) / "transcode",  # type: ignore[reportCallIssue]
        )
    )


I = TypeVar("I", Album, Track)  # noqa: E741
"""Type hint representing either an Album or a Track."""


def transcode(
    item: I,
    to_format: TranscodeFormat,
    out_path: Path | None = None,
    overwrite: bool = False,  # noqa: FBT001, FBT002
) -> I:
    """Transcodes a track or album to a specific format.

    Args:
        item: Track or Album to transcode. The track, or tracks contained
            in the album will only be transcoded if they are flacs.
        to_format: Format to transcode to.
        out_path: Path of the transcoded item. This defaults to the formatted path per
            the configuration relative to the ``transcode_path`` setting.
        overwrite: Whether or not to overwrite existing files.

    Returns:
        The transcoded track or album.

    Raises:
        ValueError: ``item`` contains a non-supported audio format.
    """
    transcode_path = Path(config.CONFIG.settings.transcode.transcode_path).expanduser()
    out_path = out_path or fmt_item_path(item, transcode_path)

    if isinstance(item, Album):
        return _transcode_album(item, to_format, out_path, overwrite)
    return _transcode_track(item, to_format, out_path, overwrite)


def _transcode_album(
    album: Album,
    to_format: TranscodeFormat,
    out_path: Path,
    overwrite: bool = False,  # noqa: FBT001, FBT002
) -> Album:
    """Transcodes an album to a specific format.

    Args:
        album: Album to transcode. Must contain flacs only.
        to_format: Format to transcode to.
        out_path: Path of the transcoded album. This defaults to the formatted path per
            the configuration relative to the ``transcode_path`` setting. Track files
            within the album will not be renamed except for any file extension changes.
        overwrite: Whether or not to overwrite existing files.

    Returns:
        The transcoded album.

    Raises:
        FileExistsError: If ``overwrite`` is ``False`` and the output path for a track
            already exists.
        ValueError: ``album`` contains a non-supported audio format.
    """
    log.debug(f"Transcoding album. [{album=!r}, {to_format=!r}, {out_path=!r}]")

    for track in album.tracks:
        if track.audio_format != "flac":
            err_msg = f"Album contains track with unsupported format. [{track=!r}]"
            raise ValueError(err_msg)

    out_path.mkdir(parents=True, exist_ok=True)

    transcode_calls = []
    for track in album.tracks:
        track_out_path = out_path / (track.path.stem + ".mp3")

        if track.audio_format != "flac":
            err_msg = f"Track has unsupported audio format. [{track=!r}]"
            raise ValueError(err_msg)

        log.debug(f"Transcoding track. [{track=!r}, {to_format=!r}, {out_path=!r}]")
        transcode_calls.append((track.path, to_format, track_out_path, overwrite))

    with multiprocessing.Pool() as pool:
        pool.starmap(_transcode_path, transcode_calls)

    transcoded_album = Album.from_dir(out_path)
    log.info(f"Transcoded album. [{transcoded_album=!r}]")

    return transcoded_album


def _transcode_track(
    track: Track,
    to_format: TranscodeFormat,
    out_path: Path,
    overwrite: bool = False,  # noqa: FBT001, FBT002
) -> Track:
    """Transcodes a track to a specific format.

    Args:
        track: Track to transcode. The track will only be transcoded if it is a flac.
        to_format: Format to transcode to.
        out_path: Path of the transcoded track. This defaults to the formatted path per
            the configuration relative to the ``transcode_path`` setting.
        overwrite: Whether or not to overwrite existing files.

    Returns:
        The transcoded track.

    Raises:
        FileExistsError: If ``out_path`` already exists and ``overwrite`` is ``False``.
        ValueError: ``track`` contains a non-supported audio format.
    """
    log.debug(f"Transcoding track. [{track=!r}, {to_format=!r}, {out_path=!r}]")

    if out_path.exists() and not overwrite:
        err_msg = f"Given output path already exists. [{out_path=}]"
        raise FileExistsError(err_msg)

    if track.audio_format != "flac":
        err_msg = f"Track has unsupported audio format. [{track=!r}]"
        raise ValueError(err_msg)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path = out_path.with_suffix(".mp3")

    _transcode_path(track.path, to_format, out_path, overwrite)

    transcoded_track = Track.from_file(out_path)
    log.info(f"Transcoded track. [{transcoded_track=!r}]")

    return transcoded_track


def _transcode_path(
    path: Path,
    to_format: TranscodeFormat,
    out_path: Path,
    overwrite: bool = False,  # noqa: FBT001, FBT002
) -> None:
    """Transcodes a file to `to_format`.

    This is a separate function in order to support multiprocessing.
    """
    overwrite_arg = "-y" if overwrite else "-n"

    args = [
        "ffmpeg",
        overwrite_arg,
        "-loglevel",
        "error",
        "-i",
        str(path.resolve()),
        "-codec:a",
        "libmp3lame",
    ]
    args.extend(shlex.split(FFMPEG_MP3_ARG[to_format]))
    args.append(str(out_path.resolve()))

    subprocess.run(args, check=False)  # noqa: S603
