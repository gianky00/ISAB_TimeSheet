from PySide6.QtCore import Qt

from src.gui.formatters import FastTableModel, format_currency_smart, format_number_smart


class TestFormatters:
    def test_format_currency_smart(self):
        assert format_currency_smart(None) == ""
        assert format_currency_smart("") == ""
        assert format_currency_smart(1200) == "1.200"
        assert format_currency_smart(1200.5) == "1.200,50"
        assert format_currency_smart("1.234,56") == "1.234,56"
        assert format_currency_smart("1,234.56") == "1.234,56"
        assert format_currency_smart("€ 100") == "100"
        assert format_currency_smart("invalid") == "invalid"

    def test_format_number_smart(self):
        assert format_number_smart(10.5) == "10,50"
        assert format_number_smart(10) == "10"


class TestFastTableModel:
    def test_model_basic(self):
        headers = ["Col1", "Col2"]
        data = [["A", 10], ["B", 20]]
        model = FastTableModel(data, headers)

        assert model.rowCount() == 2
        assert model.columnCount() == 2
        assert model.headerData(0, Qt.Orientation.Horizontal) == "Col1"

        index = model.index(0, 1)
        assert model.data(index, Qt.ItemDataRole.DisplayRole) == "10"
        assert model.data(index, Qt.ItemDataRole.EditRole) == 10

    def test_model_formatting(self):
        data = [[1200.5]]
        headers = ["Val"]
        model = FastTableModel(data, headers)
        model.set_column_formatter(0, format_currency_smart)

        index = model.index(0, 0)
        assert model.data(index, Qt.ItemDataRole.DisplayRole) == "1.200,50"
        assert model.data(index, Qt.ItemDataRole.TextAlignmentRole) == (
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )

    def test_model_sort(self):
        data = [["B", 20], ["A", 10], ["C", 15]]
        headers = ["Name", "Val"]
        model = FastTableModel(data, headers)

        # Sort by Name Ascending
        model.sort(0, Qt.SortOrder.AscendingOrder)
        assert model.get_raw_row(0)[0] == "A"

        # Sort by Val Descending
        model.sort(1, Qt.SortOrder.DescendingOrder)
        assert model.get_raw_row(0)[1] == 20

    def test_model_sort_dates(self):
        data = [["15/10/2023"], ["01/01/2023"], ["20/05/2023"]]
        model = FastTableModel(data, ["Date"])

        model.sort(0, Qt.SortOrder.AscendingOrder)
        assert model.get_raw_row(0)[0] == "01/01/2023"
        assert model.get_raw_row(2)[0] == "15/10/2023"  # No, 20/05/2023 is index 1, 15/10/2023 is index 2
        assert model.get_raw_row(1)[0] == "20/05/2023"
        assert model.get_raw_row(2)[0] == "15/10/2023"
