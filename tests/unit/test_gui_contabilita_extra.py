from unittest.mock import MagicMock, patch

from PySide6.QtWidgets import QWidget


class TestContabilitaExtra:
    """Test suite for ContabilitaPanel container logic.
    Uses extensive mocking to avoid instantiating heavy child tabs.
    """

    def test_contabilita_panel_init(self, qapp, qtbot):
        from src.gui.panels.contabilita_panel import ContabilitaPanel

        # We mock EVERYTHING inside the panel to isolate the container logic
        with (
            patch("src.gui.panels.contabilita_panel.ContabilitaManager") as mock_manager,
            patch("src.gui.panels.contabilita_panel.ContabilitaYearTab") as mock_year_tab,
            patch("src.gui.panels.contabilita_panel.GiornaliereYearTab") as mock_giorn_tab,
            patch("src.gui.panels.contabilita_panel.ContabilitaKPIPanel") as mock_kpi_class,
            patch("src.gui.panels.contabilita_panel.AttivitaProgrammateTab") as mock_att_tab,
            patch("src.gui.panels.contabilita_panel.CertificatiCampioneTab") as mock_cert_tab,
        ):
            # Setup Mocks to behave like QWidgets without strictly being fully initialized ones
            # We use a real simple QWidget as base for the return value to satisfy addTab types
            def create_mock_widget(*args, **kwargs):
                w = QWidget()
                w.refresh_years = MagicMock()
                w.refresh_data = MagicMock()
                w.apply_filters = MagicMock()
                return w

            mock_year_tab.side_effect = create_mock_widget
            mock_giorn_tab.side_effect = create_mock_widget
            mock_kpi_class.return_value = create_mock_widget()
            mock_att_tab.return_value = create_mock_widget()
            mock_cert_tab.return_value = create_mock_widget()

            # Mock Manager Data
            mock_manager.get_available_years.return_value = [2023, 2024]
            mock_manager.get_data_by_year.return_value = []
            mock_manager.get_giornaliere_by_year.return_value = []
            mock_manager.get_attivita_programmate_data.return_value = []
            mock_manager.get_certificati_campione_data.return_value = []

            # Instantiate Panel without qtbot.addWidget (to avoid strict integration)
            panel = ContabilitaPanel()

            try:
                # Manually trigger deferred loading (simulating the QTimer callback)
                panel._safe_refresh_tabs()

                # Assertions
                assert panel is not None
                assert panel.main_tabs.count() > 0
                mock_kpi_class.return_value.refresh_years.assert_called()
            finally:
                panel.close()
                panel.deleteLater()

    def test_contabilita_panel_tab_switch(self, qapp, qtbot):
        from src.gui.panels.contabilita_panel import ContabilitaPanel

        with (
            patch("src.gui.panels.contabilita_panel.ContabilitaManager") as mock_manager,
            patch("src.gui.panels.contabilita_panel.ContabilitaYearTab") as mock_year_tab,
            patch("src.gui.panels.contabilita_panel.GiornaliereYearTab") as mock_giorn_tab,
            patch("src.gui.panels.contabilita_panel.ContabilitaKPIPanel") as mock_kpi_class,
            patch("src.gui.panels.contabilita_panel.AttivitaProgrammateTab") as mock_att_tab,
            patch("src.gui.panels.contabilita_panel.CertificatiCampioneTab") as mock_cert_tab,
        ):

            def create_mock_widget(*args, **kwargs):
                w = QWidget()
                w.refresh_years = MagicMock()
                w.refresh_data = MagicMock()
                w.apply_filters = MagicMock()
                return w

            mock_year_tab.side_effect = create_mock_widget
            mock_giorn_tab.side_effect = create_mock_widget
            mock_kpi_class.return_value = create_mock_widget()
            mock_att_tab.return_value = create_mock_widget()
            mock_cert_tab.return_value = create_mock_widget()

            mock_manager.get_available_years.return_value = [2024]  # Single year for simplicity

            panel = ContabilitaPanel()

            try:
                panel._safe_refresh_tabs()

                # Switch to "Giornaliere" (Index 1)
                panel.main_tabs.setCurrentIndex(1)
                assert panel.main_tabs.currentIndex() == 1

                # Switch to "KPI" (Index 4)
                panel.main_tabs.setCurrentIndex(4)
                assert panel.main_tabs.currentIndex() == 4
            finally:
                panel.close()
                panel.deleteLater()
