import pytest
import os
import base64
from unittest.mock import patch, MagicMock, mock_open
from src.core.secrets_manager import SecretsManager

class TestSecretsManager:
    """Test coverage for src/core/secrets_manager.py"""

    @pytest.fixture
    def mock_keyring(self):
        with patch('src.core.secrets_manager.keyring') as m:
            yield m

    def test_get_license_key_env_var(self):
        test_key = "dGVzdF9rZXk=" # base64 for "test_key"
        with patch.dict(os.environ, {"SYNCROJOB_LICENSE_KEY": test_key}):
            key = SecretsManager.get_license_key()
            assert key == b"test_key"

    def test_get_license_key_file(self, tmp_path):
        test_key = "dGVzdF9rZXk="
        env_content = f'SYNCROJOB_LICENSE_KEY="{test_key}"\n'
        
        # Mock _get_env_file_path to return a temp file
        with patch('src.core.secrets_manager.SecretsManager._get_env_file_path') as mock_path:
            p = tmp_path / ".env"
            p.write_text(env_content)
            mock_path.return_value = p
            
            # Ensure env var is not set
            with patch.dict(os.environ, {}, clear=True):
                key = SecretsManager.get_license_key()
                assert key == b"test_key"

    def test_get_license_key_keyring(self, mock_keyring):
        test_key = "dGVzdF9rZXk="
        mock_keyring.get_password.return_value = test_key
        
        # Ensure env var and file are not used/found
        with patch.dict(os.environ, {}, clear=True):
            with patch('src.core.secrets_manager.SecretsManager._get_env_file_path') as mock_path:
                mock_path.return_value = MagicMock(exists=lambda: False)
                
                key = SecretsManager.get_license_key()
                assert key == b"test_key"
                mock_keyring.get_password.assert_called_with(SecretsManager.APP_NAME, "license_key")

    def test_get_fallback_key(self, mock_keyring):
        # Force all methods to fail
        mock_keyring.get_password.return_value = None
        with patch.dict(os.environ, {}, clear=True):
            with patch('src.core.secrets_manager.SecretsManager._get_env_file_path') as mock_path:
                mock_path.return_value = MagicMock(exists=lambda: False)
                
                key = SecretsManager.get_license_key()
                assert key is not None # Should return fallback
                # Decode fallback to check logic (optional, but good for regression)

    def test_store_credential(self, mock_keyring):
        SecretsManager.store_credential("svc", "user", "pass")
        mock_keyring.set_password.assert_called_with("SyncroJob_svc", "user", "pass")

    def test_get_credential(self, mock_keyring):
        mock_keyring.get_password.return_value = "pass"
        assert SecretsManager.get_credential("svc", "user") == "pass"
        mock_keyring.get_password.assert_called_with("SyncroJob_svc", "user")

    def test_delete_credential(self, mock_keyring):
        SecretsManager.delete_credential("svc", "user")
        mock_keyring.delete_password.assert_called_with("SyncroJob_svc", "user")

    def test_derive_key(self):
        password = "mypassword"
        salt = b"salt1234"
        key = SecretsManager.derive_key(password, salt)
        assert isinstance(key, bytes)
        assert len(key) > 0

    def test_get_specific_keys(self):
        with patch.object(SecretsManager, 'get_credential') as mock_get:
            mock_get.return_value = "API123"
            assert SecretsManager.get_exa_api_key() == "API123"
            assert SecretsManager.get_github_token() == "API123"
            
            mock_get.return_value = None
            assert SecretsManager.get_openai_key() == ""