from unittest.mock import MagicMock

import pytest

from src.core.database.repositories.oda_repository import OdaRepository


@pytest.fixture
def mock_db():
    return MagicMock()


def test_oda_repository_initialization(mock_db):
    repo = OdaRepository(db_manager_instance=mock_db)
    assert repo.db == mock_db


def test_oda_repository_get_all_empty(mock_db):
    # Mocking the database file not existing
    mock_db.DB_STORICO_ODA = MagicMock()
    mock_db.DB_STORICO_ODA.exists.return_value = False

    repo = OdaRepository(db_manager_instance=mock_db)
    res = repo.get_all()
    assert res == []
