import json
from unittest.mock import patch

import pytest

from src.core import config_manager
from src.core.secrets_manager import SecretsManager
from src.utils.security import password_manager


# Usa pytest invece di unittest
class TestConfigSecurity:
    @pytest.fixture(autouse=True)
    def setup_method(self, _isolate_config):
        """
        Questa fixture usa _isolate_config per creare un ambiente pulito
        e applica patch aggiuntive necessarie per questo test.
        """
        fake_file = _isolate_config
        # Patch SECURITY_DIR per usare la directory temporanea
        with (
            patch("src.utils.security.SECURITY_DIR", fake_file.parent),
        ):
            # Forza il ricaricamento della chiave nel contesto patchato
            password_manager._reset_for_testing()

            # Mock SecretsManager per essere non disponibile
            with patch.object(SecretsManager, "is_available", return_value=False):
                yield

    def test_save_and_load_encrypted(self):
        # 1. Crea una config con una password
        username = "testuser"
        password = "secret_password"

        # Usa add_account che chiama save_config
        config_manager.add_account("isab", {"username": username, "password": password})

        # 2. Verifica che il file sia criptato
        with open(config_manager.CONFIG_FILE) as f:
            saved_data = json.load(f)

        # Cerca l'account creato (nella chiave 'accounts' per bot_type 'isab')
        saved_account = next(a for a in saved_data["accounts"] if a["username"] == username)
        saved_password = saved_account["password"]
        assert saved_password != password
        assert saved_password.startswith("ENC:")

        # 3. Carica la config - deve essere in chiaro
        loaded_config = config_manager.load_config()
        loaded_account = next(a for a in loaded_config["accounts"] if a["username"] == username)
        loaded_password = loaded_account["password"]

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
        with open(config_manager.CONFIG_FILE) as f:
            saved_data = json.load(f)

        saved_pass = saved_data["accounts"][0]["password"]
        assert saved_pass.startswith("ENC:")
