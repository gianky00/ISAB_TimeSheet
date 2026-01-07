from unittest.mock import patch

import pytest

from src.gui.panels import BaseBotPanel, ScaricaTSPanel


class TestBotPanels:

    @pytest.fixture
    def app(self, qapp):
        return qapp

    def test_base_bot_panel(self, app, qtbot):
        panel = BaseBotPanel("test_bot", "Bot Name", "Bot Desc")
        qtbot.addWidget(panel)

        assert panel.bot_id == "test_bot"
        assert panel.start_btn.text() == "Avvia"

    @patch("src.gui.panels.config_manager.load_config")
    def test_scarica_ts_panel(self, mock_load, app, qtbot):
        mock_load.return_value = {"fornitori": ["F1"], "last_ts_data": [{"numero_oda": "123"}]}

        panel = ScaricaTSPanel()
        qtbot.addWidget(panel)

        assert panel.fornitore_combo.count() >= 1
        # Check if data loaded into table
        assert panel.data_table.table.rowCount() >= 1
        assert panel.data_table.table.item(0, 0).text() == "123"
