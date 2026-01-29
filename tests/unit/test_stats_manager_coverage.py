import json

import pytest

from src.core.stats_manager import StatsManager


class TestStatsManager:
    @pytest.fixture
    def manager(self, tmp_path, mocker):
        # Mock config_manager to avoid real disk I/O
        self.mock_config = {"statistics": {}}
        mocker.patch("src.core.config_manager.load_config", return_value=self.mock_config)
        mocker.patch(
            "src.core.config_manager.set_config_value",
            side_effect=lambda k, v: self.mock_config.update({k: v}),
        )
        mocker.patch("src.core.config_manager.CONFIG_DIR", tmp_path)

        # Reset singleton
        StatsManager._instance = None
        return StatsManager()

    def test_increment_usage(self, manager):
        manager.increment_usage("bot_a")
        stats = manager.get_all_stats()

        assert stats["bot_a"]["runs"] == 1
        assert stats["bot_a"]["last_run"] is not None

        manager.increment_usage("bot_a")
        assert stats["bot_a"]["runs"] == 2

    def test_increment_error(self, manager):
        manager.increment_error("bot_b")
        stats = manager.get_all_stats()

        assert stats["bot_b"]["errors"] == 1
        assert stats["bot_b"]["runs"] == 0

    def test_migration_from_old_file(self, tmp_path, mocker):
        # Setup old file
        old_file = tmp_path / "statistics.json"
        old_data = {"legacy_bot": {"runs": 10, "errors": 2}}
        with open(old_file, "w") as f:
            json.dump(old_data, f)

        # Mock config without stats
        empty_config = {}
        mocker.patch("src.core.config_manager.load_config", return_value=empty_config)
        mocker.patch("src.core.config_manager.CONFIG_DIR", tmp_path)
        mocker.patch("src.core.config_manager.set_config_value")

        StatsManager._instance = None
        manager = StatsManager()

        assert manager.get_all_stats() == old_data

    def test_persistence_via_config(self, manager):
        manager.increment_usage("bot_c")
        # Verify it went to mock_config (simulating config_manager persistence)
        assert self.mock_config["statistics"]["bot_c"]["runs"] == 1
