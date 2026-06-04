"""Unit tests for SecurityDashboard."""

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QMessageBox

from src.gui.widgets.security_dashboard import SecurityDashboard


@pytest.fixture
def mock_audit_manager(mocker):
    """Fixture per mockare AuditManager."""
    mock_mgr = mocker.patch("src.application.services.audit_manager.AuditManager.instance")
    instance = mocker.MagicMock()
    mock_mgr.return_value = instance
    return instance


class TestSecurityDashboard:
    """Test suite per SecurityDashboard."""

    def test_initialization(self, qtbot, mock_audit_manager):
        """Verifica lbl'inizializzazione della dashboard."""
        widget = SecurityDashboard()
        qtbot.addWidget(widget)

        assert widget.windowTitle() == ""
        assert widget.timer.isActive()
        assert widget.kpi_layout is not None
        assert widget.chart_container is not None

    def test_refresh_populates_data(self, qtbot, mock_audit_manager):
        """Verifica che il refresh popoli correttamente i dati."""
        # Configurazione mock dati
        mock_audit_manager.get_stats_by_day.return_value = {
            "2026-05-24": {"success": 10, "error": 2, "warning": 1},
            "2026-05-23": {"success": 5, "error": 0, "warning": 0},
        }
        mock_audit_manager.get_filtered_logs.return_value = (
            [{"timestamp": "2026-05-24 10:00:00", "action": "Test action", "level": "error"}],
            1,
        )

        widget = SecurityDashboard()
        qtbot.addWidget(widget)

        widget.refresh()

        # Verifica KPI (3 card: Success Rate, Errori, Warning)
        assert widget.kpi_layout.count() == 3

        # Verifica Chart (2 barre per i 2 giorni)
        assert widget.chart_container.count() == 2

        # Verifica Logs (1 riga di log)
        assert widget.log_layout.count() == 1

    def test_success_rate_calculation(self, qtbot, mock_audit_manager):
        """Verifica il calcolo della percentuale di successo."""
        mock_audit_manager.get_stats_by_day.return_value = {
            "day1": {"success": 8, "error": 2, "warning": 0}  # 8/10 = 80%
        }
        mock_audit_manager.get_filtered_logs.return_value = ([], 0)

        widget = SecurityDashboard()
        qtbot.addWidget(widget)
        widget.refresh()

        # La prima card KPI deve contenere "80.0%"
        rate_card = widget.kpi_layout.itemAt(0).widget()
        labels = rate_card.findChildren(QLabel)
        value_label = next(lbl for lbl in labels if "%" in lbl.text())
        assert value_label.text() == "80.0%"

    def test_empty_logs_fallback(self, qtbot, mock_audit_manager):
        """Verifica il messaggio di fallback quando non ci sono log."""
        mock_audit_manager.get_stats_by_day.return_value = {}
        mock_audit_manager.get_filtered_logs.return_value = ([], 0)

        widget = SecurityDashboard()
        qtbot.addWidget(widget)
        widget.refresh()

        # Dovrebbe esserci una label con il messaggio di fallback
        assert widget.log_layout.count() == 1
        label = widget.log_layout.itemAt(0).widget()
        assert "Nessun evento critico" in label.text()

    def test_integrity_check_trigger(self, qtbot, mock_audit_manager, mocker):
        """Verifica lbl'avvio del controllo di integrità."""
        # Mock IntegrityWorker
        mock_worker_cls = mocker.patch("src.gui.widgets.security_dashboard.IntegrityWorker")
        mock_worker = mocker.MagicMock()
        mock_worker_cls.return_value = mock_worker

        widget = SecurityDashboard()
        qtbot.addWidget(widget)

        # Cerchiamo il bottone e lo clicchiamo
        btn = widget.findChild(pytest.importorskip("src.gui.widgets.core_widgets").PrimaryButton)
        qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)

        assert mock_worker_cls.called

    def test_on_integrity_checked_dialog(self, qtbot, mocker):
        """Verifica la visualizzazione del dialog al termine del controllo."""
        widget = SecurityDashboard()
        qtbot.addWidget(widget)

        # Mock QMessageBox
        mock_info = mocker.patch.object(QMessageBox, "information")
        mock_warn = mocker.patch.object(QMessageBox, "warning")

        # Caso successo
        widget._on_integrity_checked(True)
        assert mock_info.called

        # Caso fallimento
        widget._on_integrity_checked(False)
        assert mock_warn.called
