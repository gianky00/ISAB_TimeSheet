from unittest.mock import patch

from PyQt6.QtCore import Qt

from src.gui.panels import DettagliOdAPanel, ScaricoPDLPanel, TimbratureDBPanel


class TestBotPanelsFinal:
    def test_dettagli_oda_panel_logic(self, qapp, qtbot):
        with patch(
            "src.core.config_manager.load_config",
            return_value={"fornitori": ["F1"]},
        ):
            panel = DettagliOdAPanel()
            qtbot.addWidget(panel)

            panel.data_table.set_data([{"numero_oda": "12345"}])
            ready, msg = panel.validate_ready()
            # If creds missing, it should be False
            assert "Credenziali" in msg or ready is True

    def test_scarico_pdl_panel_ui(self, qapp, qtbot):
        with patch("src.utils.printing.get_installed_printers", return_value=["Printer1"]):
            panel = ScaricoPDLPanel()
            qtbot.addWidget(panel)
            assert panel.combo_stampanti.count() > 0

            panel.check_stampa.setChecked(True)
            assert panel.check_stampa.isChecked()

    def test_timbrature_db_panel_refresh(self, qapp, qtbot):
        with patch("src.gui.panels.timbrature.panel.TimbratureStorage") as mock_storage:
            # Mock data matching the expected row structure (at least 18 elements)
            mock_row = [None] * 20
            mock_row[0] = "2024-01-01"
            mock_row[1] = "08:00"
            mock_row[2] = "17:00"
            mock_row[3] = "Mario"
            mock_row[4] = "Rossi"
            mock_row[16] = "R1"
            mock_row[17] = "C1"

            mock_storage.return_value.get_timbrature_with_reparto.return_value = [tuple(mock_row)]
            mock_storage.return_value.get_lists.return_value = {
                "reparti": [],
                "cantieri": [],
            }

            panel = TimbratureDBPanel()
            qtbot.addWidget(panel)

            panel.refresh_data()
            assert panel.model.rowCount() == 1

            # Verifichiamo il valore formattato
            display_val = panel.model.data(panel.model.index(0, 0), Qt.ItemDataRole.DisplayRole)
            assert "01/01/2024" in display_val
