"""
Tests for SecretsManager.get_license_key refactoring.
Aims for 100% coverage and functional parity.
"""

import base64
import os
import sys
from pathlib import Path
from unittest.mock import patch

from src.core.secrets_manager import SecretsManager


def test_get_key_from_env():
    """Test variabile d'ambiente."""
    test_key_bytes = b"env_test_key"
    test_key_b64 = base64.urlsafe_b64encode(test_key_bytes).decode()
    with patch.dict(os.environ, {"SYNCROJOB_LICENSE_KEY": test_key_b64}):
        res = SecretsManager._get_key_from_env()
        assert res == test_key_bytes

def test_get_key_from_env_invalid():
    """Test variabile d'ambiente non valida."""
    with patch.dict(os.environ, {"SYNCROJOB_LICENSE_KEY": "!!!not_b64!!!"}):
        res = SecretsManager._get_key_from_env()
        assert res is None

def test_get_key_from_env_file(tmp_path):
    """Test caricamento da file .env."""
    test_key_bytes = b"file_test_key"
    test_key_b64 = base64.urlsafe_b64encode(test_key_bytes).decode()
    env_file = tmp_path / ".env"
    env_file.write_text(f'SYNCROJOB_LICENSE_KEY="{test_key_b64}"\n')

    with patch.object(SecretsManager, "_get_env_file_path", return_value=env_file):
        res = SecretsManager._get_key_from_env_file()
        assert res == test_key_bytes

def test_get_env_file_path_logic():
    """Test logica path file .env."""
    # Scenario standard (non frozen)
    with patch.object(sys, "frozen", False, create=True):
        path = SecretsManager._get_env_file_path()
        assert path.name == ".env"

    # Scenario frozen (PyInstaller)
    with patch.object(sys, "frozen", True, create=True), \
         patch.object(sys, "executable", "C:\\App\\app.exe"):
        path = SecretsManager._get_env_file_path()
        assert path == Path("C:\\App\\.env")

def test_get_key_from_keyring():
    """Test caricamento da keyring."""
    test_key_bytes = b"keyring_key"
    test_key_b64 = base64.urlsafe_b64encode(test_key_bytes).decode()
    with patch("keyring.get_password", return_value=test_key_b64):
        res = SecretsManager._get_key_from_keyring()
        assert res == test_key_bytes

def test_get_fallback_key():
    """Test fallback hardcoded."""
    res = SecretsManager._get_fallback_key()
    assert res is not None
    assert len(res) == 32

def test_get_license_key_priority():
    """Verifica le priorità di caricamento."""
    with patch.object(SecretsManager, "_get_key_from_env", return_value=b"env"), \
         patch.object(SecretsManager, "_get_key_from_env_file", return_value=b"file"), \
         patch.object(SecretsManager, "_get_key_from_keyring", return_value=b"keyring"):

        # Priority 1: Env
        assert SecretsManager.get_license_key() == b"env"

        # Priority 2: File
        with patch.object(SecretsManager, "_get_key_from_env", return_value=None):
            assert SecretsManager.get_license_key() == b"file"

            # Priority 3: Keyring
            with patch.object(SecretsManager, "_get_key_from_env_file", return_value=None):
                assert SecretsManager.get_license_key() == b"keyring"

                # Priority 4: Fallback
                with patch.object(SecretsManager, "_get_key_from_keyring", return_value=None):
                    assert SecretsManager.get_license_key() == SecretsManager._get_fallback_key()

def test_is_available():
    with patch("keyring.get_password", return_value="ok"):
        assert SecretsManager.is_available() is True
    with patch("keyring.get_password", side_effect=Exception()):
        assert SecretsManager.is_available() is False

def test_credentials_wrappers():
    with patch.object(SecretsManager, "get_credential", return_value="fake"):
        assert SecretsManager.get_exa_api_key() == "fake"
        assert SecretsManager.get_github_token() == "fake"
        assert SecretsManager.get_openai_key() == "fake"
        assert SecretsManager.get_gemini_api_key() == "fake"

def test_derive_key():
    key = SecretsManager.derive_key("pass", b"salt")
    assert isinstance(key, bytes)
    assert len(key) > 0

def test_store_delete_credential():
    with patch("keyring.set_password") as m_set, \
         patch("keyring.delete_password") as m_del:
        SecretsManager.store_credential("svc", "usr", "pwd")
        m_set.assert_called_once()
        SecretsManager.delete_credential("svc", "usr")
        m_del.assert_called_once()
