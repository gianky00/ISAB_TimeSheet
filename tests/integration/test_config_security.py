import json

import pytest

from src.core import config_manager


class TestConfigSecurity:
    @pytest.fixture(autouse=True)
    def setup_config(self, tmp_path, mocker):
        env_dir = tmp_path / "syncrojob_test_env"
        env_dir.mkdir(parents=True, exist_ok=True)
        config_file = env_dir / "config.json"

        config_manager._config_cache = None
        mocker.patch("src.core.config_manager.CONFIG_DIR", env_dir)
        mocker.patch("src.core.config_manager.CONFIG_FILE", config_file)
        mocker.patch("src.core.paths.CONFIG_DIR", env_dir)
        mocker.patch("src.core.paths.CONFIG_FILE", config_file)

        original_save = config_manager.save_config

        def sync_save(cfg, async_save=True):
            return original_save(cfg, async_save=False)

        mocker.patch("src.core.config_manager.save_config", side_effect=sync_save)

        mocker.patch("src.core.config.account_manager.SecretsManager.is_available", return_value=False)

        yield config_file
        config_manager._config_cache = None

    def test_save_and_load_encrypted(self, setup_config):
        username = "testuser"
        password = "secret_password"

        config_manager.add_account("isab", {"username": username, "password": password})

        assert setup_config.exists()
        with open(setup_config) as f:
            data = json.load(f)
            acc = data["accounts"][0]
            assert "password" in acc
            assert acc["password"].startswith("ENC:")

        config_manager._config_cache = None
        config = config_manager.load_config()
        assert config["accounts"][0]["password"] == password

    def test_legacy_plaintext_migration(self, setup_config):
        # Usa il formato REALMENTE legacy per innescare migrate_legacy_keys
        legacy_data = {"isab_username": "old_user", "isab_password": "plaintext_pass"}
        with open(setup_config, "w") as f:
            json.dump(legacy_data, f)

        # Caricamento innesca migrazione -> migrate_legacy_keys -> save_config (sync)
        config = config_manager.load_config()
        assert config["accounts"][0]["username"] == "old_user"
        assert config["accounts"][0]["password"] == "plaintext_pass"

        # Verifica che su disco sia ora criptata grazie al salvataggio automatico dopo migrazione
        with open(setup_config) as f:
            data = json.load(f)
            assert "isab_username" not in data
            assert data["accounts"][0]["password"].startswith("ENC:")
