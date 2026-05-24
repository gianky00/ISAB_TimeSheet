"""Unit tests for ActivityFeed widget."""

from unittest.mock import MagicMock

import pytest

from src.gui.widgets.activity_feed import ActivityFeed, ActivityItem


@pytest.fixture
def mock_audit_manager(mocker):
    """Mock di AuditManager."""
    mock_mgr = mocker.patch("src.core.audit_manager.AuditManager.instance")
    instance = MagicMock()
    # Mock segnali
    instance.signals.log_added = MagicMock()
    instance.get_logs.return_value = [
        {"timestamp": "2026-05-24T10:00:00", "action": "Action 1", "status": "success"},
        {"timestamp": "2026-05-24T09:00:00", "action": "Action 2", "status": "error"},
    ]
    mock_mgr.return_value = instance
    return instance


class TestActivityFeed:
    """Test suite per ActivityFeed."""

    def test_initialization(self, qtbot, mock_audit_manager):
        """Verifica lbl'inizializzazione del widget."""
        widget = ActivityFeed()
        qtbot.addWidget(widget)

        assert widget.height() == 90
        # Il caricamento iniziale è in un singleShot(800)
        qtbot.wait(900)

        # Dovrebbe avere 2 ActivityItem + 1 stretch
        items = widget.findChildren(ActivityItem)
        assert len(items) == 2

    def test_refresh_feed_empty(self, qtbot, mock_audit_manager):
        """Verifica lo stato vuoto."""
        mock_audit_manager.get_logs.return_value = []

        widget = ActivityFeed()
        qtbot.addWidget(widget)
        widget.refresh_feed()

        from PySide6.QtWidgets import QLabel

        labels = widget.findChildren(QLabel)
        assert any("Nessuna attività recente" in lbl.text() for lbl in labels)

    def test_on_new_log_added_signal(self, qtbot, mock_audit_manager, mocker):
        """Verifica che il segnale log_added triggeri il refresh."""
        widget = ActivityFeed()
        qtbot.addWidget(widget)

        mock_refresh = mocker.patch.object(widget, "refresh_feed")

        # Emuliamo lbl'arrivo di un segnale
        # Poiché log_added è un MagicMock() nel fixture, dobbiamo emetterlo correttamente
        # Se fosse un segnale reale useremmo .emit()
        widget._on_new_log_added({"action": "new"})

        assert mock_refresh.called

    def test_activity_item_styling(self, qtbot):
        """Verifica lo stile di un ActivityItem."""
        # Caso Successo
        item_ok = ActivityItem({"status": "success", "action": "OK"})
        assert item_ok.border_color != ""

        # Caso Errore
        item_err = ActivityItem({"status": "error", "action": "FAIL"})
        from src.gui.styles import COLORS

        assert item_err.border_color == COLORS["error_red"]

    def test_activity_item_time_formatting(self, qtbot):
        """Verifica la formattazione del tempo nell'item."""
        from datetime import datetime, timedelta

        now = datetime.now()
        entry = {"timestamp": (now - timedelta(minutes=5)).isoformat(), "action": "T"}

        item = ActivityItem(entry)
        qtbot.addWidget(item)

        from PySide6.QtWidgets import QLabel

        labels = item.findChildren(QLabel)
        time_text = labels[2].text()  # La terza label è il tempo (badge, action, time)
        assert "5 min" in time_text or "fa" in time_text  # log_humanizer output
