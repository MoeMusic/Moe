"""Test the musicbrainz cli plugin."""

from unittest.mock import Mock, patch

from moe.plugins import moe_import
from moe.plugins import musicbrainz as moe_mb


class TestAddImportPromptChoice:
    """Test the `add_import_prompt_choice` hook implementation."""

    def test_add_choice(self, tmp_config):
        """The "m" key to add a musicbrainz id is added."""
        config = tmp_config("default_plugins = ['cli', 'import', 'musicbrainz']")
        prompt_choices = []

        config.plugin_manager.hook.add_import_prompt_choice(
            prompt_choices=prompt_choices
        )

        assert any(choice.shortcut_key == "m" for choice in prompt_choices)

    def test_enter_id(self, mock_album_factory, tmp_config):
        """When selected, the 'm' key should allow the user to enter an mb_id."""
        config = tmp_config(
            "default_plugins = ['cli', 'import', 'musicbrainz']", tmp_db=True
        )

        with patch.object(moe_import.import_cli, "_get_input", side_effect=["m", "a"]):
            mock_q = Mock()
            mock_q.ask.return_value = "new id"
            with patch(
                "moe.plugins.musicbrainz.mb_cli.questionary.text", return_value=mock_q
            ):
                with patch.object(moe_mb, "get_album_by_id") as mock_album_by_id:
                    moe_import.import_prompt(
                        config, mock_album_factory(), mock_album_factory()
                    )

        mock_album_by_id.assert_called_with("new id")


class TestPluginRegistration:
    """Test the `plugin_registration` hook implementation."""

    def test_no_cli(self, tmp_config):
        """Don't enable the musicbrainz cli plugin if the `cli` plugin is disabled."""
        config = tmp_config(settings='default_plugins = ["musicbrainz"]')

        assert not config.plugin_manager.has_plugin("musicbrainz_cli")

    def test_cli(self, tmp_config):
        """Enable the musicbrainz cli plugin if the `cli` plugin is enabled."""
        config = tmp_config(settings='default_plugins = ["musicbrainz", "cli"]')

        assert config.plugin_manager.has_plugin("musicbrainz_cli")
