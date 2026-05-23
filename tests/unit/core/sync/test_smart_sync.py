from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.core.exceptions import ValidationError
from src.core.sync.smart_sync import SmartSyncEngine, SyncTarget


class TestSmartSyncEngine:
    @pytest.fixture
    def target(self):
        return SyncTarget(
            db_path=Path("/fake/db.sqlite"), table_name="test_table", columns=["id", "name", "value"]
        )

    @patch("src.core.database.db_manager.get_connection")
    def test_sync_upsert_smart_success(self, mock_get_conn, target):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Mock _calculate_diff return value
        mock_cursor.fetchone.return_value = [5]  # 5 records diff

        new_data = [(1, "A", "V1"), (2, "B", "V2")]

        # Eseguiamo il metodo
        added, _deleted = SmartSyncEngine.sync_upsert_smart(
            target, new_data, conflict_cols=["id"], mirror=True
        )

        assert added == 5
        assert mock_cursor.execute.called
        assert mock_cursor.executemany.called
        assert mock_conn.commit.called

    @patch("src.core.database.db_manager.get_connection")
    def test_sync_full_replace_with_metadata(self, mock_get_conn, target):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Simula metadati esistenti: id=1 ha annotazione="Old"
        mock_cursor.fetchall.return_value = [(1, "Old")]

        new_data = [(1, "A", "V1"), (2, "B", "V2")]

        added, deleted = SmartSyncEngine.sync_full_replace_with_metadata(
            target, new_data, key_cols=["id"], metadata_cols=["annotazioni"]
        )

        assert added == 2
        assert deleted == 0

        # Verifica che executemany sia stato chiamato con i metadati uniti
        args = mock_cursor.executemany.call_args[0]
        final_rows = args[1]
        assert final_rows[0] == (1, "A", "V1", "Old")
        assert final_rows[1] == (2, "B", "V2", "")

    def test_clean_value(self):
        # BaseSyncEngine._clean_value normalizza tutto a stringa (strip)
        assert SmartSyncEngine._clean_value(None) == ""
        assert SmartSyncEngine._clean_value("  text  ") == "text"
        assert SmartSyncEngine._clean_value(10.5) == "10.5"

    def test_validate_identifier(self):
        assert SmartSyncEngine._validate_identifier("table") == "table"
        with pytest.raises(ValidationError):
            SmartSyncEngine._validate_identifier("table; DROP TABLE users")

    def test_sync_upsert_smart_empty(self, target):
        added, deleted = SmartSyncEngine.sync_upsert_smart(target, [])
        assert added == 0
        assert deleted == 0
