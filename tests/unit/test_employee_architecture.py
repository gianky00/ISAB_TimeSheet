from unittest.mock import MagicMock

import pytest

from src.core.database.repositories.employee_repository import EmployeeRepository
from src.models import EmployeeRecord


class TestEmployeeArchitecture:
    @pytest.fixture
    def mock_db_manager(self):
        mock = MagicMock()
        mock.DB_DIPENDENTI = "mock_db"
        return mock

    def test_repository_get_all(self, mock_db_manager):
        repo = EmployeeRepository(db_manager_instance=mock_db_manager)

        # Mock row that matches EmployeeRecord fields
        mock_row = {
            "id_risorsa": 1, "cognome": "ROSSI", "nome": "MARIO",
            "badge": "123", "codice_fiscale": "RSSMRA...",
            "data_assunzione": "2024-01-01", "monitoraggio_attivo": 1,
            "data_nascita": "1990-01-01"
        }

        mock_db_manager.execute_query.return_value = [mock_row]

        records = repo.get_all(as_objects=True)
        assert len(records) == 1
        assert isinstance(records[0], EmployeeRecord)
        assert records[0].cognome == "ROSSI"

    def test_repository_save_insert(self, mock_db_manager):
        repo = EmployeeRepository(db_manager_instance=mock_db_manager)
        emp = EmployeeRecord(
            id_risorsa=None, cognome="VERDI", nome="LUIGI",
            badge="456", codice_fiscale="VRDLGU...",
            data_assunzione="2024-02-01"
        )

        success = repo.save(emp)
        assert success is True
        assert mock_db_manager.execute_query.called
