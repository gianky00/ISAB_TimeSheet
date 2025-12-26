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

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

def pytest_configure(config):
    """
    Prevents OSError: [Errno 25] Inappropriate ioctl for device in CI/CD.
    This error occurs because PasswordManager is initialized at module import
    time and calls os.getlogin(), which fails in non-interactive shells.
    """
    patcher = patch('os.getlogin', return_value='testuser')
    patcher.start()
    # Ensure the patch is stopped after the test session finishes
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

# The qapp fixture is now provided automatically by the pytest-qt plugin.
# Defining it here would override the plugin's fixture and cause conflicts.
