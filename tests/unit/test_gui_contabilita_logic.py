from unittest.mock import patch

import pytest

from src.gui.contabilita_panel import ContabilitaYearTab, GiornaliereYearTab


class TestContabilitaTableLogic:

    @pytest.fixture
    def app(self, qapp):
        return qapp

    @patch("src.gui.contabilita_panel.ContabilitaManager.get_data_by_year")
    def test_contabilita_year_tab_totals(self, mock_get_data, app, qtbot):
        # Mock data: [visible cols...] + [indirizzo, nomefile]
        # visible cols: data, mese, n_prev, totale, attivita, tcl, odc, stato, tipologia, ore, resa, note
        mock_get_data.return_value = [
            ["2023-01-01", "Gen", "1", "1000", "A", "T", "O", "S", "T", "10", "100", "Note", "path", "file"]
        ]

        tab = ContabilitaYearTab(2023)
        qtbot.addWidget(tab)

        # Verify totals row added (data row + totals row = 2 rows)
        assert tab.table.rowCount() == 2

        # Check totals values (column 3 is Totale, column 9 is Ore)
        assert "1.000" in tab.table.item(1, 3).text()
        assert "10" in tab.table.item(1, 9).text()

    @patch("src.gui.contabilita_panel.ContabilitaManager.get_giornaliere_by_year")
    def test_giornaliere_year_tab_format(self, mock_get_data, app, qtbot):
        # Mock data: data, personale, tcl, descrizione, n_prev, odc, pdl, inizio, fine, ore, nome_file
        mock_get_data.return_value = [
            ["2023-01-01", "Mario", "T", "D", "1", "O", "P", "08", "17", 8.5, "file.xlsx"]
        ]

        tab = GiornaliereYearTab(2023)
        qtbot.addWidget(tab)

        # Check formatting of ore (index 9)
        assert tab.table.item(0, 9).text() == "8,5"
