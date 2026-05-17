
import pytest
from PySide6.QtWidgets import QApplication

from src.gui.panels.carico_ts import CaricoTSPanel
from src.gui.panels.scarico_ts import ScaricaTSPanel


class TestGUIPanels:
    @pytest.fixture
    def app(self, qapp):
        return qapp

    def test_scarica_ts_panel_init(self, app, qtbot):
        panel = ScaricaTSPanel()
        qtbot.addWidget(panel)
        QApplication.processEvents()

        panel.params_widget.fornitore_combo.addItem("F1")
        from PySide6.QtCore import QDate

        panel.params_widget.date_da.setDate(QDate(2025, 1, 1))

        assert panel.params_widget.fornitore_combo.count() >= 1
        panel.data_table.set_data([{"numero_oda": "123"}])
        assert panel.data_table.table.rowCount() >= 1

    def test_carico_ts_panel_structure(self, app, qtbot):
        panel = CaricoTSPanel()
        qtbot.addWidget(panel)
        QApplication.processEvents()

        assert panel.data_table is not None
        assert panel.bot_id == "carico_ts"
