from unittest.mock import patch

from src.core.dipendenti.anagrafica_controller import AnagraficaController
from src.core.dipendenti.employee_dto import EmployeeDTO


class TestAnagraficaController:
    @patch("src.core.dipendenti.anagrafica_controller.db_manager")
    def test_get_employees_search_terms_logic(self, mock_db):
        """Verifica che la ricerca per più termini usi l'operatore AND correttamente."""
        # Setup: simula risposta DB
        mock_db.execute_query.return_value = []
        mock_db.DB_DIPENDENTI = "dip.db"

        # Esecuzione: cerchiamo due termini
        AnagraficaController.get_employees("Rossi Mario")

        # Verifica query prodotta
        assert mock_db.execute_query.called
        query = mock_db.execute_query.call_args[0][1]
        params = mock_db.execute_query.call_args[0][2]

        # Ogni termine deve apparire nella query (AND) e avere i suoi parametri (4 per termine)
        assert query.count("AND (cognome LIKE ?") == 2
        assert len(params) == 8
        assert "%rossi%" in params
        assert "%mario%" in params

    @patch("src.core.dipendenti.anagrafica_controller.db_manager")
    def test_toggle_monitoring_error_handling(self, mock_db):
        """Verifica che un errore nel DB ritorni False invece di crashare."""
        mock_db.execute_query.side_effect = Exception("Write Lock")
        mock_db.DB_DIPENDENTI = "dip.db"

        success = AnagraficaController.toggle_monitoring("R001", True)
        assert success is False

    @patch("src.core.dipendenti.anagrafica_controller.db_manager")
    @patch("src.core.dipendenti.anagrafica_controller.compute_employee_status")
    def test_process_rows_full_cycle(self, mock_compute, mock_db):
        """Testa l'intero ciclo di trasformazione in DTO e conteggio."""
        # Mocking compute_employee_status: (diff_days, cf_warning, ...)
        mock_compute.return_value = (5, False, None, None, None)
        mock_db.execute_query.return_value = []  # Timbrature

        raw_rows = [("R001", "ROSSI", "MARIO", "1980", "B001", "2020", None, "RSSMRA80", 1)]

        dtos, counts = AnagraficaController.process_rows(raw_rows)

        assert len(dtos) == 1
        assert isinstance(dtos[0], EmployeeDTO)
        assert dtos[0].id_risorsa == "R001"
        assert counts["ok"] == 1
        assert counts["warning"] == 0
