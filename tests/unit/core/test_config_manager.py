import json
import os
from pathlib import Path
from unittest.mock import patch

import pytest

from src.core.config.defaults import DEFAULT_CONFIG
from src.core.config_manager import (
    _reset_configuration_for_testing,
    get_config_value,
    get_download_path,
    import_config_from_file,
    load_config,
    reset_to_defaults,
    save_config,
    set_config_value,
)


class TestConfigManager:
    @pytest.fixture(autouse=True)
    def setup_fake_config(self, fs):
        _reset_configuration_for_testing()
        from src.core.paths import CONFIG_DIR, CONFIG_FILE

        fs.create_dir(str(CONFIG_DIR))
        self.config_file = CONFIG_FILE
        self.config_dir = CONFIG_DIR

    @patch("src.core.config_manager.decrypt_all_credentials")
    def test_load_config_default(self, mock_decrypt):
        config = load_config()
        # automation_engine è presente nei default
        assert config["automation_engine"] == DEFAULT_CONFIG["automation_engine"]
        assert mock_decrypt.called

    def test_load_config_with_file(self, fs):
        data = {"automation_engine": "playwright", "browser_headless": True}
        fs.create_file(str(self.config_file), contents=json.dumps(data))

        config = load_config()
        assert config["automation_engine"] == "playwright"
        assert config["browser_headless"] is True

    @patch.dict(os.environ, {"SYNCROJOB_AUTOMATION_ENGINE": "custom_engine"})
    def test_load_config_env_override(self):
        config = load_config()
        assert config["automation_engine"] == "custom_engine"

    def test_save_config_sync(self, fs):
        config = {"test": "val"}
        # Usiamo async_save=False per il test sincrono
        res = save_config(config, async_save=False)

        assert res is True
        assert self.config_file.exists()
        saved_data = json.loads(self.config_file.read_text(encoding="utf-8"))
        assert saved_data["test"] == "val"

    def test_get_set_config_value(self):
        set_config_value("custom_key", "custom_val", async_save=False)
        assert get_config_value("custom_key") == "custom_val"

    def test_reset_to_defaults(self):
        set_config_value("automation_engine", "modified", async_save=False)
        reset_to_defaults(async_save=False)
        assert get_config_value("automation_engine") == DEFAULT_CONFIG["automation_engine"]

    def test_get_download_path_standard(self, fs):
        # Path esistente
        path = "/tmp/downloads"
        fs.create_dir(path)
        set_config_value("download_path", path, async_save=False)
        assert get_download_path() == path

    @patch("src.core.config_manager.Path.home")
    def test_get_download_path_fallback(self, mock_home, fs):
        mock_home.return_value = Path("/home/user")
        fs.create_dir("/home/user/Downloads")

        # Path non esistente
        set_config_value("download_path", "/non/existent", async_save=False)
        assert get_download_path() == str(Path("/home/user/Downloads"))

    def test_import_config_from_file(self, fs):
        old_config = {"k": "old"}
        save_config(old_config, async_save=False)

        import_file = Path("/backup.json")
        new_data = {"k": "new"}
        fs.create_file(str(import_file), contents=json.dumps(new_data))

        success, _msg = import_config_from_file(import_file, async_save=False)

        assert success is True
        assert get_config_value("k") == "new"
        # Deve esistere un backup del vecchio
        backups = list(self.config_dir.glob("config_backup_*.json"))
        assert len(backups) == 1
