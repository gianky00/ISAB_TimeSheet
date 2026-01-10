"""
Bot TS - Test Configuration
Shared fixtures and configuration.
"""

import os
import shutil
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))

# Set matplotlib backend to 'Agg' to avoid GUI issues during tests
def pytest_sessionstart(session):
    """
    Called after the Session object has been created and before performing collection and entering the run test loop.
    """
    try:
        import matplotlib
        matplotlib.use("Agg")
    except ImportError:
        pass


def pytest_configure(config):
    """
    Prevents OSError: [Errno 25] Inappropriate ioctl for device in CI/CD.
    This error occurs because PasswordManager is initialized at module import
    time and calls os.getlogin(), which fails in non-interactive shells.
    """
    patcher = patch("os.getlogin", return_value="testuser")
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


@pytest.fixture
def setup_clean_config(tmp_path):
    """
    Fixture to ensure a clean, isolated config for specific tests.
    This is more explicit than autouse for tests that heavily modify config.
    """
    from src.core import config_manager

    original_dir = config_manager.CONFIG_DIR
    original_file = config_manager.CONFIG_FILE

    test_dir = tmp_path / "test_config"
    test_dir.mkdir()
    test_file = test_dir / "config.json"

    # Patch the constants
    config_manager.CONFIG_DIR = test_dir
    config_manager.CONFIG_FILE = test_file

    # Clear cache before test
    config_manager._config_cache = None

    yield test_file  # The test runs with the patched config

    # Restore original constants and clear cache after test
    config_manager.CONFIG_DIR = original_dir
    config_manager.CONFIG_FILE = original_file
    config_manager._config_cache = None


@pytest.fixture(autouse=True)
def _isolate_config(tmp_path):
    """
    Global isolation for configuration.
    Ensures NO test ever writes to the real %LOCALAPPDATA% directory.
    """
    from src.core import config_manager

    # Clean cache
    config_manager._config_cache = None

    fake_dir = tmp_path / "syncrojob_test_config"
    fake_dir.mkdir(parents=True, exist_ok=True)
    fake_file = fake_dir / "config.json"

    with patch("src.core.config_manager.CONFIG_DIR", fake_dir), patch(
        "src.core.config_manager.CONFIG_FILE", fake_file
    ):
        yield fake_file

    # Clean cache again
    config_manager._config_cache = None


# The qapp fixture is now provided automatically by the pytest-qt plugin.
# Defining it here would override the plugin's fixture and cause conflicts.
