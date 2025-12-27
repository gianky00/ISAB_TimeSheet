"""
Gestione sicura dei segreti dell'applicazione.
Utilizza variabili d'ambiente con fallback su file protetti.
"""
import os
import json
import base64
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import keyring  # Per integrazione con credential manager OS

class SecretsManager:
    """Gestisce i segreti in modo sicuro."""

    APP_NAME = "BotTS"

    @classmethod
    def get_license_key(cls) -> bytes:
        """
        Recupera la chiave di licenza in ordine di priorità:
        1. Variabile d'ambiente BOT_TS_LICENSE_KEY
        2. File .env nella root del progetto
        3. Keyring di sistema
        4. Fallback (Temporaneo, per non rompere l'esistente se non configurato, ma DEPRECATO)
        """
        # 1. Environment variable
        env_key = os.environ.get('BOT_TS_LICENSE_KEY')
        if env_key:
            return base64.urlsafe_b64decode(env_key)

        # 2. File .env (solo per sviluppo)
        env_file = Path(__file__).parent.parent.parent / '.env'
        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    if line.startswith('BOT_TS_LICENSE_KEY='):
                        key = line.split('=', 1)[1].strip()
                        # Handle potential quotes
                        key = key.strip('"').strip("'")
                        try:
                            return base64.urlsafe_b64decode(key)
                        except Exception:
                            pass

        # 3. Keyring di sistema
        try:
            stored = keyring.get_password(cls.APP_NAME, "license_key")
            if stored:
                return base64.urlsafe_b64decode(stored)
        except Exception:
            pass # Keyring might fail in headless/some envs

        # Fallback Hardcoded (Legacy - to be removed)
        # Questo serve per mantenere il software funzionante finché la chiave non viene distribuita via env/keyring
        return b'8kHs_rmwqaRUk1AQLGX65g4AEkWUDapWVsMFUQpN9Ek='

    @classmethod
    def is_available(cls) -> bool:
        """Verifica se il servizio di keyring è disponibile."""
        try:
            # Prova a recuperare una chiave dummy per vedere se il backend risponde
            # Non salviamo nulla per evitare sporcizia, solo get
            keyring.get_password("test_backend_availability", "test")
            return True
        except Exception:
            return False

    @classmethod
    def store_credential(cls, service: str, username: str, password: str):
        """Salva credenziali nel keyring di sistema."""
        try:
            keyring.set_password(f"{cls.APP_NAME}_{service}", username, password)
        except Exception as e:
            print(f"Warning: Could not store credential in keyring: {e}")

    @classmethod
    def get_credential(cls, service: str, username: str) -> str | None:
        """Recupera password dal keyring di sistema."""
        try:
            return keyring.get_password(f"{cls.APP_NAME}_{service}", username)
        except Exception:
            return None

    @classmethod
    def delete_credential(cls, service: str, username: str):
        """Elimina credenziali dal keyring."""
        try:
            keyring.delete_password(f"{cls.APP_NAME}_{service}", username)
        except (keyring.errors.PasswordDeleteError, Exception):
            pass

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
