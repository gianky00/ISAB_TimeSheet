from unittest.mock import patch

import pytest

from src.core import config_manager


@pytest.fixture(autouse=True)
def reset_config_state(tmp_path):
    """Isolamento totale: reset cache e path temporanei."""
    from src.core.config_manager import _reset_configuration_for_testing  # noqa: PLC0415

    _reset_configuration_for_testing()

    config_path = tmp_path / "config.json"

    with (
        patch("src.core.config_manager.CONFIG_DIR", tmp_path),
        patch("src.core.config_manager.CONFIG_FILE", config_path),
    ):
        yield config_path

    _reset_configuration_for_testing()


class TestConfigManager:
    def test_load_default_config(self, reset_config_state):
        config = config_manager.load_config()
        # Non testiamo valori specifici che potrebbero cambiare,
        # ma la struttura base
        assert "browser_timeout" in config
        assert "accounts" in config

    def test_save_load_config(self, reset_config_state):
        config = config_manager.load_config()
        config["browser_timeout"] = 99
        config_manager.save_config(config)

        from src.core.config_manager import _reset_configuration_for_testing  # noqa: PLC0415

        _reset_configuration_for_testing()

        new_config = config_manager.load_config()
        assert new_config["browser_timeout"] == 99

    def test_add_remove_account(self, reset_config_state, mocker):
        # Mock security to avoid real encryption/keyring
        mocker.patch("src.core.config.account_manager.SecretsManager.is_available", return_value=False)
        mocker.patch("src.utils.security.password_manager.encrypt", side_effect=lambda x: f"enc_{x}")

        # Nuova firma: add_account(bot_type, account_data)
        config_manager.add_account("isab", {"username": "user1", "password": "pass1", "is_default": True})
        config_manager.add_account("isab", {"username": "user2", "password": "pass2", "is_default": False})

        accounts = config_manager.get_config_value("accounts")
        assert len(accounts) == 2

        config_manager.set_default_account("isab", "user2")
        assert config_manager.get_default_account("isab")["username"] == "user2"

        config_manager.remove_account("isab", "user1")
        assert len(config_manager.get_config_value("accounts")) == 1

    def test_get_download_path(self, reset_config_state, tmp_path):
        config_manager.set_config_value("download_path", str(tmp_path))
        assert config_manager.get_download_path() == str(tmp_path)

    def test_get_data_path(self, reset_config_state, tmp_path):
        # get_data_path è ora in src.core.paths
        from src.core.paths import get_data_path  # noqa: PLC0415

        with patch("src.core.paths.DB_DIR", tmp_path):
            path = get_data_path()
            assert str(tmp_path) in str(path)
