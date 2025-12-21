"""
Bot TS - Security Utils
Gestisce la cifratura e decifratura delle password salvate.
"""
import os
from pathlib import Path
from cryptography.fernet import Fernet

class PasswordManager:
    """
    Manages encryption and decryption of sensitive data (passwords).
    Uses a locally stored key.
    """
    
    _KEY_DIR = Path.home() / ".bot_ts"
    _KEY_FILE = _KEY_DIR / "secret.key"
    _PREFIX = "ENC:"
    
    def __init__(self):
        self._key = self._load_or_create_key()
        self._cipher = Fernet(self._key)
        
    def _load_or_create_key(self) -> bytes:
        """Loads the encryption key or creates it if missing."""
        try:
            self._KEY_DIR.mkdir(parents=True, exist_ok=True)
            
            if self._KEY_FILE.exists():
                try:
                    with open(self._KEY_FILE, 'rb') as f:
                        key = f.read()
                        # Validate key format
                        Fernet(key)
                        return key
                except Exception:
                    # Key invalid or unreadable, regenerate
                    pass
            
            # Generate new key
            key = Fernet.generate_key()
            try:
                with open(self._KEY_FILE, 'wb') as f:
                    f.write(key)
            except Exception as e:
                print(f"Warning: Could not save encryption key: {e}")
                
            return key
        except Exception:
            # Fallback for environments where home is not writable?
            return Fernet.generate_key()

    def encrypt(self, text: str) -> str:
        """Encrypts a string."""
        if not text:
            return ""
        # Idempotency check: if already looks encrypted, assume it is
        if text.startswith(self._PREFIX):
            return text
            
        try:
            encrypted_bytes = self._cipher.encrypt(text.encode('utf-8'))
            return f"{self._PREFIX}{encrypted_bytes.decode('utf-8')}"
        except Exception:
            return text
    
    def decrypt(self, text: str) -> str:
        """Decrypts a string. Returns original if not encrypted or error."""
        if not text:
            return ""
            
        if not text.startswith(self._PREFIX):
            return text
            
        try:
            payload = text[len(self._PREFIX):]
            decrypted_bytes = self._cipher.decrypt(payload.encode('utf-8'))
            return decrypted_bytes.decode('utf-8')
        except Exception:
            # Decryption failed (wrong key, corruption)
            # Return original text so we don't crash, 
            # user will likely see "ENC:..." and realize they need to re-login
            return text 

# Singleton instance
password_manager = PasswordManager()
