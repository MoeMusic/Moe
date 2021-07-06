"""Interactive prompt for adding items to the library.

Provides an interactive overview of changes to be made to an album prior to it being
added to the library.
"""

import logging
import operator
from typing import List, Optional, cast

import pluggy
import questionary
from sqlalchemy.orm.session import Session

import moe
from moe.core.config import Config
from moe.core.library.album import Album
from moe.core.library.track import Track
from moe.plugins.add import match as add_match

log = logging.getLogger(__name__)


class Hooks:
    """Add prompt hooks."""

    @staticmethod
    @moe.hookspec
    def add_prompt_choice(prompt_choices: List[questionary.Choice]):
        """Add a user input choice to the prompt.

        Args:
            prompt_choices: List of prompt choices. To add a prompt choice, simply
                append it to this list. The prompt_choice is a ``questionary.Choice``
                object.

        Important:
            Ensure to set the choice ``value`` to the function you want to be called
            if the choice is selected by the user. The function should return the album
            to be added to the library (or ``None`` if no album should be added) and
            will be supplied the following keyword arguments:

            ``config (Config)``: Moe config.
            ``session (Session)``: Current db session.
            ``old_album (Album)``: Old album with no changes applied.
            ``new_album (Album)``: New album consisting of all the new changes.

        Example:
            Inside your hook implementation::

                prompt_choices.append(
                    questionary.Choice(
                        title="Abort", value=_abort_changes, shortcut_key="b"
                    )
                )

        For a full reference on ``questionary.Choice`` see:
        https://questionary.readthedocs.io/en/stable/pages/api_reference.html#questionary.Choice
        """


@moe.hookimpl
def add_hooks(plugin_manager: pluggy.manager.PluginManager):
    """Registers `add` hookspecs to Moe."""
    from moe.plugins.add.prompt import Hooks  # noqa: WPS433, WPS442

    plugin_manager.add_hookspecs(Hooks)


@moe.hookimpl
def add_prompt_choice(prompt_choices: List[questionary.Choice]):
    """Adds the ``apply`` and ``abort`` prompt choices to the user prompt."""
    prompt_choices.append(
        questionary.Choice(
            title="Apply changes", value=_apply_changes, shortcut_key="a"
        )
    )
    prompt_choices.append(
        questionary.Choice(title="Abort", value=_abort_changes, shortcut_key="x")
    )


def run_prompt(
    config: Config, session: Session, old_album: Album, new_album: Album
) -> Optional[Album]:
    """Runs the interactive prompt for the given album changes.

    Args:
        config: Moe config.
        session: Current db session.
        old_album: Original album to be added.
        new_album: New album with all metadata changes. Will be compared against
            ``old_album``.

    Returns:
        The album to be added to the library.
    """
    if old_album == new_album:
        return old_album

    existing_album = new_album.get_existing(session)
    old_album.merge(existing_album, overwrite_album_info=False)

    print(_fmt_album_changes(old_album, new_album))  # noqa: WPS421

    prompt_choices: List[questionary.Choice] = []
    config.plugin_manager.hook.add_prompt_choice(prompt_choices=prompt_choices)
    prompt_choices.sort(key=operator.attrgetter("shortcut_key"))

    prompt_choice_func = questionary.rawselect(
        "What do you want to do?", choices=prompt_choices
    ).ask()
    if prompt_choice_func:
        return prompt_choice_func(
            config=config,
            session=session,
            old_album=old_album,
            new_album=new_album,
        )

    return None


def _fmt_album_changes(old_album: Album, new_album: Album) -> str:
    """Formats the changes of the album between the old and new album."""
    album_info_str = ""
    album_title = f"Album: {old_album.title}"
    if old_album.title != new_album.title:
        album_title += f" -> {new_album.title}"
    album_info_str += album_title

    album_artist = f"Album Artist: {old_album.artist}"
    if old_album.artist != new_album.artist:
        album_artist = album_artist + f" -> {new_album.artist}"
    album_info_str += "\n" + album_artist

    album_year = f"Year: {old_album.year}"
    if old_album.year != new_album.year:
        album_year = album_year + f" -> {new_album.year}"
    album_info_str += "\n" + album_year
    if new_album.mb_album_id:
        mb_album_id = f"Musicbrainz ID: {new_album.mb_album_id}"
        album_info_str += "\n" + mb_album_id

    tracklist_str = _fmt_tracklist(old_album, new_album)

    extra_str = ""
    extra_str += "\nExtras:\n"
    extra_str += "\n".join([extra.filename for extra in old_album.extras])

    album_str = album_info_str + "\n" + tracklist_str
    if old_album.extras:
        album_str += "\n" + extra_str

    return album_str


def _fmt_tracklist(old_album: Album, new_album: Album) -> str:
    """Formats the changes of the tracklist between two albums."""
    tracklist_str = ""

    matches = add_match.get_matching_tracks(old_album, new_album)
    matches.sort(
        key=lambda match: match[1].track_num + match[1].disc * len(matches)
        if match[1] is not None
        else 0
    )  # sort by new track's track number and disc
    unmatched_tracks: List[Track] = []
    for old_track, new_track in matches:
        if not new_track:
            unmatched_tracks.append(cast(Track, old_track))
            continue

        tracklist_str += _fmt_track_change(old_track, new_track)

    if unmatched_tracks:
        tracklist_str += "\n\nUnmatched Tracks:\n"
        tracklist_str += "\n".join([str(track) for track in unmatched_tracks])

    return tracklist_str


def _fmt_track_change(old_track: Optional[Track], new_track: Track) -> str:
    """Formats the changes between two tracks."""
    track_change = ""
    new_disc = ""
    old_disc = ""
    if new_track.disc_total > 1:
        new_disc = f"{new_track.disc}."
        if old_track:
            old_disc = f"{old_track.disc}."
    if old_track:
        old_track_title = f"{old_disc}{old_track.track_num}: {old_track.title}"
    else:
        old_track_title = "(missing)"
    track_change += old_track_title

    return f"\n{old_track_title} -> {new_disc}{new_track.track_num}: {new_track.title}"


def _apply_changes(
    config: Config,
    session: Session,
    old_album: Album,
    new_album: Album,
) -> Optional[Album]:
    """Applies the album changes."""
    new_album.path = old_album.path
    for old_track, new_track in add_match.get_matching_tracks(old_album, new_album):
        if not old_track:
            new_track.album_obj = None  # type: ignore # (causes mypy error)
        elif new_track:
            new_track.path = old_track.path
            new_track.file_ext = old_track.file_ext

    for extra in old_album.extras:
        extra.album = new_album

    new_album.merge(old_album)
    return new_album


def _abort_changes(
    config: Config,
    session: Session,
    old_album: Album,
    new_album: Album,
) -> Optional[Album]:
    """Aborts the album changes."""
    return None  # noqa: WPS324
