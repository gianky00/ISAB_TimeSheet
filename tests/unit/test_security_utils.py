from unittest.mock import patch

import pytest

from src.infrastructure.utils.security import PasswordManager


@pytest.fixture
def clean_security_dir(tmp_path):
    # Mocking di SECURITY_DIR con una dir temporanea
    with patch("src.infrastructure.utils.security.SECURITY_DIR", tmp_path):
        yield tmp_path


def test_password_manager_singleton(clean_security_dir):
    mgr1 = PasswordManager()
    mgr2 = PasswordManager()
    assert mgr1 is mgr2


def test_encrypt_decrypt_flow(clean_security_dir):
    mgr = PasswordManager()
    mgr._reset_for_testing()

    secret = "my_secret_password_123"
    encrypted = mgr.encrypt(secret)
    assert encrypted.startswith("ENC:v2:")

    decrypted = mgr.decrypt(encrypted)
    assert decrypted == secret


def test_decrypt_empty(clean_security_dir):
    mgr = PasswordManager()
    assert mgr.decrypt("") == ""
    assert mgr.encrypt("") == ""


def test_decrypt_invalid_format(clean_security_dir):
    mgr = PasswordManager()
    # Stringa che non inizia con ENC:v2: o ENC:
    raw = "plain_text_not_encrypted"
    assert mgr.decrypt(raw) == raw


def test_legacy_decryption(clean_security_dir):
    # Test migrazione da formato legacy (ENC:) a v2
    mgr = PasswordManager()
    mgr._reset_for_testing()

    secret = "legacy_secret"
    # Criptiamo manualmente con la chiave corrente per simulare formato legacy
    cipher = mgr._cipher
    encrypted_legacy = f"ENC:{cipher.encrypt(secret.encode()).decode()}"

    decrypted = mgr.decrypt(encrypted_legacy)
    assert decrypted == secret


def test_decryption_error_handling(clean_security_dir, caplog):
    mgr = PasswordManager()
    mgr._reset_for_testing()

    # Tentativo di decriptare una stringa v2 malformata
    invalid_encrypted = "ENC:v2:invalid_base64_data_!!!"

    with caplog.at_level("ERROR"):
        decrypted = mgr.decrypt(invalid_encrypted)
        assert decrypted == ""
        assert "Decryption error (v2)" in caplog.text
