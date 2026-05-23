from unittest.mock import patch

from PySide6.QtGui import QColor

from src.gui.styles import COLORS


class TestHealthScoreBadge:
    """Test per HealthScoreBadge widget."""

    def test_badge_initialization(self, qtbot):
        from src.gui.panels.health_panel import HealthScoreBadge

        badge = HealthScoreBadge(size=160)
        qtbot.addWidget(badge)
        assert badge._score == 100
        assert badge._size == 160

    def test_badge_score_setter(self, qtbot):
        from src.gui.panels.health_panel import HealthScoreBadge

        badge = HealthScoreBadge()
        qtbot.addWidget(badge)
        badge.score = 75
        assert badge.score == 75
        badge.score = 150
        assert badge.score == 100
        badge.score = -10
        assert badge.score == 0

    def test_badge_color_thresholds(self, qtbot):
        """Testa i colori basati su soglie V9.0."""
        from src.gui.panels.health_panel import HealthScoreBadge

        badge = HealthScoreBadge()
        qtbot.addWidget(badge)

        badge.score = 90
        assert badge._get_gradient() == QColor(COLORS["success_green"])

        badge.score = 65
        assert badge._get_gradient() == QColor(COLORS["warning_yellow"])

        badge.score = 45
        assert badge._get_gradient() == QColor(COLORS["warning_orange"])

        badge.score = 30
        assert badge._get_gradient() == QColor(COLORS["error_red"])

    def test_badge_status_text(self, qtbot):
        """Testa i testi di stato V9.0."""
        from src.gui.panels.health_panel import HealthScoreBadge

        badge = HealthScoreBadge()
        qtbot.addWidget(badge)

        badge.score = 90
        assert "OTTIMO" in badge._get_status_text()
        badge.score = 30
        assert "CRITICO" in badge._get_status_text()


class TestStatCard:
    def test_statcard_initialization(self, qtbot):
        from src.gui.panels.health_panel import StatCard

        card = StatCard("Test", "42")
        qtbot.addWidget(card)
        assert card.val_lbl.text() == "42"

    def test_statcard_set_value(self, qtbot):
        from src.gui.panels.health_panel import StatCard

        card = StatCard("Test", "0")
        qtbot.addWidget(card)
        card.set_value("100")
        assert card.val_lbl.text() == "100"


class TestAnomalyCard:
    def test_anomaly_card_initialization(self, qtbot):
        from dataclasses import dataclass

        from src.gui.panels.health_panel import AnomalyCard

        @dataclass
        class MockAnomaly:
            severity: str = "medium"
            message: str = "Test"
            suggestion: str = "Suggest"

        card = AnomalyCard(MockAnomaly())
        qtbot.addWidget(card)
        assert card is not None

    def test_anomaly_severity_colors(self, qtbot):
        from dataclasses import dataclass

        from src.gui.panels.health_panel import AnomalyCard

        @dataclass
        class MockAnomaly:
            severity: str = "low"
            message: str = "T"
            suggestion: str = ""

        card = AnomalyCard(MockAnomaly())
        assert card._get_severity_color("low") == COLORS["info_blue"]
        assert card._get_severity_color("critical") == COLORS["error_red"]


class TestHealthPanel:
    @patch("src.gui.panels.health_panel.QTimer")
    def test_panel_initialization(self, mock_timer, qtbot):
        from src.gui.panels.health_panel import HealthPanel

        panel = HealthPanel()
        qtbot.addWidget(panel)
        assert panel._score_badge is not None
        assert panel._stat_runs_ok is not None

    @patch("src.gui.panels.health_panel.QTimer")
    @patch("src.gui.panels.health_panel.generate_analytics_report")
    def test_panel_refresh(self, mock_report, mock_timer, qtbot):
        from dataclasses import dataclass

        from src.gui.panels.health_panel import HealthPanel

        @dataclass
        class MockReport:
            health_score: int = 85
            anomalies: list = None
            bot_runs_ok: int = 10
            bot_runs_fail: int = 2
            error_rate: float = 5.0
            timestamp: str = "2024-01-01 10:00"

            def __post_init__(self):
                if self.anomalies is None:
                    self.anomalies = []

        mock_report.return_value = MockReport()

        panel = HealthPanel()
        # Mocking the worker to avoid real thread execution in this unit test
        panel._on_health_data_ready(
            {
                "health_score": 85,
                "bot_runs_ok": 10,
                "bot_runs_fail": 2,
                "error_rate": 5.0,
                "anomalies": [],
                "timestamp": "2024-01-01 10:00",
            }
        )

        assert panel._score_badge.score == 85
        assert panel._stat_runs_ok.val_lbl.text() == "10"
