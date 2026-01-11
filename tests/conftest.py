"""
Bot TS - Test Configuration
Shared fixtures and configuration.
"""

import os
import shutil
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

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
    
    # Global mock for Selenium and ChromeDriverManager to avoid downloads/browser popups
    selenium_patcher = patch("selenium.webdriver.Chrome", return_value=MagicMock())
    manager_patcher = patch("webdriver_manager.chrome.ChromeDriverManager.install", return_value="/mock/path/chromedriver")
    
    selenium_patcher.start()
    manager_patcher.start()
    
    # Ensure the patches are stopped after the test session finishes
    config.add_cleanup(patcher.stop)
    config.add_cleanup(selenium_patcher.stop)
    config.add_cleanup(manager_patcher.stop)


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


@pytest.fixture(autouse=True)
def cleanup_widgets(qapp):
    """
    Force clean up of all top-level widgets after each test.
    This prevents "Widget Zombie" leaks and GDI handle exhaustion on Windows.
    """
    yield
    
    from PyQt6.QtWidgets import QApplication
    import gc
    
    # Try to import sip for explicit C++ deletion
    try:
        from PyQt6 import sip
    except ImportError:
        sip = None
    
    # Close all top-level widgets
    for widget in QApplication.topLevelWidgets():
        try:
            if widget.isVisible():
                widget.close()
            widget.deleteLater()
            if sip and not sip.isdeleted(widget):
                # Dangerous but necessary for GDI leak prevention in massive suites
                # sip.delete(widget) 
                pass 
        except Exception:
            pass
    
    # Process deferred delete events
    qapp.processEvents()
    
    # Force Python Garbage Collection
    gc.collect()
    gc.collect() # Double collect for cyclic references


@pytest.fixture
def mock_ui_dependencies(mocker):
    """
    Mock massivo delle dipendenze UI per evitare I/O su disco e DB reali.
    Permette di istanziare Widget complessi in isolamento.
    """
    # Mock Database Instance (db_manager)
    mock_db = MagicMock()
    mocker.patch("src.core.database.db_manager", mock_db)
    
    # Mock ContabilitaManager (Class Mock)
    mock_contabilita_class = mocker.patch("src.core.contabilita_manager.ContabilitaManager")
    
    # Configure Class Methods and Attributes
    mock_contabilita_class.DB_PATH = MagicMock()
    mock_contabilita_class.DB_PATH.exists.return_value = True
    mock_contabilita_class.get_available_years.return_value = [2024, 2025]
    mock_contabilita_class.get_scarico_ore_data.return_value = []
    
    # Configure Instance Methods (if any are used)
    mock_contabilita_instance = mock_contabilita_class.return_value
    mock_contabilita_instance.get_status_message.return_value = "Ready"
    
    # Mock TimbratureStorage
    # Force import to avoid AttributeError: module 'src' has no attribute 'bots'
    import src.bots.portale_fornitori.timbrature.storage
    mocker.patch.object(src.bots.portale_fornitori.timbrature.storage, "TimbratureStorage", return_value=MagicMock())
    
    # Mock LyraSentinel & Telegram
    mocker.patch("src.core.lyra_sentinel.LyraSentinel", return_value=MagicMock())
    mocker.patch("src.core.telegram_manager.TelegramService", return_value=MagicMock())
    
    # Mock ConfigManager per evitare scritture reali
    mocker.patch("src.core.config_manager.save_config")

    return {
        "contabilita": mock_contabilita_instance,
        "db": mock_db
    }


@pytest.fixture
def mock_driver(mocker):
    """
    Mock del driver Selenium per testare i Bot senza aprire il browser.
    """
    mock = MagicMock()
    mock.page_source = "<html><body><div id='test'></div></body></html>"
    # Mocking wait instance behavior
    mock_wait = MagicMock()
    mocker.patch("selenium.webdriver.support.ui.WebDriverWait", return_value=mock_wait)
    return mock


@pytest.fixture
def create_mock_html(tmp_path):
    """
    Crea un file HTML temporaneo per testare i selettori.
    """
    def _create(content, filename="test.html"):
        html_file = tmp_path / filename
        html_file.write_text(content, encoding="utf-8")
        return html_file
    return _create
