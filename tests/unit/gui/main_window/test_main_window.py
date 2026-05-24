"""Unit tests for MainWindow."""

from unittest.mock import MagicMock

import pytest
from PySide6.QtWidgets import QApplication, QSystemTrayIcon

from src.gui.main_window.main import MainWindow
from src.gui.main_window.page_index import PageIndex


@pytest.fixture
def mock_all_services(mocker):
    """Mock di tutti i servizi esterni e worker per isolare MainWindow."""
    mocker.patch("src.core.audit_manager.AuditManager.instance")
    mocker.patch("src.core.telegram_manager.TelegramService")
    mocker.patch("src.core.config_manager.get_config_value", return_value="light")
    mocker.patch("src.core.config_manager.load_config", return_value={})
    mocker.patch("src.gui.styles.apply_theme")
    mocker.patch("src.gui.workers.license_worker.LicenseWorker")
    mocker.patch.object(QSystemTrayIcon, "isSystemTrayAvailable", return_value=True)


class TestMainWindow:
    """Test suite per MainWindow."""

    def test_initialization(self, qtbot, mock_all_services):
        """Verifica che MainWindow si inizializzi senza crashare."""
        window = MainWindow()
        qtbot.addWidget(window)
        assert "SyncroJob" in window.windowTitle()

    def test_navigation_delegation(self, qtbot, mock_all_services, mocker):
        """Verifica che la navigazione deleghi correttamente al controller."""
        window = MainWindow()
        qtbot.addWidget(window)
        mock_nav = mocker.patch.object(window.navigation_controller, "navigate_to")
        window.show_settings()
        mock_nav.assert_called_with(PageIndex.SETTINGS)

    def test_toast_delegation(self, qtbot, mock_all_services, mocker):
        """Verifica la visualizzazione dei toast."""
        window = MainWindow()
        qtbot.addWidget(window)
        mock_toast_mgr = mocker.patch("src.gui.widgets.toast.ToastManager.instance")
        mock_toast = MagicMock()
        mock_toast_mgr.return_value = mock_toast
        window.show_toast("Test", "success")
        mock_toast.show.assert_called_with("Test", "success")

    def test_license_heartbeat_revoked(self, qtbot, mock_all_services, mocker):
        """Verifica il comportamento in caso di licenza revocata."""
        window = MainWindow()
        qtbot.addWidget(window)
        mocker.patch("src.gui.dialogs.confirmation_dialog.ConfirmationDialog.show_error")
        mock_quit = mocker.patch.object(QApplication, "quit")
        window._on_license_check_finished(False, "LICENZA REVOCATA")
        assert window._force_quit is True
        assert mock_quit.called

    def test_switch_account_delegation(self, qtbot, mock_all_services, mocker):
        """Verifica la rotazione account."""
        window = MainWindow()
        qtbot.addWidget(window)
        mock_status_ctrl = mocker.patch.object(window.app_status_controller, "rotate_account")
        window._switch_account("isab")
        mock_status_ctrl.assert_called_with("isab")

    def test_finalize_init_flow(self, qtbot, mock_all_services, mocker):
        """Verifica il completamento dell'inizializzazione post-show."""
        window = MainWindow()
        qtbot.addWidget(window)
        mock_status_bar = mocker.patch.object(window.status_bar_component, "show_operational_state")
        window.finalize_init()
        assert mock_status_bar.called

    def test_close_event_minimize_to_tray(self, qtbot, mock_all_services, mocker):
        """Verifica la riduzione a tray alla chiusura se abilitata."""
        mocker.patch("src.core.config_manager.get_config_value", return_value=True)
        window = MainWindow()
        qtbot.addWidget(window)
        window.show()
        event = MagicMock()
        window.closeEvent(event)
        assert window.isHidden()
        assert event.ignore.called

    def test_close_event_actual_exit(self, qtbot, mock_all_services, mocker):
        """Verifica lbl'uscita reale con conferma."""
        mocker.patch("src.core.config_manager.get_config_value", return_value=False)
        mocker.patch("src.gui.dialogs.confirmation_dialog.ConfirmationDialog.confirm", return_value=True)
        window = MainWindow()
        qtbot.addWidget(window)
        mock_service_ctrl = mocker.patch.object(window, "service_controller")
        event = MagicMock()
        window.closeEvent(event)
        assert mock_service_ctrl.stop_all.called
        assert event.accept.called

    def test_trigger_pdl_print(self, qtbot, mock_all_services, mocker):
        """Verifica il trigger della stampa PDL."""
        window = MainWindow()
        qtbot.addWidget(window)
        mock_nav_panel = mocker.patch.object(window.navigation_controller, "navigate_to_panel")
        window.pdl_panel = MagicMock()
        window.trigger_pdl_print(["PDL1"])
        mock_nav_panel.assert_called_with("scarico_pdl")
        window.pdl_panel.set_pdl_list.assert_called_with(["PDL1"])

    def test_shortcuts_manual_trigger(self, qtbot, mock_all_services, mocker):
        """Verifica lbl'attivazione degli shortcut tramite segnale diretto."""
        window = MainWindow()
        qtbot.addWidget(window)
        mock_bug = mocker.patch.object(window, "_open_bug_reporter")
        # Attiviamo manualmente lo shortcut
        window.bug_shortcut.activated.emit()
        assert mock_bug.called
