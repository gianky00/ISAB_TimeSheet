from unittest.mock import patch

import pytest

from src.core.stats_manager import StatsManager


class TestStatsManager:
    @pytest.fixture(autouse=True)
    def reset_singleton(self):
        """Reset Singleton instance before and after each test."""
        StatsManager._instance = None
        yield
        StatsManager._instance = None

    @patch("src.core.config_manager.load_config")
    def test_init_load_stats(self, mock_load):  # noqa: ANN001
        mock_load.return_value = {"statistics": {"bot1": {"runs": 5, "errors": 1}}}
        manager = StatsManager()
        assert manager.stats["bot1"]["runs"] == 5  # noqa: PLR2004

    @patch("src.core.config_manager.load_config")
    @patch("src.core.config_manager.set_config_value")
    def test_increment_usage(self, mock_set, mock_load):  # noqa: ANN001
        mock_load.return_value = {}
        manager = StatsManager()

        manager.increment_usage("new_bot")
        # Attendi il worker thread asincrono
        manager._save_queue.join()

        assert manager.stats["new_bot"]["runs"] == 1
        assert manager.stats["new_bot"]["last_run"] is not None
        mock_set.assert_called_with("statistics", manager.stats)

    @patch("src.core.config_manager.load_config")
    @patch("src.core.config_manager.set_config_value")
    def test_increment_error(self, mock_set, mock_load):  # noqa: ANN001
        mock_load.return_value = {"statistics": {"bot1": {"runs": 5, "errors": 1}}}
        manager = StatsManager()

        manager.increment_error("bot1")
        # Attendi il worker thread asincrono
        manager._save_queue.join()

        assert manager.stats["bot1"]["errors"] == 2  # noqa: PLR2004
        mock_set.assert_called_with("statistics", manager.stats)

    @patch("src.core.config_manager.load_config")
    def test_get_all_stats(self, mock_load):  # noqa: ANN001
        mock_load.return_value = {"statistics": {"a": 1}}
        manager = StatsManager()
        assert manager.get_all_stats() == {"a": 1}
