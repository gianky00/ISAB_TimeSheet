import pytest

from src.gui.panels import BaseBotPanel, ScaricaTSPanel


class TestBotPanels:
    @pytest.fixture
    def app(self, qapp):  # noqa: ANN001
        return qapp

    def test_base_bot_panel(self, app, qtbot):  # noqa: ANN001
        panel = BaseBotPanel("test_bot", "Bot Name", "Bot Desc")
        qtbot.addWidget(panel)

        assert panel.bot_id == "test_bot"
        assert panel.start_btn.text() == "Avvia"

    def test_scarica_ts_panel(self, app, qtbot):  # noqa: ANN001
        panel = ScaricaTSPanel()
        qtbot.addWidget(panel)

        # Manually set data to verify components
        panel.params_widget.fornitore_combo.addItem("F1")
        panel.data_table.set_data([{"numero_oda": "123"}])

        assert panel.params_widget.fornitore_combo.count() >= 1
        # Check if data loaded into table
        assert panel.data_table.table.rowCount() >= 1
        assert panel.data_table.table.item(0, 0).text() == "123"
