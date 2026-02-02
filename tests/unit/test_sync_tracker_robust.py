import json
from unittest.mock import patch

import pytest

from src.core.sync_tracker import SyncTracker


class TestSyncTrackerRobust:
    @pytest.fixture(autouse=True)
    def reset_tracker(self, tmp_path):
        """Fixture che resetta lo stato del tracker e mocka il path del file."""
        # Reset stato interno
        SyncTracker._cache = {}
        SyncTracker._loaded = False

        # Mock del percorso file
        test_state_file = tmp_path / "data" / "sync_state.json"

        with patch("src.core.sync_tracker.SyncTracker.STATE_FILE", test_state_file):
            yield test_state_file

    def test_update_and_get_status(self, reset_tracker):
        """Test flusso base: aggiornamento e recupero stato."""
        SyncTracker.update_status("module_a", added=10, removed=5, duration=1.5)

        # Verifica Cache interna
        status = SyncTracker.get_status("module_a")
        assert status["added"] == 10
        assert status["removed"] == 5
        assert status["duration"] == 1.5
        assert "timestamp" in status
        assert "last_ts" in status

        # Verifica persistenza su file
        assert reset_tracker.exists()
        with open(reset_tracker, "r") as f:
            data = json.load(f)
            assert data["module_a"]["added"] == 10

    def test_persistence_reload(self, reset_tracker):
        """Test ricaricamento stato da file."""
        # 1. Scrivi dati
        SyncTracker.update_status("module_b", added=1, removed=0)

        # 2. Resetta memoria
        SyncTracker._cache = {}
        SyncTracker._loaded = False

        # 3. Leggi (dovrebbe ricaricare da file)
        status = SyncTracker.get_status("module_b")
        assert status["added"] == 1
        assert status["removed"] == 0

    def test_load_corrupted_file(self, reset_tracker):
        """Test resilienza con file JSON corrotto."""
        # Crea file corrotto
        reset_tracker.parent.mkdir(parents=True, exist_ok=True)
        reset_tracker.write_text("{invalid_json", encoding="utf-8")

        # Dovrebbe gestire l'errore e tornare dict vuoto senza crashare
        SyncTracker._loaded = False
        status = SyncTracker.get_status("any_module")
        assert status == {}

        # Se aggiorno, dovrebbe sovrascrivere il file corrotto
        SyncTracker.update_status("new_module", 1, 1)
        assert SyncTracker.get_status("new_module")["added"] == 1

    def test_get_formatted_status(self):
        """Test formattazione stringa per UI."""
        SyncTracker.update_status("mod_short", added=5, removed=2, duration=30.5)
        formatted = SyncTracker.get_formatted_status("mod_short")

        assert "+5" in formatted
        assert "-2" in formatted
        assert "Tempo: 30.5s" in formatted
        assert "font color='green'" in formatted
        assert "font color='red'" in formatted

    def test_get_formatted_status_long_duration(self):
        """Test formattazione tempi lunghi (>60s)."""
        SyncTracker.update_status("mod_long", added=0, removed=0, duration=125)  # 2m 5s
        formatted = SyncTracker.get_formatted_status("mod_long")
        assert "Tempo: 2m 5s" in formatted

    def test_get_formatted_status_missing(self):
        """Test formattazione per modulo mai sincronizzato."""
        formatted = SyncTracker.get_formatted_status("unknown_module")
        assert formatted == "Mai sincronizzato"

    def test_save_permission_error(self, reset_tracker):
        """Test gestione errore permessi in scrittura."""
        # Mock open per lanciare eccezione durante il save
        with patch("builtins.open", side_effect=PermissionError("Access Denied")):
            # Non deve crashare
            SyncTracker.update_status("module_err", 1, 1)

        # Verifica che i dati siano comunque in cache (memoria) anche se save fallisce
        assert SyncTracker.get_status("module_err")["added"] == 1
