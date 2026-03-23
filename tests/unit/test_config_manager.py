from unittest.mock import patch

import pytest

from src.core import config_manager


@pytest.fixture(autouse=True)
def reset_config_state(tmp_path):  # noqa: ANN001
    """Isolamento totale: reset cache e path temporanei."""
    config_manager._config_cache = None
    config_path = tmp_path / "config.json"

    # Assicura che il file non esista
    if config_path.exists():
        config_path.unlink()

    with (
        patch("src.core.config_manager.CONFIG_DIR", tmp_path),
        patch("src.core.config_manager.CONFIG_FILE", config_path),
    ):
        yield config_path

    config_manager._config_cache = None


class TestConfigManager:
    def test_load_default_config(self, reset_config_state):  # noqa: ANN001
        config = config_manager.load_config()
        assert config["browser_timeout"] == 30  # noqa: PLR2004
        assert config["accounts"] == []

    def test_save_load_config(self, reset_config_state):  # noqa: ANN001
        config = config_manager.load_config()
        config["browser_timeout"] = 99
        config_manager.save_config(config)

        config_manager._config_cache = None
        new_config = config_manager.load_config()
        assert new_config["browser_timeout"] == 99  # noqa: PLR2004

    def test_add_remove_account(self, reset_config_state):  # noqa: ANN001
        # Clear any residue
        config_manager._config_cache = None

        config_manager.add_account("user1", "pass1", is_default=True)
        config_manager.add_account("user2", "pass2", is_default=False)

        accounts = config_manager.get_accounts()
        assert len(accounts) == 2  # noqa: PLR2004

        config_manager.set_default_account("user2")
        assert config_manager.get_default_account()["username"] == "user2"

        config_manager.remove_account("user1")
        assert len(config_manager.get_accounts()) == 1

    def test_get_download_path(self, reset_config_state, tmp_path):  # noqa: ANN001
        config_manager.set_config_value("download_path", str(tmp_path))
        assert config_manager.get_download_path() == str(tmp_path)

    def test_get_data_path(self, reset_config_state, tmp_path):  # noqa: ANN001
        path = config_manager.get_data_path()
        assert str(tmp_path) in path
