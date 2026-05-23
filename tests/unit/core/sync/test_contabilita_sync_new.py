from unittest.mock import patch

import pytest

from src.core.sync.contabilita_sync import ContabilitaSyncEngine


class TestContabilitaSyncEngine:
    @patch("src.core.sync.contabilita_sync.sqlite3.connect")
    @patch("src.core.sync.contabilita_sync.ContabilitaSyncEngine.sync_partitioned_data")
    def test_sync_giornaliere(self, mock_sync, mock_conn):
        mock_sync.return_value = (10, 5)  # added, removed

        added, removed = ContabilitaSyncEngine.sync_giornaliere(
            "db.sqlite", [(2023, "R1")], [2023], ["year", "data"]
        )

        assert added == 10
        assert removed == 5
        assert mock_conn.called
        assert mock_sync.called

    @patch("src.core.sync.contabilita_sync.sqlite3.connect")
    @patch("src.core.sync.contabilita_sync.ContabilitaSyncEngine.sync_partitioned_data")
    def test_sync_contabilita(self, mock_sync, mock_conn):
        mock_sync.return_value = (20, 0)

        added, removed = ContabilitaSyncEngine.sync_contabilita(
            "db.sqlite", [(2023, "C1")], [2023], ["year", "id"]
        )

        assert added == 20
        assert removed == 0
        assert mock_sync.called

    @patch("src.core.sync.contabilita_sync.sqlite3.connect")
    def test_sync_error_rollback(self, mock_connect):
        mock_conn = mock_connect.return_value.__enter__.return_value
        with patch.object(ContabilitaSyncEngine, "sync_partitioned_data", side_effect=Exception("Crash")):
            with pytest.raises(Exception, match="Crash"):
                ContabilitaSyncEngine.sync_contabilita("db.sqlite", [], [], [])
            assert mock_conn.rollback.called
