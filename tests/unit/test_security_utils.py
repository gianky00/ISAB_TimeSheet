import pytest

from src.utils.security import PasswordManager


class TestPasswordManager:
    @pytest.fixture(autouse=True)
    def setup_pm(self, fs):
        """Setup virtual filesystem and reset singleton."""
        # SECURITY_DIR path is needed in the mock fs
        from src.core.paths import SECURITY_DIR

        fs.create_dir(SECURITY_DIR)

        # Reset the singleton state if needed or ensure it re-initializes
        PasswordManager._instance = None
        pm = PasswordManager()
        return pm

    def test_singleton(self):
        PasswordManager._instance = None
        pm1 = PasswordManager()
        pm2 = PasswordManager()
        assert pm1 is pm2

    def test_initialization_creates_files(self, fs):
        from src.core.paths import SECURITY_DIR

        pm = PasswordManager()
        assert (SECURITY_DIR / "secret.key").exists()
        assert (SECURITY_DIR / "encryption.salt").exists()

    def test_encrypt_decrypt_cycle(self):
        pm = PasswordManager()
        original = "SuperSecret123!"
        encrypted = pm.encrypt(original)

        assert encrypted.startswith("ENC:v2:")
        assert encrypted != original

        decrypted = pm.decrypt(encrypted)
        assert decrypted == original

    def test_encrypt_empty_or_none(self):
        pm = PasswordManager()
        assert pm.encrypt("") == ""
        assert pm.encrypt(None) == ""

    def test_decrypt_empty_or_none(self):
        pm = PasswordManager()
        assert pm.decrypt("") == ""
        assert pm.decrypt(None) == ""

    def test_decrypt_plaintext(self):
        pm = PasswordManager()
        assert pm.decrypt("plain_password") == "plain_password"

    def test_decrypt_legacy_format(self):
        pm = PasswordManager()
        # Generate a legacy encryption (prefix ENC:)
        raw_encrypted = pm._cipher.encrypt(b"legacy_pass").decode()
        legacy_cipher = f"ENC:{raw_encrypted}"

        assert pm.decrypt(legacy_cipher) == "legacy_pass"

    def test_key_persistence(self, fs):
        pm1 = PasswordManager()
        encrypted = pm1.encrypt("persistence_test")

        # Simula restart: cancella istanza e ricarica
        PasswordManager._instance = None
        pm2 = PasswordManager()

        assert pm2.decrypt(encrypted) == "persistence_test"

    def test_encryption_error_handling(self, mocker):
        pm = PasswordManager()
        # Mock cipher to fail
        mocker.patch.object(pm._cipher, "encrypt", side_effect=Exception("Crypt fail"))
        assert pm.encrypt("test") == ""

    def test_decryption_error_handling(self, mocker):
        pm = PasswordManager()
        mocker.patch.object(pm._cipher, "decrypt", side_effect=Exception("Decrypt fail"))
        assert pm.decrypt("ENC:v2:garbage") == ""
