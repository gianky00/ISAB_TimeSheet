import json
from unittest.mock import patch

import pytest

from src.application.services.config_manager import (
    DEFAULT_CONFIG,
    _reset_configuration_for_testing,
    add_account,
    get_config_value,
    load_config,
    remove_account,
    save_config,
    set_config_value,
)


class TestConfigManager:
    @pytest.fixture(autouse=True)
    def setup_test(self, tmp_path, mocker):
        # Reset cache before each test
        _reset_configuration_for_testing()
        # Mock paths
        mocker.patch("src.application.services.config_manager.CONFIG_DIR", tmp_path)
        mocker.patch("src.application.services.config_manager.CONFIG_FILE", tmp_path / "config.json")
        yield

    def test_load_default_config(self):
        config = load_config()
        assert config == DEFAULT_CONFIG

    def test_save_and_load_config(self):
        config = load_config()
        config["browser_headless"] = True
        save_config(config, async_save=False)

        # Reset cache to force reload from disk
        _reset_configuration_for_testing()

        new_config = load_config()
        assert new_config["browser_headless"] is True

    def test_get_set_value(self):
        set_config_value("custom_key", "custom_value", async_save=False)
        assert get_config_value("custom_key") == "custom_value"

    def test_add_remove_account(self, mocker):
        # Mock SecretsManager to avoid keyring issues
        mocker.patch(
            "src.application.services.config.account_manager.SecretsManager.is_available", return_value=False
        )
        mocker.patch(
            "src.infrastructure.utils.security.password_manager.encrypt",
            side_effect=lambda x: f"enc_{x}",
        )
        mocker.patch(
            "src.infrastructure.utils.security.password_manager.decrypt",
            side_effect=lambda x: x.replace("enc_", ""),
        )

        # Nuova firma: add_account(bot_type, account_data)
        add_account("isab", {"username": "user1", "password": "pass1", "is_default": True}, async_save=False)
        accounts = get_config_value("accounts")
        assert len(accounts) == 1
        assert accounts[0]["username"] == "user1"
        assert accounts[0]["default"] is True

        add_account("isab", {"username": "user2", "password": "pass2", "is_default": False}, async_save=False)
        assert len(get_config_value("accounts")) == 2

        remove_account("isab", "user1", async_save=False)
        accounts = get_config_value("accounts")
        assert len(accounts) == 1
        assert accounts[0]["username"] == "user2"
        assert accounts[0]["default"] is True  # user2 became default

    def test_legacy_migration(self, tmp_path):
        # Create legacy config file
        legacy_data = {
            "isab_username": "legacy_user",
            "isab_password": "legacy_password",
        }
        config_file = tmp_path / "config.json"
        with open(config_file, "w") as f:
            json.dump(legacy_data, f)

        config = load_config()
        assert "isab_username" not in config
        assert len(config["accounts"]) == 1
        assert config["accounts"][0]["username"] == "legacy_user"
        assert config["accounts"][0]["default"] is True

    def test_atomic_write_failure_cleanup(self, tmp_path, mocker):
        from src.application.services.config_manager import _atomic_write_json

        target = tmp_path / "fail.json"

        # Mock Path.open to fail (since we use temp_file.open)
        # La funzione cattura l'errore e torna False invece di propagare
        with patch("pathlib.Path.open", side_effect=OSError("Disk full")):
            res = _atomic_write_json(target, {"data": 1})
            assert res is False

        assert not target.exists()
        # Il file temporaneo usa thread ID nel nome in V9.0
        # Quindi cerchiamo qualsiasi .tmp
        temps = list(tmp_path.glob("*.tmp"))
        assert len(temps) == 0
