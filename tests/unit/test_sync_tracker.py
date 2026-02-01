import json
from unittest.mock import MagicMock, mock_open, patch

import pytest

from src.core.sync_tracker import SyncTracker


class TestSyncTracker:
    @pytest.fixture(autouse=True)
    def reset_tracker(self):
        """Reset SyncTracker state between tests."""
        SyncTracker._cache = {}
        SyncTracker._loaded = False

    @patch("src.core.sync_tracker.SyncTracker.STATE_FILE")
    def test_load_save_cycle(self, mock_file):
        mock_file.exists.return_value = True
        mock_data = {"pdl": {"added": 10, "removed": 2}}

        m_open = mock_open(read_data=json.dumps(mock_data))
        with patch("src.core.sync_tracker.open", m_open):
            SyncTracker._load()
            assert SyncTracker._cache["pdl"]["added"] == 10

        SyncTracker.update_status("dipendenti", 5, 0, 1.5)

        # Check if saved
        assert "dipendenti" in SyncTracker._cache
        assert SyncTracker._cache["dipendenti"]["added"] == 5

    def test_get_status_empty(self):
        with patch(
            "src.core.sync_tracker.SyncTracker.STATE_FILE.exists", return_value=False
        ):
            status = SyncTracker.get_status("unknown")
            assert status == {}

    def test_formatted_status(self):
        # Mocking get_status to avoid loading issues
        with patch.object(SyncTracker, "get_status") as mock_get:
            # Case: Mai sincronizzato
            mock_get.return_value = {}
            assert SyncTracker.get_formatted_status("mod") == "Mai sincronizzato"

            # Case: Normal sync
            mock_get.return_value = {
                "timestamp": "01/01/2026 10:00",
                "added": 10,
                "removed": 2,
                "duration": 5.5,
            }
            res = SyncTracker.get_formatted_status("mod")
            assert "01/01/2026 10:00" in res
            assert "+10" in res
            assert "-2" in res
            assert "5.5s" in res

            # Case: Long duration
            mock_get.return_value = {
                "timestamp": "01/01/2026 10:00",
                "added": 0,
                "removed": 0,
                "duration": 65.0,
            }
            res = SyncTracker.get_formatted_status("mod")
            assert "1m 5s" in res

    @patch("src.core.sync_tracker.SyncTracker.STATE_FILE")
    @patch("src.core.sync_tracker.open", new_callable=mock_open)
    def test_update_status_persistence(self, mock_file_open, mock_state_file):
        mock_state_file.exists.return_value = False
        mock_state_file.parent.mkdir = MagicMock()

        SyncTracker.update_status("test", 1, 1, 0.1)

        mock_state_file.parent.mkdir.assert_called()
        mock_file_open.assert_called()
        # Check written content
        handle = mock_file_open()
        written = "".join(call.args[0] for call in handle.write.call_args_list)
        data = json.loads(written)
        assert data["test"]["added"] == 1
