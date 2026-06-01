"""Unit tests for NotificationsPanel."""

from datetime import UTC, datetime, timedelta

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from src.core.notification_manager import NotificationManager
from src.gui.panels.notifications_panel import NotificationsPanel


@pytest.fixture
def mock_notifs():
    """Dati di test per le notifiche."""
    now = datetime.now(UTC)
    return [
        {
            "id": "1",
            "title": "Errore Test",
            "message": "Qualcosa è andato storto",
            "level": "error",
            "timestamp": now.isoformat(),
            "read": False,
            "priority": "high",
        },
        {
            "id": "2",
            "title": "Avviso Ieri",
            "message": "Attenzione ai dati",
            "level": "warning",
            "timestamp": (now - timedelta(days=1)).isoformat(),
            "read": True,
            "priority": "medium",
        },
    ]


@pytest.fixture
def panel(qtbot, mocker, mock_notifs):
    """Istanza di NotificationsPanel per i test."""
    mgr = NotificationManager.instance()
    mocker.patch.object(mgr, "notifications", mock_notifs)
    mocker.patch.object(mgr, "get_notifications", return_value=mock_notifs)

    p = NotificationsPanel()
    p.setAttribute(Qt.WidgetAttribute.WA_DontShowOnScreen)
    p.show()
    qtbot.addWidget(p)
    return p


class TestNotificationsPanel:
    """Test suite per NotificationsPanel."""

    def test_initialization(self, panel):
        """Verifica lbl'inizializzazione corretta."""
        assert panel.tabs.count() == 3
        assert panel.tabs.tabText(0) == "Notifiche"

    def test_filter_unread(self, qtbot, panel, mocker):
        """Verifica il filtraggio 'Non lette'."""
        mgr = NotificationManager.instance()
        unread_only = [n for n in mgr.notifications if not n["read"]]
        mocker.patch.object(mgr, "get_notifications", return_value=unread_only)

        panel._on_filter_changed("unread")
        panel.refresh_notifications()

        assert "today" in panel._group_widgets
        assert len(panel._group_widgets) == 1

    def test_group_toggling(self, qtbot, panel):
        """Verifica lbl'espansione e contrazione dei gruppi."""
        panel.refresh_notifications()
        QApplication.processEvents()

        group_key = "today"
        container = panel._group_widgets[group_key]["container"]
        # In un ambiente di test headless/offscreen, i widget potrebbero non
        # attivare isVisible() correttamente, ma isHidden() dovrebbe riflettere lo stato.

        # Forza il widget a mostrare il suo stato desiderato
        container.show()
        assert not container.isHidden()

        # Toggle off (Simuliamo lbl'evento click sull'header)
        header = panel._group_widgets[group_key]["header"]
        qtbot.mouseClick(header, Qt.MouseButton.LeftButton)

        assert container.isHidden()

        # Toggle on
        qtbot.mouseClick(header, Qt.MouseButton.LeftButton)
        assert not container.isHidden()

    def test_tab_change_refresh(self, qtbot, panel, mocker):
        """Verifica che il cambio tab triggeri il refresh dei componenti."""
        mock_audit_refresh = mocker.patch.object(panel.audit_tab, "refresh")
        mock_health_refresh = mocker.patch.object(panel.health_tab, "refresh")

        panel.tabs.setCurrentIndex(1)
        assert mock_audit_refresh.called

        panel.tabs.setCurrentIndex(2)
        assert mock_health_refresh.called

    def test_clear_all_confirmed(self, qtbot, panel, mocker):
        """Verifica la pulizia totale."""
        from PySide6.QtWidgets import QMessageBox

        mocker.patch.object(QMessageBox, "question", return_value=QMessageBox.StandardButton.Yes)
        mock_clear = mocker.patch.object(NotificationManager.instance(), "clear_all")

        panel._clear_notifications()
        assert mock_clear.called

    def test_sort_logic(self, panel):
        """Verifica ordinamento."""
        notifs = [
            {"id": "1", "timestamp": "2026-05-24T10:00:00", "priority": "high", "level": "error"},
            {"id": "2", "timestamp": "2026-05-24T09:00:00", "priority": "low", "level": "info"},
        ]
        panel.current_sort = "priority"
        res = panel._sort_notifications(notifs)
        assert res[0]["priority"] == "high"
