
import os
import base64
import pytest
from unittest.mock import MagicMock, patch
from src.utils.security import PasswordManager

class TestSecurity:
    @pytest.fixture
    def manager(self, tmp_path, mocker):
        # Mock class-level attributes to use tmp_path
        key_dir = tmp_path / "security"
        mocker.patch("src.utils.security.PasswordManager._KEY_DIR", key_dir)
        mocker.patch("src.utils.security.PasswordManager._KEY_FILE", key_dir / "secret.key")
        mocker.patch("src.utils.security.PasswordManager._SALT_FILE", key_dir / "encryption.salt")
        
        # Reset singleton
        PasswordManager._instance = None
        return PasswordManager()

    def test_key_creation_persistence(self, manager, tmp_path):
        """Test that keys are created and persisted."""
        key_file = tmp_path / "security" / "secret.key"
        salt_file = tmp_path / "security" / "encryption.salt"
        
        assert key_file.exists()
        assert salt_file.exists()
        
        first_key = key_file.read_bytes()
        
        # New instance should load same key
        PasswordManager._instance = None
        new_manager = PasswordManager()
        assert key_file.read_bytes() == first_key

    def test_encrypt_decrypt(self, manager):
        plaintext = "my_secret_password"
        ciphertext = manager.encrypt(plaintext)
        
        assert ciphertext.startswith("ENC:v2:")
        assert ciphertext != plaintext
        
        decrypted = manager.decrypt(ciphertext)
        assert decrypted == plaintext

    def test_encrypt_idempotency(self, manager):
        plaintext = "secret"
        c1 = manager.encrypt(plaintext)
        c2 = manager.encrypt(c1)
        assert c1 == c2 # Should not re-encrypt

    def test_decrypt_legacy(self, manager):
        plaintext = "legacy_secret"
        # Manually create a "legacy" style encryption (which just used the same cipher but ENC: prefix)
        raw_encrypted = manager._cipher.encrypt(plaintext.encode()).decode()
        legacy_cipher = f"ENC:{raw_encrypted}"
        
        assert manager.decrypt(legacy_cipher) == plaintext

    def test_decrypt_plaintext_fallback(self, manager):
        assert manager.decrypt("not_encrypted") == "not_encrypted"
        assert manager.decrypt("") == ""

    def test_encryption_error_handling(self, manager):
        # Mock cipher to fail
        manager._cipher.encrypt = MagicMock(side_effect=Exception("Crypt fail"))
        assert manager.encrypt("data") == ""
        
        # Corrupt ciphertext
        assert manager.decrypt("ENC:v2:corrupted") == ""
