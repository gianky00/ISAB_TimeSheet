
import pytest
import sys
from unittest.mock import MagicMock, patch
from src.core.app_initializer import AppInitializer
from src.core.license_validator import LicenseStatus

class TestAppInitializerDeep:
    @pytest.fixture
    def mock_msgbox(self, mocker):
        return mocker.patch("PyQt6.QtWidgets.QMessageBox.critical")

    @pytest.fixture
    def mock_msgbox_warn(self, mocker):
        return mocker.patch("PyQt6.QtWidgets.QMessageBox.warning")

    def test_initialize_full_success(self, mocker):
        """Verifica avvio con successo (Licenza valida + DB OK)."""
        m_status = mocker.patch("src.core.app_initializer.get_detailed_license_status")
        m_status.return_value = (LicenseStatus.VALID, "OK")
        mocker.patch("src.core.app_initializer.db_manager.init_db")
        
        assert AppInitializer.initialize() is True

    def test_initialize_update_trigger(self, mocker):
        """Verifica che se la licenza manca, venga tentato l'aggiornamento."""
        m_status = mocker.patch("src.core.app_initializer.get_detailed_license_status")
        m_status.side_effect = [
            (LicenseStatus.INVALID, "Missing"), 
            (LicenseStatus.VALID, "OK")
        ]
        
        mock_update = mocker.patch("src.core.app_initializer.run_update")
        mocker.patch("src.core.app_initializer.db_manager.init_db")
        mocker.patch("sys.exit")
        
        res = AppInitializer.initialize()
        assert res is True
        assert mock_update.call_count == 1

    def test_initialize_emergency_grace_success(self, mocker, mock_msgbox_warn):
        """Verifica avvio in modalità provvisoria tramite periodo di grazia."""
        m_status = mocker.patch("src.core.app_initializer.get_detailed_license_status")
        m_status.return_value = (LicenseStatus.INVALID, "Expired")
        mocker.patch("src.core.app_initializer.run_update")
        
        mocker.patch("src.core.app_initializer.check_emergency_grace_period", 
                     return_value=(True, "Grace Active", 3))
        mocker.patch("src.core.app_initializer.get_hardware_id", return_value="HWID")
        mocker.patch("src.core.app_initializer.db_manager.init_db")
        
        assert AppInitializer.initialize() is True
        mock_msgbox_warn.assert_called_once()

    def test_initialize_failed_license_exit(self, mocker, mock_msgbox):
        """Verifica che l'app esca se licenza e grazia falliscono."""
        m_status = mocker.patch("src.core.app_initializer.get_detailed_license_status")
        m_status.return_value = (LicenseStatus.INVALID, "Banned")
        mocker.patch("src.core.app_initializer.run_update")
        mocker.patch("src.core.app_initializer.check_emergency_grace_period", 
                     return_value=(False, "Grace Expired", 0))
        mocker.patch("src.core.app_initializer.get_hardware_id", return_value="HWID")
        
        mock_exit = mocker.patch("sys.exit")
        
        AppInitializer.initialize()
        
        mock_exit.assert_called_once_with(1)
        mock_msgbox.assert_called_once()

    def test_initialize_db_error_exit(self, mocker, mock_msgbox):
        """Verifica che l'app esca se il database non si inizializza."""
        m_status = mocker.patch("src.core.app_initializer.get_detailed_license_status")
        m_status.return_value = (LicenseStatus.VALID, "OK")
        
        m_db = mocker.patch("src.core.app_initializer.db_manager.init_db")
        m_db.side_effect = Exception("DB Corrupted")
        
        mock_exit = mocker.patch("sys.exit")
        
        AppInitializer.initialize()
        
        mock_exit.assert_called_once_with(1)
        mock_msgbox.assert_called_once()
