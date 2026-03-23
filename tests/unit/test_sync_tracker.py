from unittest.mock import patch

import pytest

from src.core.sync_tracker import SyncTracker


class TestSyncTracker:
    @pytest.fixture(autouse=True)
    def reset_state(self, tmp_path):  # noqa: ANN001
        # Reset class state before each test
        SyncTracker._cache = {}
        SyncTracker._loaded = False
        state_file = tmp_path / "sync_state.json"
        with patch.object(SyncTracker, "STATE_FILE", state_file):
            yield state_file
        SyncTracker._cache = {}
        SyncTracker._loaded = False

    def test_update_status(self, reset_state):  # noqa: ANN001
        SyncTracker.update_status("pdl", added=10, removed=2, duration=5.5)

        status = SyncTracker.get_status("pdl")

        assert status["added"] == 10  # noqa: PLR2004
        assert status["removed"] == 2  # noqa: PLR2004
        assert status["duration"] == 5.5  # noqa: PLR2004
        assert "timestamp" in status

    def test_get_status_empty(self, reset_state):  # noqa: ANN001
        status = SyncTracker.get_status("nonexistent")
        assert status == {}

    def test_get_formatted_status_never_synced(self, reset_state):  # noqa: ANN001
        result = SyncTracker.get_formatted_status("nonexistent")
        assert result == "Mai sincronizzato"

    def test_get_formatted_status_seconds(self, reset_state):  # noqa: ANN001
        SyncTracker.update_status("test", added=5, removed=1, duration=30.5)

        result = SyncTracker.get_formatted_status("test")

        assert "+5" in result
        assert "-1" in result
        assert "30.5s" in result

    def test_get_formatted_status_minutes(self, reset_state):  # noqa: ANN001
        SyncTracker.update_status("test", added=100, removed=50, duration=125.0)

        result = SyncTracker.get_formatted_status("test")

        assert "2m 5s" in result

    def test_persistence_save_and_load(self, reset_state):  # noqa: ANN001
        SyncTracker.update_status("persist_test", added=20, removed=3, duration=10.0)

        # Simulate app restart
        SyncTracker._loaded = False
        SyncTracker._cache = {}
        SyncTracker._load()

        status = SyncTracker.get_status("persist_test")
        assert status["added"] == 20  # noqa: PLR2004

    def test_load_handles_corrupted_file(self, reset_state):  # noqa: ANN001
        reset_state.parent.mkdir(parents=True, exist_ok=True)
        reset_state.write_text("not valid json", encoding="utf-8")

        SyncTracker._loaded = False
        SyncTracker._load()

        assert SyncTracker._cache == {}

    def test_multiple_modules(self, reset_state):  # noqa: ANN001
        SyncTracker.update_status("pdl", added=10, removed=0, duration=1.0)
        SyncTracker.update_status("dipendenti", added=5, removed=2, duration=2.0)
        SyncTracker.update_status("storico_oda", added=100, removed=10, duration=30.0)

        assert SyncTracker.get_status("pdl")["added"] == 10  # noqa: PLR2004
        assert SyncTracker.get_status("dipendenti")["added"] == 5  # noqa: PLR2004
        assert SyncTracker.get_status("storico_oda")["added"] == 100  # noqa: PLR2004
