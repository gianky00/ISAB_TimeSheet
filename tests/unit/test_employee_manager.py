from unittest.mock import patch

import pytest

from src.core.employees import EmployeeManager


class TestEmployeeManager:
    @pytest.fixture
    def manager(self):
        with patch("src.core.employees.db_manager") as mock_db:
            em = EmployeeManager()
            em.db = mock_db
            yield em

    def test_get_all_employees_active_only(self, manager):
        manager.db.execute_query.return_value = [
            (1, "ROSSI", "MARIO", "001", "RSSMRA80A01H501Z", "2020-01-01", 1),
            (2, "VERDI", "LUIGI", "002", "VRDLGU75B02H501Y", "2019-05-15", 1),
        ]

        employees = manager.get_all_employees(active_only=True)

        assert len(employees) == 2
        assert employees[0]["cognome"] == "ROSSI"
        assert employees[0]["monitoraggio_attivo"] == 1

    def test_get_all_employees_fallback_schema(self, manager):
        # First call fails (old schema), second succeeds
        import sqlite3

        manager.db.execute_query.side_effect = [
            sqlite3.OperationalError("no such column"),
            [(1, "BIANCHI", "ANNA", "003", "BNCNNA85C03H501X", "2021-03-20")],
        ]

        employees = manager.get_all_employees()

        assert len(employees) == 1
        assert employees[0]["monitoraggio_attivo"] == 1  # Default value

    def test_get_employee_by_badge(self, manager):
        manager.db.execute_query.return_value = [(1, "ROSSI", "MARIO", "001", "CF123", "2020-01-01", 1)]

        result = manager.get_employee_by_badge("001")

        assert result is not None

    def test_get_employee_by_badge_not_found(self, manager):
        manager.db.execute_query.return_value = []

        result = manager.get_employee_by_badge("999")

        assert result is None

    def test_add_employee(self, manager):
        manager.db.execute_query.return_value = None

        data = {
            "cognome": "Neri",
            "nome": "Paolo",
            "badge": "004",
            "codice_fiscale": "NRIPLP90D04H501W",
        }

        result = manager.add_employee(data)

        assert result is True
        manager.db.execute_query.assert_called_once()

    def test_add_employee_integrity_error(self, manager):
        import sqlite3

        manager.db.execute_query.side_effect = sqlite3.IntegrityError("UNIQUE constraint")

        data = {"cognome": "Duplicate", "nome": "User"}

        result = manager.add_employee(data)

        assert result is False

    def test_update_employee(self, manager):
        manager.db.execute_query.return_value = None

        result = manager.update_employee(1, {"cognome": "ROSSI UPDATED", "nome": "MARIO"})

        assert result is True

    @patch("builtins.open")
    @patch("src.core.sync_tracker.SyncTracker.update_status")
    def test_import_from_csv(self, mock_tracker, mock_open, manager, tmp_path):
        csv_content = (
            "id_risorsa;Cognome;Nome;Badge;Codice_fiscale;Data_assunzione\n1;ROSSI;MARIO;001;CF001;2020-01-01"
        )

        csv_file = tmp_path / "dipendenti.csv"
        csv_file.write_text(csv_content, encoding="utf-8-sig")

        # Mock the file operations
        manager.db.execute_query.return_value = []  # No existing employee

        with patch.object(manager, "add_employee", return_value=True):
            manager.import_from_csv(str(csv_file))

        mock_tracker.assert_called_once()
