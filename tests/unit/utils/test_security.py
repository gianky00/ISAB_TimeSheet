from pathlib import Path
from unittest.mock import patch

import pytest

from src.utils.security import PasswordManager


class TestSecurity:
    @pytest.fixture(autouse=True)
    def setup_security(self, fs):
        # Setup fake security dir
        self.security_dir = Path("/security")
        fs.create_dir(str(self.security_dir))

        # Patch SECURITY_DIR in paths used by PasswordManager
        with patch("src.utils.security.SECURITY_DIR", self.security_dir):
            # Reset singleton for each test to use the new security_dir
            PasswordManager._instance = None
            self.pm = PasswordManager()
            yield

    def test_singleton(self):
        pm2 = PasswordManager()
        assert self.pm is pm2

    def test_key_creation(self):
        assert self.pm.key_file.exists()
        assert self.pm.salt_file.exists()
        key1 = self.pm.key_file.read_bytes()

        # Ricaricamento chiave esistente
        PasswordManager._instance = None
        pm_reload = PasswordManager()
        assert pm_reload.key_file.read_bytes() == key1

    def test_encrypt_decrypt_v2(self):
        secret = "MyPassword123!"
        encrypted = self.pm.encrypt(secret)

        assert encrypted.startswith("ENC:v2:")
        assert encrypted != secret

        decrypted = self.pm.decrypt(encrypted)
        assert decrypted == secret

    def test_encrypt_already_encrypted(self):
        secret = "ENC:v2:already"
        assert self.pm.encrypt(secret) == secret

    def test_decrypt_legacy(self):
        # Simula formato legacy ENC: (senza v2)
        # Per testarlo dobbiamo usare lo stesso cipher
        raw_encrypted = self.pm._cipher.encrypt(b"legacy_pass").decode()
        legacy_ciphertext = f"ENC:{raw_encrypted}"

        assert self.pm.decrypt(legacy_ciphertext) == "legacy_pass"

    def test_decrypt_plaintext(self):
        # Se non inizia con ENC:, lo torna cos  com'è (compatibilità)
        assert self.pm.decrypt("plaintext") == "plaintext"

    def test_empty_handling(self):
        assert self.pm.encrypt("") == ""
        assert self.pm.decrypt(None) == ""

    def test_invalid_decryption(self):
        assert self.pm.decrypt("ENC:v2:invalid_data") == ""

    @patch("src.utils.security.platform.node", return_value="node1")
    @patch("src.utils.security.uuid.getnode", return_value=12345)
    def test_machine_entropy(self, mock_node, mock_uuid):
        entropy = self.pm._get_machine_entropy()
        assert b"node1" in entropy
        assert b"12345" in entropy
