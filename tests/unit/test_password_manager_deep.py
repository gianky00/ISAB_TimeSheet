from src.utils.security import PasswordManager


class TestPasswordManagerDeep:
    def test_encrypt_decrypt_v2(self):
        pm = PasswordManager()
        # Reset to ensure key is created
        pm._initialize()

        plaintext = "SuperSecret123"
        encrypted = pm.encrypt(plaintext)
        assert encrypted.startswith("ENC:v2:")

        decrypted = pm.decrypt(encrypted)
        assert decrypted == plaintext

    def test_legacy_format_decryption(self):
        pm = PasswordManager()
        plaintext = "Legacy"
        # Manually create legacy format ENC:
        raw_enc = pm._cipher.encrypt(plaintext.encode()).decode()
        legacy_ciphertext = f"ENC:{raw_enc}"

        assert pm.decrypt(legacy_ciphertext) == plaintext

    def test_encrypt_empty_and_already_encrypted(self):
        pm = PasswordManager()
        assert pm.encrypt("") == ""
        assert pm.encrypt("ENC:v2:data") == "ENC:v2:data"

    def test_decrypt_errors(self):
        pm = PasswordManager()
        assert pm.decrypt("ENC:v2:INVALID") == ""
        assert pm.decrypt("ENC:INVALID") == ""
        assert pm.decrypt(None) == ""
