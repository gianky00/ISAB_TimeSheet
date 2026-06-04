import json
import os
from pathlib import Path
from unittest.mock import patch

import pytest

from src.application.services.config_manager import (
    _reset_configuration_for_testing,
    add_account,
    ensure_config_dir,
    get_config_value,
    get_default_account,
    get_download_path,
    import_config_from_file,
    invalidate_config_cache,
    load_config,
    remove_account,
    reset_to_defaults,
    save_config,
    set_config_value,
    set_config_values,
    set_default_account,
    switch_default_account,
)


class TestConfigManager:
    @pytest.fixture(autouse=True)
    def setup_config(self, tmp_path, mocker):
        """Setup temporary config environment for each test."""
        _reset_configuration_for_testing()

        # Mock paths
        mock_config_dir = tmp_path / "config"
        mock_config_file = mock_config_dir / "config.json"

        mocker.patch("src.application.services.config_manager.CONFIG_DIR", mock_config_dir)
        mocker.patch("src.application.services.config_manager.CONFIG_FILE", mock_config_file)

        return mock_config_dir, mock_config_file

    def test_ensure_config_dir(self, setup_config):
        config_dir, _ = setup_config
        ensure_config_dir()
        assert config_dir.exists()

    def test_load_config_default(self, setup_config):
        config = load_config()
        assert isinstance(config, dict)
        assert "browser_headless" in config

    def test_save_and_load_config(self, setup_config):
        _, _ = setup_config
        config = load_config()
        config["test_key"] = "test_value"

        assert save_config(config, async_save=False) is True

        invalidate_config_cache()
        new_config = load_config()
        assert new_config["test_key"] == "test_value"

    def test_get_set_config_value(self, setup_config):
        set_config_value("another_key", 123, async_save=False)
        assert get_config_value("another_key") == 123
        assert get_config_value("non_existent", "default") == "default"

    def test_set_config_values(self, setup_config):
        updates = {"k1": "v1", "k2": "v2"}
        set_config_values(updates, async_save=False)
        assert get_config_value("k1") == "v1"
        assert get_config_value("k2") == "v2"

    def test_reset_to_defaults(self, setup_config):
        set_config_value("browser_headless", not get_config_value("browser_headless"), async_save=False)
        reset_to_defaults(async_save=False)
        from src.application.services.config.defaults import DEFAULT_CONFIG

        assert get_config_value("browser_headless") == DEFAULT_CONFIG["browser_headless"]

    def test_get_download_path(self, setup_config, mocker):
        # Case 1: Configured path exists
        mock_path = str(Path("/mock/downloads").resolve())
        # Use patch to make it "exist"
        with patch("src.application.services.config_manager.Path.exists", return_value=True):
            set_config_value("download_path", mock_path, async_save=False)
            assert get_download_path() == mock_path

        # Case 2: Configured path doesn't exist -> Fallback to system Downloads
        set_config_value("download_path", "/non/existent/path", async_save=False)
        with patch("src.application.services.config_manager.Path.exists", return_value=False):
            path = get_download_path()
            assert "Downloads" in path

    def test_account_management_isab(self, setup_config):
        acc = {"username": "user1", "password": "pass1", "is_default": True}
        assert add_account("isab", acc, async_save=False) is True

        default = get_default_account("isab")
        assert default["username"] == "user1"

        assert remove_account("isab", "user1", async_save=False) is True
        assert get_default_account("isab") is None

    def test_account_management_safework(self, setup_config):
        acc = {"username": "sw_user", "password": "sw_pass"}
        add_account("safework", acc, async_save=False)

        default = get_default_account("safework")
        assert default["username"] == "sw_user"

    def test_switch_default_account(self, setup_config):
        add_account("isab", {"username": "u1", "password": "p1"}, async_save=False)
        add_account("isab", {"username": "u2", "password": "p2"}, async_save=False)

        set_default_account("isab", "u1", async_save=False)
        assert get_default_account("isab")["username"] == "u1"

        assert switch_default_account("isab", async_save=False) is True
        assert get_default_account("isab")["username"] == "u2"

    def test_import_config_from_file(self, setup_config, tmp_path):
        config_dir, config_file = setup_config
        config_dir.mkdir(parents=True, exist_ok=True)

        # Create a "backup" style file
        import_file = tmp_path / "import.json"
        import_data = {"imported": True, "accounts": []}
        import_file.write_text(json.dumps(import_data), encoding="utf-8")

        # Create existing config to test backup rename
        config_file.write_text("{}", encoding="utf-8")

        success, _ = import_config_from_file(import_file, async_save=False)
        assert success is True
        assert get_config_value("imported") is True

        # Check if backup was created
        backups = list(config_dir.glob("config_backup_*.json"))
        assert len(backups) == 1

    def test_import_config_invalid_json(self, setup_config, tmp_path):
        import_file = tmp_path / "bad.json"
        import_file.write_text("not json", encoding="utf-8")
        success, msg = import_config_from_file(import_file, async_save=False)
        assert success is False
        assert "non è un JSON valido" in msg

    def test_env_var_override(self, setup_config, mocker):
        mocker.patch.dict(os.environ, {"SYNCROJOB_BROWSER_HEADLESS": "true"})
        invalidate_config_cache()
        config = load_config()
        assert config["browser_headless"] is True

        mocker.patch.dict(os.environ, {"SYNCROJOB_MAX_RETRIES": "10"})
        invalidate_config_cache()
        config = load_config()
        if "max_retries" in config:
            assert config["max_retries"] == 10
