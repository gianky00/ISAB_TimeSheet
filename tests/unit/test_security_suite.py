from unittest.mock import patch

import pytest

from src.utils.security import PasswordManager


class TestSecuritySuite:
    """Test suite per src/utils/security.py"""

    @pytest.fixture(autouse=True)
    def setup_security(self, tmp_path):
        """Setup isolato."""
        # Reset Singleton
        PasswordManager._instance = None

        # Patch paths directly on the class
        fake_key_dir = tmp_path / "security"
        fake_key_file = fake_key_dir / "secret.key"
        fake_salt_file = fake_key_dir / "encryption.salt"

        # Patching class attributes
        with patch.object(PasswordManager, '_KEY_DIR', fake_key_dir), \
             patch.object(PasswordManager, '_KEY_FILE', fake_key_file), \
             patch.object(PasswordManager, '_SALT_FILE', fake_salt_file):

            self.pm = PasswordManager()
            yield

        PasswordManager._instance = None

    def test_key_files_creation(self):
        """Verifica creazione file chiavi."""
        assert self.pm._KEY_DIR.exists()
        assert self.pm._KEY_FILE.exists()
        assert self.pm._SALT_FILE.exists()

    def test_encrypt_decrypt_cycle(self):
        """Test roundtrip encrypt -> decrypt."""
        secret = "MySecretData123!"
        enc = self.pm.encrypt(secret)

        assert enc != secret
        assert enc.startswith("ENC:v2:")

        dec = self.pm.decrypt(enc)
        assert dec == secret

    def test_encrypt_idempotency(self):
        """Se cripto un valore già taggato, non lo cripta di nuovo."""
        enc = "ENC:v2:GiàCriptato"
        assert self.pm.encrypt(enc) == enc

    def test_decrypt_legacy(self):
        """Test decrypt vecchio formato ENC: (simulato)."""
        # Creiamo un ciphertext legacy valido
        # Per farlo, dobbiamo usare la stessa chiave del PM corrente
        from cryptography.fernet import Fernet
        fernet = Fernet(self.pm._key)
        raw_enc = fernet.encrypt(b"LegacySecret").decode()
        legacy_cipher = f"ENC:{raw_enc}"

        dec = self.pm.decrypt(legacy_cipher)
        assert dec == "LegacySecret"

    def test_decrypt_plaintext(self):
        """Se non ha tag, restituisce plaintext."""
        assert self.pm.decrypt("PlainData") == "PlainData"

    def test_corrupted_key_regeneration(self):
        """Se il file chiave è corrotto, deve rigenerarlo."""
        # Corrompiamo il file
        self.pm._KEY_FILE.write_bytes(b"TrashData")

        # Resettiamo singleton per forzare ricaricamento
        PasswordManager._instance = None

        # Re-inizializzazione (i patch sono ancora attivi nel setup)
        new_pm = PasswordManager()

        # Il file chiave dovrebbe essere stato sovrascritto con una chiave valida
        content = new_pm._KEY_FILE.read_bytes()
        assert content != b"TrashData"
        assert len(content) > 30 # Fernet key length base64 encoded

    def test_decrypt_error_returns_empty(self):
        """Test gestione errori decrypt."""
        # Stringa corrotta
        bad_enc = "ENC:v2:BadData"
        assert self.pm.decrypt(bad_enc) == ""
