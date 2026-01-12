import base64
import os
import pytest
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path
from src.core.secrets_manager import SecretsManager

class TestSecretsManagerCoverage:
    """Test suite for increasing coverage of SecretsManager."""

    @pytest.fixture
    def mock_keyring(self):
        with patch("src.core.secrets_manager.keyring") as mk:
            yield mk

    def test_derive_key(self):
        """Test PBKDF2 key derivation."""
        password = "test_password"
        salt = b"test_salt_123456"  # Must be bytes
        
        key1 = SecretsManager.derive_key(password, salt)
        key2 = SecretsManager.derive_key(password, salt)
        
        assert isinstance(key1, bytes)
        assert len(key1) > 0
        assert key1 == key2  # Deterministic
        
        # Change password
        key3 = SecretsManager.derive_key("wrong_password", salt)
        assert key1 != key3

    def test_get_license_key_from_env(self, mock_keyring):
        """Test retrieval from environment variable (Priority 1)."""
        fake_key = b"fake_license_key_123"
        encoded_key = base64.urlsafe_b64encode(fake_key).decode('utf-8')
        
        with patch.dict(os.environ, {"SYNCROJOB_LICENSE_KEY": encoded_key}):
            # Ensure other methods fail or are not called if logic is correct, 
            # but even if they exist, Env should win.
            result = SecretsManager.get_license_key()
            assert result == fake_key

    def test_get_license_key_from_file(self, mock_keyring):
        """Test retrieval from .env file (Priority 2)."""
        fake_key = b"file_license_key_456"
        encoded_key = base64.urlsafe_b64encode(fake_key).decode('utf-8')
        file_content = f'SYNCROJOB_LICENSE_KEY="{encoded_key}"\nOTHER=THING'
        
        # Ensure Env var is NOT set
        with patch.dict(os.environ, {}, clear=True):
            # Mock Path.exists and open
            with patch("pathlib.Path.exists", return_value=True), \
                 patch("builtins.open", mock_open(read_data=file_content)):
                
                result = SecretsManager.get_license_key()
                assert result == fake_key

    def test_get_license_key_from_keyring(self, mock_keyring):
        """Test retrieval from keyring (Priority 3)."""
        fake_key = b"keyring_license_key_789"
        encoded_key = base64.urlsafe_b64encode(fake_key).decode('utf-8')
        
        mock_keyring.get_password.return_value = encoded_key
        
        # Ensure Env var and File are NOT available
        with patch.dict(os.environ, {}, clear=True):
            with patch("pathlib.Path.exists", return_value=False):
                result = SecretsManager.get_license_key()
                assert result == fake_key
                mock_keyring.get_password.assert_called_with(SecretsManager.APP_NAME, "license_key")

    def test_get_license_key_none_found(self, mock_keyring):
        """Test return None when no key is found."""
        mock_keyring.get_password.return_value = None
        with patch.dict(os.environ, {}, clear=True):
            with patch("pathlib.Path.exists", return_value=False):
                assert SecretsManager.get_license_key() is None

    def test_get_license_key_invalid_base64_env(self):
        """Test graceful failure on invalid base64 in env."""
        with patch.dict(os.environ, {"SYNCROJOB_LICENSE_KEY": "!!!INVALID!!!"}):
            with patch("pathlib.Path.exists", return_value=False):
                # Should return None (or check next steps, but here next steps are empty)
                assert SecretsManager.get_license_key() is None

    def test_get_license_key_invalid_base64_file(self):
        """Test graceful failure on invalid base64 in file."""
        with patch.dict(os.environ, {}, clear=True):
            with patch("pathlib.Path.exists", return_value=True), \
                 patch("builtins.open", mock_open(read_data='SYNCROJOB_LICENSE_KEY="!!!INVALID!!!"')):
                assert SecretsManager.get_license_key() is None

    def test_is_available_true(self, mock_keyring):
        """Test keyring availability check - Success."""
        mock_keyring.get_password.return_value = None # Doesn't raise
        assert SecretsManager.is_available() is True

    def test_is_available_false(self, mock_keyring):
        """Test keyring availability check - Failure."""
        mock_keyring.get_password.side_effect = Exception("Keyring broken")
        assert SecretsManager.is_available() is False

    def test_store_credential(self, mock_keyring):
        """Test storing credential."""
        SecretsManager.store_credential("test_service", "user", "pass")
        mock_keyring.set_password.assert_called_with(
            f"{SecretsManager.APP_NAME}_test_service", "user", "pass"
        )

    def test_store_credential_error(self, mock_keyring):
        """Test storing credential handles error silently (prints warning)."""
        mock_keyring.set_password.side_effect = Exception("Db locked")
        # Should not raise
        SecretsManager.store_credential("test_service", "user", "pass")

    def test_get_credential(self, mock_keyring):
        """Test getting credential."""
        mock_keyring.get_password.return_value = "secret_pass"
        res = SecretsManager.get_credential("api", "gh_token")
        assert res == "secret_pass"
        mock_keyring.get_password.assert_called_with(
            f"{SecretsManager.APP_NAME}_api", "gh_token"
        )

    def test_get_credential_error(self, mock_keyring):
        """Test getting credential handles error."""
        mock_keyring.get_password.side_effect = Exception("Error")
        assert SecretsManager.get_credential("foo", "bar") is None

    def test_delete_credential(self, mock_keyring):
        """Test deleting credential."""
        SecretsManager.delete_credential("api", "user")
        mock_keyring.delete_password.assert_called_with(
            f"{SecretsManager.APP_NAME}_api", "user"
        )

    def test_delete_credential_error(self, mock_keyring):
        """Test deleting credential handles error."""
        mock_keyring.delete_password.side_effect = Exception("Not found")
        # Should not raise
        SecretsManager.delete_credential("api", "user")

    def test_delete_credential_exception(self):
        """Test delete_credential exception handling."""
        with patch("keyring.delete_password", side_effect=Exception("Keyring Fail")):
            # Should not crash
            SecretsManager.delete_credential("any", "user")

    def test_specific_api_getters(self, mock_keyring):
        """Test wrapper methods for specific keys."""
        mock_keyring.get_password.return_value = "test_val"
        
        assert SecretsManager.get_exa_api_key() == "test_val"
        assert SecretsManager.get_github_token() == "test_val"
        assert SecretsManager.get_openai_key() == "test_val"
        assert SecretsManager.get_gemini_api_key() == "test_val"

    def test_specific_api_getters_none(self, mock_keyring):
        """Test wrapper methods when key is missing."""
        mock_keyring.get_password.return_value = None
        
        assert SecretsManager.get_exa_api_key() == ""

