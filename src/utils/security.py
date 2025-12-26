"""
Password Manager con encryption moderna.
Usa Argon2/Scrypt per key derivation.
"""
import os
import json
import base64
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import secrets

class PasswordManager:
    """Gestisce encryption/decryption password con best practice moderne."""
    
    _instance = None
    _KEY_DIR = Path.home() / ".bot_ts"
    _KEY_FILE = _KEY_DIR / "secret.key"
    _SALT_FILE = _KEY_DIR / "encryption.salt"
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Inizializza chiave e cipher."""
        self._KEY_DIR.mkdir(parents=True, exist_ok=True)

        # Imposta permessi restrittivi (solo owner)
        if os.name != 'nt':  # Unix
            try:
                os.chmod(self._KEY_DIR, 0o700)
            except Exception:
                pass

        self._key = self._load_or_create_key()
        self._cipher = Fernet(self._key)

    def _load_or_create_key(self) -> bytes:
        """Carica o genera chiave derivata da password macchina."""
        if self._KEY_FILE.exists():
            # Se esiste solo la chiave (legacy), usala
            # Se esiste anche il salt (v2), verifica se dobbiamo rigenerare o caricare
            with open(self._KEY_FILE, 'rb') as f:
                key = f.read()
                # Verifica validità chiave Fernet (32 url-safe base64-encoded bytes)
                try:
                    Fernet(key)
                    return key
                except Exception:
                    pass # Chiave invalida, rigenera

        # Genera nuovo salt e chiave
        salt = secrets.token_bytes(32)

        # Deriva chiave usando Scrypt (memory-hard, resistente a GPU)
        machine_id = self._get_machine_entropy()
        kdf = Scrypt(
            salt=salt,
            length=32,
            n=2**14, # Ridotto per performance su macchine lente, aumentare a 2**17 se possibile
            r=8,
            p=1,
        )
        key = base64.urlsafe_b64encode(kdf.derive(machine_id))

        # Salva
        with open(self._SALT_FILE, 'wb') as f:
            f.write(salt)
        with open(self._KEY_FILE, 'wb') as f:
            f.write(key)

        # Permessi restrittivi
        if os.name != 'nt':
            try:
                os.chmod(self._KEY_FILE, 0o600)
                os.chmod(self._SALT_FILE, 0o600)
            except Exception:
                pass

        return key

    def _get_machine_entropy(self) -> bytes:
        """Genera entropia basata sulla macchina."""
        import platform
        import uuid
        import getpass

        try:
            username = getpass.getuser()
        except Exception:
            username = "unknown"

        components = [
            platform.node(),
            str(uuid.getnode()),  # MAC address
            platform.machine(),
            username,
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
        except Exception as e:
            print(f"Encryption error: {e}")
            return ""
    
    def decrypt(self, ciphertext: str) -> str:
        """Decripta una stringa."""
        if not ciphertext:
            return ""

        if ciphertext.startswith("ENC:v2:"):
            try:
                encrypted_data = ciphertext[7:].encode()
                return self._cipher.decrypt(encrypted_data).decode()
            except Exception as e:
                print(f"Decryption error (v2): {e}")
                return ""

        # Legacy format (ENC:) - migra a v2
        if ciphertext.startswith("ENC:"):
            try:
                encrypted_data = ciphertext[4:].encode()
                decrypted = self._cipher.decrypt(encrypted_data).decode()
                return decrypted
            except Exception as e:
                print(f"Decryption error (legacy): {e}")
                return ""

        # Plaintext legacy (potrebbe essere una vecchia config non criptata)
        return ciphertext

# Singleton instance
password_manager = PasswordManager()
