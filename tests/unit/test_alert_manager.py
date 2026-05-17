from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest

from src.core.logging.alert_manager import AlertConfig, AlertManager, Anomaly


class TestAlertManager:
    @pytest.fixture(autouse=True)
    def setup_manager(self):
        AlertManager._instance = None
        self.config = AlertConfig(cooldown_minutes=1)
        self.manager = AlertManager(self.config)
        return self.manager

    def test_singleton(self):
        m1 = AlertManager.instance()
        m2 = AlertManager.instance()
        assert m1 is m2

    def test_configure(self):
        self.manager.configure(enabled=False, cooldown_minutes=10)
        assert self.manager.config.enabled is False
        assert self.manager.config.cooldown_minutes == 10

    def test_should_alert_logic(self):
        anomaly_low = Anomaly(type="error_spike", severity="low", message="test low")
        anomaly_high = Anomaly(type="error_spike", severity="high", message="test high")

        # Default min_severity is high
        assert self.manager._should_alert(anomaly_low) is False
        assert self.manager._should_alert(anomaly_high) is True

        # Disabled
        self.manager.config.enabled = False
        assert self.manager._should_alert(anomaly_high) is False

    def test_should_alert_cooldown(self):
        anomaly = Anomaly(type="spike", severity="high", message="same message")

        assert self.manager._should_alert(anomaly) is True
        self.manager._record_alert(anomaly)

        # Next call should be False due to cooldown
        assert self.manager._should_alert(anomaly) is False

        # Simulate time passing
        with patch("src.core.logging.alert_manager.datetime") as mock_dt:
            # Shift now to 2 minutes later
            mock_dt.now.return_value = datetime.now(UTC) + timedelta(minutes=2)
            # Since _record_alert used real datetime.now(UTC) at the time of recording,
            # and _should_alert uses datetime.now(UTC) now.
            # I need to mock both consistently if I want to test delta.

    def test_format_alert_message(self):
        anomaly = Anomaly(
            type="slow_operation",
            severity="high",
            message="Very slow",
            suggestion="Check DB",
            details={"op": "VACUUM"},
        )
        msg = self.manager._format_alert_message(anomaly)
        assert "❌" in msg
        assert "Operazione Lenta" in msg
        assert "Very slow" in msg
        assert "Check DB" in msg
        assert "op: VACUUM" in msg

    @patch("src.core.logging.alert_manager.get_anomalies")
    def test_check_and_alert_flow(self, mock_anomalies):
        mock_anomalies.return_value = [Anomaly(type="spike", severity="high", message="Alert me")]

        # Mock Telegram
        mock_telegram = MagicMock()
        self.manager._telegram_service = mock_telegram

        count = self.manager.check_and_alert(hours=1)
        assert count == 1
        assert mock_telegram.send_message_sync.called

    def test_send_alert_manual(self):
        mock_telegram = MagicMock()
        self.manager._telegram_service = mock_telegram

        res = self.manager.send_alert("Title", "Message", level="error")
        assert res is True
        assert mock_telegram.send_message_sync.called
        assert "❌" in mock_telegram.send_message_sync.call_args[0][0]

    def test_alert_on_critical_bypass(self):
        mock_telegram = MagicMock()
        self.manager._telegram_service = mock_telegram

        critical = Anomaly(type="crash", severity="critical", message="CRASH")
        high = Anomaly(type="crash", severity="high", message="HIGH")

        assert self.manager.alert_on_critical(critical) is True
        assert self.manager.alert_on_critical(high) is False  # Only critical
