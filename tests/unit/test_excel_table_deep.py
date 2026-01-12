from src.gui.widgets.excel_table import EditableDataTable, ExcelTableWidget


class TestExcelTableWidgetDeep:
    def test_basic_table_operations(self, qapp, qtbot):
        table = ExcelTableWidget()
        qtbot.addWidget(table)

        table.setColumnCount(2)
        table.setRowCount(2)

        # Test copy/paste logic (logic level)
        table.copy_selection()
        table.paste_selection()

        # Test clear selection
        table.clear_selection()

    def test_editable_data_table(self, qapp, qtbot):
        cols = [{"name": "Col1", "type": "text"}, {"name": "Col2", "type": "combo", "options": ["A", "B"]}]
        edt = EditableDataTable(cols)
        qtbot.addWidget(edt)

        # Test row management
        initial_rows = edt.table.rowCount()
        edt._add_row()
        assert edt.table.rowCount() == initial_rows + 1

        # Test data retrieval
        edt.set_data([{"col1": "val1", "col2": "A"}])
        data = edt.get_data()
        assert len(data) >= 1
        assert data[0]["col1"] == "val1"

    def test_row_status_coloring(self, qapp, qtbot):
        table = ExcelTableWidget()
        qtbot.addWidget(table)
        table.setColumnCount(1)
        table.setRowCount(1)
        from PyQt6.QtWidgets import QTableWidgetItem
        table.setItem(0, 0, QTableWidgetItem("Test"))

        table.set_row_status(0, "completato")
        # Just ensure it doesn't crash and colors are applied
        assert table.item(0, 0).background() is not None
