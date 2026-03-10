"""
Bot TS - Test Configuration
Shared fixtures and configuration.
"""

import contextlib
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add src to path
ROOT_DIR = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(ROOT_DIR / "src"))


# --- GLOBAL MATPLOTLIB MOCK FOR HEADLESS ENVIRONMENTS ---
# Eradicates Access Violation crashes in headless Windows by intercepting Qt backends
try:
    import sys
    from unittest.mock import MagicMock

    class MockCanvas(MagicMock):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.figure = MagicMock()

    mock_backend = MagicMock()
    mock_backend.FigureCanvasQTAgg = MockCanvas
    mock_backend.FigureCanvas = MockCanvas

    sys.modules["matplotlib.backends.backend_qtagg"] = mock_backend
    sys.modules["matplotlib.backends.backend_qt5agg"] = mock_backend
    sys.modules["matplotlib.backends.backend_qt"] = mock_backend
    sys.modules["matplotlib.backends.qt_compat"] = MagicMock()
except Exception:  # noqa: S110
    # Matplotlib might not be installed, ignore error for headless environments
    pass
# --------------------------------------------------------


# --- GLOBAL PYQT6 MOCK FOR HEADLESS ENVIRONMENTS ---
try:
    import PyQt6  # noqa: F401
except (ImportError, RuntimeError):
    # If PyQt6 is missing or DLLs fail to load, provide a minimal mock infrastructure
    class MockQObject:
        def __init__(self, *args, **kwargs):
            pass

        def setParent(self, parent):
            pass

    class MockPyqtSignal:
        def __init__(self, *args, **kwargs):
            pass

        def emit(self, *args, **kwargs):
            pass

        def connect(self, slot):
            pass

    mock_qt_core = MagicMock()
    mock_qt_core.QObject = MockQObject
    mock_qt_core.pyqtSignal = MockPyqtSignal

    sys.modules["PyQt6"] = MagicMock()
    sys.modules["PyQt6.QtCore"] = mock_qt_core
    sys.modules["PyQt6.QtGui"] = MagicMock()
    sys.modules["PyQt6.QtWidgets"] = MagicMock()
    sys.modules["PyQt6.QtTest"] = MagicMock()
# ---------------------------------------------------


# --- GLOBAL MATPLOTLIB MOCK FOR HEADLESS ENVIRONMENTS ---
try:
    import matplotlib
    matplotlib.use("Agg")

    # Mock canvas classes that cause native crashes in headless Windows
    mock_canvas = MagicMock()
    sys.modules["matplotlib.backends.backend_qt5agg"] = mock_canvas
    sys.modules["matplotlib.backends.backend_qtagg"] = mock_canvas
    sys.modules["matplotlib.backends.backend_qt"] = mock_canvas
except (ImportError, RuntimeError):
    pass
# --------------------------------------------------------


# Set matplotlib backend to 'Agg' to avoid GUI issues during tests
def pytest_sessionstart(session):
    """
    Called after the Session object has been created and before performing collection and entering the run test loop.
    """
    with contextlib.suppress(ImportError):
        import matplotlib

        matplotlib.use("Agg")


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
    manager_patcher = patch(
        "webdriver_manager.chrome.ChromeDriverManager.install",
        return_value="/mock/path/chromedriver",
    )

    selenium_patcher.start()
    manager_patcher.start()

    # Ensure the patches are stopped after the test session finishes
    config.add_cleanup(patcher.stop)
    config.add_cleanup(selenium_patcher.stop)
    config.add_cleanup(manager_patcher.stop)


@pytest.fixture
def temp_dir(tmp_path):
    """Create a temporary directory for tests using pytest built-in tmp_path."""
    return tmp_path


@pytest.fixture
def mock_config(temp_dir):
    """Create a mock configuration file."""
    return temp_dir / "config.json"


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
    test_dir.mkdir(parents=True, exist_ok=True)
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

    with (
        patch("src.core.config_manager.CONFIG_DIR", fake_dir),
        patch("src.core.config_manager.CONFIG_FILE", fake_file),
        patch("src.core.config_manager.check_and_migrate_local_config", return_value=False),
    ):
        yield fake_file

    # Clean cache again
    config_manager._config_cache = None


# The qapp fixture is now provided automatically by the pytest-qt plugin.
# Defining it here would override the plugin's fixture and cause conflicts.


@pytest.fixture(autouse=True)
def cleanup_widgets():
    """
    Force clean up of all top-level widgets after each test.
    This prevents "Widget Zombie" leaks and GDI handle exhaustion on Windows.
    Does NOT require 'qapp' fixture to avoid creating QApplication for non-GUI tests.
    """
    yield

    import gc

    try:
        from PyQt6.QtWidgets import QApplication
    except (ImportError, RuntimeError):
        # PyQt6 not available or broken in this environment
        gc.collect()
        return

    # Only clean up if QApplication exists
    if not QApplication.instance():
        return

    # Try to import sip for explicit C++ deletion
    with contextlib.suppress(ImportError):
        pass

    # Close all top-level widgets
    for widget in QApplication.topLevelWidgets():
        with contextlib.suppress(Exception):
            if widget.isVisible():
                widget.close()
            widget.deleteLater()

    # Process deferred delete events
    QApplication.processEvents()

    # Force Python Garbage Collection
    gc.collect()
    gc.collect()  # Double collect for cyclic references


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
    with contextlib.suppress(ImportError):
        import src.bots.portale_fornitori.timbrature.storage

        mocker.patch.object(
            src.bots.portale_fornitori.timbrature.storage,
            "TimbratureStorage",
            return_value=MagicMock(),
        )

    # Mock LyraSentinel & Telegram
    mocker.patch("src.core.lyra_sentinel.LyraSentinel", return_value=MagicMock())
    mocker.patch("src.core.telegram_manager.TelegramService", return_value=MagicMock())

    # Mock ConfigManager per evitare scritture reali
    mocker.patch("src.core.config_manager.save_config")

    return {"contabilita": mock_contabilita_instance, "db": mock_db}


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
