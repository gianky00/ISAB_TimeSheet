from unittest.mock import MagicMock, patch

import pytest

from src.core.sync.contabilita_sync import ContabilitaSyncEngine


class TestContabilitaSyncEngine:
    @patch("src.core.sync.contabilita_sync.sqlite3.connect")
    @patch("src.core.sync.contabilita_sync.ContabilitaSyncEngine.sync_partitioned_data")
    def test_sync_giornaliere_success(self, mock_sync, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_sync.return_value = (5, 2)

        added, removed = ContabilitaSyncEngine.sync_giornaliere(
            db_path="dummy.db", new_data=[("A",)], years=[2023], columns=["col1"]
        )

        assert added == 5
        assert removed == 2
        assert mock_conn.commit.called
        assert mock_sync.called

    @patch("src.core.sync.contabilita_sync.sqlite3.connect")
    @patch("src.core.sync.contabilita_sync.ContabilitaSyncEngine.sync_partitioned_data")
    def test_sync_giornaliere_failure(self, mock_sync, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_sync.side_effect = Exception("DB Error")

        with pytest.raises(Exception, match="DB Error"):
            ContabilitaSyncEngine.sync_giornaliere("dummy.db", [("A",)], [2023], ["col1"])

        assert mock_conn.rollback.called

    @patch("src.core.sync.contabilita_sync.sqlite3.connect")
    @patch("src.core.sync.contabilita_sync.ContabilitaSyncEngine.sync_partitioned_data")
    def test_sync_contabilita_success(self, mock_sync, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_sync.return_value = (10, 1)

        added, removed = ContabilitaSyncEngine.sync_contabilita(
            db_path="dummy.db", new_data=[("B",)], years=[2023, 2024], columns=["col1"]
        )

        assert added == 10
        assert removed == 1
        assert mock_conn.commit.called

    @patch("src.core.sync.contabilita_sync.sqlite3.connect")
    @patch("src.core.sync.contabilita_sync.ContabilitaSyncEngine.sync_partitioned_data")
    def test_sync_contabilita_failure(self, mock_sync, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_sync.side_effect = Exception("Fail")

        with pytest.raises(Exception, match="Fail"):
            ContabilitaSyncEngine.sync_contabilita("dummy.db", [("B",)], [2023], ["col1"])

        assert mock_conn.rollback.called
