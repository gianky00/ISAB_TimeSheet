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
try:
    import sys
    from unittest.mock import MagicMock

    class MockCanvas(MagicMock):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.figure = MagicMock()

        def setParent(self, parent):  # noqa: N802
            pass

        def setMinimumHeight(self, h):  # noqa: N802
            pass

        def setSizePolicy(self, *args):  # noqa: N802
            pass

        def setGraphicsEffect(self, effect):  # noqa: N802
            pass

        def setStyleSheet(self, style):  # noqa: N802
            pass

    mock_backend = MagicMock()
    mock_backend.FigureCanvasQTAgg = MockCanvas
    mock_backend.FigureCanvas = MockCanvas

    sys.modules["matplotlib.backends.backend_qtagg"] = mock_backend
    sys.modules["matplotlib.backends.backend_qt5agg"] = mock_backend
    sys.modules["matplotlib.backends.backend_qt"] = mock_backend
    sys.modules["matplotlib.backends.qt_compat"] = MagicMock()
except Exception:  # noqa: S110
    pass
# --------------------------------------------------------


# --- GLOBAL PYQT6 MOCK FOR HEADLESS ENVIRONMENTS ---
try:
    import PyQt6  # noqa: F401
except (ImportError, RuntimeError):

    class MockQObject:
        def __init__(self, *args, **kwargs):
            pass

        def setParent(self, parent):  # noqa: N802
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


def pytest_configure(config):
    """
    Setup global mocks and patches.
    """
    patcher = patch("os.getlogin", return_value="testuser")
    patcher.start()

    selenium_patcher = patch("selenium.webdriver.Chrome", return_value=MagicMock())
    manager_patcher = patch(
        "webdriver_manager.chrome.ChromeDriverManager.install",
        return_value="/mock/path/chromedriver",
    )

    selenium_patcher.start()
    manager_patcher.start()

    config.add_cleanup(patcher.stop)
    config.add_cleanup(selenium_patcher.stop)
    config.add_cleanup(manager_patcher.stop)


@pytest.fixture
def temp_dir(tmp_path):
    """Create a temporary directory for tests."""
    return tmp_path


@pytest.fixture(autouse=True)
def _isolate_config(tmp_path):
    """
    Global isolation for configuration and data.
    Ensures NO test ever writes to real user directories.
    """
    from src.core import config_manager  # noqa: PLC0415
    from src.core.database import db_manager  # noqa: PLC0415
    from src.utils.security import password_manager  # noqa: PLC0415

    # 1. Setup fake paths
    fake_dir = tmp_path / "syncrojob_test_env"
    fake_dir.mkdir(parents=True, exist_ok=True)
    (fake_dir / "data").mkdir(exist_ok=True)
    (fake_dir / "logs").mkdir(exist_ok=True)
    (fake_dir / "security").mkdir(exist_ok=True)
    fake_file = fake_dir / "config.json"

    # 2. Apply patches
    with (
        patch("src.core.config_manager.CONFIG_DIR", fake_dir),
        patch("src.core.config_manager.CONFIG_FILE", fake_file),
        patch("src.core.config_manager.check_and_migrate_local_config", return_value=False),
    ):
        # 3. Reset Singletons to use new paths
        config_manager._config_cache = None
        password_manager._reset_for_testing()
        # db_manager uses dynamic properties, but we ensure directories exist
        db_manager._ensure_dirs()

        yield fake_file

        # 4. Cleanup after test
        config_manager._config_cache = None


@pytest.fixture(autouse=True)
def cleanup_widgets():
    """Force clean up of top-level widgets."""
    yield
    import gc  # noqa: PLC0415

    try:
        from PyQt6.QtWidgets import QApplication  # noqa: PLC0415

        if QApplication.instance():
            for widget in QApplication.topLevelWidgets():
                with contextlib.suppress(Exception):
                    widget.close()
                    widget.deleteLater()
            QApplication.processEvents()
    except (ImportError, RuntimeError):
        pass
    gc.collect()


@pytest.fixture
def mock_ui_dependencies(mocker):
    """Mock massive UI dependencies."""
    mock_db = MagicMock()
    mocker.patch("src.core.database.db_manager", mock_db)

    mock_contabilita_class = mocker.patch("src.core.contabilita_manager.ContabilitaManager")
    mock_contabilita_class.get_available_years.return_value = [2024, 2025]

    mocker.patch("src.core.telegram_manager.TelegramService", return_value=MagicMock())
    mocker.patch("src.core.config_manager.save_config")

    return {"db": mock_db}
