from unittest.mock import MagicMock, patch

class TestContabilitaExtra:

    def test_contabilita_panel_init(self, qapp, qtbot):
        from PyQt6.QtWidgets import QWidget
        from src.gui.contabilita_panel import ContabilitaPanel
        
        with patch("src.gui.contabilita_panel.ContabilitaManager") as mock_manager, \
             patch("src.gui.contabilita_panel.ContabilitaYearTab") as mock_year_tab, \
             patch("src.gui.contabilita_panel.GiornaliereYearTab") as mock_giorn_tab, \
             patch("src.gui.contabilita_kpi_panel.ContabilitaKPIPanel") as mock_kpi_class, \
             patch("src.gui.contabilita_panel.AttivitaProgrammateTab") as mock_att_tab, \
             patch("src.gui.contabilita_panel.CertificatiCampioneTab") as mock_cert_tab, \
             patch("src.gui.contabilita_panel.QTimer.singleShot") as mock_timer:
            
            # Ensure mock returns a QWidget with the required methods
            for m in [mock_cert_tab, mock_att_tab, mock_kpi_class, mock_giorn_tab, mock_year_tab]:
                instance = QWidget()
                qtbot.addWidget(instance)
                instance.refresh_years = MagicMock()
                instance.refresh_data = MagicMock()
                instance.apply_filters = MagicMock()
                m.return_value = instance

            # Mock for ContabilitaPanel's direct calls
            mock_manager.get_available_years.return_value = [2023, 2024]
            mock_manager.get_data_by_year.return_value = []
            mock_manager.get_giornaliere_by_year.return_value = []
            mock_manager.get_attivita_programmate_data.return_value = []
            mock_manager.get_certificati_campione_data.return_value = []

            panel = ContabilitaPanel()
            qtbot.addWidget(panel)
            
            # Manually trigger the deferred loading since timer is mocked
            panel._safe_refresh_tabs()

            assert panel is not None
            assert panel.main_tabs.count() >= 5

    def test_contabilita_panel_tab_switch(self, qapp, qtbot):
        from PyQt6.QtWidgets import QWidget
        from src.gui.contabilita_panel import ContabilitaPanel

        with patch("src.gui.contabilita_panel.ContabilitaManager") as mock_manager, \
             patch("src.gui.contabilita_panel.ContabilitaYearTab") as mock_year_tab, \
             patch("src.gui.contabilita_panel.GiornaliereYearTab") as mock_giorn_tab, \
             patch("src.gui.contabilita_kpi_panel.ContabilitaKPIPanel") as mock_kpi_class, \
             patch("src.gui.contabilita_panel.AttivitaProgrammateTab") as mock_att_tab, \
             patch("src.gui.contabilita_panel.CertificatiCampioneTab") as mock_cert_tab, \
             patch("src.gui.contabilita_panel.QTimer.singleShot") as mock_timer:

            # Ensure mock returns a real QWidget with required methods
            for m in [mock_cert_tab, mock_att_tab, mock_kpi_class, mock_giorn_tab, mock_year_tab]:
                instance = QWidget()
                qtbot.addWidget(instance)
                instance.refresh_years = MagicMock()
                instance.refresh_data = MagicMock()
                instance.apply_filters = MagicMock()
                m.return_value = instance

            mock_manager.get_available_years.return_value = [2023, 2024]
            mock_manager.get_data_by_year.return_value = []
            mock_manager.get_giornaliere_by_year.return_value = []
            mock_manager.get_attivita_programmate_data.return_value = []
            mock_manager.get_certificati_campione_data.return_value = []

            panel = ContabilitaPanel()
            qtbot.addWidget(panel)
            
            # Manually trigger
            panel._safe_refresh_tabs()

            # Switch to "Giornaliere" (Index 1)
            panel.main_tabs.setCurrentIndex(1)
            assert panel.main_tabs.currentIndex() == 1

            # Switch to "Attività Programmate" (Index 2)
            panel.main_tabs.setCurrentIndex(2)
            assert panel.main_tabs.currentIndex() == 2
