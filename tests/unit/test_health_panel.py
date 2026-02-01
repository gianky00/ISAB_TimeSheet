"""
Test per HealthPanel e componenti correlati.
Verifica che i widget si inizializzino correttamente.
"""

from unittest.mock import MagicMock, patch


class TestHealthScoreBadge:
    """Test per HealthScoreBadge widget."""

    def test_badge_initialization(self, qtbot):
        """Testa che il badge si inizializzi correttamente."""
        from src.gui.panels.health_panel import HealthScoreBadge

        badge = HealthScoreBadge(size=160)
        qtbot.addWidget(badge)

        assert badge._score == 100
        assert badge._size == 160

    def test_badge_score_setter(self, qtbot):
        """Testa il setter dello score."""
        from src.gui.panels.health_panel import HealthScoreBadge

        badge = HealthScoreBadge()
        qtbot.addWidget(badge)

        badge.score = 75
        assert badge.score == 75

        # Test clamping
        badge.score = 150
        assert badge.score == 100

        badge.score = -10
        assert badge.score == 0

    def test_badge_color_thresholds(self, qtbot):
        """Testa i colori basati su soglie."""
        from src.gui.panels.health_panel import HealthScoreBadge

        badge = HealthScoreBadge()
        qtbot.addWidget(badge)

        badge.score = 90
        assert badge._get_color().name() == "#28a745"  # Verde

        badge.score = 65
        assert badge._get_color().name() == "#ffc107"  # Giallo

        badge.score = 45
        assert badge._get_color().name() == "#fd7e14"  # Arancio

        badge.score = 30
        assert badge._get_color().name() == "#dc3545"  # Rosso

    def test_badge_status_text(self, qtbot):
        """Testa i testi di stato."""
        from src.gui.panels.health_panel import HealthScoreBadge

        badge = HealthScoreBadge()
        qtbot.addWidget(badge)

        badge.score = 90
        assert badge._get_status_text() == "OTTIMO"

        badge.score = 65
        assert badge._get_status_text() == "DISCRETO"

        badge.score = 45
        assert badge._get_status_text() == "ATTENZIONE"

        badge.score = 30
        assert badge._get_status_text() == "CRITICO"


class TestStatCard:
    """Test per StatCard widget."""

    def test_statcard_initialization(self, qtbot):
        """Testa l'inizializzazione della card."""
        from src.gui.panels.health_panel import StatCard

        card = StatCard("Test Title", "42", "🔥", "#007bff")
        qtbot.addWidget(card)

        assert card._value_label.text() == "42"

    def test_statcard_set_value(self, qtbot):
        """Testa il cambio di valore."""
        from src.gui.panels.health_panel import StatCard

        card = StatCard("Test", "0")
        qtbot.addWidget(card)

        card.set_value("100")
        assert card._value_label.text() == "100"


class TestAnomalyCard:
    """Test per AnomalyCard widget."""

    def test_anomaly_card_initialization(self, qtbot):
        """Testa la creazione della card anomalia."""
        from dataclasses import dataclass

        from src.gui.panels.health_panel import AnomalyCard

        @dataclass
        class MockAnomaly:
            type: str = "error_spike"
            severity: str = "medium"
            message: str = "Test anomaly message"
            suggestion: str = "Test suggestion"
            details: dict = None

        anomaly = MockAnomaly()
        card = AnomalyCard(anomaly)
        qtbot.addWidget(card)

        # Verifica che non sollevi eccezioni
        assert card is not None

    def test_anomaly_severity_colors(self, qtbot):
        """Testa i colori in base alla severity."""
        from dataclasses import dataclass

        from src.gui.panels.health_panel import AnomalyCard

        @dataclass
        class MockAnomaly:
            type: str = "test"
            severity: str = "low"
            message: str = "Test"
            suggestion: str = ""
            details: dict = None

        card = AnomalyCard(MockAnomaly())
        qtbot.addWidget(card)

        assert card._get_severity_color("low") == "#007bff"
        assert card._get_severity_color("medium") == "#ffc107"
        assert card._get_severity_color("high") == "#fd7e14"
        assert card._get_severity_color("critical") == "#dc3545"


class TestHealthPanel:
    """Test per HealthPanel widget."""

    @patch("src.gui.panels.health_panel.QTimer")
    def test_panel_initialization(self, mock_timer, qtbot):
        """Testa l'inizializzazione del pannello."""
        from src.gui.panels.health_panel import HealthPanel

        panel = HealthPanel()
        qtbot.addWidget(panel)

        assert panel._score_badge is not None
        assert panel._status_label is not None
        assert panel._stat_runs_ok is not None
        assert panel._stat_runs_fail is not None
        assert panel._stat_error_rate is not None
        assert panel._stat_anomalies is not None

    @patch("src.gui.panels.health_panel.QTimer")
    @patch("src.core.logging.analytics.generate_analytics_report")
    @patch("src.core.logging.viewer.LogViewer")
    def test_panel_refresh(self, mock_viewer, mock_report, mock_timer, qtbot):
        """Testa il refresh dei dati."""
        from dataclasses import dataclass

        from src.gui.panels.health_panel import HealthPanel

        @dataclass
        class MockReport:
            health_score: int = 85
            anomalies: list = None

            def __post_init__(self):
                if self.anomalies is None:
                    self.anomalies = []

        mock_report.return_value = MockReport()
        mock_viewer_instance = MagicMock()
        mock_viewer_instance.generate_health_report.return_value = {
            "bot_runs": {"successful": 10, "failed": 2},
            "error_rate_percent": 5.0,
        }
        mock_viewer.return_value = mock_viewer_instance

        panel = HealthPanel()
        qtbot.addWidget(panel)

        panel.refresh()

        assert panel._score_badge.score == 85
        assert panel._stat_runs_ok._value_label.text() == "10"
        assert panel._stat_runs_fail._value_label.text() == "2"
        assert panel._stat_error_rate._value_label.text() == "5.0%"
