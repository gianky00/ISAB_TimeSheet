from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.core.contabilita_queries import ContabilitaQueries


class TestContabilitaQueries:
    @pytest.fixture
    def db_path(self, tmp_path):  # noqa: ANN001
        p = tmp_path / "test_contabilita.db"
        p.touch()
        return p

    @patch("src.core.database.db_manager.get_connection")
    def test_get_available_years_success(self, mock_get_conn, db_path):  # noqa: ANN001
        mock_conn = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchall.return_value = [(2024,), (2023,)]

        years = ContabilitaQueries.get_available_years(db_path)

        assert years == [2024, 2023]
        assert "UNION" in mock_cursor.execute.call_args[0][0]

    def test_get_available_years_no_file(self):
        # Path inesistente
        years = ContabilitaQueries.get_available_years(Path("non_existent.db"))
        assert years == []

    @patch("src.core.database.db_manager.get_connection")
    def test_get_data_by_year_db_error(self, mock_get_conn, db_path):  # noqa: ANN001
        mock_get_conn.side_effect = Exception("SQLite locked")

        # Non deve sollevare eccezioni, ma ritornare lista vuota (SOP attuale)
        data = ContabilitaQueries.get_data_by_year(db_path, 2024)
        assert data == []

    @patch("src.core.database.db_manager.get_connection")
    def test_get_certificati_campione_logic(self, mock_get_conn, db_path):  # noqa: ANN001
        mock_conn = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn
        mock_cursor = mock_conn.cursor.return_value

        mock_cursor.fetchall.return_value = [("Cert1", "Note", "Lab", 1)]

        data = ContabilitaQueries.get_certificati_campione_data(db_path)
        assert len(data) == 1
        assert data[0][0] == "Cert1"
        assert "certificati_campione" in mock_cursor.execute.call_args[0][0]
