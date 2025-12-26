import pytest
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

@pytest.fixture
def temp_config():
    """Setup and teardown for a temporary config directory and files."""
    test_dir = Path("tests/temp_config")
    test_dir.mkdir(parents=True, exist_ok=True)

    original_config_dir = config_manager.CONFIG_DIR
    original_config_file = config_manager.CONFIG_FILE

    config_manager.CONFIG_DIR = test_dir
    config_manager.CONFIG_FILE = test_dir / "config.json"

    original_key_file = password_manager._KEY_FILE
    original_key_dir = password_manager._KEY_DIR

    password_manager._KEY_DIR = test_dir
    password_manager._KEY_FILE = test_dir / "secret.key"

    password_manager._key = password_manager._load_or_create_key()
    password_manager._cipher = Fernet(password_manager._key)

    yield  # This is where the test runs

    config_manager.CONFIG_DIR = original_config_dir
    config_manager.CONFIG_FILE = original_config_file
    password_manager._KEY_FILE = original_key_file
    password_manager._KEY_DIR = original_key_dir

    if test_dir.exists():
        shutil.rmtree(test_dir)

def test_save_and_load_encrypted(qapp, temp_config):
    """
    Tests that passwords are encrypted on save and decrypted on load.
    """
    # 1. Create a config with a password
    username = "testuser"
    password = "secret_password"

    config_manager.add_account(username, password)

    # 2. Check the file content - MUST BE ENCRYPTED
    with open(config_manager.CONFIG_FILE, 'r') as f:
        saved_data = json.load(f)
        
    saved_password = saved_data["accounts"][0]["password"]
    assert saved_password != password
    assert saved_password.startswith("ENC:")

    # 3. Load config via manager - MUST BE PLAINTEXT
    loaded_config = config_manager.load_config()
    loaded_password = loaded_config["accounts"][0]["password"]

    assert loaded_password == password

def test_legacy_plaintext_migration(qapp, temp_config):
    """
    Tests that legacy plaintext passwords are migrated to encrypted format on save.
    """
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
    assert config["accounts"][0]["password"] == "plaintext_pass"

    # 3. Save it (trigger migration)
    config_manager.save_config(config)

    # 4. Check file - should now be encrypted
    with open(config_manager.CONFIG_FILE, 'r') as f:
        saved_data = json.load(f)
        
    saved_pass = saved_data["accounts"][0]["password"]
    assert saved_pass.startswith("ENC:")
