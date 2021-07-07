"""Add plugin hookspecs."""

from typing import List

import pluggy
from sqlalchemy.orm.session import Session

import moe
from moe.core.config import Config
from moe.core.library.album import Album
from moe.plugins import add

__all__ = ["Hooks"]


class Hooks:
    """Add plugin hook specifications."""

    @staticmethod
    @moe.hookspec
    def add_prompt_choice(prompt_choices: List["add.PromptChoice"]):
        """Add a user input choice to the prompt.

        Args:
            prompt_choices: List of prompt choices. To add a prompt choice, simply
                append it to this list.

        Example:
            Inside your hook implementation::

                prompt_choices.append(
                    PromptChoice(
                        title="Abort", shortcut_key="x", func=_abort_changes
                    )
                )
        """

    @staticmethod
    @moe.hookspec
    def import_album(config: Config, session: Session, album: Album) -> Album:
        """Return an album with changes to be applied by the user via the prompt.

        This hook is intended to be used to import metadata from an external source.
        The user will then select one of the imported albums to apply the changes prior
        to the album being added to the library.

        Args:
            config: Moe config.
            session: Currrent db session.
            album: Original album to alter.

        Returns:
            The new, altered album to compare against the original in the prompt.
        """  # noqa: DAR202

    @staticmethod
    @moe.hookspec
    def pre_add(config: Config, session: Session, album: Album):
        """Provides an album prior to it being added to the library."""


@moe.hookimpl
def add_hooks(plugin_manager: pluggy.manager.PluginManager):
    """Registers `add` hookspecs to Moe."""
    from moe.plugins.add import Hooks  # noqa: WPS433, WPS442, WPS458

    plugin_manager.add_hookspecs(Hooks)
