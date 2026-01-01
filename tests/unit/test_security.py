import pytest
from src.utils.security import password_manager

class TestSecurity:

    def test_encryption_decryption(self):
        text = "my_secret_password"
        encrypted = password_manager.encrypt(text)
        assert encrypted != text
        
        decrypted = password_manager.decrypt(encrypted)
        assert decrypted == text

    def test_decrypt_invalid_data(self):
        # The current implementation returns the original string if decryption fails
        assert password_manager.decrypt("not_encrypted") == "not_encrypted"
        assert password_manager.decrypt(None) == ""

    def test_encrypt_none(self):
        assert password_manager.encrypt(None) == ""