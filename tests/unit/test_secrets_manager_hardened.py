"""
Hardened tests for SecretsManager.
Verifies secure storage and retrieval of credentials.
"""

import base64
import os

from src.core.secrets_manager import SecretsManager


class TestSecretsManagerHardened:
    def test_get_license_key_env_priority(self, mocker):
        """Verifica che la variabile d'ambiente abbia la priorità massima."""
        encoded_key = base64.urlsafe_b64encode(b"my_env_key").decode()
        mocker.patch.dict(os.environ, {"SYNCROJOB_LICENSE_KEY": encoded_key})

        # Mock degli altri metodi per evitare interferenze
        mocker.patch.object(SecretsManager, "_get_key_from_env_file", return_value=None)
        mocker.patch.object(SecretsManager, "_get_key_from_keyring", return_value=None)

        key = SecretsManager.get_license_key()
        assert key == b"my_env_key"

    def test_get_license_key_fallback(self, mocker):
        """Verifica il fallback sulla chiave hardcoded se tutto il resto manca."""
        mocker.patch.dict(os.environ, {}, clear=True)
        mocker.patch.object(SecretsManager, "_get_key_from_env_file", return_value=None)
        mocker.patch.object(SecretsManager, "_get_key_from_keyring", return_value=None)

        key = SecretsManager.get_license_key()
        assert key is not None
        # La chiave hardcoded inizia con 8kHs...
        assert len(key) == 32

    def test_keyring_store_retrieve(self, mocker):
        """Testa l'integrazione con keyring (mocked)."""
        mock_keyring = mocker.patch("src.core.secrets_manager.keyring")

        SecretsManager.store_credential("test_service", "user1", "pass123")
        mock_keyring.set_password.assert_called_once_with("SyncroJob_test_service", "user1", "pass123")

        mock_keyring.get_password.return_value = "pass123"
        val = SecretsManager.get_credential("test_service", "user1")
        assert val == "pass123"

    def test_derive_key_robustness(self):
        """Verifica la derivazione deterministica della chiave."""
        password = "strong_password"
        salt = b"random_salt_16bytes"

        key1 = SecretsManager.derive_key(password, salt)
        key2 = SecretsManager.derive_key(password, salt)

        assert key1 == key2
        assert len(key1) > 0

        # Cambio password -> cambio chiave
        key3 = SecretsManager.derive_key("different", salt)
        assert key1 != key3

    def test_delete_credential_handling(self, mocker):
        """Verifica la gestione sicura dell'eliminazione (anche se fallisce)."""
        # Patchiamo keyring e la sua sottoclasse errors in modo che l'exception sia valida
        mock_keyring = mocker.patch("src.core.secrets_manager.keyring")

        # Definiamo una eccezione reale per il mock
        class MockDeleteError(Exception):
            pass

        mock_keyring.errors.PasswordDeleteError = MockDeleteError

        # Simula eccezione (es. password non trovata) usando l'eccezione mockata
        mock_keyring.delete_password.side_effect = MockDeleteError("Not found")

        # Non deve sollevare eccezioni
        SecretsManager.delete_credential("service", "user")
        assert mock_keyring.delete_password.called
