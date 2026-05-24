"""Unit tests for BotSavingsWidget (ROI)."""

from unittest.mock import MagicMock

import pytest

from src.core.stats.roi_engine import ROIMetrics
from src.gui.widgets.dashboard.roi_widget import BotSavingsWidget


@pytest.fixture
def mock_roi_metrics():
    """Mock delle metriche ROI."""
    return ROIMetrics(
        total_minutes_saved=1000,
        net_minutes_saved=900,
        total_operations=50,
        success_rate=95.5,
        reliability_score=98,
        total_days=30,
        trend_percentage=12.5,
        top_task_name="Bot A",
        top_task_pct=40.0,
        top_tasks=[("Bot A", 40.0), ("Bot B", 30.0)],
    )


class TestBotSavingsWidget:
    """Test suite per BotSavingsWidget."""

    def test_initialization(self, qtbot):
        """Verifica lbl'inizializzazione del widget."""
        widget = BotSavingsWidget()
        qtbot.addWidget(widget)

        assert "EFFICIENZA" in widget.lbl_title.text()
        assert widget.progress_success is not None
        assert widget.progress_rel is not None

    def test_update_ui(self, qtbot, mock_roi_metrics):
        """Verifica lbl'aggiornamento UI con nuove metriche."""
        widget = BotSavingsWidget()
        qtbot.addWidget(widget)

        widget._update_ui(mock_roi_metrics)

        # Tempo risparmiato
        assert widget.lbl_time.text() != "Calcolo..."

        # Task completati
        assert widget.lbl_ops.text() == "50"

        # Percentuali
        assert "95.5%" in widget.lbl_success_pct.text()
        assert "98%" in widget.lbl_rel_pct.text()

        # Progress bars (utilizzando il metodo value())
        assert widget.progress_success.value() == 95
        assert widget.progress_rel.value() == 98

    def test_trend_styling(self, qtbot, mock_roi_metrics):
        """Verifica il colore del trend."""
        from src.gui.styles import COLORS

        widget = BotSavingsWidget()
        qtbot.addWidget(widget)

        # Trend positivo -> Successo
        widget._update_ui(mock_roi_metrics)
        assert COLORS["success_dark"] in widget.lbl_trend.styleSheet()

        # Trend negativo
        from dataclasses import replace

        metrics_neg = replace(mock_roi_metrics, trend_percentage=-5.0)
        widget._update_ui(metrics_neg)
        assert COLORS["error_red"] in widget.lbl_trend.styleSheet()

    def test_refresh_stats_trigger(self, qtbot, mocker):
        """Verifica lbl'avvio del worker ROI."""
        mock_worker_cls = mocker.patch("src.gui.widgets.dashboard.roi_widget.ROIWorker")
        mock_worker = MagicMock()
        mock_worker_cls.return_value = mock_worker

        widget = BotSavingsWidget()
        qtbot.addWidget(widget)

        widget.refresh_stats()

        assert mock_worker_cls.called
        assert mock_worker.start.called
