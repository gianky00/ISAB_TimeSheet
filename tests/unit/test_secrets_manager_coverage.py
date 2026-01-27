import base64
import os
from pathlib import Path
from unittest.mock import patch

import keyring
import pytest

from src.core.secrets_manager import SecretsManager


class TestSecretsManager:
    @pytest.fixture
    def mock_env(self, mocker):
        return mocker.patch.dict(os.environ, {}, clear=True)

    @pytest.fixture
    def mock_keyring(self, mocker):
        mocker.patch("keyring.get_password")
        mocker.patch("keyring.set_password")
        mocker.patch("keyring.delete_password")
        return keyring

    def test_get_license_key_priority_env(self, mock_env):
        """Test retrieving license key from environment variable."""
        valid_key_b64 = "8kHs_rmwqaRUk1AQLGX65g4AEkWUDapWVsMFUQpN9Ek="
        os.environ["SYNCROJOB_LICENSE_KEY"] = valid_key_b64

        key = SecretsManager.get_license_key()
        assert key == base64.urlsafe_b64decode(valid_key_b64)

    def test_get_license_key_priority_file(self, mock_env, tmp_path):
        """Test retrieving license key from .env file when env var is missing."""
        valid_key_b64 = "8kHs_rmwqaRUk1AQLGX65g4AEkWUDapWVsMFUQpN9Ek="
        env_file = tmp_path / ".env"
        env_file.write_text(f'SYNCROJOB_LICENSE_KEY="{valid_key_b64}"')

        with patch.object(SecretsManager, "_get_env_file_path", return_value=env_file):
            key = SecretsManager.get_license_key()
            assert key == base64.urlsafe_b64decode(valid_key_b64)

    def test_get_license_key_priority_keyring(self, mock_env, mock_keyring):
        """Test retrieving license key from keyring when others missing."""
        valid_key_b64 = "8kHs_rmwqaRUk1AQLGX65g4AEkWUDapWVsMFUQpN9Ek="
        keyring.get_password.return_value = valid_key_b64  # mocked

        # Ensure env file fallback fails
        with patch.object(
            SecretsManager, "_get_env_file_path", return_value=Path("non_existent")
        ):
            key = SecretsManager.get_license_key()
            assert key == base64.urlsafe_b64decode(valid_key_b64)
            keyring.get_password.assert_called_with("SyncroJob", "license_key")

    def test_get_license_key_fallback(self, mock_env, mock_keyring):
        """Test fallback hardcoded key."""
        keyring.get_password.return_value = None
        with patch.object(
            SecretsManager, "_get_env_file_path", return_value=Path("non_existent")
        ):
            key = SecretsManager.get_license_key()
            # Should be the hardcoded one
            expected_b64 = "8kHs_rmwqaRUk1AQLGX65g4AEkWUDapWVsMFUQpN9Ek="
            assert key == base64.urlsafe_b64decode(expected_b64)

    def test_get_api_keys(self, mock_keyring):
        """Test retrieval of various API keys."""
        keyring.get_password.return_value = "secret_value"

        assert SecretsManager.get_exa_api_key() == "secret_value"
        keyring.get_password.assert_called_with("SyncroJob_api", "exa_api_key")

        assert SecretsManager.get_gemini_api_key() == "secret_value"
        keyring.get_password.assert_called_with("SyncroJob_api", "GEMINI_API_KEY")

    def test_store_credential(self, mock_keyring):
        SecretsManager.store_credential("api", "user", "pass")
        keyring.set_password.assert_called_with("SyncroJob_api", "user", "pass")

    def test_store_credential_error(self, mock_keyring, capsys):
        keyring.set_password.side_effect = Exception("Keyring locked")
        SecretsManager.store_credential("api", "user", "pass")
        captured = capsys.readouterr()
        assert "Warning: Could not store credential" in captured.out

    def test_delete_credential(self, mock_keyring):
        SecretsManager.delete_credential("api", "user")
        keyring.delete_password.assert_called_with("SyncroJob_api", "user")

    def test_derive_key(self):
        password = "my_password"
        salt = os.urandom(16)
        key = SecretsManager.derive_key(password, salt)
        assert isinstance(key, bytes)
        assert len(base64.urlsafe_b64decode(key)) == 32

    def test_is_available_true(self, mock_keyring):
        assert SecretsManager.is_available() is True

    def test_is_available_false(self, mock_keyring):
        keyring.get_password.side_effect = Exception("Backend unavailable")
        assert SecretsManager.is_available() is False
