from unittest.mock import MagicMock, patch

import pytest

from src.application.services.database.repositories.contabilita_repository import ContabilitaRepository
from src.domain import (
    AttivitaProgrammataRecord,
    ContabilitaRecord,
    GiornalieraRecord,
)


class TestContabilitaRepository:
    @pytest.fixture
    def mock_db(self):
        m = MagicMock()
        m.DB_CONTABILITA = MagicMock()
        m.DB_CONTABILITA.exists.return_value = True
        return m

    @pytest.fixture
    def repo(self, mock_db):
        return ContabilitaRepository(db_manager_instance=mock_db)

    def test_get_available_years(self, repo, mock_db):
        mock_conn = MagicMock()
        mock_db.get_connection.return_value.__enter__.return_value = mock_conn

        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [(2023,), (2022,)]

        years = repo.get_available_years()
        assert years == [2023, 2022]

    def test_get_data_by_year_objects(self, repo, mock_db):
        mock_conn = MagicMock()
        mock_db.get_connection.return_value.__enter__.return_value = mock_conn
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        fields = dict.fromkeys(ContabilitaRecord.__dataclass_fields__)
        fields.update({"year": 2023, "n_prev": "100"})
        mock_cursor.fetchall.return_value = [fields]

        with patch(
            "src.application.services.database.repositories.contabilita_repository.dict",
            side_effect=lambda x: x,
        ):
            results = repo.get_data_by_year(2023, as_objects=True)
            assert len(results) == 1
            assert results[0].year == 2023

    def test_get_data_by_year_tuples(self, repo, mock_db):
        mock_conn = MagicMock()
        mock_db.get_connection.return_value.__enter__.return_value = mock_conn
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [("2023-01-01", "VAL")]

        results = repo.get_data_by_year(2023, as_objects=False)
        assert len(results) == 1
        assert results[0][0] == "2023-01-01"

    def test_get_giornaliere_by_year(self, repo, mock_db):
        mock_conn = MagicMock()
        mock_db.get_connection.return_value.__enter__.return_value = mock_conn
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        fields = dict.fromkeys(GiornalieraRecord.__dataclass_fields__, "")
        fields.update({"year": 2023, "personale": "P1"})
        mock_cursor.fetchall.return_value = [fields]

        with patch(
            "src.application.services.database.repositories.contabilita_repository.dict",
            side_effect=lambda x: x,
        ):
            results = repo.get_giornaliere_by_year(2023, as_objects=True)
            assert results[0].personale == "P1"

    def test_get_attivita_programmate(self, repo, mock_db):
        mock_conn = MagicMock()
        mock_db.get_connection.return_value.__enter__.return_value = mock_conn
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        fields = dict.fromkeys(AttivitaProgrammataRecord.__dataclass_fields__, "")
        fields.update({"id": 1, "descrizione": "D1"})
        mock_cursor.fetchall.return_value = [fields]

        with patch(
            "src.application.services.database.repositories.contabilita_repository.dict",
            side_effect=lambda x: x,
        ):
            results = repo.get_attivita_programmate(as_objects=True)
            assert results[0].descrizione == "D1"

    def test_get_certificati_campione_with_migration(self, repo, mock_db):
        mock_conn = MagicMock()
        mock_db.get_connection.return_value.__enter__.return_value = mock_conn
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        mock_cursor.fetchall.side_effect = [
            [(0, "id_strumento"), (1, "certificato")],
            [
                {
                    "id_strumento": "COE1",
                    "certificato": "C1",
                    "modello": "M",
                    "costruttore": "C",
                    "matricola": "M",
                    "range_strumento": "R",
                    "errore_max": "E",
                    "emissione": "2023",
                    "scadenza": "2024",
                    "stato": "OK",
                }
            ],
        ]

        with patch(
            "src.application.services.database.repositories.contabilita_repository.dict",
            side_effect=lambda x: x,
        ):
            results = repo.get_certificati_campione(as_objects=True)
            assert len(results) == 1
            assert results[0].id_coemi == "COE1"

    def test_get_scarico_ore(self, repo, mock_db):
        mock_conn = MagicMock()
        mock_db.get_connection.return_value.__enter__.return_value = mock_conn
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [("ROW",)]

        res = repo.get_scarico_ore(as_objects=False)
        assert len(res) == 1
        assert res[0][0] == "ROW"

    def test_db_not_exists(self, repo, mock_db):
        mock_db.DB_CONTABILITA.exists.return_value = False
        assert repo.get_available_years() == []
        assert repo.get_data_by_year(2023) == []
