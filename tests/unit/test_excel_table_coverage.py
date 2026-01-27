import pytest
from PyQt6.QtWidgets import QApplication, QComboBox, QTableWidgetItem

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

        # Inserisci dati
        table.setItem(0, 0, QTableWidgetItem("Test"))
        combo = QComboBox()
        combo.addItems(["", "Option 1"])
        combo.setCurrentText("Option 1")
        table.setCellWidget(1, 1, combo)

        # Seleziona tutto
        table.selectAll()
        table.clear_selection()

        assert table.item(0, 0).text() == ""
        assert combo.currentText() == ""

    def test_editable_data_table_row_management(self, app):
        """Verifica l'aggiunta di righe sopra e l'aggiornamento opzioni."""
        cols = [
            {"name": "Col1", "type": "text"},
            {"name": "Col2", "type": "combo", "options": ["A", "B"]},
        ]
        data_table = EditableDataTable(cols)

        # Inizialmente 5 righe (come da _setup_ui)
        assert data_table.table.rowCount() == 5

        # Aggiungi riga sopra (alla prima riga)
        data_table.table.setCurrentCell(0, 0)
        data_table._add_row_above()
        assert data_table.table.rowCount() == 6  # 5 default + 1

        # Aggiorna opzioni combo
        data_table.update_column_options("Col2", ["C", "D"])
        combo = data_table.table.cellWidget(0, 1)
        # L'indice 0 è sempre la stringa vuota ""
        assert combo.itemText(0) == ""
        assert combo.itemText(1) == "C"


    def test_copy_paste_cycle(self, app):
        """Simula il ciclo di copia e incolla tramite appunti."""
        table = ExcelTableWidget()
        table.setRowCount(2)
        table.setColumnCount(1)
        table.setItem(0, 0, QTableWidgetItem("Data1"))

        # Mock clipboard
        clipboard = QApplication.clipboard()

        # Copia
        table.setCurrentCell(0, 0)
        table.copy_selection()

        clipboard.setText("PastedData")
        table.setCurrentCell(1, 0)
        table.paste_selection()

        assert table.item(1, 0).text() == "PastedData"

    def test_set_row_status_colors(self, app):
        """Verifica che i colori degli stati riga siano applicati correttamente."""
        table = ExcelTableWidget()
        table.setRowCount(1)
        table.setColumnCount(1)
        table.setItem(0, 0, QTableWidgetItem("Item"))

        table.set_row_status(0, "completato")
        color = table.item(0, 0).background().color().name().upper()
        assert color == "#C8E6C9"

        table.set_row_status(0, "errore")
        color = table.item(0, 0).background().color().name().upper()
        assert color == "#FFCDD2"

    def test_analyze_with_lyra_selection(self, app, mocker):
        """Verifica che la selezione venga formattata correttamente per Lyra."""
        table = ExcelTableWidget()
        table.setRowCount(1)
        table.setColumnCount(1)
        table.setHorizontalHeaderLabels(["H1"])
        table.setItem(0, 0, QTableWidgetItem("Value1"))
        table.selectAll()

        # Mock window and its method
        mock_win = mocker.MagicMock()
        mocker.patch.object(table, "window", return_value=mock_win)

        table._analyze_selection()

        # Verifica chiamata (formato: Header: Value)
        mock_win.analyze_with_lyra.assert_called_once()
        args = mock_win.analyze_with_lyra.call_args[0][0]
        assert "H1: Value1" in args
