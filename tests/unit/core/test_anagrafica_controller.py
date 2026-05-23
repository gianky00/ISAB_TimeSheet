from unittest.mock import patch

import pytest

from src.core.dipendenti.anagrafica_controller import AnagraficaController
from src.core.dipendenti.employee_dto import EmployeeDTO
from src.models.employee import EmployeeRecord


class TestAnagraficaController:
    @pytest.fixture
    def controller(self):
        with patch("src.core.dipendenti.anagrafica_controller.EmployeeRepository") as mock_repo:
            ctrl = AnagraficaController()
            ctrl.repository = mock_repo
            yield ctrl

    def test_get_employees_search_terms_logic(self, controller):
        """Verifica che la ricerca per più termini."""
        controller.repository.get_filtered.return_value = []

        controller.get_employees("Rossi Mario")

        controller.repository.get_filtered.assert_called_once_with(search_text="Rossi Mario", as_objects=True)

    @patch("src.core.dipendenti.anagrafica_controller.db_manager")
    def test_toggle_monitoring_error_handling(self, mock_db, controller):
        """Verifica che un errore nel repository ritorni False."""
        controller.repository.toggle_monitoring.side_effect = Exception("DB Error")

        success = controller.toggle_monitoring("R001", True)
        assert success is False

    @patch("src.core.dipendenti.anagrafica_controller.compute_employee_status")
    @patch("src.core.dipendenti.anagrafica_controller.db_manager")
    def test_process_rows_full_cycle(self, mock_db, mock_compute, controller):
        """Testa l'intero ciclo di trasformazione in DTO e conteggio."""
        # V9.4: compute_employee_status returns 6 elements:
        # diff_days, cf_warning, last_date, cog_val, nom_val, cf_val
        mock_compute.return_value = (5, False, "01/01/2024", "ROSSI", "MARIO", "RSSMRA")
        mock_db.execute_query.return_value = []  # Timbrature

        record = EmployeeRecord(
            id_risorsa=1,
            cognome="ROSSI",
            nome="MARIO",
            data_nascita="1980",
            badge="B001",
            data_assunzione="2020",
            codice_fiscale="RSSMRA80",
            monitoraggio_attivo=1,
        )

        raw_rows = [record]

        dtos, counts = controller.process_rows(raw_rows)

        assert len(dtos) == 1
        assert isinstance(dtos[0], EmployeeDTO)
        # Verify id_risorsa as string (DTO normalization)
        assert str(dtos[0].id_risorsa) == "1"
        assert counts["ok"] == 1
        assert counts["warning"] == 0
