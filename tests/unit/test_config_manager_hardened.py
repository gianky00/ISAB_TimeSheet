import json
import os
import threading
from unittest.mock import patch

import pytest

from src.core import config_manager
from src.core.config_manager import (
    load_config,
    save_config,
)


class TestConfigManagerHardened:
    @pytest.fixture(autouse=True)
    def setup_config(self, tmp_path, mocker):
        """Setup isolato per ogni test."""
        # Patch delle directory di configurazione
        mock_config_dir = tmp_path / "syncrojob_config"
        mock_config_file = mock_config_dir / "config.json"

        mocker.patch("src.core.config_manager.CONFIG_DIR", mock_config_dir)
        mocker.patch("src.core.config_manager.CONFIG_FILE", mock_config_file)

        # Reset cache globale tra i test
        config_manager._reset_configuration_for_testing()
        return mock_config_file

    def test_load_config_defaults(self, setup_config):
        """Verifica caricamento dei valori di default se il file non esiste."""
        config = load_config()
        assert config["browser_timeout"] == 30
        assert config["ai_model"] == "gemini-1.5-pro"
        assert setup_config.parent.exists()  # Verifica creazione directory

    def test_load_config_corrupted_json(self, setup_config):
        """Verifica resilienza a file JSON corrotto."""
        setup_config.parent.mkdir(parents=True, exist_ok=True)
        setup_config.write_text("{ invalid json ...")

        config = load_config()
        # Deve tornare ai default senza crashare
        assert config["browser_timeout"] == 30

    def test_atomic_save_mechanism(self, setup_config, mocker):
        """Verifica il meccanismo di salvataggio atomico tramite file .tmp."""
        m_replace = mocker.patch("os.replace", side_effect=os.replace)
        mocker.patch("os.fsync")

        config = load_config()
        config["test_key"] = "test_val"
        save_config(config)

        # Verifica che os.replace sia stato chiamato (ultimo step atomico)
        assert m_replace.called
        assert setup_config.exists()

        # Verifica contenuto
        with open(setup_config, "r") as f:
            saved = json.load(f)
            assert saved["test_key"] == "test_val"

    def test_legacy_migration(self, setup_config):
        """Verifica migrazione automatica dai vecchi campi isab_username."""
        setup_config.parent.mkdir(parents=True, exist_ok=True)
        old_data = {
            "isab_username": "old_user",
            "isab_password": "old_password_encrypted",
        }
        setup_config.write_text(json.dumps(old_data))

        # Mock password_manager per decrittare la vecchia pass
        with patch("src.utils.security.password_manager.decrypt", return_value="plain_pass"):
            config = load_config()

        assert "isab_username" not in config
        assert len(config["accounts"]) == 1
        assert config["accounts"][0]["username"] == "old_user"

    def test_concurrent_access_thread_safety(self, setup_config):
        """Verifica che l'accesso multithread alla config sia sicuro."""
        setup_config.parent.mkdir(parents=True, exist_ok=True)
        initial_data = {"base_key": "base_val"}
        setup_config.write_text(json.dumps(initial_data))

        config_manager._reset_configuration_for_testing()

        results = []
        errors = []

        def thread_task():
            try:
                conf = load_config()
                results.append(conf.get("base_key"))
            except Exception as e:
                errors.append(str(e))

        threads = []
        for _i in range(20):
            t = threading.Thread(target=thread_task)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        assert len(errors) == 0, f"Errori rilevati: {errors}"
        assert len(results) == 20
        assert all(v == "base_val" for v in results)

    def test_credential_storage_priority(self, mocker):
        """Verifica che il keyring abbia priorità sul file."""
        mocker.patch("src.core.secrets_manager.SecretsManager.is_available", return_value=True)
        m_store = mocker.patch("src.core.secrets_manager.SecretsManager.store_credential")

        config = load_config()
        config["accounts"] = [{"username": "boss", "password": "top_secret"}]

        save_config(config)

        # Deve aver salvato nel keyring e rimosso la pass dal file
        m_store.assert_called_with("isab_portal", "boss", "top_secret")

        with open(config_manager.CONFIG_FILE, "r") as f:
            data = json.load(f)
            assert "password" not in data["accounts"][0]
