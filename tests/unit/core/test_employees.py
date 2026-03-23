import sqlite3
from unittest.mock import patch

import pytest

from src.core.employees import EmployeeManager


class TestEmployeeManager:
    @pytest.fixture
    def mock_db(self):
        with patch("src.core.employees.db_manager") as mock:
            # Mock DB paths
            mock.DB_DIPENDENTI = "mock_dipendenti.db"
            yield mock

    @pytest.fixture
    def manager(self, mock_db):
        return EmployeeManager()

    def test_get_all_employees_success(self, manager, mock_db):
        """Verifica il recupero di tutti i dipendenti con schema moderno."""
        mock_db.execute_query.return_value = [
            (1, "Rossi", "Mario", "B001", "RSSMRA80", "2020-01-01", 1),
            (2, "Verdi", "Luigi", "B002", "VRDLGU85", "2021-05-10", 0),
        ]

        employees = manager.get_all_employees(active_only=False)

        assert len(employees) == 2
        assert employees[0]["cognome"] == "Rossi"
        assert employees[0]["monitoraggio_attivo"] == 1
        assert employees[1]["monitoraggio_attivo"] == 0

        # Verifica la query
        args = mock_db.execute_query.call_args
        assert "WHERE monitoraggio_attivo = 1" not in args[0][1]

    def test_get_all_employees_active_only(self, manager, mock_db):
        """Verifica il filtro sui dipendenti attivi."""
        manager.get_all_employees(active_only=True)
        args = mock_db.execute_query.call_args
        assert "WHERE monitoraggio_attivo = 1" in args[0][1]

    def test_get_all_employees_fallback_schema(self, manager, mock_db):
        """Verifica il fallback se la colonna monitoraggio_attivo non esiste."""
        # Primo tentativo fallisce (OperationalError: no such column)
        mock_db.execute_query.side_effect = [
            sqlite3.OperationalError("no such column: monitoraggio_attivo"),
            [(1, "Rossi", "Mario", "B001", "RSSMRA80", "2020-01-01")],  # Fallback data
        ]

        employees = manager.get_all_employees()

        assert len(employees) == 1
        assert employees[0]["cognome"] == "Rossi"
        # Deve essere 1 di default nel fallback
        assert employees[0]["monitoraggio_attivo"] == 1
        assert mock_db.execute_query.call_count == 2

    def test_get_employee_by_badge(self, manager, mock_db):
        """Verifica la ricerca per badge."""
        mock_db.execute_query.return_value = [("row_data")]
        res = manager.get_employee_by_badge("B123")
        assert res == "row_data"
        mock_db.execute_query.assert_called_with(
            mock_db.DB_DIPENDENTI, "SELECT * FROM dipendenti WHERE badge = ?", ("B123",)
        )

    def test_add_employee_success(self, manager, mock_db):
        """Verifica l'aggiunta di un dipendente con normalizzazione nomi."""
        emp_data = {"cognome": "rossi", "nome": "mario", "badge": "B999", "codice_fiscale": "rssmra"}

        success = manager.add_employee(emp_data)
        assert success is True

        # Verifica normalizzazione UPPER
        args = mock_db.execute_query.call_args
        params = args[0][2]
        assert params[1] == "ROSSI"
        assert params[2] == "MARIO"
        assert params[4] == "RSSMRA"

    def test_add_employee_integrity_error(self, manager, mock_db):
        """Verifica la gestione di errori di integrità (es. badge duplicato)."""
        mock_db.execute_query.side_effect = sqlite3.IntegrityError("UNIQUE constraint failed")
        emp_data = {"cognome": "X", "nome": "Y", "badge": "DUP"}

        success = manager.add_employee(emp_data)
        assert success is False

    def test_update_employee(self, manager, mock_db):
        """Verifica l'aggiornamento dinamico dei campi."""
        data = {"nome": "Paolo", "monitoraggio_attivo": 0}
        success = manager.update_employee(10, data)

        assert success is True
        args = mock_db.execute_query.call_args
        query = args[0][1]
        params = args[0][2]

        assert "nome = ?" in query
        assert "monitoraggio_attivo = ?" in query
        assert params == ("Paolo", 0, 10)

    def test_import_from_csv_new_and_update(self, manager, mock_db, tmp_path):
        """Verifica l'importazione mista (nuovi + aggiornamenti) da CSV."""
        csv_file = tmp_path / "test_emps.csv"
        csv_file.write_text(
            "ID;Cognome;Nome;Badge\n1;Rossi;Mario;B001\n2;Verdi;Luigi;B002\n", encoding="utf-8-sig"
        )

        # Mocking per distinguere esistenti e nuovi
        # ID 1 esiste, ID 2 no
        mock_db.execute_query.side_effect = [
            [(1,)],  # Check ID 1
            None,  # UPDATE ID 1 (add_employee called if not existing, but here we mock differently)
            [],  # Check ID 2 (not found)
            None,  # INSERT ID 2
        ]

        with patch("src.core.sync_tracker.SyncTracker.update_status") as mock_sync:
            count = manager.import_from_csv(str(csv_file))
            assert count == 2
            assert mock_sync.called
