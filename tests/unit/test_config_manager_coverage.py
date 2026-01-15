import json
import pytest
from unittest.mock import MagicMock, patch
from src.core import config_manager

@pytest.fixture(autouse=True)
def mock_config_paths(tmp_path):
    """Reindirizza i path di configurazione su una directory temporanea."""
    # Reset cache before each test
    config_manager._reset_configuration_for_testing()
    
    # Mock CONFIG_DIR and CONFIG_FILE
    new_config_dir = tmp_path / "SyncroJob"
    new_config_dir.mkdir()
    new_config_file = new_config_dir / "config.json"
    
    with patch("src.core.config_manager.CONFIG_DIR", new_config_dir), \
         patch("src.core.config_manager.CONFIG_FILE", new_config_file):
        yield new_config_file

def test_load_defaults(mock_config_paths):
    """Se il file non esiste, deve caricare i default."""
    config = config_manager.load_config()
    assert config["browser_timeout"] == 30
    assert config["reparti"] == ["STRUMENTALE", "ELETTRICO", "CANTIERE", "ANALISI"]

def test_save_and_load_persistence(mock_config_paths):
    """Verifica che i valori salvati vengano ricaricati."""
    config_manager.set_config_value("browser_timeout", 60)
    
    # Force reload by resetting cache
    config_manager._reset_configuration_for_testing()
    
    config = config_manager.load_config()
    assert config["browser_timeout"] == 60

def test_account_management():
    """Test aggiunta, rimozione e default account."""
    # Mock SecretsManager to avoid keyring interactions
    with patch("src.core.config_manager.SecretsManager") as MockSecrets:
        MockSecrets.is_available.return_value = True
        
        # Add Account 1 (Default)
        config_manager.add_account("user1", "pass1")
        accs = config_manager.get_accounts()
        assert len(accs) == 1
        assert accs[0]["username"] == "user1"
        assert accs[0]["default"] is True
        
        # Add Account 2
        config_manager.add_account("user2", "pass2")
        accs = config_manager.get_accounts()
        assert len(accs) == 2
        assert accs[1]["username"] == "user2"
        assert accs[1]["default"] is False # First remains default
        
        # Set Default
        config_manager.set_default_account("user2")
        default = config_manager.get_default_account()
        assert default["username"] == "user2"
        
        # Remove Account
        config_manager.remove_account("user2")
        accs = config_manager.get_accounts()
        assert len(accs) == 1
        assert accs[0]["username"] == "user1"
        assert accs[0]["default"] is True # user1 becomes default again

def test_secure_password_storage(mock_config_paths):
    """Verifica che le password non siano salvate in chiaro nel JSON."""
    with patch("src.core.config_manager.SecretsManager") as MockSecrets, \
         patch("src.utils.security.password_manager.encrypt") as mock_encrypt:
        
        # Scenario 1: Keyring Available
        MockSecrets.is_available.return_value = True
        config_manager.add_account("secure_user", "secure_pass")
        
        # Verify stored in keyring
        MockSecrets.store_credential.assert_called_with("isab_portal", "secure_user", "secure_pass")
        
        # Verify JSON file does NOT contain password
        with open(mock_config_paths, "r") as f:
            data = json.load(f)
            acc = data["accounts"][0]
            assert "password" not in acc or acc["password"] is None

        # Scenario 2: Keyring Unavailable (Fallback encryption)
        MockSecrets.is_available.return_value = False
        mock_encrypt.return_value = "ENCRYPTED_BLOB"
        
        config_manager.add_account("local_user", "local_pass")
        
        # Verify JSON file contains encrypted password
        with open(mock_config_paths, "r") as f:
            data = json.load(f)
            # Find the local_user account
            acc = next(a for a in data["accounts"] if a["username"] == "local_user")
            assert acc["password"] == "ENCRYPTED_BLOB"

def test_atomic_write_failure(mock_config_paths):
    """Test resilienza salvataggio se la scrittura fallisce."""
    # Create valid config first
    config_manager.save_config({"test": 1})
    
    # Mock open to raise exception
    with patch("builtins.open", side_effect=IOError("Disk full")):
        config_manager.save_config({"test": 2})
        
    # Check that original file is untouched (still {"test": 1} effectively, 
    # but we check if it's corrupted or empty)
    with open(mock_config_paths, "r") as f:
        content = json.load(f)
    assert content["test"] == 1