from unittest.mock import patch

from src.application.services.config.security import decrypt_all_credentials, encrypt_all_credentials


class TestConfigSecurity:
    @patch("src.application.services.secrets_manager.SecretsManager.get_credential")
    @patch("src.infrastructure.utils.security.password_manager.decrypt")
    def test_decrypt_all_credentials(self, mock_decrypt, mock_get_cred):
        """Testa la decrittazione delle credenziali."""
        config = {
            "accounts": [
                {"username": "user1", "password": "ENC:v2:encrypted_pass"},
                {"username": "user2", "password": "clear_pass"},
            ],
            "safework_accounts": [{"username": "sf1", "password": ""}],
        }

        # user1: keyring fallisce, usa decrypt locale
        mock_get_cred.side_effect = lambda s, u: "keyring_pass" if u == "sf1" else None
        mock_decrypt.return_value = "decrypted_pass"

        decrypt_all_credentials(config)

        assert config["accounts"][0]["password"] == "decrypted_pass"
        assert config["accounts"][1]["password"] == "clear_pass"  # Invariata
        assert config["safework_accounts"][0]["password"] == "keyring_pass"

    @patch("src.application.services.secrets_manager.SecretsManager.is_available")
    @patch("src.application.services.secrets_manager.SecretsManager.store_credential")
    @patch("src.infrastructure.utils.security.password_manager.encrypt")
    def test_encrypt_all_credentials(self, mock_encrypt, mock_store, mock_avail):
        """Testa la protezione delle credenziali."""
        config = {
            "accounts": [{"username": "user1", "password": "pass1"}],
            "safework_accounts": [{"username": "sf1", "password": "pass2"}],
        }

        # Case 1: Keyring disponibile
        mock_avail.return_value = True
        encrypt_all_credentials(config)

        assert mock_store.call_count == 2
        # La password dovrebbe essere rimossa dal dict se salvata in keyring
        assert "password" not in config["accounts"][0]
        assert "password" not in config["safework_accounts"][0]

    @patch("src.application.services.secrets_manager.SecretsManager.is_available")
    @patch("src.infrastructure.utils.security.password_manager.encrypt")
    def test_encrypt_all_credentials_no_keyring(self, mock_encrypt, mock_avail):
        """Testa il fallback su crittografia locale se keyring non c'è."""
        config = {"accounts": [{"username": "user1", "password": "pass1"}]}

        mock_avail.return_value = False
        mock_encrypt.return_value = "ENC:v2:local_encrypted"

        encrypt_all_credentials(config)

        assert config["accounts"][0]["password"] == "ENC:v2:local_encrypted"
