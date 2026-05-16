"""
Tests for load_config and save_config in config_manager.py.
Aims for 100% coverage and functional parity before refactoring.
"""

import json
from unittest.mock import patch

import pytest

from src.core import config_manager
from src.core.config_manager import (
    DEFAULT_CONFIG,
    _reset_configuration_for_testing,
    load_config,
    save_config,
)


@pytest.fixture(autouse=True)
def clean_config_env(tmp_path):
    """Fixture to isolate config environment for each test."""
    _reset_configuration_for_testing()

    # Patch CONFIG_DIR and CONFIG_FILE to use tmp_path
    mock_dir = tmp_path / "SyncroJob"
    mock_file = mock_dir / "config.json"

    # Ensure dir exists
    mock_dir.mkdir(parents=True, exist_ok=True)

    with (
        patch("src.core.config_manager.CONFIG_DIR", mock_dir),
        patch("src.core.config_manager.CONFIG_FILE", mock_file),
    ):
        yield mock_dir, mock_file


def test_load_config_default(clean_config_env):
    """Test loading config when file doesn't exist."""
    _mock_dir, mock_file = clean_config_env
    if mock_file.exists():
        mock_file.unlink()
    config = load_config()
    assert config["accounts"] == []


def test_load_config_from_file(clean_config_env):
    """Test loading config from an existing file."""
    _mock_dir, mock_file = clean_config_env
    data = {"browser_headless": True}
    mock_file.write_text(json.dumps(data), encoding="utf-8")

    config = load_config()
    assert config["browser_headless"] is True
    # Default values should still be there
    assert config["browser_timeout"] == 300


def test_load_config_corrupted_file(clean_config_env):
    """Test loading config from a corrupted file."""
    _mock_dir, mock_file = clean_config_env
    mock_file.write_text("invalid json{", encoding="utf-8")

    config = load_config()
    assert config == DEFAULT_CONFIG


def test_load_config_with_credentials_keyring(clean_config_env):
    """Test loading config with credentials stored in keyring."""
    _mock_dir, mock_file = clean_config_env
    data = {
        "accounts": [{"username": "user1", "password": "ENC:v2:encrypted_pw"}],
        "safework_accounts": [{"username": "sw_user", "password": "ENC:v2:sw_encrypted"}],
    }
    mock_file.write_text(json.dumps(data), encoding="utf-8")

    with patch("src.core.secrets_manager.SecretsManager.get_credential") as mock_get:

        def side_effect(service, username):
            if service == "isab_portal" and username == "user1":
                return "keyring_password"
            if service == "safework_portal" and username == "sw_user":
                return "sw_keyring_pw"
            return None

        mock_get.side_effect = side_effect

        config = load_config()
        assert config["accounts"][0]["password"] == "keyring_password"
        assert config["safework_accounts"][0]["password"] == "sw_keyring_pw"


def test_load_config_with_credentials_fallback(clean_config_env):
    """Test loading config with credentials decrypted from file (fallback)."""
    _mock_dir, mock_file = clean_config_env
    data = {
        "accounts": [{"username": "user1", "password": "ENC:v2:encrypted_pw"}],
        "safework_accounts": [{"username": "sw_user", "password": "ENC:v2:sw_encrypted"}],
    }
    mock_file.write_text(json.dumps(data), encoding="utf-8")

    with (
        patch("src.core.secrets_manager.SecretsManager.get_credential", return_value=None),
        patch("src.utils.security.password_manager.decrypt") as mock_decrypt,
    ):
        mock_decrypt.side_effect = lambda x: f"decrypted_{x}"

        config = load_config()
        assert config["accounts"][0]["password"] == "decrypted_ENC:v2:encrypted_pw"


def test_load_config_legacy_migration(clean_config_env):
    """Test migration from old config keys."""
    _mock_dir, mock_file = clean_config_env
    data = {"isab_username": "legacy_user", "isab_password": "legacy_password"}
    mock_file.write_text(json.dumps(data), encoding="utf-8")

    with patch("src.core.config_manager.save_config") as mock_save:
        config = load_config()
        assert "isab_username" not in config
        assert any(a["username"] == "legacy_user" for a in config["accounts"])
        assert mock_save.called


def test_save_config_with_keyring(clean_config_env):
    """Test saving config when keyring is available."""
    _mock_dir, mock_file = clean_config_env
    config = {
        "accounts": [{"username": "user1", "password": "plain_password"}],
        "safework_accounts": [{"username": "sw1", "password": "sw_plain"}],
    }

    with (
        patch("src.core.secrets_manager.SecretsManager.is_available", return_value=True),
        patch("src.core.secrets_manager.SecretsManager.store_credential") as mock_store,
    ):
        save_config(config)

        # Verify stored in keyring
        mock_store.assert_any_call("isab_portal", "user1", "plain_password")
        mock_store.assert_any_call("safework_portal", "sw1", "sw_plain")

        # Verify saved file doesn't have plain password
        saved_data = json.loads(mock_file.read_text(encoding="utf-8"))
        assert "password" not in saved_data["accounts"][0]
        assert "password" not in saved_data["safework_accounts"][0]


def test_save_config_fallback_encryption(clean_config_env):
    """Test saving config when keyring is NOT available (fallback to encryption)."""
    _mock_dir, mock_file = clean_config_env
    config = {"accounts": [{"username": "user1", "password": "plain_password"}]}

    with (
        patch("src.core.secrets_manager.SecretsManager.is_available", return_value=False),
        patch("src.utils.security.password_manager.encrypt", return_value="encrypted_val"),
    ):
        save_config(config)

        saved_data = json.loads(mock_file.read_text(encoding="utf-8"))
        assert saved_data["accounts"][0]["password"] == "encrypted_val"


def test_save_config_io_error(clean_config_env):
    """Test handling of IO errors during save."""
    config = {"test": "data"}
    with patch("os.replace", side_effect=OSError("Permission denied")):
        save_config(config)


def test_save_config_critical_exception(clean_config_env):
    """Test handling of unexpected exceptions during save."""
    config = {"test": "data"}
    with patch("src.core.config_manager.json.dump", side_effect=Exception("Critical Failure")):
        save_config(config)


def test_cache_logic(clean_config_env):
    """Test that cache is used correctly."""
    _reset_configuration_for_testing()
    config1 = load_config()
    config1["test_key"] = "value1"

    # Manually update cache
    config_manager._config_cache = config1

    config2 = load_config()
    assert config2["test_key"] == "value1"
    assert config2 is not config1  # Should be a deepcopy
