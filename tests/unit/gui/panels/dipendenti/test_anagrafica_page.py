from unittest.mock import MagicMock, patch

import pytest

from src.gui.panels.dipendenti.pages.anagrafica_page import AnagraficaPage


class MockAnagraficaController:
    def __init__(self):
        self.get_employees = MagicMock(return_value=[])
        self.process_rows = MagicMock(return_value=([], {"totale": 0}))
        self.get_last_isab_access = MagicMock(return_value={})
        self.toggle_monitoring = MagicMock(return_value=True)


class TestAnagraficaPage:
    @pytest.fixture
    def controller(self):
        return MockAnagraficaController()

    @pytest.fixture
    def page(self, controller, qtbot):
        with patch("src.gui.panels.dipendenti.pages.anagrafica_page.SyncTracker") as mock_st:
            mock_st.get_formatted_status.return_value = "TestStatus"
            p = AnagraficaPage(controller)
            qtbot.addWidget(p)
            return p

    def test_initialization(self, page):
        """Verifica che la pagina si inizializzi correttamente."""
        assert page.controller is not None
        assert page.model is not None
        assert len(page.headers) > 0

    def test_refresh_data_call(self, page, controller):
        """Verifica che refresh_data chiami il controller."""
        page.refresh_data()
        assert controller.get_employees.called
        assert controller.process_rows.called

    def test_on_selection_changed(self, page, controller, qtbot):
        """Verifica che la selezione di una riga aggiorni la detail_view."""
        # Mock dei dati del modello
        row_data = [
            "10",
            "ID1",
            "Rossi",
            "Mario",
            "RSSMRA",
            "B01",
            "2020-01-01",
            "1990-01-01",
            "2023-01-01",
            "Rossi",
        ]
        page.model.get_raw_row = MagicMock(return_value=row_data)

        with patch.object(page.detail_view, "update_data") as mock_update:
            page._on_selection_changed(0)
            assert mock_update.called
            # Verifica che le chiavi attese siano presenti nei dettagli
            details = mock_update.call_args[0][0]
            assert "Cognome" in details
            assert details["Cognome"] == "Rossi"
