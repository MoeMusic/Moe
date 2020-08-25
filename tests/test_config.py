"""Test configuration."""


from unittest.mock import patch

from moe.core.config import Config


class TestInit:
    """Test configuration initialization."""

    def test_dirs_dne(self, tmp_path):
        """Should create the config and database directories if they don't exist."""
        fake_path = tmp_path / "this_definitely_doesnt_exist"

        with patch.object(Config, "_db_init"):
            Config(config_dir=fake_path)

        assert fake_path.exists()
