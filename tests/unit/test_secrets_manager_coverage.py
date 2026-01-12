import base64

from src.core.secrets_manager import SecretsManager


class TestSecretsManagerCoverage:
    def test_derive_key(self):
        """Verifica che la derivazione chiave sia deterministica."""
        pwd = "mypassword"
        salt = b"staticsalt"
        key1 = SecretsManager.derive_key(pwd, salt)
        key2 = SecretsManager.derive_key(pwd, salt)

        assert key1 == key2
        assert len(key1) > 32 # Base64 encoded 32 bytes

    def test_get_license_key_from_env(self, mocker):
        """Verifica recupero da variabile d'ambiente (Priorità 1)."""
        secret = b"my-secret-key"
        encoded = base64.urlsafe_b64encode(secret).decode()
        mocker.patch("os.environ.get", return_value=encoded)

        res = SecretsManager.get_license_key()
        assert res == secret

    def test_get_license_key_from_file(self, tmp_path, mocker):
        """Verifica recupero da file .env (Priorità 2)."""
        mocker.patch("os.environ.get", return_value=None)

        # Simula il contenuto del file .env
        secret_bytes = b"file_secret_key"
        encoded_secret = base64.urlsafe_b64encode(secret_bytes).decode()
        env_content = f"SYNCROJOB_LICENSE_KEY={encoded_secret}\n"

        # Invece di mockare Path in modo complesso, mockiamo direttamente
        # i punti di ingresso della logica di SecretsManager.get_license_key

        # 1. Mock Path.exists per far sembrare che il file esista
        from src.core.secrets_manager import Path as SMPath
        mocker.patch.object(SMPath, "exists", return_value=True)

        # 2. Mock della funzione open globale per restituire il contenuto voluto
        mocker.patch("builtins.open", mocker.mock_open(read_data=env_content))

        # 3. Assicuriamoci che non fallisca per il Keyring dopo
        mocker.patch("keyring.get_password", return_value=None)

        res = SecretsManager.get_license_key()
        assert res == secret_bytes

    def test_get_license_key_from_keyring(self, mocker):
        """Verifica recupero da Keyring (Priorità 3)."""
        mocker.patch("os.environ.get", return_value=None)
        # Mock Path per dire che .env non esiste
        from src.core.secrets_manager import Path as SMPath
        mocker.patch.object(SMPath, "exists", return_value=False)

        secret = b"keyring_secret"
        encoded = base64.urlsafe_b64encode(secret).decode()
        mocker.patch("keyring.get_password", return_value=encoded)

        res = SecretsManager.get_license_key()
        assert res == secret

    def test_get_license_key_none_found(self, mocker):
        """Verifica comportamento se non viene trovato nulla."""
        mocker.patch("os.environ.get", return_value=None)
        from src.core.secrets_manager import Path as SMPath
        mocker.patch.object(SMPath, "exists", return_value=False)
        mocker.patch("keyring.get_password", return_value=None)

        assert SecretsManager.get_license_key() is None

    def test_get_license_key_invalid_base64_env(self, mocker):
        """Verifica resilienza a base64 malformato in ENV."""
        mocker.patch("os.environ.get", return_value="!!!invalid!!!")
        from src.core.secrets_manager import Path as SMPath
        mocker.patch.object(SMPath, "exists", return_value=False)
        mocker.patch("keyring.get_password", return_value=None)

        assert SecretsManager.get_license_key() is None

    def test_is_available_true(self, mocker):
        """Verifica disponibilità backend keyring."""
        mocker.patch("keyring.get_password", return_value=None)
        assert SecretsManager.is_available() is True

    def test_is_available_false(self, mocker):
        """Verifica gestione backend keyring non funzionante."""
        mocker.patch("keyring.get_password", side_effect=Exception("No backend"))
        assert SecretsManager.is_available() is False

    def test_store_credential(self, mocker):
        """Verifica salvataggio credenziali."""
        mock_set = mocker.patch("keyring.set_password")
        SecretsManager.store_credential("svc", "user", "pass")
        mock_set.assert_called_once_with("SyncroJob_svc", "user", "pass")

    def test_get_credential(self, mocker):
        """Verifica recupero credenziali."""
        mocker.patch("keyring.get_password", return_value="mypass")
        res = SecretsManager.get_credential("svc", "user")
        assert res == "mypass"

    def test_delete_credential(self, mocker):
        """Verifica eliminazione credenziali."""
        mock_del = mocker.patch("keyring.delete_password")
        SecretsManager.delete_credential("svc", "user")
        mock_del.assert_called_once()

    def test_delete_credential_exception(self, mocker):
        """Verifica che l'eliminazione non crashi se la password non esiste."""
        mocker.patch("keyring.delete_password", side_effect=Exception("Not found"))
        # Non deve sollevare eccezioni
        SecretsManager.delete_credential("svc", "user")

    def test_specific_api_getters(self, mocker):
        """Verifica i getter specifici per le API Key."""
        def mock_get(service, key):
            if "exa" in key: return "exa_val"
            if "GEMINI" in key: return "gemini_val"
            return None

        mocker.patch.object(SecretsManager, "get_credential", side_effect=mock_get)

        assert SecretsManager.get_exa_api_key() == "exa_val"
        assert SecretsManager.get_gemini_api_key() == "gemini_val"
        assert SecretsManager.get_openai_key() == ""
