import pytest

from src.infrastructure.utils.security import PasswordManager


class TestSecuritySuite:
    """Test suite per src/infrastructure/utils/security.py"""

    @pytest.fixture(autouse=True)
    def setup_security(self, tmp_path, mocker):
        """Setup isolato."""
        # Reset Singleton
        PasswordManager._instance = None

        # Patch paths via the module-level SECURITY_DIR
        fake_key_dir = tmp_path / "security"
        mocker.patch("src.infrastructure.utils.security.SECURITY_DIR", fake_key_dir)

        self.pm = PasswordManager()
        yield

        PasswordManager._instance = None

    def test_key_files_creation(self):
        """Verifica creazione file chiavi."""
        assert self.pm.key_dir.exists()
        assert self.pm.key_file.exists()
        assert self.pm.salt_file.exists()

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
        from cryptography.fernet import Fernet

        fernet = Fernet(self.pm._key)
        raw_enc = fernet.encrypt(b"LegacySecret").decode()
        legacy_cipher = f"ENC:{raw_enc}"

        dec = self.pm.decrypt(legacy_cipher)
        assert dec == "LegacySecret"

    def test_decrypt_plaintext(self):
        """Se non ha tag, restituisce plaintext."""
        assert self.pm.decrypt("PlainData") == "PlainData"

    def test_corrupted_key_regeneration(self, tmp_path, mocker):
        """Se il file chiave è corrotto, deve rigenerarlo."""
        # Corrompiamo il file
        self.pm.key_file.write_bytes(b"TrashData")

        # Resettiamo singleton per forzare ricaricamento
        PasswordManager._instance = None

        # Riapplichiamo il patch per il nuovo setup
        mocker.patch("src.infrastructure.utils.security.SECURITY_DIR", tmp_path / "security")

        # Re-inizializzazione
        new_pm = PasswordManager()

        # Il file chiave dovrebbe essere stato sovrascritto con una chiave valida
        content = new_pm.key_file.read_bytes()
        assert content != b"TrashData"
        assert len(content) > 30  # Fernet key length base64 encoded

    def test_decrypt_error_returns_empty(self):
        """Test gestione errori decrypt."""
        # Stringa corrotta
        bad_enc = "ENC:v2:BadData"
        assert self.pm.decrypt(bad_enc) == ""
