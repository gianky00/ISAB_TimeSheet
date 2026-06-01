import os
from pathlib import Path
from unittest.mock import patch

from src.core.secrets_manager import SecretsManager


class TestSecretsManager:
    @patch("src.core.secrets_manager.keyring.get_password")
    def test_get_github_token_stored(self, mock_get):
        mock_get.return_value = "stored_token"
        assert SecretsManager.get_github_token() == "stored_token"

    @patch("src.core.secrets_manager.keyring.get_password", return_value=None)
    def test_get_github_token_reconstruction(self, mock_get):
        # Deve ricostruire il token hhp_...
        token = SecretsManager.get_github_token()
        assert token.startswith("ghp_")
        assert len(token) == 40

    @patch("src.core.secrets_manager.get_hardware_id", return_value="HW123")
    def test_get_grace_period_key(self, mock_hwid):
        key = SecretsManager.get_grace_period_key()
        assert isinstance(key, bytes)
        assert len(key) == 44  # Fernet base64 length

    @patch.dict(os.environ, {"SYNCROJOB_LICENSE_KEY": "env_key"})
    def test_get_license_key_env(self):
        assert SecretsManager.get_license_key() == b"env_key"

    def test_get_license_key_env_file(self, fs):
        # Mocking _get_env_file_path to point to fake file
        with patch.object(SecretsManager, "_get_env_file_path", return_value=Path("/.env")):
            fs.create_file("/.env", contents='SYNCROJOB_LICENSE_KEY="file_key"\n')
            with patch.dict(os.environ, {"SYNCROJOB_LICENSE_KEY": ""}, clear=True):
                assert SecretsManager.get_license_key() == b"file_key"

    @patch("src.core.secrets_manager.keyring.get_password")
    def test_get_license_key_keyring(self, mock_get):
        mock_get.return_value = "keyring_key"
        with patch.dict(os.environ, {}, clear=True):
            with patch.object(SecretsManager, "_get_key_from_env_file", return_value=None):
                assert SecretsManager.get_license_key() == b"keyring_key"

    @patch("src.core.secrets_manager.keyring.get_password", side_effect=Exception("Failed"))
    def test_is_available_false(self, mock_get):
        SecretsManager._keyring_available = None  # Reset cache
        assert SecretsManager.is_available() is False

    @patch("src.core.secrets_manager.keyring.set_password")
    def test_store_credential(self, mock_set):
        SecretsManager.store_credential("srv", "user", "pass")
        mock_set.assert_called_with("SyncroJob_srv", "user", "pass")

    @patch("src.core.secrets_manager.keyring.get_password")
    def test_get_credential(self, mock_get):
        mock_get.return_value = "secret"
        assert SecretsManager.get_credential("srv", "user") == "secret"

    @patch("src.core.secrets_manager.keyring.delete_password")
    def test_delete_credential(self, mock_delete):
        SecretsManager.delete_credential("srv", "user")
        assert mock_delete.called

    def test_derive_key(self):
        key = SecretsManager.derive_key("pwd", b"salt")
        assert isinstance(key, bytes)
        # Determinismo
        assert SecretsManager.derive_key("pwd", b"salt") == key
