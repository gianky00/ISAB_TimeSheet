from unittest.mock import MagicMock

import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QWidget

from src.gui.panels.dashboard_panel import DashboardPanel
from src.gui.widgets.activity_feed import ActivityFeed
from src.gui.widgets.quick_actions import QuickActions


class TestDashboardComponents:
    def test_quick_actions_signals(self, qapp, qtbot):  # noqa: ANN001
        widget = QuickActions()
        qtbot.addWidget(widget)
        with qtbot.waitSignal(widget.action_clicked, timeout=1000) as blocker:
            tgt_btn = None
            layout = widget.chips_layout
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item and item.widget() and "Scarico" in item.widget().text():
                    tgt_btn = item.widget()
                    break
            assert tgt_btn is not None
            qtbot.mouseClick(tgt_btn, Qt.MouseButton.LeftButton)
        assert blocker.args is not None

    def test_activity_feed_refresh(self, qapp, mocker):  # noqa: ANN001
        # Patch corretta della fonte del singleton
        mock_audit = mocker.patch("src.core.audit_manager.AuditManager.instance")
        mock_audit.return_value.get_logs.return_value = [
            {"action": "A", "entity": "E", "status": "success", "timestamp": "2023-01-01"}
        ]
        feed = ActivityFeed()
        feed.refresh_feed()
        all_text = [lbl.text() for lbl in feed.findChildren(QLabel)]
        assert any("A" in t for t in all_text)


class TestDashboardPanelFull:
    @pytest.fixture
    def mock_dashboard_deps(self, mocker):  # noqa: ANN001
        # Patch centralizzato della configurazione
        mocker.patch("src.core.config_manager.get_config_value", return_value={})
        mocker.patch("src.core.audit_manager.AuditManager.get_logs", return_value=[])

        # Mock PDL e Database
        mocker.patch("src.core.database.pdl_queries.PDLQueries.get_all_pdl", return_value=[])
        mocker.patch("src.core.database.db_manager.get_connection")

        # Mock WIDGET CRITICI (Don Ciro e Meteo) per evitare crash grafici/rete
        mocker.patch("src.gui.widgets.dashboard.don_ciro_widget.DonCiroWidget", return_value=QWidget())
        mocker.patch("src.gui.widgets.dashboard.weather_widget.WeatherWidget", return_value=QWidget())

    @pytest.mark.skip(
        reason="Crash nativo in ambiente headless Windows dovuto a rendering complesso (Don Ciro/Weather)."
    )
    def test_dashboard_initialization(self, qapp, mock_dashboard_deps, qtbot):  # noqa: ANN001
        """Verifica che la dashboard si inizializzi senza crash."""
        panel = DashboardPanel()
        qtbot.addWidget(panel)
        assert hasattr(panel, "activity_feed")
        assert hasattr(panel, "quick_actions")

    @pytest.mark.skip(
        reason="Crash nativo in ambiente headless Windows dovuto a rendering complesso (Don Ciro/Weather)."
    )
    def test_dashboard_quick_action_integration(self, qapp, mock_dashboard_deps, qtbot, mocker):  # noqa: ANN001
        """Verifica l'integrazione della navigazione tramite Quick Action."""
        panel = DashboardPanel()
        mw_mock = MagicMock()
        mw_mock.navigation_controller = MagicMock()
        mocker.patch.object(panel, "window", return_value=mw_mock)

        # Simuliamo il click su Lyra AI
        panel._handle_quick_action("nav_page_2")
        mw_mock.navigation_controller.navigate_to.assert_called_with(2)
