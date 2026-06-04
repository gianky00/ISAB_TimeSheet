from unittest.mock import MagicMock, patch

import pytest

from src.gui.panels.base import BaseBotPanel
from src.gui.styles import STATUS_COLORS


class TestBaseBotPanel:
    @pytest.fixture
    def panel(self, qtbot):
        p = BaseBotPanel("test_bot", "Test Bot", "Desc")
        qtbot.addWidget(p)
        return p

    def test_initialization(self, panel):
        assert panel.bot_id == "test_bot"
        assert panel.bot_name == "Test Bot"
        assert panel.controls is not None
        assert panel.log_widget is not None

    @patch("src.application.services.audit_manager.AuditManager.instance")
    @patch("src.application.services.stats_manager.StatsManager.increment_usage")
    def test_on_start_flow(self, mock_stats, mock_audit, panel, qtbot):
        panel._on_start()

        assert panel.start_time is not None
        assert panel.controls.start_btn.isEnabled() is False  # Running
        assert panel.status_card._status == STATUS_COLORS["running"]

        # Audit/Stats called via timer, but we call the internal method for sync test
        panel._log_startup_telemetry()
        assert mock_audit.return_value.log_action.called
        assert mock_stats.called

    def test_on_stop_requested(self, panel):
        panel.worker = MagicMock()
        panel._on_stop()
        assert panel.worker.stop.called
        assert "Arresto richiesto" in panel.status_card._status_label.text()

    @patch("src.application.services.audit_manager.AuditManager.instance")
    def test_on_worker_finished_success(self, mock_audit, panel, qtbot):
        panel.start_time = panel.start_time or MagicMock()  # Simula start
        panel.worker = MagicMock()

        panel._on_worker_finished(True)

        assert panel.controls.start_btn.isEnabled() is True
        assert panel.status_card._status == STATUS_COLORS["completed"]

        # Wait for the QTimer(0) lambda to be called
        qtbot.wait_until(lambda: mock_audit.return_value.log_action.called, timeout=1000)

    @patch("src.application.services.config_manager.get_default_account")
    def test_get_credentials(self, mock_get, panel):
        mock_get.return_value = {"username": "admin", "password": "123"}
        u, p = panel.get_credentials()
        assert u == "admin"
        assert p == "123"

    def test_update_status_manual(self, panel):
        panel._update_status(STATUS_COLORS["error"], "Fatal Error")
        assert panel.status_card._status == STATUS_COLORS["error"]
        assert panel.status_card._status_label.text() == "Fatal Error"

    def test_duration_calculation(self, panel):
        from datetime import UTC, datetime, timedelta

        panel.start_time = datetime.now(UTC) - timedelta(minutes=5, seconds=10)
        dur = panel._calculate_duration_str()
        assert "5m 10s" in dur
