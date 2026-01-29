"""
Gestione sicura dei segreti dell'applicazione.
Utilizza variabili d'ambiente con fallback su file protetti.
"""

import base64
import logging
import os
import sys
from contextlib import suppress
from pathlib import Path

import keyring  # Per integrazione con credential manager OS
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

logger = logging.getLogger(__name__)


class SecretsManager:
    """Gestisce i segreti in modo sicuro."""

    APP_NAME = "SyncroJob"

    @classmethod
    def get_license_key(cls) -> bytes | None:
        """
        Recupera la chiave di licenza in ordine di priorità.
        """
        # 1. Environment variable
        key = cls._get_key_from_env()
        if key:
            return key

        # 2. File .env
        key = cls._get_key_from_env_file()
        if key:
            return key

        # 3. Keyring di sistema
        key = cls._get_key_from_keyring()
        if key:
            return key

        # 4. Fallback Hardcoded (Embedded for Distribution)
        try:
            return base64.urlsafe_b64decode("8kHs_rmwqaRUk1AQLGX65g4AEkWUDapWVsMFUQpN9Ek=")
        except Exception:
            pass

        return None

    @classmethod
    def _get_key_from_env(cls) -> bytes | None:
        env_key = os.environ.get("SYNCROJOB_LICENSE_KEY")
        if env_key:
            with suppress(Exception):
                return base64.urlsafe_b64decode(env_key)
        return None

    @classmethod
    def _get_key_from_env_file(cls) -> bytes | None:
        with suppress(Exception):
            env_file = cls._get_env_file_path()
            if env_file.exists():
                with env_file.open("r", encoding="utf-8") as f:
                    for line in f:
                        if line.startswith("SYNCROJOB_LICENSE_KEY="):
                            key_str = line.split("=", 1)[1].strip()
                            key_str = key_str.strip('"').strip("'")
                            with suppress(Exception):
                                return base64.urlsafe_b64decode(key_str)
        return None

    @staticmethod
    def _get_env_file_path() -> Path:
        if getattr(sys, "frozen", False):
            return Path(sys.executable).parent / ".env"
        return Path(__file__).parent.parent.parent / ".env"

    @classmethod
    def _get_key_from_keyring(cls) -> bytes | None:
        with suppress(Exception):
            stored = keyring.get_password(cls.APP_NAME, "license_key")
            if stored:
                return base64.urlsafe_b64decode(stored)
        return None

    @classmethod
    def get_exa_api_key(cls) -> str:
        """Recupera Exa API Key dal Keyring."""
        return cls.get_credential("api", "exa_api_key") or ""

    @classmethod
    def get_gemini_api_key(cls) -> str:
        """Recupera Gemini API Key dal Keyring."""
        return cls.get_credential("api", "GEMINI_API_KEY") or ""

    @classmethod
    def is_available(cls) -> bool:
        """Verifica se il servizio di keyring è disponibile."""
        with suppress(Exception):
            # Prova a recuperare una chiave dummy per vedere se il backend risponde
            # Non salviamo nulla per evitare sporcizia, solo get
            keyring.get_password("test_backend_availability", "test")
            return True
        return False

    @classmethod
    def store_credential(cls, service: str, username: str, password: str):
        """Salva credenziali nel keyring di sistema."""
        try:
            keyring.set_password(f"{cls.APP_NAME}_{service}", username, password)
        except Exception as e:
            # Print for tests (capsys) and log for production
            print(f"Warning: Could not store credential for {service}: {e}")
            logger.warning(f"Could not store credential for {service}: {e}")

    @classmethod
    def get_credential(cls, service: str, username: str) -> str | None:
        """Recupera password dal keyring di sistema."""
        try:
            return keyring.get_password(f"{cls.APP_NAME}_{service}", username)
        except Exception as e:
            logger.warning(f"Could not retrieve credential for {service}: {e}")
            return None

    @classmethod
    def delete_credential(cls, service: str, username: str):
        """Elimina credenziali dal keyring."""
        try:
            keyring.delete_password(f"{cls.APP_NAME}_{service}", username)
        except (keyring.errors.PasswordDeleteError, Exception) as e:
            logger.warning(f"Could not delete credential for {service}: {e}")

    @staticmethod
    def derive_key(password: str, salt: bytes) -> bytes:
        """Deriva una chiave crittografica da una password."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,  # OWASP 2023 recommendation
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))
