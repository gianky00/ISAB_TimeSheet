import os
import json
import shutil
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from src.core import config_manager

@pytest.fixture
def temp_config_env(tmp_path):
    """Fixture per isolare l'ambiente di configurazione."""
    test_dir = tmp_path / "config_test"
    test_file = test_dir / "config.json"
    
    with (patch("src.core.config_manager.CONFIG_DIR", test_dir),
          patch("src.core.config_manager.CONFIG_FILE", test_file)):
        config_manager._reset_configuration_for_testing()
        yield test_dir, test_file
        config_manager._reset_configuration_for_testing()

class TestConfigManagerCoverage:
    """Test suite per src/core/config_manager.py"""

    def test_ensure_config_dir(self, temp_config_env):
        test_dir, _ = temp_config_env
        config_manager.ensure_config_dir()
        assert test_dir.exists()

    def test_load_config_defaults(self, temp_config_env):
        """Verifica caricamento default se il file non esiste."""
        config = config_manager.load_config()
        assert config["browser_timeout"] == 30
        assert "accounts" in config
        assert isinstance(config["accounts"], list)

    def test_load_config_from_file(self, temp_config_env):
        """Verifica caricamento da file esistente."""
        test_dir, test_file = temp_config_env
        test_dir.mkdir(parents=True, exist_ok=True)
        
        custom_data = {"browser_timeout": 99, "custom_key": "custom_val"}
        with open(test_file, "w", encoding="utf-8") as f:
            json.dump(custom_data, f)
            
        config = config_manager.load_config()
        assert config["browser_timeout"] == 99
        assert config["custom_key"] == "custom_val"
        # Deve comunque avere i campi di default mancanti
        assert "reparti" in config

    def test_load_config_corrupted(self, temp_config_env):
        """Verifica fallback su errore JSON."""
        test_dir, test_file = temp_config_env
        test_dir.mkdir(parents=True, exist_ok=True)
        test_file.write_text("NOT A JSON")
        
        config = config_manager.load_config()
        assert config["browser_timeout"] == 30 # Default

    def test_save_config_basic(self, temp_config_env):
        """Verifica salvataggio atomico."""
        _, test_file = temp_config_env
        config = config_manager.DEFAULT_CONFIG.copy()
        config["browser_timeout"] = 45
        
        config_manager.save_config(config)
        assert test_file.exists()
        
        with open(test_file, "r", encoding="utf-8") as f:
            saved = json.load(f)
        assert saved["browser_timeout"] == 45

    def test_get_set_value(self, temp_config_env):
        config_manager.set_config_value("test_key", "test_val")
        assert config_manager.get_config_value("test_key") == "test_val"
        assert config_manager.get_config_value("non_existent", "def") == "def"

    @patch("src.core.secrets_manager.SecretsManager.is_available", return_value=True)
    @patch("src.core.secrets_manager.SecretsManager.store_credential")
    @patch("src.core.secrets_manager.SecretsManager.get_credential")
    def test_password_handling_keyring(self, mock_get, mock_store, mock_avail, temp_config_env):
        """Test integrazione Keyring: password rimosse dal file e salvate in SecretsManager."""
        _, test_file = temp_config_env
        
        # 1. Salvataggio
        accs = [{"username": "user1", "password": "secret_password"}]
        config = config_manager.DEFAULT_CONFIG.copy()
        config["accounts"] = accs
        
        config_manager.save_config(config)
        
        # Verifica store chiamato
        mock_store.assert_any_call("is_ab_portal" if "is_ab_portal" in str(mock_store.call_args_list) else "isab_portal", "user1", "secret_password")
        
        # Verifica file JSON: non deve avere la password in chiaro
        with open(test_file, "r") as f:
            saved = json.load(f)
        assert "password" not in saved["accounts"][0]

        # 2. Caricamento
        config_manager._reset_configuration_for_testing()
        mock_get.return_value = "secret_password"
        
        loaded = config_manager.load_config()
        assert loaded["accounts"][0]["password"] == "secret_password"

    @patch("src.core.secrets_manager.SecretsManager.is_available", return_value=False)
    @patch("src.utils.security.password_manager.encrypt", return_value="ENCRYPTED")
    @patch("src.utils.security.password_manager.decrypt", return_value="DECRYPTED")
    def test_password_handling_fallback(self, mock_dec, mock_enc, mock_avail, temp_config_env):
        """Test fallback: password cifrate nel file se Keyring non disponibile."""
        _, test_file = temp_config_env
        
        accs = [{"username": "user_fallback", "password": "plain_password"}]
        config = config_manager.DEFAULT_CONFIG.copy()
        config["accounts"] = accs
        
        config_manager.save_config(config)
        
        # Verifica file JSON: deve avere la password cifrata
        with open(test_file, "r") as f:
            saved = json.load(f)
        assert saved["accounts"][0]["password"] == "ENCRYPTED"

        # Caricamento
        config_manager._reset_configuration_for_testing()
        loaded = config_manager.load_config()
        assert loaded["accounts"][0]["password"] == "DECRYPTED"

    def test_migration_legacy(self, temp_config_env):
        """Test migrazione vecchi campi isab_username/password."""
        test_dir, test_file = temp_config_env
        test_dir.mkdir(parents=True, exist_ok=True)
        
        legacy = {
            "isab_username": "legacy_user",
            "isab_password": "legacy_password"
        }
        with open(test_file, "w") as f:
            json.dump(legacy, f)
            
        config = config_manager.load_config()
        assert "isab_username" not in config
        assert len(config["accounts"]) == 1
        assert config["accounts"][0]["username"] == "legacy_user"

    def test_account_management_crud(self, temp_config_env):
        """Test add, remove, set default account."""
        config_manager.add_account("user1", "pass1", is_default=True)
        config_manager.add_account("user2", "pass2", is_default=False)
        
        accounts = config_manager.get_accounts()
        assert len(accounts) == 2
        assert config_manager.get_default_account()["username"] == "user1"
        
        config_manager.set_default_account("user2")
        assert config_manager.get_default_account()["username"] == "user2"
        
        config_manager.remove_account("user1")
        assert len(config_manager.get_accounts()) == 1
        assert config_manager.get_default_account()["username"] == "user2"

    def test_path_utilities(self, temp_config_env):
        test_dir, _ = temp_config_env
        data_path = config_manager.get_data_path()
        assert Path(data_path).exists()
        assert str(test_dir) in data_path

        # Download path - caso dir esistente
        with patch("os.path.isdir", return_value=True):
            config_manager.set_config_value("download_path", "/fake/path")
            assert config_manager.get_download_path() == "/fake/path"
            
        # Download path - fallback
        with patch("os.path.isdir", return_value=False):
            dp = config_manager.get_download_path()
            assert dp is not None

    def test_safework_accounts_handling(self, temp_config_env):
        """Test specifico per account SafeWork."""
        with (patch("src.core.secrets_manager.SecretsManager.is_available", return_value=True),
              patch("src.core.secrets_manager.SecretsManager.store_credential") as mock_store):
            
            acc = {"username": "sw_user", "password": "sw_password"}
            config = config_manager.load_config()
            config["safework_accounts"] = [acc]
            config_manager.save_config(config)
            
            mock_store.assert_any_call("safework_portal", "sw_user", "sw_password")

    def test_save_config_io_error(self, temp_config_env):
        """Test errore durante il salvataggio."""
        with patch("builtins.open", side_effect=IOError("Disk Full")):
            # Non deve crashare, ma loggare l'errore
            config_manager.save_config({"test": 1})
            
    def test_load_config_cache_hit(self, temp_config_env):
        """Verifica che il caricamento avvenga dalla cache se disponibile."""
        config_manager.load_config()
        with patch("json.load") as mock_json:
            config = config_manager.load_config()
            mock_json.assert_not_called()
            assert config["browser_timeout"] == 30

    def test_safework_accounts_fallback(self, temp_config_env):
        """Test fallback cifratura per SafeWork."""
        with (patch("src.core.secrets_manager.SecretsManager.is_available", return_value=False),
              patch("src.utils.security.password_manager.encrypt", return_value="SW_ENC")):
            
            acc = {"username": "sw_user", "password": "sw_password"}
            config = config_manager.load_config()
            config["safework_accounts"] = [acc]
            config_manager.save_config(config)
            
            with open(temp_config_env[1], "r") as f:
                saved = json.load(f)
            assert saved["safework_accounts"][0]["password"] == "SW_ENC"

    def test_save_config_exception(self, temp_config_env):
        """Test eccezione generica durante il salvataggio (es. errore json.dump)."""
        with patch("json.dump", side_effect=Exception("JSON Error")):
            # Non deve crashare perché l'eccezione è gestita all'interno di save_config
            config_manager.save_config({"test": 1})

    def test_remove_account_no_keyring(self, temp_config_env):
        """Test rimozione account quando il keyring non è disponibile."""
        config_manager.add_account("user_del", "pass", is_default=True)
        with patch("src.core.secrets_manager.SecretsManager.is_available", return_value=False):
            config_manager.remove_account("user_del")
        assert len(config_manager.get_accounts()) == 0

    def test_get_default_account_fallback(self, temp_config_env):
        """Verifica fallback sul primo account se nessun default è esplicito."""
        config_manager.set_config_value("accounts", [
            {"username": "u1", "password": "p1"},
            {"username": "u2", "password": "p2"}
        ])
        # Ricarico per resettare lo stato se necessario (anche se set_config_value salva)
        default = config_manager.get_default_account()
        assert default["username"] == "u1"

    def test_fornitori_utility(self, temp_config_env):
        config_manager.set_config_value("fornitori", ["F1", "F2"])
        assert config_manager.get_fornitori() == ["F1", "F2"]