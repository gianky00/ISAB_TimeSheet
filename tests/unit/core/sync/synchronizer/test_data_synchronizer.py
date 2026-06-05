from unittest.mock import patch

import pytest

from src.application.services.data_synchronizer import DataSynchronizer


@pytest.fixture
def db_path(tmp_path):
    return tmp_path / "test.db"


def test_sync_storico_oda(db_path):
    # Setup mock per SmartSyncEngine.sync_upsert_smart
    with patch("src.application.services.data_synchronizer.SmartSyncEngine.sync_upsert_smart") as mock_sync:
        mock_sync.return_value = (5, 2)

        data = [("O1", 1, 1), ("O2", 1, 2)]
        added, deleted = DataSynchronizer.sync_storico_oda(db_path, data)

        assert added == 5
        assert deleted == 2
        mock_sync.assert_called_once()


def test_sync_attivita_programmate(db_path):
    # Setup mock per SmartSyncEngine.sync_full_replace_with_metadata
    with patch(
        "src.application.services.data_synchronizer.SmartSyncEngine.sync_full_replace_with_metadata"
    ) as mock_sync:
        mock_sync.return_value = (10, 0)

        data = [("ps1", "a1", "desc1")]
        added, deleted = DataSynchronizer.sync_attivita_programmate(db_path, data)

        assert added == 10
        assert deleted == 0
        mock_sync.assert_called_once()
