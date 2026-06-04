"""Unit tests for AuditLogWidget."""

from unittest.mock import MagicMock

import pytest

from src.gui.widgets.audit_log_widget import AuditLogWidget


@pytest.fixture
def mock_audit_manager(mocker):
    """Fixture per mockare AuditManager."""
    mock_mgr = mocker.patch("src.application.services.audit_manager.AuditManager.instance")
    instance = MagicMock()
    instance.get_categories.return_value = ["CAT1", "CAT2"]
    instance.get_filtered_logs.return_value = (
        [
            {
                "timestamp": "2026-05-24 10:00:00",
                "action": "Action 1",
                "category": "CAT1",
                "level": "info",
                "user": "test",
            }
        ],
        1,
    )
    mock_mgr.return_value = instance
    return instance


@pytest.fixture
def widget(qtbot, mock_audit_manager):
    """Istanza di AuditLogWidget per i test."""
    w = AuditLogWidget()
    qtbot.addWidget(w)
    return w


class TestAuditLogWidget:
    """Test suite per AuditLogWidget."""

    def test_initialization(self, widget, mock_audit_manager):
        """Verifica lbl'inizializzazione del widget."""
        assert widget.PAGE_SIZE == 50
        assert widget.current_page == 0
        assert widget.filter_bar is not None
        assert widget.pagination_bar is not None
        assert widget.live_timer.interval() == 5000
        assert mock_audit_manager.get_categories.called

    def test_refresh_populates_data(self, qtbot, widget, mock_audit_manager):
        """Verifica che il refresh carichi i dati nel modello."""
        widget.refresh(reset_page=True)
        assert widget.total_logs == 1
        assert widget.model.rowCount() == 1
        assert mock_audit_manager.get_filtered_logs.called

    def test_toggle_live_mode(self, qtbot, widget):
        """Verifica lbl'attivazione della modalità Live."""
        widget.live_check.setChecked(True)
        assert widget.live_timer.isActive()
        widget.live_check.setChecked(False)
        assert not widget.live_timer.isActive()

    def test_pagination_navigation(self, qtbot, widget, mock_audit_manager):
        """Verifica la navigazione tra le pagine."""
        widget.total_logs = 150
        widget._on_page_changed(1)
        assert widget.current_page == 1
        widget._on_page_changed(-1)
        assert widget.current_page == 0

    def test_integrity_checked_callback(self, qtbot, widget):
        """Verifica lbl'aggiornamento UI dopo il controllo integrità."""
        widget._on_integrity_checked(True)
        assert widget.integrity_lbl.text() == "Integro"
        widget._on_integrity_checked(False)
        assert widget.integrity_lbl.text() == "Legacy/Manomesso"

    def test_row_double_click_opens_dialog(self, qtbot, widget, mocker):
        """Verifica che il doppio click apra il dettaglio."""
        mock_dialog_cls = mocker.patch("src.gui.widgets.audit_log_widget.AuditDetailDialog")
        mock_dialog = MagicMock()
        mock_dialog_cls.return_value = mock_dialog
        widget.model.update_data([{"id": 1, "msg": "test"}])
        idx = widget.model.index(0, 0)
        widget._on_row_double_click(idx)
        assert mock_dialog_cls.called
        assert mock_dialog.exec.called

    def test_filter_change_triggers_refresh(self, qtbot, widget, mocker):
        """Verifica che la modifica dei filtri scateni il refresh."""
        mock_refresh = mocker.patch.object(widget, "refresh")
        # Il segnale filters_applied richiede un argomento (QVariantMap)
        widget.filter_bar.filters_applied.emit({})
        assert mock_refresh.called
        assert mock_refresh.call_args[1]["reset_page"] is True
