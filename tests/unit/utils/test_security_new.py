from pathlib import Path
from unittest.mock import patch

import pytest

from src.utils.security import PasswordManager


class TestPasswordManager:
    @pytest.fixture(autouse=True)
    def setup_mock_security(self, fs):
        # Patchiamo SECURITY_DIR all'interno del modulo security prima di istanziare
        self.fake_sec_dir = Path("/fake_security")
        fs.create_dir(str(self.fake_sec_dir))

        with patch("src.utils.security.SECURITY_DIR", self.fake_sec_dir):
            PasswordManager._instance = None
            self.pm = PasswordManager()
            yield self.pm

    def test_key_creation(self):
        assert self.pm.key_file.exists()
        assert self.pm.salt_file.exists()
        key = self.pm.key_file.read_bytes()
        assert len(key) == 44  # base64 length for 32 bytes

    def test_encrypt_decrypt_v2(self):
        secret = "my_password_123"
        encrypted = self.pm.encrypt(secret)
        assert encrypted.startswith("ENC:v2:")

        decrypted = self.pm.decrypt(encrypted)
        assert decrypted == secret

    def test_encrypt_idempotent(self):
        encrypted = self.pm.encrypt("secret")
        assert self.pm.encrypt(encrypted) == encrypted

    def test_decrypt_plaintext_fallback(self):
        assert self.pm.decrypt("raw_text") == "raw_text"
        assert self.pm.decrypt("") == ""

    def test_decrypt_legacy_format(self):
        secret = "legacy_pwd"
        encrypted_raw = self.pm._cipher.encrypt(secret.encode()).decode()
        legacy = f"ENC:{encrypted_raw}"
        assert self.pm.decrypt(legacy) == secret

    @patch("src.utils.security.logger")
    def test_decrypt_error_handling(self, mock_logger):
        invalid = "ENC:v2:invalid_base64"
        assert self.pm.decrypt(invalid) == ""
        assert mock_logger.exception.called

    def test_get_machine_entropy(self):
        entropy = self.pm._get_machine_entropy()
        assert isinstance(entropy, bytes)
        assert b"|" in entropy

    def test_singleton(self):
        pm2 = PasswordManager()
        assert self.pm is pm2
