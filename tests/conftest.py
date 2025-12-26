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

@pytest.fixture(scope="session", autouse=True)
def mock_os_getlogin():
    """Mock os.getlogin() to prevent OSError in headless CI environments."""
    with patch('os.getlogin', return_value='testuser') as mock:
        yield mock

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
