# ruff: noqa: N802
"""Bot TS - Test Configuration
Shared fixtures and configuration.
"""

import contextlib
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import keyring
import keyring.backend
import pytest


class InMemoryKeyring(keyring.backend.KeyringBackend):
    """Backend per i test che mantiene le credenziali solo in memoria."""

    priority = 10

    def __init__(self):
        self.passwords = {}

    def get_password(self, service, username):
        return self.passwords.get((service, username))

    def set_password(self, service, username, password):
        self.passwords[(service, username)] = password

    def delete_password(self, service, username):
        self.passwords.pop((service, username), None)


# Add project root to path to support src.* imports
ROOT_DIR = Path(__file__).parent.parent.resolve()
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


# --- GLOBAL MATPLOTLIB MOCK FOR HEADLESS ENVIRONMENTS ---
with contextlib.suppress(Exception):
    import sys
    from unittest.mock import MagicMock

    class MockCanvas(MagicMock):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.figure = MagicMock()

        def setParent(self, parent):
            pass

        def setMinimumHeight(self, h):
            pass

        def setSizePolicy(self, *args):
            pass

        def setGraphicsEffect(self, effect):
            pass

        def setStyleSheet(self, style):
            pass

    mock_backend = MagicMock()
    mock_backend.FigureCanvasQTAgg = MockCanvas
    mock_backend.FigureCanvas = MockCanvas

    sys.modules["matplotlib.backends.backend_qtagg"] = mock_backend
    sys.modules["matplotlib.backends.backend_qt5agg"] = mock_backend
    sys.modules["matplotlib.backends.backend_qt"] = mock_backend
    sys.modules["matplotlib.backends.qt_compat"] = MagicMock()
# --------------------------------------------------------


# --- GLOBAL PySide6 MOCK FOR HEADLESS ENVIRONMENTS ---
try:
    import PySide6  # noqa: F401
except (ImportError, RuntimeError):

    class MockQObject:
        def __init__(self, *args, **kwargs):
            pass

        def setParent(self, parent):
            pass

    class MockSignal:
        def __init__(self, *args, **kwargs):
            pass

        def emit(self, *args, **kwargs):
            pass

        def connect(self, slot):
            pass

    mock_qt_core = MagicMock()
    mock_qt_core.QObject = MockQObject
    mock_qt_core.Signal = MockSignal

    sys.modules["PySide6"] = MagicMock()
    sys.modules["PySide6.QtCore"] = mock_qt_core
    sys.modules["PySide6.QtGui"] = MagicMock()
    sys.modules["PySide6.QtWidgets"] = MagicMock()
    sys.modules["PySide6.QtTest"] = MagicMock()
# ---------------------------------------------------


def pytest_configure(config):
    """Setup global mocks and patches."""
    patcher = patch("os.getlogin", return_value="testuser")
    patcher.start()

    selenium_patcher = patch("selenium.webdriver.Chrome", return_value=MagicMock())
    manager_patcher = patch(
        "webdriver_manager.chrome.ChromeDriverManager.install",
        return_value="/mock/path/chromedriver",
    )

    selenium_patcher.start()
    manager_patcher.start()

    # 4. Isolare il Keyring
    keyring.set_keyring(InMemoryKeyring())

    config.add_cleanup(patcher.stop)
    config.add_cleanup(selenium_patcher.stop)
    config.add_cleanup(manager_patcher.stop)


@pytest.fixture
def temp_dir(tmp_path):
    """Create a temporary directory for tests."""
    return tmp_path


@pytest.fixture(autouse=True)
def _isolate_config(tmp_path, monkeypatch):
    """Global isolation for configuration and data.
    Ensures NO test ever writes to real user directories.
    """
    from src.core import (
        config_manager,
        paths,
    )
    from src.core.audit_manager import AuditManager
    from src.core.database.manager import DatabaseManager
    from src.core.secrets_manager import SecretsManager
    from src.core.stats_manager import StatsManager
    from src.utils.security import password_manager

    # 1. Setup fake paths
    fake_dir = tmp_path / "syncrojob_test_env"
    fake_dir.mkdir(parents=True, exist_ok=True)
    (fake_dir / "data").mkdir(exist_ok=True)
    (fake_dir / "logs").mkdir(exist_ok=True)
    (fake_dir / "security").mkdir(exist_ok=True)
    fake_file = fake_dir / "config.json"

    # 2. Inject environment variable for subprocesses/late imports
    monkeypatch.setenv("SYNCROJOB_CONFIG_DIR", str(fake_dir))

    # 3. Apply patches to global path constants
    with (
        patch("src.core.paths.CONFIG_DIR", fake_dir),
        patch("src.core.paths.CONFIG_FILE", fake_file),
        patch("src.core.paths.DB_DIR", fake_dir / "data"),
        patch("src.core.paths.LOGS_DIR", fake_dir / "logs"),
        patch("src.core.config_manager.CONFIG_DIR", fake_dir),
        patch("src.core.config_manager.CONFIG_FILE", fake_file),
        patch("src.core.config_manager.check_and_migrate_local_config", return_value=False),
    ):
        # 4. Reset Singletons to use new paths
        config_manager._config_cache = None
        password_manager._reset_for_testing()

        # Reset Audit, DB and Stats Managers to force re-initialization with patched paths
        AuditManager._instance = None
        DatabaseManager._instance = None
        StatsManager._instance = None
        SecretsManager._keyring_available = None

        # Re-ensure dirs in the new fake path
        paths.DB_DIR.mkdir(parents=True, exist_ok=True)

        yield fake_file

        # 5. Cleanup after test
        config_manager._config_cache = None
        AuditManager._instance = None
        DatabaseManager._instance = None
        StatsManager._instance = None
        SecretsManager._keyring_available = None


@pytest.fixture(autouse=True)
def cleanup_widgets():
    """Force clean up of top-level widgets."""
    yield
    import gc

    with contextlib.suppress(ImportError, RuntimeError):
        from PySide6.QtWidgets import QApplication

        if QApplication.instance():
            for widget in QApplication.topLevelWidgets():
                with contextlib.suppress(Exception):
                    widget.close()
                    widget.deleteLater()
            QApplication.processEvents()
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
