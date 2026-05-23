import pytest
from PySide6.QtCore import Qt

from src.gui.formatters import (
    FastTableModel,
    _try_parse_date,
    _try_parse_numeric,
    format_currency_smart,
)


class TestFormatters:
    def test_format_currency_smart(self):
        # Integri
        assert format_currency_smart(1200) == "1.200"
        assert format_currency_smart("1200") == "1.200"

        # Decimali IT
        assert format_currency_smart(1200.5) == "1.200,50"
        assert format_currency_smart("1.234,56") == "1.234,56"

        # Decimali EN
        assert format_currency_smart("1,234.56") == "1.234,56"

        # Simboli e spazi
        assert format_currency_smart(" € 10,50 ") == "10,50"

        # Vuoti
        assert format_currency_smart(None) == ""
        assert format_currency_smart("") == ""

        # Invalido
        assert format_currency_smart("abc") == "abc"

    def test_try_parse_numeric(self):
        assert _try_parse_numeric("1.234,56") == 1234.56
        assert _try_parse_numeric("1,234.56") == 1234.56
        assert _try_parse_numeric("10") == 10.0
        assert _try_parse_numeric("invalid") is None

    def test_try_parse_date(self):
        # ISO
        assert _try_parse_date("2023-05-23") is not None
        # IT
        assert _try_parse_date("23/05/2023") is not None
        assert _try_parse_date("invalid") is None


class TestFastTableModel:
    @pytest.fixture
    def model(self):
        data = [["B", "2023-01-01", 100.5], ["A", "2023-01-02", 50.0], ["C", "2022-12-31", 200.0]]
        headers = ["Nome", "Data", "Valore"]
        return FastTableModel(data, headers)

    def test_basic_structure(self, model):
        assert model.rowCount() == 3
        assert model.columnCount() == 3
        assert model.headerData(0, Qt.Orientation.Horizontal) == "Nome"

    def test_data_retrieval(self, model):
        idx = model.index(0, 0)
        assert model.data(idx, Qt.ItemDataRole.DisplayRole) == "B"

        # EditRole deve tornare il dato grezzo
        assert model.data(idx, Qt.ItemDataRole.EditRole) == "B"

    def test_column_formatter(self, model):
        model.set_column_formatter(2, format_currency_smart)
        idx = model.index(0, 2)
        # 100.5 -> "100,50"
        assert model.data(idx, Qt.ItemDataRole.DisplayRole) == "100,50"
        # Deve aver impostato allineamento a destra
        assert model.data(idx, Qt.ItemDataRole.TextAlignmentRole) & Qt.AlignmentFlag.AlignRight

    def test_sort_strings(self, model):
        model.sort(0, Qt.SortOrder.AscendingOrder)
        assert model.data(model.index(0, 0)) == "A"
        assert model.data(model.index(1, 0)) == "B"

        model.sort(0, Qt.SortOrder.DescendingOrder)
        assert model.data(model.index(0, 0)) == "C"

    def test_sort_dates(self, model):
        model.sort(1, Qt.SortOrder.AscendingOrder)
        # 2022-12-31 è il più vecchio
        assert model.data(model.index(0, 1)) == "2022-12-31"

    def test_sort_numbers(self, model):
        model.sort(2, Qt.SortOrder.AscendingOrder)
        # 50.0 è il minimo
        assert model.data(model.index(0, 2)) == "50.0"

    def test_update_data(self, model):
        new_data = [["X", "Y", "Z"]]
        model.update_data(new_data)
        assert model.rowCount() == 1
        assert model.data(model.index(0, 0)) == "X"

    def test_get_raw_row(self, model):
        row = model.get_raw_row(0)
        assert row == ["B", "2023-01-01", 100.5]
        assert model.get_raw_row(99) is None
