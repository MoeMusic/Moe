"""Functionality related to prompting the user for some action."""

import logging
import operator
from dataclasses import dataclass
from typing import Callable

import questionary

__all__ = ["PromptChoice", "choice_prompt"]

log = logging.getLogger("moe.cli")


@dataclass
class PromptChoice:
    """A single, user-selectable choice for a CLI prompt.

    Attributes:
        title: Title of the prompt choice that is displayed to the user.
        shortcut_key: Single character the user will use to select the choice.

            Important:
                Ensure each shortcut key is not in use by another PromptChoice.
        func: The function that should get called if a choice is selected.
            The definition for how to call ``func`` should be specified by the plugin.
    """

    title: str
    shortcut_key: str
    func: Callable


def choice_prompt(
    prompt_choices: list[PromptChoice], question: str = "What do you want to do?"
) -> PromptChoice:
    """Generates a user choice prompt.

    Args:
        prompt_choices: Prompt choices to be used.
        question: Question prompted to the user.

    Returns:
        The chosen prompt choice.

    Raises:
        SystemExit: Invalid user input.
    """
    prompt_choices.sort(key=operator.attrgetter("shortcut_key"))

    questionary_choices: list[questionary.Choice] = []
    for prompt_choice in prompt_choices:
        questionary_choices.append(
            questionary.Choice(
                title=prompt_choice.title,
                shortcut_key=prompt_choice.shortcut_key,
                value=prompt_choice.shortcut_key,
            )
        )

    user_input = questionary.rawselect(question, choices=questionary_choices).ask()

    for prompt_choice in prompt_choices:
        if prompt_choice.shortcut_key == user_input:
            return prompt_choice

    log.error(f"Invalid option selected. [{user_input=!r}]")
    raise SystemExit(1)
