"""Unit tests for PDLStatsWidget."""

import pytest
from PySide6.QtCore import Qt

from src.core.stats.pdl_stats_engine import AreaStats, PDLMetrics
from src.gui.widgets.dashboard.pdl_stats_widget import AreaBadge, PDLStatsWidget


@pytest.fixture
def mock_metrics():
    """Mock delle metriche PDL."""
    area1 = AreaStats(name="Area 1", current_count=10, trend_percentage=35.0)
    area2 = AreaStats(name="Area 2", current_count=5, trend_percentage=-10.0)

    metrics = PDLMetrics(
        total_count=100,
        active_count=40,
        closed_count=60,
        trend_percentage=15.0,
        weekly_trend_percentage=5.0,
        areas_stats=[area1, area2],
        last_sync="24/05/2026 10:00",
    )
    return metrics


class TestPDLStatsWidget:
    """Test suite per PDLStatsWidget."""

    def test_initialization(self, qtbot):
        """Verifica lbl'inizializzazione del widget."""
        widget = PDLStatsWidget()
        qtbot.addWidget(widget)

        assert widget.lbl_total.text() == "0"
        assert "DATABASE PDL" in widget.lbl_title.text()

    def test_update_ui(self, qtbot, mock_metrics):
        """Verifica lbl'aggiornamento UI con nuove metriche."""
        widget = PDLStatsWidget()
        qtbot.addWidget(widget)

        widget._update_ui(mock_metrics)

        assert widget.lbl_total.text() == "100"
        assert "24/05/2026" in widget.lbl_sync.text()
        assert "+15%" in widget.lbl_trend_month.text()

        # Verifica creazione badge aree
        assert widget.area_layout.count() > 0

    def test_area_selection_signal(self, qtbot, mock_metrics):
        """Verifica lbl'emissione del segnale al click su un'area."""
        widget = PDLStatsWidget()
        qtbot.addWidget(widget)
        widget._update_ui(mock_metrics)

        # Trova il primo badge
        badge = widget.findChild(AreaBadge)
        assert badge is not None

        with qtbot.waitSignal(widget.area_selected) as blocker:
            qtbot.mouseClick(badge, Qt.MouseButton.LeftButton)

        assert blocker.args[0] == "Area 1"

    def test_trend_styling(self, qtbot):
        """Verifica i colori dei trend (Invertiti: Incremento = Rosso)."""
        from src.gui.styles import COLORS

        widget = PDLStatsWidget()
        qtbot.addWidget(widget)

        # Trend positivo -> Rosso (allerta carico)
        widget._apply_trend_style(widget.lbl_trend_month, 20.0, "Test")
        assert COLORS["error_red"] in widget.lbl_trend_month.styleSheet()

        # Trend negativo -> Verde
        widget._apply_trend_style(widget.lbl_trend_month, -10.0, "Test")
        assert COLORS["success_dark"] in widget.lbl_trend_month.styleSheet()
