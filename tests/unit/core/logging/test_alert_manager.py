from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest

from src.core.logging.alert_manager import AlertManager, Anomaly


class TestAlertManager:
    @pytest.fixture(autouse=True)
    def reset_singleton(self):
        AlertManager._instance = None
        self.manager = AlertManager.instance()
        self.manager._telegram_service = MagicMock()
        return self.manager

    def test_configure(self):
        self.manager.configure(enabled=False, error_rate_threshold=50.0)
        assert self.manager.config.enabled is False
        assert self.manager.config.error_rate_threshold == 50.0

    def test_should_alert_pass(self):
        anomaly = Anomaly(type="error_spike", severity="high", message="Too many errors")
        assert self.manager._should_alert(anomaly) is True

    def test_should_alert_disabled(self):
        self.manager.config.enabled = False
        anomaly = Anomaly(type="error_spike", severity="high", message="M")
        assert self.manager._should_alert(anomaly) is False

    def test_should_alert_min_severity(self):
        self.manager.config.min_severity = "critical"
        anomaly = Anomaly(type="error_spike", severity="high", message="M")
        assert self.manager._should_alert(anomaly) is False

        anomaly_crit = Anomaly(type="unusual_pattern", severity="critical", message="M")
        assert self.manager._should_alert(anomaly_crit) is True

    def test_should_alert_cooldown(self):
        anomaly = Anomaly(type="type1", severity="high", message="Msg")
        self.manager._record_alert(anomaly)

        # Secondo tentativo immediato -> False
        assert self.manager._should_alert(anomaly) is False

        # Dopo cooldown -> True
        with patch("src.core.logging.alert_manager.datetime") as mock_dt:
            # Shift 31 minuti nel futuro
            future = datetime.now(UTC) + timedelta(minutes=31)
            mock_dt.now.return_value = future
            assert self.manager._should_alert(anomaly) is True

    def test_format_alert_message(self):
        anomaly = Anomaly(
            type="slow_operation",
            severity="high",
            message="Slow",
            suggestion="Fix it",
            details={"op": "backup", "time": "40s"},
        )
        msg = self.manager._format_alert_message(anomaly)
        assert "ALERT SyncroJob" in msg
        assert "Operazione Lenta" in msg
        assert "Fix it" in msg
        assert "op: backup" in msg

    def test_send_alert_manual(self):
        res = self.manager.send_alert("Title", "Body", level="warning")
        assert res is True
        args = self.manager._telegram_service.send_message_sync.call_args[0][0]
        assert "Title" in args
        assert "⚠️" in args

    @patch("src.core.logging.alert_manager.get_anomalies")
    def test_check_and_alert(self, mock_get):
        a1 = Anomaly(type="t1", severity="high", message="m1")
        a2 = Anomaly(type="t2", severity="low", message="m2")  # Sotto soglia
        mock_get.return_value = [a1, a2]

        count = self.manager.check_and_alert(hours=1)
        assert count == 1
        assert self.manager._telegram_service.send_message_sync.call_count == 1

    def test_alert_on_critical(self):
        a_high = Anomaly(type="t", severity="high", message="m")
        assert self.manager.alert_on_critical(a_high) is False

        a_crit = Anomaly(type="t", severity="critical", message="m")
        assert self.manager.alert_on_critical(a_crit) is True
        assert self.manager._telegram_service.send_message_sync.called
