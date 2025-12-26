"""
Bot TS - Test Configuration
Shared fixtures and configuration.
"""
import pytest
import tempfile
import shutil
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
import keyring
from keyring.backends.null import Keyring as NullKeyring

# Set a null keyring for tests to avoid OS credential store interaction
keyring.set_keyring(NullKeyring())

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

def pytest_configure(config):
    """Mock os.getlogin() before test collection to prevent OSError in CI."""
    # This patch is applied before any tests are collected or run.
    patcher = patch('os.getlogin', return_value='testuser')
    patcher.start()

    # Ensure the patch is stopped when pytest exits.
    config.add_cleanup(patcher.stop)

@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    path = Path(tempfile.mkdtemp())
    yield path
    shutil.rmtree(path, ignore_errors=True)

@pytest.fixture
def mock_config(temp_dir):
    """Create a mock configuration file."""
    config_file = temp_dir / "config.json"
    return config_file

@pytest.fixture(scope="session")
def qapp():
    """Shared QApplication for all GUI tests."""
    from PyQt6.QtWidgets import QApplication
    app = QApplication.instance() or QApplication([])
    yield app
