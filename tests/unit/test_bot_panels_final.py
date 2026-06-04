from unittest.mock import MagicMock, patch

import pytest

from src.gui.panels import TimbratureDBPanel


class TestBotPanelsFinal:
    @pytest.fixture
    def panel(self, qtbot, mocker):
        mocker.patch("src.gui.panels.timbrature.panel.TimbratureStorage")
        mocker.patch("src.application.services.config_manager.load_config", return_value={})
        mocker.patch("src.gui.panels.timbrature.panel.TimbratureDataWorker")

        p = TimbratureDBPanel()
        qtbot.addWidget(p)
        return p

    def test_timbrature_db_panel_refresh(self, panel, mocker):
        panel.refresh_data()

        # Correzione firma: _on_filters_ready prende un dizionario 'lists'
        panel.storage.get_employees.return_value = []
        panel._on_filters_ready({"reparti": ["R1"]})

        assert panel.reparto_filter.count() >= 1

    def test_dettagli_oda_panel_logic(self, qtbot):
        from src.gui.panels.storico_oda.oda_panel import StoricoOdaPanel

        mock_ctrl = MagicMock()
        with patch("src.application.services.sync_tracker.SyncTracker.get_formatted_status", return_value="N/D"):
            p = StoricoOdaPanel(mock_ctrl)
            qtbot.addWidget(p)
            assert p.controller == mock_ctrl

    def test_scarico_pdl_panel_ui(self, qtbot):
        from src.gui.panels.scarico_pdl import ScaricoPDLPanel

        p = ScaricoPDLPanel()
        qtbot.addWidget(p)
        assert p.start_btn.isEnabled()
