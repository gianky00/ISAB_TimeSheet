import sqlite3
from unittest.mock import MagicMock

import pytest

from src.core.database.repositories.employee_repository import EmployeeRepository


@pytest.fixture
def mock_db_manager(tmp_path):
    # Crea un DB temporaneo per dipendenti
    db_path = tmp_path / "dipendenti.db"
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE dipendenti (
            id_risorsa TEXT, cognome TEXT, nome TEXT, badge TEXT,
            codice_fiscale TEXT, data_assunzione TEXT,
            monitoraggio_attivo INTEGER, data_nascita TEXT
        )
    """)
    conn.execute(
        "INSERT INTO dipendenti VALUES ('1', 'Rossi', 'Mario', 'B01', 'RSSMRA...', '2020-01-01', 1, '1990-01-01')"
    )
    conn.commit()
    conn.close()

    db_mgr = MagicMock()
    db_mgr.DB_DIPENDENTI = db_path
    db_mgr.execute_query = lambda db_path, query, params=(): [
        {
            "id_risorsa": "1",
            "cognome": "Rossi",
            "nome": "Mario",
            "badge": "B01",
            "codice_fiscale": "RSSMRA...",
            "data_assunzione": "2020-01-01",
            "monitoraggio_attivo": 1,
            "data_nascita": "1990-01-01",
        }
    ]
    return db_mgr


def test_get_all(mock_db_manager):
    repo = EmployeeRepository(db_manager_instance=mock_db_manager)
    employees = repo.get_all(active_only=False, as_objects=False)
    assert len(employees) > 0
    assert employees[0]["cognome"] == "Rossi"


def test_get_filtered(mock_db_manager):
    repo = EmployeeRepository(db_manager_instance=mock_db_manager)
    employees = repo.get_filtered(search_text="Rossi", as_objects=False)
    assert len(employees) > 0
    assert employees[0]["cognome"] == "Rossi"
