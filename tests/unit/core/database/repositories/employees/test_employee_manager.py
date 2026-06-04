from unittest.mock import MagicMock

import pytest

from src.application.services.employees import EmployeeManager
from src.domain import EmployeeRecord


@pytest.fixture
def mock_db():
    return MagicMock()


def test_employee_manager_initialization(mock_db):
    manager = EmployeeManager(db_manager_instance=mock_db)
    assert manager.db == mock_db


def test_get_all_employees(mock_db):
    manager = EmployeeManager(db_manager_instance=mock_db)
    # Mocking repository
    manager._repo = MagicMock()
    manager._repo.get_all.return_value = [{"cognome": "ROSSI"}]

    emps = manager.get_all_employees()
    assert len(emps) == 1
    assert emps[0]["cognome"] == "ROSSI"


def test_add_employee(mock_db):
    manager = EmployeeManager(db_manager_instance=mock_db)
    manager._repo = MagicMock()
    manager._repo.save.return_value = True

    data = {
        "id_risorsa": 1,
        "cognome": "Rossi",
        "nome": "Mario",
        "badge": "123456",
        "codice_fiscale": "RSSMRA80A01H501U",
    }

    success = manager.add_employee(data)
    assert success is True
    manager._repo.save.assert_called_once()
    # Verifica che il record sia stato creato correttamente
    saved_emp = manager._repo.save.call_args[0][0]
    assert isinstance(saved_emp, EmployeeRecord)
    assert saved_emp.cognome == "ROSSI"
