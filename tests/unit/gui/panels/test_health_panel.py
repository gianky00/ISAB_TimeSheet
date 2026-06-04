"""Unit tests for HealthPanel."""

from unittest.mock import MagicMock

import pytest
from PySide6.QtGui import QColor

from src.application.services.logging.analytics import Anomaly
from src.gui.panels.health_panel import AnomalyCard, HealthPanel, HealthScoreBadge, StatCard
from src.gui.styles import COLORS


@pytest.fixture
def mock_health_data():
    """Dati di test per il pannello health."""
    return {
        "health_score": 85,
        "bot_runs_ok": 50,
        "bot_runs_fail": 2,
        "error_rate": 4.0,
        "timestamp": "24/05/2026 16:00",
        "anomalies": [
            Anomaly(type="error_spike", message="Test high", severity="high", suggestion="Fix it"),
            Anomaly(type="slow_operation", message="Test low", severity="low", suggestion=None),
        ],
    }


class TestHealthPanel:
    """Test suite per HealthPanel."""

    def test_initialization(self, qtbot):
        """Verifica lbl'inizializzazione corretta."""
        panel = HealthPanel()
        qtbot.addWidget(panel)

        assert panel._score_badge is not None
        assert panel._refresh_timer.isActive()
        assert panel._alert_timer.isActive()

    def test_on_health_data_ready(self, qtbot, mock_health_data):
        """Verifica lbl'aggiornamento UI alla ricezione dei dati."""
        panel = HealthPanel()
        qtbot.addWidget(panel)

        panel._on_health_data_ready(mock_health_data)

        assert panel._score_badge.score == 85
        assert panel._stat_runs_ok.val_lbl.text() == "50"
        assert panel._stat_error_rate.val_lbl.text() == "4.0%"
        assert "2 problemi" in panel._anomaly_count_label.text()

        # Verifica creazione card anomalie (2 card + 1 stretch)
        assert panel._anomalies_layout.count() == 3

    def test_refresh_trigger(self, qtbot, mocker):
        """Verifica lbl'avvio del worker al refresh."""
        mock_worker_cls = mocker.patch("src.gui.panels.health_panel.HealthWorker")
        mock_worker = MagicMock()
        mock_worker_cls.return_value = mock_worker

        panel = HealthPanel()
        qtbot.addWidget(panel)

        panel.refresh()

        assert mock_worker_cls.called
        assert mock_worker.start.called
        assert panel._last_update.text() == "Analisi in corso..."

    def test_send_telegram_alert(self, qtbot, mocker):
        """Verifica lbl'invio dell'alert Telegram."""
        # Mock report generation
        mock_report = MagicMock()
        mock_report.anomalies = [Anomaly(type="error_spike", message="X", severity="high")]
        mock_report.health_score = 50
        mocker.patch("src.gui.panels.health_panel.generate_analytics_report", return_value=mock_report)

        # Mock AlertManager
        mock_am = MagicMock()
        mocker.patch("src.gui.panels.health_panel.get_alert_manager", return_value=mock_am)

        # Mock Toast
        mock_toast = mocker.patch.object(panel := HealthPanel(), "_show_toast")
        qtbot.addWidget(panel)

        panel._send_telegram_alert()

        assert mock_am.send_alert.called
        assert mock_toast.called
        assert "✅" in mock_toast.call_args[0][0]

    def test_empty_anomalies_feedback(self, qtbot):
        """Verifica la visualizzazione del feedback 'Nessuna anomalia'."""
        panel = HealthPanel()
        qtbot.addWidget(panel)

        panel._update_anomalies([])

        assert "0 problemi" in panel._anomaly_count_label.text()
        # Dovrebbe esserci un frame vuoto
        from PySide6.QtWidgets import QLabel

        found_empty = False
        for i in range(panel._anomalies_layout.count()):
            w = panel._anomalies_layout.itemAt(i).widget()
            if w:
                labels = w.findChildren(QLabel)
                if any("Nessuna anomalia" in lbl.text() for lbl in labels):
                    found_empty = True
                    break
        assert found_empty


class TestHealthScoreBadge:
    """Test per il widget HealthScoreBadge."""

    def test_score_thresholds(self):
        badge = HealthScoreBadge()

        badge.score = 90
        assert badge._get_status_text() == "SISTEMA OTTIMO"
        assert badge._get_gradient() == QColor(COLORS["success_green"])

        badge.score = 70
        assert badge._get_status_text() == "SISTEMA STABILE"

        badge.score = 50
        assert badge._get_status_text() == "ATTENZIONE RICHIESTA"

        badge.score = 20
        assert badge._get_status_text() == "STATO CRITICO"
        assert badge._get_gradient() == QColor(COLORS["error_red"])

    def test_paint_event_no_crash(self, qtbot):
        """Fumo test per il paint event."""
        badge = HealthScoreBadge()
        qtbot.addWidget(badge)
        badge.update()


class TestStatCard:
    """Test per StatCard."""

    def test_set_value(self, qtbot):
        card = StatCard("Test", "0")
        qtbot.addWidget(card)
        card.set_value("100")
        assert card.val_lbl.text() == "100"


class TestAnomalyCard:
    """Test per AnomalyCard."""

    def test_severity_colors(self):
        a = Anomaly(type="error_spike", message="M", severity="critical")
        card = AnomalyCard(a)
        assert card._get_severity_color("critical") == COLORS["error_red"]
        assert card._get_severity_color("low") == COLORS["info_blue"]
