"""
SyncroJob - Test Bot Queue Manager
Verifica la logica di parallelismo e accodamento dei bot.
"""

from unittest.mock import MagicMock

import pytest

from src.gui.controllers.bot_queue_manager import BotQueueManager


class TestBotQueueManager:
    @pytest.fixture
    def manager(self):
        return BotQueueManager()

    def test_schedule_free_site(self, manager):
        """Verifica avvio immediato se il sito è libero."""
        mock_panel = MagicMock()
        mock_panel.start_btn.isEnabled.return_value = True

        manager.schedule_bot("bot1", mock_panel, "portale_fornitori", "msg")

        assert "bot1" in manager.running_bots_by_site["portale_fornitori"]
        assert mock_panel._on_start.called

    def test_schedule_busy_site(self, manager):
        """Verifica accodamento se il sito è occupato."""
        manager.running_bots_by_site["portale_fornitori"] = ["other_bot"]
        mock_panel = MagicMock()

        manager.schedule_bot("bot1", mock_panel, "portale_fornitori", "msg")

        assert "bot1" not in manager.running_bots_by_site["portale_fornitori"]
        assert len(manager.pending_bots_by_site["portale_fornitori"]) == 1
        assert "Bot in coda" in mock_panel.log_widget.append.call_args[0][0]

    def test_on_bot_completed_triggers_next(self, manager):
        """Verifica che il completamento di un bot avvii il successivo in coda."""
        manager.running_bots_by_site["portale_fornitori"] = ["bot1"]
        next_panel = MagicMock()
        next_panel.start_btn.isEnabled.return_value = True
        manager.pending_bots_by_site["portale_fornitori"] = [("bot2", next_panel, "msg2")]

        manager._on_bot_completed("bot1", "portale_fornitori", MagicMock())

        assert "bot1" not in manager.running_bots_by_site["portale_fornitori"]
        assert "bot2" in manager.running_bots_by_site["portale_fornitori"]
        assert next_panel._on_start.called
        # Verifica che entrambi i messaggi siano stati loggati
        appends = [call[0][0] for call in next_panel.log_widget.append.call_args_list]
        assert any("Avvio da coda" in s for s in appends)
        assert any("msg2" in s for s in appends)

    def test_status_callback_registration(self, manager):
        """Verifica che il manager si colleghi al segnale status_changed del pannello."""
        mock_panel = MagicMock()
        mock_panel.start_btn.isEnabled.return_value = True

        manager.schedule_bot("bot1", mock_panel, "portale_fornitori", "msg")

        assert hasattr(mock_panel, "_service_callback")
        assert mock_panel.status_changed.connect.called
