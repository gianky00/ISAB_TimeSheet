import unittest
import shutil
import json
import os
import sys
from pathlib import Path
from cryptography.fernet import Fernet

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.core import config_manager
from src.utils.security import password_manager

class TestConfigSecurity(unittest.TestCase):
    def setUp(self):
        # Use a temporary config dir
        self.test_dir = Path("tests/temp_config")
        self.test_dir.mkdir(parents=True, exist_ok=True)
        
        # Monkey patch config_manager
        self.original_config_dir = config_manager.CONFIG_DIR
        self.original_config_file = config_manager.CONFIG_FILE
        
        config_manager.CONFIG_DIR = self.test_dir
        config_manager.CONFIG_FILE = self.test_dir / "config.json"
        
        # Patch password_manager to use temp dir
        self.original_key_file = password_manager._KEY_FILE
        self.original_key_dir = password_manager._KEY_DIR
        
        password_manager._KEY_DIR = self.test_dir
        password_manager._KEY_FILE = self.test_dir / "secret.key"
        
        # Force reload key for this test context
        password_manager._key = password_manager._load_or_create_key()
        password_manager._cipher = Fernet(password_manager._key)

    def tearDown(self):
        config_manager.CONFIG_DIR = self.original_config_dir
        config_manager.CONFIG_FILE = self.original_config_file
        password_manager._KEY_FILE = self.original_key_file
        password_manager._KEY_DIR = self.original_key_dir
        
        # Restore original cipher (best effort, though it was singleton)
        # Ideally we should reload it from original file but that's complex.
        # This test runs in isolation usually.
        
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_save_and_load_encrypted(self):
        # 1. Create a config with a password
        username = "testuser"
        password = "secret_password"
        
        # Use add_account which calls save_config
        config_manager.add_account(username, password)
        
        # 2. Check the file content - MUST BE ENCRYPTED
        with open(config_manager.CONFIG_FILE, 'r') as f:
            saved_data = json.load(f)
            
        saved_password = saved_data["accounts"][0]["password"]
        self.assertNotEqual(saved_password, password)
        self.assertTrue(saved_password.startswith("ENC:"))
        
        # 3. Load config via manager - MUST BE PLAINTEXT
        loaded_config = config_manager.load_config()
        loaded_password = loaded_config["accounts"][0]["password"]
        
        self.assertEqual(loaded_password, password)

    def test_legacy_plaintext_migration(self):
        # 1. Write a legacy config manually
        legacy_data = {
            "accounts": [
                {"username": "old", "password": "plaintext_pass", "default": True}
            ]
        }
        with open(config_manager.CONFIG_FILE, 'w') as f:
            json.dump(legacy_data, f)
            
        # 2. Load it - should handle plaintext
        config = config_manager.load_config()
        self.assertEqual(config["accounts"][0]["password"], "plaintext_pass")
        
        # 3. Save it (trigger migration)
        config_manager.save_config(config)
        
        # 4. Check file - should now be encrypted
        with open(config_manager.CONFIG_FILE, 'r') as f:
            saved_data = json.load(f)
            
        saved_pass = saved_data["accounts"][0]["password"]
        self.assertTrue(saved_pass.startswith("ENC:"))
        
if __name__ == '__main__':
    unittest.main()
