from unittest.mock import MagicMock, patch

import pytest

from src.core.database.repositories.oda_repository import OdaRepository
from src.models import OdaRecord


class TestOdaRepository:
    @pytest.fixture
    def mock_db(self):
        m = MagicMock()
        m.DB_STORICO_ODA = MagicMock()
        m.DB_STORICO_ODA.exists.return_value = True
        return m

    @pytest.fixture
    def repo(self, mock_db):
        return OdaRepository(db_manager_instance=mock_db)

    @patch("src.core.database.repositories.oda_repository.dict", side_effect=lambda x: x)
    def test_get_all_as_objects(self, mock_dict, repo, mock_db):
        mock_conn = MagicMock()
        mock_db.get_connection.return_value.__enter__.return_value = mock_conn

        # Setup mock cursor
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        # Setup riga con campi OdaRecord
        fields = dict.fromkeys(OdaRecord.__dataclass_fields__, "")
        fields.update({"oda": "100", "pos_oda": "10"})

        mock_cursor.fetchall.return_value = [fields]

        results = repo.get_all(as_objects=True)
        assert len(results) == 1
        assert results[0].oda == "100"

    def test_get_all_filtered_date(self, repo, mock_db):
        mock_conn = MagicMock()
        mock_db.get_connection.return_value.__enter__.return_value = mock_conn
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [tuple([""] * len(repo.columns))]

        # Ricerca per data italiana
        repo.get_all(search_text="23/05/2023", as_objects=False)

        args = mock_cursor.execute.call_args
        params = args[0][1]
        # Deve aver convertito la data in ISO
        assert "%2023-05-23%" in params

    def test_get_all_db_not_exists(self, repo, mock_db):
        mock_db.DB_STORICO_ODA.exists.return_value = False
        assert repo.get_all() == []

    def test_get_all_exception(self, repo, mock_db):
        mock_db.get_connection.side_effect = Exception("DB error")
        assert repo.get_all() == []
