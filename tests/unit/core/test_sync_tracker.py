from unittest.mock import patch

import pytest

from src.core.sync_tracker import SyncTracker


class TestSyncTracker:
    @pytest.fixture(autouse=True)
    def reset_tracker(self, fs):
        """Resetta lo stato della classe prima di ogni test."""
        SyncTracker._cache = {}
        SyncTracker._loaded = False
        # Assicura che la directory del file di stato esista
        fs.create_dir(str(SyncTracker.STATE_FILE.parent))

    def test_load_non_existent(self):
        SyncTracker._load()
        assert SyncTracker._cache == {}

    def test_load_corrupt_file(self, fs):
        fs.create_file(str(SyncTracker.STATE_FILE), contents="invalid json")
        SyncTracker._load()
        assert SyncTracker._cache == {}

    def test_update_status_and_save(self, fs):
        SyncTracker.update_status("test_module", added=10, removed=2, duration=1.5)
        assert SyncTracker.get_status("test_module")["added"] == 10
        assert SyncTracker.STATE_FILE.exists()

    def test_mark_start_and_failure(self, fs):
        SyncTracker.mark_start("pdl")
        assert SyncTracker.get_status("pdl")["last_attempt_success"] is None
        SyncTracker.mark_failure("pdl", error="err")
        assert SyncTracker.get_status("pdl")["last_error"] == "err"

    def test_get_formatted_status(self):
        assert SyncTracker.get_formatted_status("unknown") == "Mai sincronizzato"
        with patch.object(SyncTracker, "get_status") as mock_get:
            mock_get.return_value = {"timestamp": "T", "added": 1, "removed": 0, "duration": 1}
            assert "T" in SyncTracker.get_formatted_status("pdl")

    def test_save_error_logs(self, fs):
        # Usiamo un approccio diverso: patchiamo l'intero modulo logger per catturare la chiamata
        with patch("src.core.sync_tracker.logger") as mock_logger:
            # Forziamo l'errore tramite un parametro non serializzabile in json.dumps
            SyncTracker._cache = {"invalid": object()}
            SyncTracker._save()
            assert mock_logger.exception.called
