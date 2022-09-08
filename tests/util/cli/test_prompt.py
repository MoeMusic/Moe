"""Tests the prompting functionality."""

from unittest.mock import Mock, patch

import pytest

from moe.util.cli import PromptChoice, choice_prompt


class TestChoicePrompt:
    """Test `choice_prompt`."""

    def test_prompt_choice_return(self, mock_track):
        """The proper PromptChoice is returned when selected."""
        mock_choice1 = PromptChoice("title a", "a", lambda a: None)
        mock_choice2 = PromptChoice("title b", "b", lambda b: None)
        mock_q = Mock()
        mock_q.ask.return_value = "a"

        assert mock_track.title != "a"

        with patch("moe.util.cli.prompt.questionary.rawselect", return_value=mock_q):
            prompt_choice = choice_prompt([mock_choice1, mock_choice2])
            prompt_choice.func(mock_track)

            assert prompt_choice == mock_choice1

    def test_invalid_input(self):
        """Raise SystemExit if an improper user choice is made."""
        mock_choice = PromptChoice("title b", "b", lambda b: None)
        mock_q = Mock()
        mock_q.ask.return_value = "a"

        with patch("moe.util.cli.prompt.questionary.rawselect", return_value=mock_q):
            with pytest.raises(SystemExit) as error:
                choice_prompt([mock_choice])

        assert error.value.code != 0
