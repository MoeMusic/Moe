"""Test the musicbrainz cli plugin."""

from unittest.mock import Mock, patch

from moe import config
from tests.conftest import album_factory


class TestAddImportPromptChoice:
    """Test the `add_import_prompt_choice` hook implementation."""

    def test_add_choice(self, tmp_config):
        """The "m" key to add a musicbrainz id is added."""
        tmp_config("default_plugins = ['cli', 'musicbrainz']")
        prompt_choices = []

        config.CONFIG.pm.hook.add_import_prompt_choice(prompt_choices=prompt_choices)

        assert any(choice.shortcut_key == "m" for choice in prompt_choices)

    def test_enter_id(self, tmp_config):
        """When selected, the 'm' key should allow the user to enter an mb_id."""
        tmp_config("default_plugins = ['cli', 'musicbrainz']", tmp_db=True)
        old_album = album_factory()
        new_album = album_factory()
        prompt_choices = []
        config.CONFIG.pm.hook.add_import_prompt_choice(prompt_choices=prompt_choices)

        mock_album = Mock()
        with patch(
            "moe.plugins.musicbrainz.mb_cli.questionary.text",
            **{"return_value.ask.return_value": "new id"}
        ):
            with patch(
                "moe.plugins.musicbrainz.mb_cli.moe_mb.get_album_by_id",
                return_value=mock_album,
                autospec=True,
            ) as mock_get_album:
                with patch(
                    "moe.plugins.musicbrainz.mb_cli.moe_import.import_prompt",
                    autospec=True,
                ) as mock_prompt:
                    prompt_choices[0].func(old_album, new_album)

        mock_get_album.assert_called_once_with("new id")
        mock_prompt.assert_called_once_with(old_album, mock_album)


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation."""

    def test_no_cli(self, tmp_config):
        """Don't enable the musicbrainz cli plugin if the `cli` plugin is disabled."""
        tmp_config(settings='default_plugins = ["musicbrainz"]')

        assert not config.CONFIG.pm.has_plugin("musicbrainz_cli")

    def test_cli(self, tmp_config):
        """Enable the musicbrainz cli plugin if the `cli` plugin is enabled."""
        tmp_config(settings='default_plugins = ["musicbrainz", "cli"]')

        assert config.CONFIG.pm.has_plugin("musicbrainz_cli")
