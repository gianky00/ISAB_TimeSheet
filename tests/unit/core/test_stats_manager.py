import time
from pathlib import Path
from unittest.mock import patch

import pytest

from src.application.services.stats_manager import StatsManager


class TestStatsManager:
    @pytest.fixture(autouse=True)
    def reset_stats_manager(self):
        # Reset singleton instance
        StatsManager._instance = None

    @patch("src.application.services.config_manager.load_config")
    @patch("src.application.services.config_manager.set_config_value")
    def test_singleton_and_init(self, mock_set, mock_load):
        mock_load.return_value = {"statistics": {"bot1": {"runs": 1}}}

        mgr = StatsManager()
        mgr2 = StatsManager()

        assert mgr is mgr2
        assert mgr.stats["bot1"]["runs"] == 1

    @patch("src.application.services.config_manager.load_config", return_value={})
    @patch("src.application.services.config_manager.set_config_value")
    def test_increment_usage(self, mock_set, mock_load):
        mgr = StatsManager()
        mgr.increment_usage("new_bot")

        assert mgr.stats["new_bot"]["runs"] == 1
        assert mgr.stats["new_bot"]["last_run"] is not None

        # Incremento successivo
        mgr.increment_usage("new_bot")
        assert mgr.stats["new_bot"]["runs"] == 2

    @patch("src.application.services.config_manager.load_config", return_value={})
    @patch("src.application.services.config_manager.set_config_value")
    def test_increment_error(self, mock_set, mock_load):
        mgr = StatsManager()
        mgr.increment_error("bot_fail")

        assert mgr.stats["bot_fail"]["errors"] == 1
        assert mgr.stats["bot_fail"]["runs"] == 0

    @patch("src.application.services.config_manager.load_config", return_value={})
    @patch("src.application.services.config_manager.set_config_value")
    def test_async_save_logic(self, mock_set, mock_load):
        mgr = StatsManager()

        mgr.increment_usage("async_bot")

        # Attendiamo un attimo per far lavorare il thread
        time.sleep(0.2)

        assert mock_set.called
        # Il primo argomento deve essere "statistics"
        args = mock_set.call_args[0]
        assert args[0] == "statistics"
        assert args[1]["async_bot"]["runs"] == 1

    @patch("src.application.services.config_manager.load_config", return_value={})
    @patch("src.application.services.config_manager.set_config_value")
    def test_migration_from_old_file(self, mock_set, mock_load, fs):
        # Setup filesystem
        config_dir = Path("/config")
        fs.create_dir(str(config_dir))
        old_file = config_dir / "statistics.json"
        fs.create_file(str(old_file), contents='{"legacy_bot": {"runs": 10}}')

        # Patch CONFIG_DIR e FileNames.STATISTICS per matchare il nostro fs simulato
        with patch("src.application.services.config_manager.CONFIG_DIR", config_dir):
            mgr = StatsManager()
            assert mgr.stats["legacy_bot"]["runs"] == 10
            # Attendiamo il salvataggio asincrono scatenato dal caricamento con migrazione
            time.sleep(0.2)
            assert mock_set.called
