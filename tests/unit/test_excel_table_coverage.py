
import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidgetItem

from src.gui.styles import COLORS
from src.gui.widgets.core_widgets import FilterComboBox
from src.gui.widgets.excel_table import EditableDataTable, ExcelTableWidget


class TestExcelTableCoverage:
    @pytest.fixture
    def app(self, qapp):
        return qapp

    def test_excel_table_clear_selection(self, app):
        """Verifica la cancellazione di celle e widget combo selezionati."""
        table = ExcelTableWidget()
        table.setRowCount(2)
        table.setColumnCount(2)

        # Inserisci dati editabili
        it = QTableWidgetItem("Test")
        it.setFlags(it.flags() | Qt.ItemFlag.ItemIsEditable)
        table.setItem(0, 0, it)

        # Usa FilterComboBox (richiesto da ExcelTableWidget per la pulizia widget)
        combo = FilterComboBox()
        combo.addItems(["", "Option 1"])
        combo.setCurrentText("Option 1")
        table.setCellWidget(1, 1, combo)

        # Seleziona tutto
        table.selectAll()
        table.clear_selection()

        assert table.item(0, 0).text() == ""
        assert combo.currentIndex() == 0

    def test_editable_data_table_basic_flow(self, app):
        """Verifica caricamento e scaricamento dati in EditableDataTable."""
        cols = [
            {"name": "Col1", "type": "text"},
            {"name": "Col2", "type": "combo", "options": ["A", "B"]},
        ]
        data_table = EditableDataTable(cols)

        # Inizialmente 20 righe vuote
        assert data_table.table.rowCount() == 20

        # Carica dati (matching flessibile)
        test_data = [{"col1": "Val1", "COL 2": "A"}]
        data_table.set_data(test_data)

        # La tabella ora padderà a 20 righe (initial_rows)
        assert data_table.table.rowCount() == 20
        assert data_table.table.item(0, 0).text() == "Val1"

        # Recupera dati
        exported = data_table.get_data()
        assert len(exported) == 1
        assert exported[0]["Col1"] == "Val1"

    def test_set_row_status_colors(self, app):
        """Verifica che i colori degli stati riga siano applicati correttamente."""
        table = ExcelTableWidget()
        table.setRowCount(1)
        table.setColumnCount(1)
        it = QTableWidgetItem("Item")
        table.setItem(0, 0, it)

        table.set_row_status(0, "completato")
        color = it.background().color().name().upper()
        # Allineamento a COLORS["table_success_bg"]
        expected = COLORS["table_success_bg"].upper()
        assert color == expected

    def test_excel_table_context_menu_event_with_qpoint(self, app, mocker):
        """Verifica che contextMenuEvent non crashi con un QPoint (CustomContextMenu)."""
        from PyQt6.QtCore import QPoint

        table = ExcelTableWidget()
        pos = QPoint(10, 10)

        # Mock QMenu.exec e mapToGlobal
        mocker.patch("PyQt6.QtWidgets.QMenu.exec")
        mocker.patch.object(table, "mapToGlobal", return_value=QPoint(100, 100))

        # Non dovrebbe sollevare AttributeError
        table.contextMenuEvent(pos)
