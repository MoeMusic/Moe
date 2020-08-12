"""Test configuration."""


from moe.core.config import Config


class TestInit:
    """Test configuration initialization."""

    def test_dirs_dne(self, tmp_path, mocker):
        """Should create the config and database directories if they don't exist."""
        fake_path = tmp_path / "this_definitely_doesnt_exist"
        fake_path2 = tmp_path / "this_definitely_doesnt_exist2"

        mocker.patch("moe.core.config.Config", "_db_init")
        Config(config_dir=fake_path, db_dir=fake_path2)

        assert fake_path.exists()
        assert fake_path2.exists()
