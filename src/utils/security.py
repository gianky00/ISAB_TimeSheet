"""
Password Manager con encryption moderna.
Usa Argon2/Scrypt per key derivation.
"""

import base64
import logging
import os
import platform
import secrets
import uuid
from contextlib import suppress
from pathlib import Path
from typing import ClassVar

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

from src.core.paths import SECURITY_DIR

logger = logging.getLogger(__name__)


class PasswordManager:
    """Gestisce encryption/decryption password con best practice moderne."""

    _instance: ClassVar["PasswordManager | None"] = None

    @property
    def key_dir(self) -> Path:
        """Percorso dinamico della directory chiavi."""
        return SECURITY_DIR

    @property
    def key_file(self) -> Path:
        """Percorso dinamico del file chiave."""
        return self.key_dir / "secret.key"

    @property
    def salt_file(self) -> Path:
        """Percorso dinamico del file salt."""
        return self.key_dir / "encryption.salt"

    def __new__(cls) -> "PasswordManager":
        """Pattern Singleton per il gestore delle password."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self) -> None:
        """Inizializza chiave e cipher."""
        self.key_dir.mkdir(parents=True, exist_ok=True)

        # Imposta permessi restrittivi (solo owner)
        if os.name != "nt":  # Unix
            with suppress(Exception):
                os.chmod(self.key_dir, 0o700)

        self._key = self._load_or_create_key()
        self._cipher = Fernet(self._key)

    def _reset_for_testing(self) -> None:
        """Resetta l'istanza per i test (re-inizializza con nuovi path)."""
        self._initialize()

    def _load_or_create_key(self) -> bytes:
        """Carica o genera chiave derivata da password macchina."""
        if self.key_file.exists():
            # Se esiste solo la chiave (legacy), usala
            # Se esiste anche il salt (v2), verifica se dobbiamo rigenerare o caricare
            key = self.key_file.read_bytes()
            # Verifica validità chiave Fernet (32 url-safe base64-encoded bytes)
            with suppress(Exception):
                Fernet(key)
                return key

        # Genera nuovo salt e chiave
        salt = secrets.token_bytes(32)

        # Deriva chiave usando Scrypt (memory-hard, resistente a GPU)
        machine_id = self._get_machine_entropy()
        kdf = Scrypt(
            salt=salt,
            length=32,
            n=2**14,  # Ridotto per performance su macchine lente, aumentare a 2**17 se possibile
            r=8,
            p=1,
        )
        key = base64.urlsafe_b64encode(kdf.derive(machine_id))

        # Salva
        self.salt_file.write_bytes(salt)
        self.key_file.write_bytes(key)

        # Permessi restrittivi
        if os.name != "nt":
            with suppress(Exception):
                os.chmod(self.key_file, 0o600)
                os.chmod(self.salt_file, 0o600)

        return key

    def _get_machine_entropy(self) -> bytes:
        """Genera entropia basata sulla macchina."""
        components = [
            platform.node(),
            str(uuid.getnode()),  # MAC address
            platform.machine(),
            os.getlogin() if hasattr(os, "getlogin") else "unknown",
        ]
        return "|".join(components).encode()

    def encrypt(self, plaintext: str) -> str:
        """Cripta una stringa."""
        if not plaintext:
            return ""
        if plaintext.startswith("ENC:v2:"):
            return plaintext  # Già criptato

        try:
            encrypted = self._cipher.encrypt(plaintext.encode())
            return f"ENC:v2:{encrypted.decode()}"
        except Exception:
            logger.exception("Encryption error")
            return ""

    def decrypt(self, ciphertext: str) -> str:
        """Decripta una stringa."""
        if not ciphertext:
            return ""

        if ciphertext.startswith("ENC:v2:"):
            try:
                encrypted_data = ciphertext[7:].encode()
                return self._cipher.decrypt(encrypted_data).decode()  # type: ignore[no-any-return]
            except Exception:
                logger.exception("Decryption error (v2)")
                return ""

        # Legacy format (ENC:) - migra a v2
        if ciphertext.startswith("ENC:"):
            try:
                encrypted_data = ciphertext[4:].encode()
                return self._cipher.decrypt(encrypted_data).decode()  # type: ignore[no-any-return]
            except Exception:
                logger.exception("Decryption error (legacy)")
                return ""

        # Plaintext legacy (potrebbe essere una vecchia config non criptata)
        return ciphertext


# Singleton instance
password_manager = PasswordManager()
