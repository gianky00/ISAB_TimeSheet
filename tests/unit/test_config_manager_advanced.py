import json
from unittest.mock import patch

import pytest

from src.core.config_manager import (
    _atomic_write_json,
    _load_base_config,
    _migrate_legacy_config,
    _reset_configuration_for_testing,
    save_config,
)


class TestConfigManagerAdvanced:
    @pytest.fixture(autouse=True)
    def clean_cache(self):
        _reset_configuration_for_testing()

    @patch("src.core.config_manager.CONFIG_FILE")
    @patch(
        "src.core.config_manager.os.environ",
        {"SYNCROJOB_BROWSER_HEADLESS": "true", "SYNCROJOB_BROWSER_TIMEOUT": "60"},
    )
    def test_load_base_config_env_override(self, mock_file):
        mock_file.exists.return_value = False
        config = _load_base_config()
        assert config["browser_headless"] is True
        assert config["browser_timeout"] == 60

    def test_atomic_write_json_safety(self, tmp_path):
        target = tmp_path / "config.json"
        data = {"key": "val"}

        # Test basic success
        _atomic_write_json(data, target)
        assert target.exists()
        with target.open("r", encoding="utf-8") as f:
            assert json.load(f) == data

        # Test replace logic
        data2 = {"key": "new_val"}
        _atomic_write_json(data2, target)
        with target.open("r", encoding="utf-8") as f:
            assert json.load(f) == data2

    @patch("src.core.config_manager.CONFIG_FILE")
    @patch("src.core.config.security.SecretsManager.is_available", return_value=True)
    @patch("src.core.config.security.SecretsManager.store_credential")
    @patch("src.core.config_manager._atomic_write_json")
    def test_save_config_credential_protection(self, mock_atomic, mock_store, mock_is_avail, mock_file):
        config = {"accounts": [{"username": "user1", "password": "clear_password"}]}
        save_config(config)

        # Should call store_credential and remove password from JSON
        mock_store.assert_called()
        config_saved = mock_atomic.call_args[0][0]
        assert "password" not in config_saved["accounts"][0]

    def test_migrate_legacy_config(self):
        legacy = {
            "isab_username": "old_user",
            "isab_password": "old_password",
            "accounts": [],
        }
        changed = _migrate_legacy_config(legacy)
        assert changed is True
        assert "isab_username" not in legacy
        assert len(legacy["accounts"]) == 1
        assert legacy["accounts"][0]["username"] == "old_user"

    @patch("src.core.config_manager.CONFIG_FILE")
    def test_load_base_config_malformed_json_fallback(self, mock_file):
        mock_file.exists.return_value = True
        mock_file.read_text.return_value = "{ incomplete json"

        config = _load_base_config()
        # Should return defaults due to suppress(json.JSONDecodeError)
        assert config["browser_timeout"] == 30
