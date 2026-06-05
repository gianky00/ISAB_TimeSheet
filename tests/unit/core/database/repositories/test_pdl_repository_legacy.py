from unittest.mock import MagicMock, patch

import pytest

from src.application.services.database.repositories.pdl_repository import PdlRepository
from src.domain import PdlProgrammazioneRecord


class TestPdlRepository:
    @pytest.fixture
    def mock_db(self):
        m = MagicMock()
        m.DB_PDL = "fake_pdl.db"
        return m

    @pytest.fixture
    def repo(self, mock_db):
        return PdlRepository(db_manager_instance=mock_db)

    def test_get_filtered_all_filters(self, repo, mock_db):
        mock_db.execute_query.return_value = []
        filters = {"search": "test", "site": "Sud", "group": "S", "area": "Area1", "unit": "U1"}

        repo.get_filtered(filters, as_objects=False)

        query = mock_db.execute_query.call_args[0][1]
        assert "sito = ?" in query
        assert "n_pdl LIKE ?" in query
        assert "area = ?" in query
        assert "unita = ?" in query
        assert "descrizione_lavoro LIKE ?" in query

    def test_get_filtered_sorting(self, repo, mock_db):
        mock_db.execute_query.return_value = []

        # Test sort per n_pdl
        repo.get_filtered({}, sort_col_name="n_pdl", sort_order="ASC")
        query = mock_db.execute_query.call_args[0][1]
        assert "ORDER BY CAST(n_pdl AS INTEGER) ASC" in query

        # Test sort per data_creazione
        repo.get_filtered({}, sort_col_name="data_creazione")
        query = mock_db.execute_query.call_args[0][1]
        assert "ORDER BY substr(data_creazione, 7, 4)" in query

    @patch("src.application.services.database.repositories.pdl_repository.dict", side_effect=lambda x: x)
    def test_get_filtered_objects(self, mock_dict, repo, mock_db):
        row = dict.fromkeys(repo.columns, "")
        row["n_pdl"] = "100"
        mock_db.execute_query.return_value = [row]

        results = repo.get_filtered({}, as_objects=True)
        assert len(results) == 1
        assert results[0].n_pdl == "100"

    def test_get_unique_requesters(self, repo, mock_db):
        mock_db.execute_query.return_value = [("  MARIO  ROSSI  ",), ("luigi verdi",)]
        res = repo.get_unique_requesters()
        assert res == ["Luigi Verdi", "Mario Rossi"]

    @patch("src.application.services.database.repositories.pdl_repository.dict", side_effect=lambda x: x)
    def test_get_programming_by_week(self, mock_dict, repo, mock_db):
        row = dict.fromkeys(PdlProgrammazioneRecord.__dataclass_fields__, "")
        row["id"] = 1
        mock_db.execute_query.return_value = [row]

        res = repo.get_programming_by_week("2023-01-01", "2023-01-07")
        assert len(res) == 1
        assert res[0].id == 1

    def test_save_programming_success(self, repo, mock_db):
        mock_conn = MagicMock()
        mock_db.get_connection.return_value.__enter__.return_value = mock_conn

        record = PdlProgrammazioneRecord(
            id=None,
            richiedente="R",
            n_pdl="1",
            area="A",
            unita="U",
            descrizione="D",
            lun_tcl=False,
            lun_tgo=False,
            mar_tcl=False,
            mar_tgo=False,
            mer_tcl=False,
            mer_tgo=False,
            gio_tcl=False,
            gio_tgo=False,
            ven_tcl=False,
            ven_tgo=False,
            sab_tcl=False,
            sab_tgo=False,
            dom_tcl=False,
            dom_tgo=False,
            settimana_start="S",
            settimana_end="E",
        )

        res = repo.save_programming([record], "S", "E")
        assert res is True
        assert mock_db.execute_query.called  # DELETE
        assert mock_conn.executemany.called  # INSERT

    @patch("sqlite3.connect")
    def test_get_interventions(self, mock_connect, repo):
        mock_conn = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        mock_row = {"fonte": "F1", "tecnico": "T1"}
        mock_cursor.fetchall.return_value = [mock_row]

        # Patching dict in the repository module to handle sqlite3.Row conversion
        with patch(
            "src.application.services.database.repositories.pdl_repository.dict", side_effect=lambda x: x
        ):
            res = repo.get_interventions("123", "ext.db")
            assert len(res) == 1
            assert res[0]["tecnico"] == "T1"
