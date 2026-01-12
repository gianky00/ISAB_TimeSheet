from unittest.mock import patch

from src.gui.panels import DettagliOdAPanel, ScaricoPDLPanel, TimbratureDBPanel


class TestBotPanelsFinal:
    def test_dettagli_oda_panel_logic(self, qapp, qtbot):
        with patch("src.gui.panels.config_manager.load_config", return_value={"fornitori": ["F1"]}):
            panel = DettagliOdAPanel()
            qtbot.addWidget(panel)

            panel.data_table.set_data([{"numero_oda": "12345"}])
            ready, msg = panel.validate_ready()
            # If creds missing, it should be False
            assert "Credenziali" in msg or ready is True

    def test_scarico_pdl_panel_ui(self, qapp, qtbot):
        with patch("src.gui.panels.get_installed_printers", return_value=["Printer1"]):
            panel = ScaricoPDLPanel()
            qtbot.addWidget(panel)
            assert panel.printer_combo.count() > 0

            panel.print_check.setChecked(True)
            assert panel.print_check.isChecked()

    def test_timbrature_db_panel_refresh(self, qapp, qtbot):
        with patch("src.gui.panels.TimbratureStorage") as mock_storage:
            mock_storage.return_value.get_timbrature_with_reparto.return_value = [
                ("2024-01-01", "08:00", "17:00", "Mario", "Rossi", "SI", "ISAB", "R1", "C1")
            ]
            panel = TimbratureDBPanel()
            qtbot.addWidget(panel)

            panel.refresh_data()
            assert panel.model.rowCount() == 1
            assert "01/01/2024" in panel.model.data(panel.model.index(0, 0))
