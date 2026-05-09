from PySide6.QtCore import Qt

from src.gui.formatters import FastTableModel, format_currency_smart


class TestFormatters:
    def test_format_currency_smart_various_inputs(self):
        """Testa la formattazione smart per valuta e numeri."""
        # Numeri puri
        assert format_currency_smart(1200) == "1.200"
        assert format_currency_smart(1200.5) == "1.200,50"
        assert format_currency_smart(1200.0000001) == "1.200"

        # Stringhe IT
        assert format_currency_smart("1.234,56") == "1.234,56"
        assert format_currency_smart("€ 1.234,56") == "1.234,56"

        # Stringhe EN o sporche
        assert format_currency_smart("1,234.56") == "1.234,56"
        assert format_currency_smart("not a number") == "not a number"
        assert format_currency_smart(None) == ""


class TestFastTableModel:
    def test_sorting_mixed_types(self):
        """Verifica che l'ordinamento gestisca tipi misti senza crashare."""
        headers = ["Col1"]
        data = [[None], [10], ["2"], ["5,5"], ["A"]]
        model = FastTableModel(data, headers)

        # Ascendente: None -> Numeri -> Stringhe
        model.sort(0, Qt.SortOrder.AscendingOrder)
        sorted_data = [model.data(model.index(i, 0), Qt.ItemDataRole.EditRole) for i in range(5)]

        # La logica sort_key attuale mette None a prioritÃ  0, numeri a 1, stringhe a 2
        assert sorted_data[0] is None
        assert sorted_data[1] == 10 or sorted_data[1] == "2"  # Dipende da parsing
        # Nota: "2" viene parsato come float 2.0 (priorità 1), "A" come stringa (priorità 2)
        assert sorted_data[-1] == "A"

    def test_sorting_dates(self):
        """Verifica l'ordinamento corretto delle date in formato stringa."""
        headers = ["Data"]
        data = [["21/03/2026"], ["01/01/2024"], ["15/06/2025"]]
        model = FastTableModel(data, headers)

        model.sort(0, Qt.SortOrder.AscendingOrder)
        assert model._data[0][0] == "01/01/2024"
        assert model._data[1][0] == "15/06/2025"
        assert model._data[2][0] == "21/03/2026"

    def test_metadata_sync_on_sort(self):
        """Verifica che i metadati rimangano allineati alle righe dopo il sort."""
        headers = ["Val"]
        data = [["B"], ["A"], ["C"]]
        meta = [{"id": 2}, {"id": 1}, {"id": 3}]
        model = FastTableModel(data, headers, metadata=meta)

        model.sort(0, Qt.SortOrder.AscendingOrder)

        # Valore in riga 0 deve essere "A", e il suo meta id deve essere 1
        assert model._data[0][0] == "A"
        assert model._metadata[0]["id"] == 1

        # Verifica tramite UserRole
        assert model.data(model.index(0, 0), Qt.ItemDataRole.UserRole)["id"] == 1
