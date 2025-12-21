import unittest
import shutil
import sys
import os
from pathlib import Path

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.utils.security import PasswordManager

class TestPasswordManager(unittest.TestCase):
    def setUp(self):
        # Use a temporary directory for keys
        self.test_dir = Path("tests/temp_security")
        self.test_dir.mkdir(parents=True, exist_ok=True)
        
        # Monkey patch class constants for testing
        self.original_key_dir = PasswordManager._KEY_DIR
        self.original_key_file = PasswordManager._KEY_FILE
        
        PasswordManager._KEY_DIR = self.test_dir
        PasswordManager._KEY_FILE = self.test_dir / "secret.key"
        
        self.mgr = PasswordManager()

    def tearDown(self):
        # Restore
        PasswordManager._KEY_DIR = self.original_key_dir
        PasswordManager._KEY_FILE = self.original_key_file
        
        # Clean up
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_encrypt_decrypt(self):
        original = "MySecretPassword123!"
        encrypted = self.mgr.encrypt(original)
        
        self.assertNotEqual(original, encrypted)
        self.assertTrue(encrypted.startswith("ENC:"))
        
        decrypted = self.mgr.decrypt(encrypted)
        self.assertEqual(original, decrypted)

    def test_decrypt_plaintext(self):
        # Legacy plaintext should remain plaintext
        plain = "plain_password"
        self.assertEqual(self.mgr.decrypt(plain), plain)

    def test_encrypt_idempotency(self):
        # Encrypting an already encrypted string should return it as is
        original = "pass"
        enc = self.mgr.encrypt(original)
        enc2 = self.mgr.encrypt(enc)
        self.assertEqual(enc, enc2)

    def test_key_persistence(self):
        # Create a new manager instance, should load same key
        mgr2 = PasswordManager()
        
        original = "persistent"
        enc = self.mgr.encrypt(original)
        dec = mgr2.decrypt(enc)
        
        self.assertEqual(original, dec)
        
if __name__ == '__main__':
    unittest.main()
