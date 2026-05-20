import json
from unittest.mock import patch

import pytest

from src.core.config_manager import (
    _atomic_write_json,
    _load_base_config,
    _reset_configuration_for_testing,
    migrate_legacy_keys,
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
        # In V9.0 _atomic_write_json(path, data)
        _atomic_write_json(target, data)
        assert target.exists()
        with target.open("r", encoding="utf-8") as f:
            assert json.load(f) == data

    @patch("src.core.config_manager.CONFIG_FILE")
    @patch("src.core.config.security.SecretsManager.is_available", return_value=True)
    @patch("src.core.config.security.SecretsManager.store_credential")
    @patch("src.core.config_manager._atomic_write_json")
    def test_save_config_credential_protection(self, mock_atomic, mock_store, mock_is_avail, mock_file):
        config = {"accounts": [{"username": "user1", "password": "clear_password"}]}
        save_config(config)

        # Should call store_credential and remove password from JSON
        mock_store.assert_called()
        # In V9.0 _atomic_write_json(CONFIG_FILE, config_to_save)
        config_saved = mock_atomic.call_args[0][1]
        assert "password" not in config_saved["accounts"][0]

    def test_migrate_legacy_config(self):
        legacy = {
            "isab_username": "old_user",
            "isab_password": "old_password",
        }
        # La funzione reale migra isab_* in accounts
        changed = migrate_legacy_keys(legacy)
        assert changed is True
        assert "accounts" in legacy
        assert any(a["username"] == "old_user" for a in legacy["accounts"])

    @patch("src.core.config_manager.CONFIG_FILE")
    def test_load_base_config_malformed_json_fallback(self, mock_file):
        mock_file.exists.return_value = True
        mock_file.read_text.return_value = "{ incomplete json"

        config = _load_base_config()
        # Should return defaults due to suppress(json.JSONDecodeError)
        assert config["browser_timeout"] == 300
