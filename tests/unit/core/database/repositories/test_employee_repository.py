import sqlite3
from unittest.mock import MagicMock, patch

import pytest

from src.core.database.repositories.employee_repository import EmployeeRepository
from src.models import EmployeeRecord


class TestEmployeeRepository:
    @pytest.fixture
    def mock_db(self):
        m = MagicMock()
        m.DB_DIPENDENTI = "fake_dip.db"
        return m

    @pytest.fixture
    def repo(self, mock_db):
        return EmployeeRepository(db_manager_instance=mock_db)

    def test_get_all_as_objects(self, repo, mock_db):
        # Simula righe ritornate dal DB
        row = {
            "id_risorsa": 1,
            "cognome": "ROSSI",
            "nome": "MARIO",
            "badge": "B1",
            "codice_fiscale": "CF1",
            "data_assunzione": "2023-01-01",
            "monitoraggio_attivo": 1,
            "data_nascita": "1990-01-01",
        }
        mock_db.execute_query.return_value = [row]

        with patch("src.core.database.repositories.employee_repository.dict", side_effect=lambda x: x):
            results = repo.get_all(active_only=False, as_objects=True)
            assert len(results) == 1
            assert isinstance(results[0], EmployeeRecord)
            assert results[0].cognome == "ROSSI"

    def test_get_all_as_dicts(self, repo, mock_db):
        row = {
            "id_risorsa": 1,
            "cognome": "ROSSI",
            "nome": "MARIO",
            "badge": "B1",
            "codice_fiscale": "CF1",
            "data_assunzione": "2023-01-01",
            "monitoraggio_attivo": 1,
            "data_nascita": "1990-01-01",
        }
        mock_db.execute_query.return_value = [row]

        with patch("src.core.database.repositories.employee_repository.dict", side_effect=lambda x: x):
            results = repo.get_all(active_only=True, as_objects=False)
            assert len(results) == 1
            assert results[0]["cognome"] == "ROSSI"
            assert "WHERE monitoraggio_attivo = 1" in mock_db.execute_query.call_args[0][1]

    def test_get_all_fallback(self, repo, mock_db):
        # Simula errore colonna mancante (OperationalError)
        mock_db.execute_query.side_effect = [
            sqlite3.OperationalError("no such column: monitoraggio_attivo"),
            [(1, "ROSSI", "MARIO", "B1", "CF1", "2023-01-01")],  # Fallback query result
        ]

        results = repo.get_all(as_objects=True)
        assert len(results) == 1
        assert results[0].cognome == "ROSSI"
        assert results[0].monitoraggio_attivo == 1

    def test_get_filtered(self, repo, mock_db):
        row = {"id_risorsa": 1, "cognome": "ROSSI"}
        mock_db.execute_query.return_value = [row]

        with patch("src.core.database.repositories.employee_repository.dict", side_effect=lambda x: x):
            results = repo.get_filtered(search_text="mario", active_only=True, as_objects=True)
            assert len(results) == 1
            assert "WHERE 1=1" in mock_db.execute_query.call_args[0][1]
            assert "AND monitoraggio_attivo = 1" in mock_db.execute_query.call_args[0][1]

    def test_get_by_badge_found(self, repo, mock_db):
        row = {"id_risorsa": 1, "cognome": "ROSSI"}
        mock_db.execute_query.return_value = [row]

        with patch("src.core.database.repositories.employee_repository.dict", side_effect=lambda x: x):
            res = repo.get_by_badge("B1")
            assert res.cognome == "ROSSI"

    def test_get_by_badge_not_found(self, repo, mock_db):
        mock_db.execute_query.return_value = []
        assert repo.get_by_badge("B999") is None

    def test_save_insert(self, repo, mock_db):
        emp = EmployeeRecord(cognome="Verdi", nome="Gius")
        res = repo.save(emp)
        assert res is True
        assert "INSERT INTO dipendenti" in mock_db.execute_query.call_args[0][1]
        params = mock_db.execute_query.call_args[0][2]
        assert "VERDI" in params  # Uppercase

    def test_save_update(self, repo, mock_db):
        emp = EmployeeRecord(id_risorsa=10, cognome="Rossi", nome="M")
        res = repo.save(emp)
        assert res is True
        assert "UPDATE dipendenti" in mock_db.execute_query.call_args[0][1]
        assert "WHERE id_risorsa = ?" in mock_db.execute_query.call_args[0][1]

    def test_toggle_monitoring(self, repo, mock_db):
        repo.toggle_monitoring(10, False)
        args = mock_db.execute_query.call_args[0][2]
        assert args == (0, 10)

    def test_get_all_exception(self, repo, mock_db):
        mock_db.execute_query.side_effect = Exception("Generic fail")
        assert repo.get_all() == []
