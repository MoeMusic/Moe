"""Tests the prompting functionality."""

from unittest.mock import patch

import pytest

from moe.util.cli import PromptChoice, choice_prompt
from tests.conftest import track_factory


class TestChoicePrompt:
    """Test `choice_prompt`."""

    def test_prompt_choice_return(self):
        """The proper PromptChoice is returned when selected."""
        track = track_factory()
        mock_choice1 = PromptChoice("title a", "a", lambda a: None)
        mock_choice2 = PromptChoice("title b", "b", lambda b: None)

        assert track.title != "a"

        with patch(
            "moe.util.cli.prompt.questionary.select",
            **{"return_value.ask.return_value": "a"}
        ):
            prompt_choice = choice_prompt([mock_choice1, mock_choice2])
            prompt_choice.func(track)

            assert prompt_choice == mock_choice1

    def test_invalid_input(self):
        """Raise SystemExit if an improper user choice is made."""
        mock_choice = PromptChoice("title b", "b", lambda b: None)

        with patch(
            "moe.util.cli.prompt.questionary.select",
            **{"return_value.ask.return_value": "a"}
        ):
            with pytest.raises(SystemExit) as error:
                choice_prompt([mock_choice])

        assert error.value.code != 0
