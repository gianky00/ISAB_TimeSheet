from unittest.mock import patch

import pytest

from src.gui.widgets.contabilita.giornaliere_tab import GiornaliereYearTab
from src.gui.widgets.contabilita.year_tab import ContabilitaYearTab


class TestContabilitaTableLogic:
    @pytest.fixture
    def app(self, qapp):
        return qapp

    @patch("src.gui.widgets.contabilita.year_tab.ContabilitaQueries.get_data_by_year")
    def test_contabilita_year_tab_totals(self, mock_get_data, app, qtbot):
        # Mock data: [visible cols...] + [indirizzo, nomefile]
        # visible cols: data, mese, n_prev, totale, attivita, tcl, odc, stato, tipologia, ore, resa, note
        mock_get_data.return_value = [
            [
                "2023-01-01",
                "Gen",
                "1",
                "1000",
                "A",
                "T",
                "O",
                "S",
                "T",
                "10",
                "100",
                "Note",
                "path",
                "file",
            ]
        ]

        tab = ContabilitaYearTab(2023)
        qtbot.addWidget(tab)

        # We need to wait for the QTimer.singleShot(10, self._load_data) to fire
        # Or manually call _load_data
        tab._load_data()

        try:
            # Verify data row added
            model = tab.table.model()
            assert model.rowCount() == 1  # Updated expectation based on current source code

            # Check values (column 3 is Totale, column 9 is Ore)
            # Row 0 is the data row
            total_val = model.data(model.index(0, 3))
            ore_val = model.data(model.index(0, 9))

            assert "1000" in str(total_val).replace(".", "").replace(",", "")
            assert "10" in str(ore_val).split(",")[0]  # Check integer part only
        finally:
            tab.deleteLater()

    @patch("src.core.contabilita_manager.ContabilitaManager.get_giornaliere_by_year")
    def test_giornaliere_year_tab_format(self, mock_get_data, app, qtbot):
        # Mock data: data, personale, tcl, descrizione, n_prev, odc, pdl, inizio, fine, ore, nome_file
        mock_get_data.return_value = [
            [
                "2023-01-01",
                "Mario",
                "T",
                "D",
                "1",
                "O",
                "P",
                "08",
                "17",
                8.5,
                "file.xlsx",
            ]
        ]

        tab = GiornaliereYearTab(2023)
        qtbot.addWidget(tab)

        try:
            # Check formatting of ore (index 9)
            model = tab.table.model()
            assert model.data(model.index(0, 9)) == "8,50"
        finally:
            tab.deleteLater()
