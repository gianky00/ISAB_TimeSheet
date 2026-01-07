import json
from unittest.mock import patch

import pytest

from src.core import config_manager
from src.core.secrets_manager import SecretsManager
from src.utils.security import password_manager


# Usa pytest invece di unittest
class TestConfigSecurity:

    @pytest.fixture(autouse=True)
    def setup_method(self, setup_clean_config):
        """
        Questa fixture usa setup_clean_config per creare un ambiente pulito
        e applica patch aggiuntive necessarie per questo test.
        """
        # Patch password_manager per usare la directory temporanea
        with patch.object(password_manager, "_KEY_DIR", new=setup_clean_config.parent), patch.object(
            password_manager, "_KEY_FILE", new=setup_clean_config.parent / "secret.key"
        ):

            # Forza il ricaricamento della chiave nel contesto patchato
            password_manager._key = password_manager._load_or_create_key()

            # Mock SecretsManager per essere non disponibile
            with patch.object(SecretsManager, "is_available", return_value=False):
                yield

    def test_save_and_load_encrypted(self):
        # 1. Crea una config con una password
        username = "testuser"
        password = "secret_password"

        # Usa add_account che chiama save_config
        config_manager.add_account(username, password)

        # 2. Verifica che il file sia criptato
        with open(config_manager.CONFIG_FILE, "r") as f:
            saved_data = json.load(f)

        saved_password = saved_data["accounts"][0]["password"]
        assert saved_password != password
        assert saved_password.startswith("ENC:")

        # 3. Carica la config - deve essere in chiaro
        loaded_config = config_manager.load_config()
        loaded_password = loaded_config["accounts"][0]["password"]

        assert loaded_password == password

    def test_legacy_plaintext_migration(self):
        # 1. Scrivi una vecchia config manualmente
        legacy_data = {"accounts": [{"username": "old", "password": "plaintext_pass", "default": True}]}
        with open(config_manager.CONFIG_FILE, "w") as f:
            json.dump(legacy_data, f)

        # 2. Caricala - dovrebbe gestire il testo in chiaro
        config = config_manager.load_config()
        assert config["accounts"][0]["password"] == "plaintext_pass"

        # 3. Salvala (innesca la migrazione)
        config_manager.save_config(config)

        # 4. Verifica che il file sia criptato
        with open(config_manager.CONFIG_FILE, "r") as f:
            saved_data = json.load(f)

        saved_pass = saved_data["accounts"][0]["password"]
        assert saved_pass.startswith("ENC:")
