
import json
import os
import pytest
from unittest.mock import MagicMock, patch
from src.core.config_manager import (
    load_config,
    save_config,
    get_config_value,
    set_config_value,
    add_account,
    remove_account,
    _reset_configuration_for_testing,
    DEFAULT_CONFIG
)

class TestConfigManager:
    @pytest.fixture(autouse=True)
    def setup_test(self, tmp_path, mocker):
        # Reset cache before each test
        _reset_configuration_for_testing()
        # Mock paths
        mocker.patch("src.core.config_manager.CONFIG_DIR", tmp_path)
        mocker.patch("src.core.config_manager.CONFIG_FILE", tmp_path / "config.json")
        yield

    def test_load_default_config(self):
        config = load_config()
        assert config == DEFAULT_CONFIG

    def test_save_and_load_config(self):
        config = load_config()
        config["browser_headless"] = True
        save_config(config)
        
        # Reset cache to force reload from disk
        _reset_configuration_for_testing()
        
        new_config = load_config()
        assert new_config["browser_headless"] is True

    def test_get_set_value(self):
        set_config_value("custom_key", "custom_value")
        assert get_config_value("custom_key") == "custom_value"

    def test_add_remove_account(self, mocker):
        # Mock SecretsManager to avoid keyring issues
        mocker.patch("src.core.config_manager.SecretsManager.is_available", return_value=False)
        mocker.patch("src.utils.security.password_manager.encrypt", side_effect=lambda x: f"enc_{x}")
        mocker.patch("src.utils.security.password_manager.decrypt", side_effect=lambda x: x.replace("enc_", ""))

        add_account("user1", "pass1", is_default=True)
        accounts = get_config_value("accounts")
        assert len(accounts) == 1
        assert accounts[0]["username"] == "user1"
        assert accounts[0]["default"] is True
        
        add_account("user2", "pass2", is_default=False)
        assert len(get_config_value("accounts")) == 2
        
        remove_account("user1")
        accounts = get_config_value("accounts")
        assert len(accounts) == 1
        assert accounts[0]["username"] == "user2"
        assert accounts[0]["default"] is True # user2 became default

    def test_legacy_migration(self, tmp_path):
        # Create legacy config file
        legacy_data = {
            "isab_username": "legacy_user",
            "isab_password": "legacy_password"
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
        from src.core.config_manager import _atomic_write_json
        target = tmp_path / "fail.json"
        
        # Mock open to fail
        with patch("builtins.open", side_effect=IOError("Disk full")):
            with pytest.raises(IOError):
                _atomic_write_json({"data": 1}, target)
        
        assert not target.exists()
        assert not (tmp_path / "fail.tmp").exists()
