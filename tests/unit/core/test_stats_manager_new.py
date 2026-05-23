import json
import queue
from unittest.mock import MagicMock, patch

import pytest

from src.core.stats_manager import StatsManager


class TestStatsManager:
    @pytest.fixture(autouse=True)
    def reset_singleton(self):
        StatsManager._instance = None
        # Evitiamo l'avvio reale del thread
        with patch("threading.Thread"):
            with patch("src.core.config_manager.load_config", return_value={}):
                self.manager = StatsManager()
                self.manager._save_queue = MagicMock()  # Mock coda salvataggio

    def test_increment_usage(self):
        self.manager.increment_usage("bot1")
        assert self.manager.stats["bot1"]["runs"] == 1
        assert self.manager.stats["bot1"]["last_run"] is not None
        assert self.manager._save_queue.put.called

    def test_increment_error(self):
        self.manager.increment_error("bot2")
        assert self.manager.stats["bot2"]["errors"] == 1
        assert self.manager._save_queue.put.called

    @patch("src.core.config_manager.load_config")
    def test_load_stats_migration(self, mock_load, fs):
        mock_load.return_value = {"statistics": None}

        # Setup legacy file
        from src.core.config_manager import CONFIG_DIR
        from src.core.constants import FileNames

        fs.create_dir(str(CONFIG_DIR))
        legacy_file = CONFIG_DIR / FileNames.STATISTICS
        legacy_data = {"old_bot": {"runs": 10}}
        fs.create_file(str(legacy_file), contents=json.dumps(legacy_data))

        with patch("src.core.config_manager.set_config_value") as mock_set:
            stats = self.manager._load_stats()
            assert stats["old_bot"]["runs"] == 10
            assert mock_set.called

    def test_get_all_stats(self):
        self.manager.stats = {"b1": {"runs": 5}}
        assert self.manager.get_all_stats()["b1"]["runs"] == 5

    def test_worker_loop_logic(self):
        # Testiamo manualmente la logica del loop senza thread
        self.manager._save_queue = queue.Queue()
        self.manager._save_queue.put({"test": 1})
        self.manager._save_queue.put(None)  # Stop signal

        with patch("src.core.config_manager.set_config_value") as mock_set:
            self.manager._worker_loop()
            assert mock_set.called
            mock_set.assert_called_with("statistics", {"test": 1})
