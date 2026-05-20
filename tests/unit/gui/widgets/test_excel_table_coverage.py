from unittest.mock import patch

import pytest
from PySide6.QtCore import QPoint

from src.gui.widgets.excel_table import EditableDataTable, ExcelTableWidget


class TestExcelTable:
    @pytest.fixture
    def columns(self):
        return [
            {"name": "id", "label": "ID", "readonly": True},
            {"name": "name", "label": "Nome"},
            {"name": "type", "label": "Tipo", "type": "combo", "options": ["A", "B"]},
            {"name": "esito", "label": "ESITO"},
        ]

    def test_excel_table_set_row_status(self, qtbot):
        table = ExcelTableWidget()
        table.setColumnCount(2)
        table.setRowCount(1)
        from src.gui.widgets.core_widgets import SortableTableWidgetItem

        table.setItem(0, 0, SortableTableWidgetItem("data"))

        table.set_row_status(0, "completato")
        item = table.item(0, 0)
        # Check background color - depends on COLORS["table_success_bg"]
        assert item.background().color().isValid()

    def test_excel_table_clear_selection(self, qtbot):
        table = ExcelTableWidget()
        table.setColumnCount(1)
        table.setRowCount(2)
        from src.gui.widgets.core_widgets import SortableTableWidgetItem

        table.setItem(0, 0, SortableTableWidgetItem("fill"))
        table.setItem(1, 0, SortableTableWidgetItem("keep"))

        # Select first row
        table.setCurrentItem(table.item(0, 0))
        table.item(0, 0).setSelected(True)

        table.clear_selection()
        assert table.item(0, 0).text() == ""
        assert table.item(1, 0).text() == "keep"

    def test_editable_data_table_basic_flow(self, qtbot, columns):
        widget = EditableDataTable(columns, initial_rows=5)
        qtbot.addWidget(widget)

        assert widget.table.rowCount() == 5
        assert widget.table.columnCount() == 4

        # Test add/remove row
        widget._add_row()
        assert widget.table.rowCount() == 6

        widget._remove_row()
        assert widget.table.rowCount() == 5

    def test_editable_data_table_get_set_data(self, qtbot, columns):
        widget = EditableDataTable(columns, initial_rows=2)
        data = [{"id": "1", "name": "Mario", "type": "A"}, {"id": "2", "name": "Luigi", "type": "B"}]

        widget.set_data(data)
        # Should have 2 data rows + padding to 2?
        # Implementation says: while rowCount < initial_rows: _add_row
        assert widget.table.rowCount() >= 2

        extracted = widget.get_data()
        assert len(extracted) == 2
        assert extracted[0]["name"] == "Mario"
        assert extracted[1]["type"] == "B"

    def test_clear_status_columns(self, qtbot, columns):
        widget = EditableDataTable(columns, initial_rows=1)
        widget.update_cell(0, 3, "OK")  # ESITO col
        widget.set_row_status(0, "completato")

        widget.clear_status_columns()
        assert widget.table.item(0, 3).text() == ""
        # Status color should be reset (white)
        # (Assuming colors[status] for da_processare is bg_white)

    def test_update_column_options(self, qtbot, columns):
        widget = EditableDataTable(columns, initial_rows=2)
        # col index 2 is "type" (combo)
        new_options = ["C", "D"]
        widget.update_column_options(2, new_options)

        combo = widget.table.cellWidget(0, 2)
        assert combo.findText("C") > 0  # index 0 is ""
        assert widget.columns[2]["options"] == new_options

    def test_excel_table_context_menu_event(self, qtbot):
        with patch("src.gui.widgets.excel_table.QMenu") as mock_menu_class:
            table = ExcelTableWidget()
            table.setColumnCount(1)
            table.setRowCount(1)

            # Test trigger with QPoint
            table.contextMenuEvent(QPoint(0, 0))

            assert mock_menu_class.called
            assert mock_menu_class.return_value.addAction.called
            assert mock_menu_class.return_value.exec.called
