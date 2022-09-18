"""Adds a duplicate resolution prompt to the CLI."""

import logging

import moe
import moe.cli
from moe.library.lib_item import LibItem
from moe.plugins.remove import remove_item
from moe.util.cli import PromptChoice, choice_prompt, fmt_item_changes

log = logging.getLogger("moe.cli.dup")


__all__: list[str] = []


@moe.hookimpl(trylast=True)
def resolve_dup_items(item_a: LibItem, item_b: LibItem):
    """Resolve any library duplicate conflicts using a user prompt."""
    print(fmt_item_changes(item_a, item_b))

    # Each PromptChoice `func` should have the following signature:
    # func(item_a, item_b) # noqa: E800
    prompt_choices = [
        PromptChoice(title="Keep item A", shortcut_key="a", func=_keep_a),
        PromptChoice(title="Keep item B", shortcut_key="b", func=_keep_b),
        PromptChoice(
            title="Merge a -> b without overwriting conflicts",
            shortcut_key="m",
            func=_merge,
        ),
        PromptChoice(
            title="Merge a -> b, overwriting any conflicts",
            shortcut_key="o",
            func=_overwrite,
        ),
    ]
    prompt_choice = choice_prompt(
        prompt_choices,
        "Duplicate items found in the library, how would you like to resolve it?",
    )
    prompt_choice.func(item_a, item_b)


def _keep_a(item_a: LibItem, item_b: LibItem):
    """Keeps `item_a`, removing `item_b` from the library."""
    log.debug("Keeping item A.")

    remove_item(item_b)


def _keep_b(item_a: LibItem, item_b: LibItem):
    """Keeps `item_a`, removing `item_b` from the library."""
    log.debug("Keeping item B.")

    remove_item(item_a)


def _merge(item_a: LibItem, item_b: LibItem):
    """Merges `item_a` into `item_b` without overwriting any conflicts."""
    log.debug("Merging A -> B without overwriting any conflicts.")

    item_b.merge(item_a)
    remove_item(item_a)


def _overwrite(item_a: LibItem, item_b: LibItem):
    """Merges `item_a` into `item_b`, overwriting any conflicts."""
    log.debug("Merging A -> B, overwriting B on conflict.")

    item_b.merge(item_a, overwrite=True)
    remove_item(item_b)
