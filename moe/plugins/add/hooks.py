"""Add plugin hookspecs."""

from typing import List

import pluggy
from sqlalchemy.orm.session import Session

import moe
from moe.core.config import Config
from moe.core.library.album import Album
from moe.core.library.lib_item import LibItem
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
        """Return an album with changes to be applied by the user via the import prompt.

        This hook is intended to be used to import metadata from an external source.
        The user will then select one of the imported albums to apply the changes prior
        to the album being added to the library.

        Note:
            This hook is run within the :meth:`pre_add` hook.

        Args:
            config: Moe config.
            session: Currrent db session.
            album: Album being added to the library.

        Returns:
            The new, altered album to compare against the original in the prompt.
        """  # noqa: DAR202

    @staticmethod
    @moe.hookspec
    def pre_add(config: Config, session: Session, item: LibItem):
        """Provides an item prior to it being added to the library.

        Use this hook if you wish to change the item's metadata.

        Args:
            config: Moe config.
            session: Currrent db session.
            item: Library item being added.

        See Also:
            * The :meth:`post_add` hook for any post-processing operations.
            * The :meth:`~moe.cli.Hooks.edit_new_items` hook.
              The difference between them is that the :meth:`pre_add` hook will only
              operate on an `add` operation, while the
              :meth:`~moe.cli.Hooks.edit_new_items` hook will run anytime an item is
              changed or added.
        """

    @staticmethod
    @moe.hookspec
    def post_add(config: Config, session: Session, item: LibItem):
        """Provides an item after it has been added to the library.

        Use this hook if you want to operate on an item after its metadata has been set.

        Args:
            config: Moe config.
            session: Currrent db session.
            item: Library item added.

        See Also:
            * The :meth:`pre_add` hook if you wish to alter item metadata.
            * The :meth:`~moe.cli.Hooks.process_new_items` hook.
              The difference between them is that the :meth:`post_add` hook will only
              operate on an `add` operation, while the
              :meth:`~moe.cli.Hooks.process_new_items` hook will run anytime an item is
              changed or added.
        """


@moe.hookimpl
def add_hooks(plugin_manager: pluggy.manager.PluginManager):
    """Registers `add` hookspecs to Moe."""
    from moe.plugins.add import Hooks  # noqa: WPS433, WPS442, WPS458

    plugin_manager.add_hookspecs(Hooks)
