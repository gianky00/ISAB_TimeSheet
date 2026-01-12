from unittest.mock import MagicMock, patch

import pytest
from src.core.app_initializer import AppInitializer
from src.core.license_validator import LicenseStatus


class TestAppInitializerCoverage:
    """Test suite for src/core/app_initializer.py"""

    @pytest.fixture
    def mock_db_manager(self):
        with patch("src.core.app_initializer.db_manager") as mock:
            yield mock

    @pytest.fixture
    def mock_license_status(self):
        with patch("src.core.app_initializer.get_detailed_license_status") as mock:
            yield mock

    @pytest.fixture
    def mock_check_grace(self):
        with patch("src.core.app_initializer.check_emergency_grace_period") as mock:
            yield mock

    @pytest.fixture
    def mock_run_update(self):
        with patch("src.core.app_initializer.run_update") as mock:
            yield mock

    @pytest.fixture
    def mock_hw_id(self):
        with patch("src.core.app_initializer.get_hardware_id", return_value="HWID123"):
            yield

    @pytest.fixture
    def mock_msg_box(self):
        with patch("src.core.app_initializer.QMessageBox") as mock:
            yield mock

    @pytest.fixture
    def mock_sys_exit(self):
        with patch("sys.exit") as mock:
            yield mock

    @pytest.fixture
    def mock_apply_theme(self):
        with patch("src.core.app_initializer.apply_theme") as mock:
            yield mock

    def test_initialize_success(self, mock_license_status, mock_db_manager):
        """Test inizializzazione completa con successo."""
        mock_license_status.return_value = (LicenseStatus.VALID, "OK")
        mock_db_manager.init_db.return_value = True

        assert AppInitializer.initialize() is True

    def test_initialize_license_fail(self, mock_license_status, mock_run_update, mock_check_grace, mock_hw_id, mock_msg_box, mock_sys_exit):
        """Test fallimento licenza -> exit."""
        mock_license_status.return_value = (LicenseStatus.INVALID, "Err")
        mock_check_grace.return_value = (False, "No Grace", 0) # No grace period

        AppInitializer.initialize()
        mock_sys_exit.assert_called_with(1)

    def test_initialize_db_fail(self, mock_license_status, mock_db_manager, mock_msg_box, mock_sys_exit):
        """Test fallimento DB -> exit."""
        mock_license_status.return_value = (LicenseStatus.VALID, "OK")
        mock_db_manager.init_db.side_effect = Exception("DB Error")

        AppInitializer.initialize()
        mock_sys_exit.assert_called_with(1)

    def test_check_license_valid(self, mock_license_status):
        """Test _check_license diretto valido."""
        mock_license_status.return_value = (LicenseStatus.VALID, "OK")
        assert AppInitializer._check_license() is True

    def test_check_license_update_fixes(self, mock_license_status, mock_run_update):
        """Test licenza invalida -> update -> valida."""
        # Prima chiamata INVALID, seconda VALID
        mock_license_status.side_effect = [(LicenseStatus.INVALID, "Err"), (LicenseStatus.VALID, "OK")]
        
        assert AppInitializer._check_license() is True
        mock_run_update.assert_called_once()

    def test_check_license_grace_period(self, mock_license_status, mock_run_update, mock_check_grace, mock_hw_id, mock_msg_box):
        """Test licenza invalida -> grace period attivo."""
        mock_license_status.return_value = (LicenseStatus.INVALID, "Err")
        mock_check_grace.return_value = (True, "Grace Active", 10)

        assert AppInitializer._check_license() is True
        # Warning mostrato
        mock_msg_box.warning.assert_called_once()

    def test_check_license_fatal(self, mock_license_status, mock_run_update, mock_check_grace, mock_hw_id, mock_msg_box):
        """Test licenza invalida -> no grace period."""
        mock_license_status.return_value = (LicenseStatus.INVALID, "Err")
        mock_check_grace.return_value = (False, "No Grace", 0)

        assert AppInitializer._check_license() is False
        mock_msg_box.critical.assert_called_once()

    def test_check_license_exception(self, mock_license_status):
        """Test eccezione durante controllo licenza."""
        mock_license_status.side_effect = Exception("Boom")
        assert AppInitializer._check_license() is False

    def test_init_db_success(self, mock_db_manager):
        """Test init db successo."""
        assert AppInitializer._init_db() is True
        mock_db_manager.init_db.assert_called_once()

    def test_init_db_exception(self, mock_db_manager, mock_msg_box):
        """Test init db eccezione."""
        mock_db_manager.init_db.side_effect = Exception("DB Fail")
        assert AppInitializer._init_db() is False
        mock_msg_box.critical.assert_called_once()

    def test_setup_app_style(self, mock_apply_theme):
        """Test configurazione stile app."""
        mock_app = MagicMock()
        AppInitializer.setup_app_style(mock_app)
        
        mock_app.setStyle.assert_called_with("Fusion")
        mock_apply_theme.assert_called_with(mock_app, "light")
        mock_app.setFont.assert_called()
        mock_app.setApplicationName.assert_called_with("SyncroJob")
