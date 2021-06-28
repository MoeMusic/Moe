"""Interactive prompt for adding items to the library.

Provides an interactive overview of changes to be made to an album prior to it being
added to the library.
"""

import logging
from typing import Callable, List, NamedTuple, Optional, cast

import pluggy
from sqlalchemy.orm.session import Session

import moe
from moe.core.config import Config
from moe.core.library.album import Album
from moe.core.library.track import Track
from moe.plugins.add import match as add_match

log = logging.getLogger(__name__)

CHANGES_SYMBOL = "->"


class PromptChoice(NamedTuple):
    """A single user-selectable choice for the album changes prompt.

    Attributes:
        title: Title of the prompt choice that is displayed to the user alongside
            the other prompt choices. The letter of the title that the user should enter
            to select this prompt option should be capitalized. For example, to
            ``aBort`` changes to an album, the user would input the letter ``b``. If
            the letter desired does not appear in the title, simply add the letter in
            parenthesis after the title. For example, if you wanted to create an option
            called "cancel", that requires the user to enter the letter "x", create the
            title as ``cancel (x)``.
        selection_strs: All possible inputs the user can use to select this prompt
            choice. Usually, this is just a single letter and the title of the of the
            prompt choice. Each input string is case-insensitive.
        func: Function to call upon this prompt choice being selected. The function
            should return the album to be added to the library (or ``None`` if no album
            should be added) and will be supplied the following keyword arguments:
                ``config (Config)``: Moe config.
                ``session (Session)``: Current db session.
                ``old_album (Album)``: Old album with no changes applied.
                ``new_album (Album)``: New album consisting of all the new changes.
                ``user_input (str)``: User inputted selection text.
    """

    title: str
    selection_strs: List[str]
    func: Callable


class Hooks:
    """Add prompt hooks."""

    @staticmethod
    @moe.hookspec
    def add_prompt_choice(prompt_choices: List[PromptChoice]):
        """Add a ``PromptChoice`` to be added as a user input option.

        See ``PromptChoice`` for more info.

        Args:
            prompt_choices: List of prompt choices. To add a prompt choice, simply
                append it to this list.
        """


@moe.hookimpl
def add_hooks(plugin_manager: pluggy.manager.PluginManager):
    """Registers `add` hookspecs to Moe."""
    from moe.plugins.add.prompt import Hooks  # noqa: WPS433, WPS442

    plugin_manager.add_hookspecs(Hooks)


@moe.hookimpl
def add_prompt_choice(prompt_choices: List[PromptChoice]):
    """Adds the ``apply`` and ``abort`` prompt choices to the user prompt."""
    prompt_choices.append(PromptChoice("[A]pply", ["a", "apply"], func=_apply_changes))
    prompt_choices.append(PromptChoice("aBort", ["b", "abort"], func=_abort_changes))


def run_prompt(
    config: Config, session: Session, old_album: Album, new_album: Album
) -> Album:
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

    prompt_choices: List[PromptChoice] = []
    config.plugin_manager.hook.add_prompt_choice(prompt_choices=prompt_choices)
    prompt_choices.sort(key=lambda prompt: prompt.title.casefold())

    user_prompt = "\n"
    user_prompt += ", ".join(prompt_choice.title for prompt_choice in prompt_choices)
    user_prompt += " ?> "

    while True:  # noqa: WPS457
        user_input = input(user_prompt).lower()  # noqa: WPS421
        if user_input.isspace() or not user_input:
            user_input = "apply"  # default is to apply changes
        for prompt_choice in prompt_choices:
            if user_input in map(str.lower, prompt_choice.selection_strs):
                return prompt_choice.func(
                    config=config,
                    session=session,
                    old_album=old_album,
                    new_album=new_album,
                    user_input=user_input,
                )
        log.warning(f"Invalid input: {user_input}")


def _fmt_album_changes(old_album: Album, new_album: Album) -> str:
    """Formats the changes of the album between the old and new album."""
    album_info_str = ""
    album_title = f"Album: {old_album.title}"
    if old_album.title != new_album.title:
        album_title += f" {CHANGES_SYMBOL} {new_album.title}"
    album_info_str += album_title

    album_artist = f"Album Artist: {old_album.artist}"
    if old_album.artist != new_album.artist:
        album_artist = album_artist + f" {CHANGES_SYMBOL} {new_album.artist}"
    album_info_str += "\n" + album_artist

    album_year = f"Year: {old_album.year}"
    if old_album.year != new_album.year:
        album_year = album_year + f" {CHANGES_SYMBOL} {new_album.year}"
    album_info_str += "\n" + album_year

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

    return (
        f"\n{old_track_title} "
        f"{CHANGES_SYMBOL} {new_disc}{new_track.track_num}: {new_track.title}"
    )


def _apply_changes(
    config: Config,
    session: Session,
    old_album: Album,
    new_album: Album,
    user_input: str,
) -> Optional[Album]:
    """Applies the album changes."""
    new_album.path = old_album.path
    for old_track, new_track in add_match.get_matching_tracks(old_album, new_album):
        if not old_track:
            new_track.album_obj = None  # type: ignore # (causes mypy error)
        elif new_track:
            new_track.path = old_track.path

    return new_album


def _abort_changes(
    config: Config,
    session: Session,
    old_album: Album,
    new_album: Album,
    user_input: str,
) -> Optional[Album]:
    """Aborts the album changes."""
    return None  # noqa: WPS324
