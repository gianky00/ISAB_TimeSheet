import pytest
from unittest.mock import patch, MagicMock
from src.core import config_manager
from src.core.secrets_manager import SecretsManager

class TestConfigSafeWork:

    @pytest.fixture(autouse=True)
    def mock_keyring(self):
        # Disable real keyring calls
        with patch('src.core.secrets_manager.keyring'):
            yield

    @patch('src.core.config_manager.SecretsManager')
    @patch('src.core.config_manager.CONFIG_FILE', new=MagicMock())
    @patch('builtins.open', new_callable=MagicMock)
    @patch('json.load')
    @patch('json.dump')
    def test_load_save_safework_accounts(self, mock_dump, mock_load, mock_open, mock_secrets):
        # Force SecretsManager to return None (simulate not found in keyring)
        mock_secrets.get_credential.return_value = None
        
        # Mock load
        mock_load.return_value = {
            "safework_accounts": [
                {"username": "user1", "password": "encrypted_pw"}
            ]
        }
        
        # Mock decrypt
        with patch('src.utils.security.password_manager.decrypt', return_value="real_pw"):
            config = config_manager.load_config()
            
            assert "safework_accounts" in config
            acc = config["safework_accounts"][0]
            assert acc["username"] == "user1"
            assert acc["password"] == "real_pw" # Should be decrypted

    @patch('src.core.config_manager.SecretsManager')
    @patch('src.core.config_manager.CONFIG_FILE', new=MagicMock())
    @patch('builtins.open', new_callable=MagicMock)
    @patch('json.dump')
    def test_save_safework_config(self, mock_dump, mock_open, mock_secrets):
        # Force SecretsManager unavailable to test file encryption fallback
        mock_secrets.is_available.return_value = False
        
        config = {
            "safework_accounts": [
                {"username": "user1", "password": "plain_pw"}
            ]
        }
        
        with patch('src.utils.security.password_manager.encrypt', return_value="encrypted_pw"):
            config_manager.save_config(config)
            
            # Check what was dumped
            args, _ = mock_dump.call_args
            dumped_config = args[0]
            
            acc = dumped_config["safework_accounts"][0]
            assert acc["password"] == "encrypted_pw"
