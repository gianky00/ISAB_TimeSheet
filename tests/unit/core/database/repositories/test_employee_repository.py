import sqlite3
from unittest.mock import MagicMock

import pytest

from src.core.database.repositories.employee_repository import EmployeeRepository
from src.models import EmployeeRecord


@pytest.fixture
def mock_db_manager():
    db = MagicMock()
    db.DB_DIPENDENTI = "test_db"
    return db


@pytest.fixture
def repo(mock_db_manager):
    return EmployeeRepository(db_manager_instance=mock_db_manager)


def test_get_all_success(repo, mock_db_manager):
    # Mocking rows
    mock_db_manager.execute_query.return_value = [
        {
            "id_risorsa": 1,
            "cognome": "Rossi",
            "nome": "Mario",
            "badge": "123",
            "codice_fiscale": "RSSMRA",
            "data_assunzione": "2020-01-01",
            "monitoraggio_attivo": 1,
            "data_nascita": "1980-01-01",
        }
    ]

    results = repo.get_all(active_only=True, as_objects=True)
    assert len(results) == 1
    assert isinstance(results[0], EmployeeRecord)
    assert results[0].cognome == "Rossi"


def test_get_all_as_dict(repo, mock_db_manager):
    mock_db_manager.execute_query.return_value = [
        {
            "id_risorsa": 1,
            "cognome": "Rossi",
            "nome": "Mario",
            "badge": "123",
            "codice_fiscale": "RSSMRA",
            "data_assunzione": "2020-01-01",
            "monitoraggio_attivo": 1,
            "data_nascita": "1980-01-01",
        }
    ]

    results = repo.get_all(active_only=False, as_objects=False)
    assert len(results) == 1
    assert isinstance(results[0], dict)
    assert results[0]["cognome"] == "Rossi"


def test_get_all_tuple_fallback(repo, mock_db_manager):
    # Mocking tuple rows
    mock_db_manager.execute_query.return_value = [
        (1, "Rossi", "Mario", "123", "RSSMRA", "2020-01-01", 1, "1980-01-01")
    ]

    results = repo.get_all(active_only=True, as_objects=True)
    assert len(results) == 1
    assert isinstance(results[0], EmployeeRecord)


def test_get_all_operational_error(repo, mock_db_manager):
    mock_db_manager.execute_query.side_effect = [
        sqlite3.OperationalError,
        [(1, "Rossi", "Mario", "123", "RSSMRA", "2020-01-01")],
    ]

    results = repo.get_all(active_only=True, as_objects=True)
    assert len(results) == 1
    assert results[0].cognome == "Rossi"
    assert results[0].monitoraggio_attivo == 1


def test_get_all_generic_error(repo, mock_db_manager):
    mock_db_manager.execute_query.side_effect = Exception("Generic Error")

    results = repo.get_all()
    assert results == []


def test_fallback_get_all_as_dict(repo, mock_db_manager):
    mock_db_manager.execute_query.return_value = [(1, "Rossi", "Mario", "123", "RSSMRA", "2020-01-01")]
    results = repo._fallback_get_all(as_objects=False)
    assert len(results) == 1
    assert results[0]["cognome"] == "Rossi"


def test_get_filtered_success(repo, mock_db_manager):
    mock_db_manager.execute_query.return_value = [
        {
            "id_risorsa": 1,
            "cognome": "Rossi",
            "nome": "Mario",
            "badge": "123",
            "codice_fiscale": "RSSMRA",
            "data_assunzione": "2020-01-01",
            "monitoraggio_attivo": 1,
            "data_nascita": "1980-01-01",
        }
    ]

    results = repo.get_filtered(search_text="Rossi", active_only=True, as_objects=True)
    assert len(results) == 1
    assert isinstance(results[0], EmployeeRecord)


def test_get_filtered_as_dict(repo, mock_db_manager):
    mock_db_manager.execute_query.return_value = [
        {
            "id_risorsa": 1,
            "cognome": "Rossi",
            "nome": "Mario",
            "badge": "123",
            "codice_fiscale": "RSSMRA",
            "data_assunzione": "2020-01-01",
            "monitoraggio_attivo": 1,
            "data_nascita": "1980-01-01",
        }
    ]

    results = repo.get_filtered(search_text="Rossi", active_only=False, as_objects=False)
    assert len(results) == 1
    assert isinstance(results[0], dict)


def test_get_filtered_error(repo, mock_db_manager):
    mock_db_manager.execute_query.side_effect = Exception("DB Error")
    results = repo.get_filtered(search_text="Rossi")
    assert results == []


def test_get_by_badge_success(repo, mock_db_manager):
    mock_db_manager.execute_query.return_value = [
        {
            "id_risorsa": 1,
            "cognome": "Rossi",
            "nome": "Mario",
            "badge": "123",
            "codice_fiscale": "RSSMRA",
            "data_assunzione": "2020-01-01",
            "monitoraggio_attivo": 1,
            "data_nascita": "1980-01-01",
        }
    ]

    result = repo.get_by_badge("123")
    assert isinstance(result, EmployeeRecord)
    assert result.badge == "123"


def test_get_by_badge_not_found(repo, mock_db_manager):
    mock_db_manager.execute_query.return_value = []

    result = repo.get_by_badge("123")
    assert result is None


def test_get_by_badge_error(repo, mock_db_manager):
    mock_db_manager.execute_query.side_effect = Exception("DB Error")
    result = repo.get_by_badge("123")
    assert result is None


def test_save_insert(repo, mock_db_manager):
    employee = EmployeeRecord(cognome="Rossi", nome="Mario", badge="123", codice_fiscale="RSSMRA")

    assert repo.save(employee) is True
    assert mock_db_manager.execute_query.call_count == 1
    args, _kwargs = mock_db_manager.execute_query.call_args
    assert "INSERT INTO dipendenti" in args[1]
    assert args[2][0] == "ROSSI"


def test_save_insert_error(repo, mock_db_manager):
    employee = EmployeeRecord(cognome="Rossi", nome="Mario", badge="123", codice_fiscale="RSSMRA")
    mock_db_manager.execute_query.side_effect = Exception("DB Error")

    assert repo.save(employee) is False


def test_save_update(repo, mock_db_manager):
    employee = EmployeeRecord(
        id_risorsa=1, cognome="Rossi", nome="Mario", badge="123", codice_fiscale="RSSMRA"
    )

    assert repo.save(employee) is True
    assert mock_db_manager.execute_query.call_count == 1
    args, _kwargs = mock_db_manager.execute_query.call_args
    assert "UPDATE dipendenti SET" in args[1]
    assert args[2][-1] == 1  # id_risorsa at the end


def test_save_update_error(repo, mock_db_manager):
    employee = EmployeeRecord(
        id_risorsa=1, cognome="Rossi", nome="Mario", badge="123", codice_fiscale="RSSMRA"
    )
    mock_db_manager.execute_query.side_effect = Exception("DB Error")

    assert repo.save(employee) is False


def test_toggle_monitoring_success(repo, mock_db_manager):
    assert repo.toggle_monitoring(1, True) is True
    args, _kwargs = mock_db_manager.execute_query.call_args
    assert args[2] == (1, 1)

    assert repo.toggle_monitoring(1, False) is True
    args, _kwargs = mock_db_manager.execute_query.call_args
    assert args[2] == (0, 1)


def test_toggle_monitoring_error(repo, mock_db_manager):
    mock_db_manager.execute_query.side_effect = Exception("DB Error")
    assert repo.toggle_monitoring(1, True) is False
