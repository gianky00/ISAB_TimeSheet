from unittest.mock import MagicMock, patch

import pytest

from src.core import config_manager


class TestConfigSafeWork:
    @pytest.fixture(autouse=True)
    def mock_keyring(self):
        # Disable real keyring calls
        with patch("src.core.secrets_manager.keyring"):
            yield

    @patch("src.core.config_manager.SecretsManager")
    @patch("src.core.config_manager._load_base_config")
    @patch("src.core.config_manager.save_config")
    def test_load_save_safework_accounts(self, mock_save, mock_load_base, mock_secrets):
        # Force SecretsManager to return None (simulate not found in keyring)
        mock_secrets.get_credential.return_value = None

        # Setup initial config with SafeWork accounts
        config_data = {
            "safework_accounts": [{"username": "user1", "password": "encrypted_pw"}],
            "accounts": [],  # Standard accounts
        }
        mock_load_base.return_value = config_data

        # Mock decrypt
        with patch("src.utils.security.password_manager.decrypt", return_value="real_pw"):
            # We must be sure load_config doesn't use cache from previous tests
            config_manager._config_cache = None
            config = config_manager.load_config()

            assert "safework_accounts" in config
            assert len(config["safework_accounts"]) > 0
            acc = config["safework_accounts"][0]
            assert acc["password"] == "real_pw"  # Should be decrypted

    @patch("src.core.config_manager.SecretsManager")
    @patch("src.core.config_manager.CONFIG_FILE", new=MagicMock())
    @patch("builtins.open", new_callable=MagicMock)
    @patch("json.dump")
    def test_save_safework_config(self, mock_dump, mock_open, mock_secrets):
        # Force SecretsManager unavailable to test file encryption fallback
        mock_secrets.is_available.return_value = False

        config = {"safework_accounts": [{"username": "user1", "password": "plain_pw"}]}

        with patch("src.utils.security.password_manager.encrypt", return_value="encrypted_pw"):
            config_manager.save_config(config)

            # Check what was dumped
            args, _ = mock_dump.call_args
            dumped_config = args[0]

            acc = dumped_config["safework_accounts"][0]
            assert acc["password"] == "encrypted_pw"
