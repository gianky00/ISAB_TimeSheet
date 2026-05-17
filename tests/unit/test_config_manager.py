from pathlib import Path

import pytest

from src.core import config_manager
from src.core.config_manager import (
    _reset_configuration_for_testing,
    get_config_value,
    load_config,
    save_config,
    set_config_value,
)


class TestConfigManager:
    @pytest.fixture(autouse=True)
    def setup_config(self, fs):
        """Setup del filesystem virtuale e reset cache."""
        fs.create_dir("/config")
        _reset_configuration_for_testing()
        yield
        _reset_configuration_for_testing()

    def test_load_config_default(self, fs):
        """Testa il caricamento dei default se il file non esiste."""
        from src.core import paths

        # pyfakefs usa 'contents'
        fs.create_file(paths.CONFIG_FILE, contents="{}")

        config = load_config()
        assert isinstance(config, dict)
        assert "browser_headless" in config

    def test_save_and_load_config(self, fs):
        """Testa il salvataggio e rilettura della configurazione."""
        from src.core import paths

        config = {"test_key": "test_value"}

        success = save_config(config)
        assert success is True
        assert Path(paths.CONFIG_FILE).exists()

        # Ricarica e verifica
        new_config = load_config()
        assert new_config["test_key"] == "test_value"

    def test_get_set_config_value(self, fs):
        """Testa getter e setter atomici."""
        set_config_value("api_key", "secret123")
        assert get_config_value("api_key") == "secret123"
        # Se chiedo una chiave che non c'è, deve ridare default
        assert get_config_value("non_existent_key", "my_default") == "my_default"

    def test_get_download_path(self, fs):
        """Testa il recupero del path di download."""
        # Se non impostato, usa home / Downloads
        path = config_manager.get_download_path()
        assert "Downloads" in path

        # Se impostato e esistente
        fs.create_dir("/custom/downloads")
        set_config_value("download_path", "/custom/downloads")
        assert config_manager.get_download_path() == "/custom/downloads"

    def test_reset_to_defaults(self, fs):
        """Testa il reset ai default."""
        set_config_value("custom_key", "custom_val")
        config_manager.reset_to_defaults()
        assert get_config_value("custom_key") is None
        assert "browser_headless" in load_config()

    def test_atomic_write_failure(self, fs, mocker):
        """Testa il fallimento della scrittura atomica."""
        # Mock open per lanciare errore
        mocker.patch("pathlib.Path.open", side_effect=OSError("Disk full"))
        success = config_manager._atomic_write_json(Path("/fake.json"), {})
        assert success is False
