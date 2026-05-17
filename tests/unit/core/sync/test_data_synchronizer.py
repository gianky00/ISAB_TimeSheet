from pathlib import Path
from unittest.mock import patch

from src.core.data_synchronizer import DataSynchronizer


def test_sync_storico_oda():
    # Mocking dependencies
    mock_db = Path("test.db")

    with patch("src.core.data_synchronizer.SmartSyncEngine") as mock_engine:
        mock_engine.sync_upsert_smart.return_value = (10, 5)  # 10 inserted, 5 updated

        rows = [("oda1", "pos1", "riga1", "val1")]
        inserted, updated = DataSynchronizer.sync_storico_oda(mock_db, rows)

        assert inserted == 10
        assert updated == 5
        mock_engine.sync_upsert_smart.assert_called_once()


def test_sync_scarico_ore():
    mock_db = Path("test.db")

    with patch("src.core.data_synchronizer.SmartSyncEngine") as mock_engine:
        mock_engine.sync_full_replace_with_metadata.return_value = (1, 0)

        rows = [("2026-05-17", "user1", "odc1", "pos1")]
        inserted, updated = DataSynchronizer.sync_scarico_ore(mock_db, rows)

        assert inserted == 1
        assert updated == 0
        mock_engine.sync_full_replace_with_metadata.assert_called_once()
