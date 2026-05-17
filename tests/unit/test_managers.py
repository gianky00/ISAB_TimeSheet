from unittest.mock import MagicMock, patch

import pytest

from src.core.notification_manager import NotificationManager
from src.core.oda_manager import OdaManager
from src.core.stats_manager import StatsManager
from src.core.sync_tracker import SyncTracker


class TestManagers:
    @pytest.fixture(autouse=True)
    def setup_env(self, tmp_path, monkeypatch):
        self.tmp_path = tmp_path
        monkeypatch.setattr("src.core.paths.DB_DIR", tmp_path)
        monkeypatch.setattr("src.core.sync_tracker.DB_DIR", tmp_path)
        monkeypatch.setattr("src.core.paths.CONFIG_DIR", tmp_path)

        SyncTracker._loaded = False
        SyncTracker.STATE_FILE = tmp_path / "sync_state.json"

        NotificationManager._instance = None
        StatsManager._instance = None

    def test_sync_tracker_flow(self):
        status = SyncTracker.get_status("pdl")
        assert status.get("added", 0) == 0
        SyncTracker.update_status("pdl", added=10, removed=2, duration=5.5)
        SyncTracker._loaded = False
        new_status = SyncTracker.get_status("pdl")
        assert new_status["added"] == 10
        assert new_status["removed"] == 2
        assert "5.5s" in SyncTracker.get_formatted_status("pdl")

    @patch("src.core.oda_manager.OdaRepository")
    @patch("src.core.importers.storico_oda.StoricoOdaImporter.import_storico_oda")
    @patch("src.core.data_synchronizer.DataSynchronizer.sync_storico_oda")
    def test_oda_manager_import(self, mock_sync, mock_import, mock_repo):
        mock_import.return_value = (True, "OK", [("row1",)])
        mock_sync.return_value = (1, 0)
        success, _msg, added, _removed = OdaManager.import_oda_from_excel("file.xlsx")
        assert success is True
        assert added == 1
        assert SyncTracker.get_status("oda")["added"] == 1

    def test_notification_manager_basic(self, qtbot):
        nm = NotificationManager.instance()
        mock_slot = MagicMock()
        nm.notification_added.connect(mock_slot.emit)
        nm.add_notification("Title", "Message", level="info")
        notifs = nm.get_notifications()
        assert len(notifs) >= 1
        assert notifs[0]["title"] == "Title"
        assert mock_slot.emit.called

    def test_notification_manager_persistence(self):
        nm1 = NotificationManager.instance()
        nm1.add_notification("T1", "M1")
        NotificationManager._instance = None
        nm2 = NotificationManager.instance()
        assert any(n["title"] == "T1" for n in nm2.get_notifications())

    def test_notification_manager_cleanup(self):
        nm = NotificationManager.instance()
        nm.clear_all()
        for i in range(5):
            nm.add_notification(f"T{i}", "M", level="error")
        assert nm.get_unread_count() == 5
        nm.mark_all_as_read()
        assert nm.get_unread_count() == 0
        nm.clear_all()
        assert len(nm.get_notifications()) == 0

    def test_stats_manager_flow(self, monkeypatch):
        config = {"statistics": {}}
        monkeypatch.setattr("src.core.config_manager.load_config", lambda: config)
        monkeypatch.setattr("src.core.config_manager.set_config_value", lambda k, v: config.update({k: v}))

        sm = StatsManager()
        sm.increment_usage("test_bot")
        sm.increment_error("test_bot")

        stats = sm.get_all_stats()
        assert stats["test_bot"]["runs"] == 1
        assert stats["test_bot"]["errors"] == 1
        assert stats["test_bot"]["last_run"] is not None
        sm._save_stats()
