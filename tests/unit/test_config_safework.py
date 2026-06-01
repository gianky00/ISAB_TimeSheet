import json

import pytest

from src.core import config_manager


class TestConfigSafeWork:
    @pytest.fixture(autouse=True)
    def setup_config(self, tmp_path, mocker):
        env_dir = tmp_path / "safework_config"
        env_dir.mkdir()
        config_file = env_dir / "config.json"

        config_manager._reset_configuration_for_testing()
        mocker.patch("src.core.config_manager.CONFIG_FILE", config_file)
        mocker.patch("src.core.config_manager.CONFIG_DIR", env_dir)
        mocker.patch("src.core.paths.CONFIG_FILE", config_file)

        # Forza salvataggio sincrono
        original_save = config_manager.save_config

        def mock_save(cfg, async_save=True):
            return original_save(cfg, async_save=False)

        mocker.patch("src.core.config_manager.save_config", side_effect=mock_save)

        yield config_file
        config_manager._reset_configuration_for_testing()

    def test_load_save_safework_accounts(self, setup_config):
        acc = {"username": "sw_user", "password": "sw_password", "is_default": True}
        config_manager.add_account("safework", acc)

        # Fondamentale: reset cache prima del ricaricamento
        config_manager._reset_configuration_for_testing()
        config = config_manager.load_config()

        assert len(config.get("safework_accounts", [])) == 1
        assert config["safework_accounts"][0]["username"] == "sw_user"

    def test_save_safework_config(self, setup_config):
        config_manager.set_config_value("safework_last_site", "SUD")
        # Sincronizzato grazie al patch

        with open(setup_config) as f:
            data = json.load(f)
            assert data["safework_last_site"] == "SUD"
