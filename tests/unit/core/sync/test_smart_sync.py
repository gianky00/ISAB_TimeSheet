import pytest
from unittest.mock import MagicMock, patch
from src.core.sync.smart_sync import SmartSyncEngine
from src.core.sync.base import SyncTarget
from pathlib import Path

@pytest.fixture
def mock_target():
    return SyncTarget(Path("test.db"), "test_table", ["col1", "col2"])

def test_sync_upsert_smart_empty():
    target = SyncTarget(Path("test.db"), "test_table", ["col1"])
    inserted, deleted = SmartSyncEngine.sync_upsert_smart(target, [])
    assert inserted == 0
    assert deleted == 0

@patch("src.core.sync.smart_sync.db_manager")
def test_sync_upsert_smart_logic(mock_db, mock_target):
    # Setup mocks
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_db.get_connection.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    # Mocking execution of internal methods
    with patch.object(SmartSyncEngine, "_create_temp_table", return_value="tmp_table"), \
         patch.object(SmartSyncEngine, "_populate_temp_table"), \
         patch.object(SmartSyncEngine, "_calculate_diff", return_value=5), \
         patch.object(SmartSyncEngine, "_execute_upsert"):
        
        inserted, deleted = SmartSyncEngine.sync_upsert_smart(mock_target, [("val1", "val2")])
        
        assert inserted == 5
        assert deleted == 0
        mock_conn.commit.assert_called_once()
