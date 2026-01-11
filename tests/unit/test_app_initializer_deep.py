from unittest.mock import MagicMock, patch

import pytest

from src.core.app_initializer import AppInitializer
from src.core.license_validator import LicenseStatus


class TestAppInitializer:
    @pytest.fixture(autouse=True)
    def mock_license_deps(self):
        """Mocka tutte le dipendenze esterne della licenza per evitare loop o chiamate reali."""
        with patch("src.core.app_initializer.get_detailed_license_status") as m_status, \
             patch("src.core.app_initializer.run_update") as m_update, \
             patch("src.core.app_initializer.check_emergency_grace_period") as m_grace, \
             patch("src.core.app_initializer.get_hardware_id") as m_hwid:

            m_status.return_value = (LicenseStatus.VALID, "OK")
            m_update.return_value = None
            m_grace.return_value = (False, "No Grace", None)
            m_hwid.return_value = "TEST-ID"
            yield m_status, m_update, m_grace

    @patch("src.core.app_initializer.db_manager.init_db")
    def test_initialize_flow_success(self, mock_db, mock_license_deps):
        m_status, _, _ = mock_license_deps
        res = AppInitializer.initialize()
        assert res is True
        mock_db.assert_called_once()

    @patch("src.core.app_initializer.sys.exit")
    def test_initialize_fail_license(self, mock_exit, mock_license_deps):
        m_status, _, m_grace = mock_license_deps
        # Forza licenza non valida e niente periodo di grazia
        m_status.return_value = (LicenseStatus.INVALID, "Expired")
        m_grace.return_value = (False, "No Grace", None)

        # Mocking QMessageBox to prevent blocking UI
        with patch("src.core.app_initializer.QMessageBox.critical"):
            AppInitializer.initialize()
            # Deve chiamare sys.exit(1)
            mock_exit.assert_called_with(1)

    @patch("src.core.app_initializer.db_manager.init_db", side_effect=Exception("DB Error"))
    @patch("src.core.app_initializer.sys.exit")
    def test_initialize_fail_db(self, mock_exit, mock_db, mock_license_deps):
        with patch("src.core.app_initializer.QMessageBox.critical"):
            AppInitializer.initialize()
            mock_exit.assert_called_with(1)

    def test_setup_app_style(self):
        mock_app = MagicMock()
        with patch("src.core.app_initializer.apply_theme"):
            AppInitializer.setup_app_style(mock_app)
            mock_app.setStyle.assert_called_with("Fusion")
            assert mock_app.setApplicationName.called
