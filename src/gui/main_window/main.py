# mypy: disable-error-code="no-untyped-def, no-untyped-call, arg-type, attr-defined, misc, no-redef"
"""
SyncroJob - Main Window
Finestra principale dell'applicazione che coordina tutti i servizi, i controller e i componenti dell'interfaccia utente.
Refactored V9.0: Orchestration with modular Workflow and Monitoring Controllers.
"""

from __future__ import annotations

import logging
from typing import Any

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QMainWindow,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.core.app_updater import (
    get_local_setup_path,
    get_pending_installer_path,
    has_pending_update,
    perform_auto_update,
    run_pending_installer,
    show_install_prompt,
)
from src.core.audit_manager import AuditManager
from src.core.license_updater import run_update
from src.core.telegram_bridge import TelegramUIBridge
from src.core.telegram_manager import TelegramService
from src.core.version import __version__ as VERSION  # noqa: N812
from src.gui.components.animated_stack import SlidingStackedWidget
from src.gui.controllers.bot_controller import BotController
from src.gui.controllers.navigation_controller import NavigationController
from src.gui.controllers.search_controller import SearchController
from src.gui.controllers.service_controller import ServiceController
from src.gui.dialogs.bug_report_dialog import BugReportDialog
from src.gui.dialogs.confirmation_dialog import ConfirmationDialog
from src.gui.styles import apply_theme
from src.gui.widgets.toast import ToastManager

from .components.menu_bar import MenuBarComponent

# Components
from .components.status_bar import StatusBarComponent
from .components.tool_bar import ToolBarComponent
from .components.tray_icon import TrayIconComponent
from .controllers.app_event_handler import AppEventHandler
from .controllers.monitoring_controller import MonitoringController
from .controllers.signal_connector import SignalConnector
from .controllers.workflow_controller import WorkflowController
from .page_index import PageIndex

logger = logging.getLogger("MainWindow")


class MainWindow(QMainWindow):
    """
    Finestra principale dell'applicazione (Facade).
    Coordina i componenti modulari e i controller, fungendo da punto centrale di orchestrazione.
    """

    # Pannelli registrati dinamicamente (per static analysis)
    dettagli_panel: Any
    prenota_panel: Any
    scarico_panel: Any
    timbrature_bot_panel: Any
    carico_panel: Any
    pdl_panel: Any
    pdl_search_panel: Any
    tab_fornitori: Any
    tab_safework: Any

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"SyncroJob v{VERSION}")

        self.setMinimumSize(1200, 800)
        self._force_quit = False
        self._init_core_services()
        self._init_ui_components()
        self._init_controllers()

        self._setup_ui_layout()
        self._init_ui_final()

    def _init_core_services(self) -> None:
        """Inizializzazione dei servizi fondamentali."""
        self.audit_manager = AuditManager.instance()
        self.telegram = TelegramService()

    def _init_ui_components(self) -> None:
        """Inizializzazione dei componenti UI modulari."""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.stacked_widget = SlidingStackedWidget()

        self.tool_bar_component = ToolBarComponent(self)
        self.menu_bar_component = MenuBarComponent(self)
        self.status_bar_component = StatusBarComponent(self)
        self.tray_icon_component = TrayIconComponent(self)

    def _init_controllers(self) -> None:
        """Inizializzazione dei controller di orchestrazione."""
        self.navigation_controller = NavigationController(self)
        self.bot_controller = BotController(self, self.telegram)
        self.search_controller = SearchController(self)
        self.service_controller = ServiceController(self, self.telegram)
        self.workflow_controller = WorkflowController(self)
        self.monitoring_controller = MonitoringController(self)
        self.app_event_handler = AppEventHandler(self)
        self.telegram_bridge = TelegramUIBridge(self)

    def _init_ui_final(self) -> None:
        """Wiring finale, shortcuts e avvio servizi."""
        self.signal_connector = SignalConnector(self)
        self.signal_connector.connect_all()
        self.telegram_bridge.setup_connections()

        # Applica Tema Default
        if app_instance := QApplication.instance():
            apply_theme(app_instance, config_manager.get_config_value("theme", "light"))

        self._setup_shortcuts()
        self.service_controller.start_all()
        self.navigation_controller.navigate_to(PageIndex.DASHBOARD)

        # License Heartbeat
        self._license_timer = QTimer(self)
        self._license_timer.timeout.connect(self._check_license_heartbeat)
        self._license_timer.start(14400000)

    def _check_license_heartbeat(self) -> None:
        """Esegue una sincronizzazione silente della licenza in background."""
        try:
            # run_update() solleva Exception("REVOCATA...") se la licenza è stata rimossa
            run_update()
        except Exception as e:
            if "REVOCATA" in str(e):
                self._license_timer.stop()
                ConfirmationDialog.show_error(
                    self,
                    "Licenza Revocata",
                    "La licenza è stata revocata dal server.\nL'applicazione verrà chiusa.",
                )
                self._force_quit = True
                QApplication.quit()

    def finalize_init(self) -> None:
        """Metodo chiamato per finalizzare l'inizializzazione dopo la visualizzazione della finestra."""
        try:
            logger.info("Finalizing UI state...")
            self.status_bar_component.show_operational_state()

            # Connect Footer Signals for Account Switching
            self.status_bar_component.footer_left.portale_clicked.connect(
                lambda: self._switch_account("isab")
            )
            self.status_bar_component.footer_left.safework_clicked.connect(
                lambda: self._switch_account("safework")
            )

            # Check for system tray support
            if not QSystemTrayIcon.isSystemTrayAvailable():
                logger.warning("System tray non disponibile su questo sistema.")

            # Check for updates on startup
            QTimer.singleShot(5000, self._check_updates_startup)

        except Exception:
            logger.exception("Errore durante la finalizzazione dell'interfaccia")

    def _setup_ui_layout(self) -> None:
        """Configura il layout principale con lo StackedWidget animato come overlay."""
        self.main_layout = QGridLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 1. Content Area
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(10, 10, 10, 10)

        (
            self.update_banner,
            self.global_search,
        ) = self.tool_bar_component.setup_content_toolbar(self.content_layout)

        self.content_layout.addWidget(self.stacked_widget)
        self.main_layout.addWidget(self.content_area, 0, 0)

        # 2. Sidebar come Overlay
        from src.gui.widgets.sidebar_widget import SidebarWidget  # noqa: PLC0415
        self.sidebar = SidebarWidget(self.central_widget)
        self.main_layout.addWidget(self.sidebar, 0, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.sidebar.raise_()

    def _setup_shortcuts(self) -> None:
        """Configura gli shortcut globali dell'applicazione."""
        # Alt+X per chiusura rapida
        self.quit_shortcut = QShortcut(QKeySequence("Alt+X"), self)
        self.quit_shortcut.activated.connect(self.close)

        # Ctrl+Shift+B per segnalazione bug rapida
        self.bug_shortcut = QShortcut(QKeySequence("Ctrl+Shift+B"), self)
        self.bug_shortcut.activated.connect(self._open_bug_reporter)

    def _open_bug_reporter(self) -> None:
        """Apre il dialogo di segnalazione bug."""
        dialog = BugReportDialog(self)
        dialog.exec()

    def _check_updates_startup(self) -> None:
        """Controlla se ci sono aggiornamenti pendenti o nuovi al boot."""
        if has_pending_update():
            path = get_pending_installer_path()
            if path:
                show_install_prompt(path, self)

    def _show_update_banner(self, version_info: dict[str, Any]) -> None:
        """Mostra il banner di aggiornamento nella toolbar."""
        if hasattr(self, "tool_bar_component") and self.tool_bar_component.update_banner:
            # Allineamento firma show_update(download_url, version_str)
            download_url = version_info.get("url", "")
            version_str = version_info.get("version", "")
            if download_url and version_str:
                self.update_banner.show_update(version_str, download_url)

    def _on_download_update_clicked(self, download_url: str) -> None:
        """Avvia il processo di download dell'aggiornamento con protezione da eccezioni."""
        try:
            # Se il banner indica che è già completo, mostra direttamente la prompt di installazione
            if hasattr(self, "update_banner") and getattr(self.update_banner, "_is_complete", False):
                setup_path = get_local_setup_path(download_url)
                show_install_prompt(setup_path, self)
                return

            perform_auto_update(download_url, self)
        except Exception as e:
            logger.exception("Inizializzazione download fallita")
            ToastManager.instance().show(f"Errore inizializzazione update: {e}", "error")

    def _on_update_error(self, message: str) -> None:
        """Gestisce errori durante lo scaricamento dell'aggiornamento."""
        if hasattr(self, "update_banner"):
            self.update_banner.show_error(message)
        ToastManager.instance().show(f"Errore download: {message}", "error")

    def _on_update_downloaded(self, setup_path: str) -> None:
        """Gestisce il completamento del download dell'aggiornamento."""
        if hasattr(self, "update_banner"):
            self.update_banner._is_complete = True
            self.update_banner.update_label.setText("Aggiornamento Pronto!")
            self.update_banner.download_btn.setText("Installa Ora")
            self.update_banner.download_btn.setVisible(True)
            self.update_banner.progress_container.setVisible(False)

        show_install_prompt(setup_path, self)

    def show_background_notification(self, title: str, message: str, is_error: bool = False) -> None:
        """Mostra una notifica balloon se l'app è in background."""
        if hasattr(self, "tray_icon_component"):
            self.tray_icon_component.show_background_notification(title, message, is_error)

    def _switch_account(self, bot_type: str) -> None:
        """Ruota l'account attivo per il portale specificato."""
        if config_manager.switch_default_account(bot_type):
            self.status_bar_component.show_operational_state()
            if hasattr(self.status_bar_component, "footer_left") and hasattr(self.status_bar_component.footer_left, "refresh_accounts"):
                self.status_bar_component.footer_left.refresh_accounts()
            ToastManager.instance().show(f"Account {bot_type.upper()} ruotate con successo.", "success")
        else:
            ToastManager.instance().show(f"Impossibile ruotare account {bot_type.upper()}.", "warning")

    def show_toast(self, message: str, level: str = "info") -> None:
        """
        Visualizza un messaggio toast.

        Args:
            message: Il messaggio da visualizzare.
            level: Livello del messaggio (info, success, warning, error).
        """
        ToastManager.instance().show(message, level)

    def closeEvent(self, event: Any) -> None:
        """Gestisce la chiusura della finestra (riduzione a tray o uscita)."""
        if self._force_quit:
            self.service_controller.stop_all()
            event.accept()
            return

        # Verifica impostazione "Chiudi in Tray"
        minimize_to_tray = config_manager.get_config_value("minimize_to_tray", True)

        if minimize_to_tray and QSystemTrayIcon.isSystemTrayAvailable():
            self.hide()
            self.tray_icon_component.show_message(
                "SyncroJob è ancora attivo", "L'applicazione è stata ridotta nella barra di sistema."
            )
            event.ignore()
        else:
            # Chiusura reale
            confirm = ConfirmationDialog.confirm(
                self,
                "Uscita",
                "Sei sicuro di voler chiudere SyncroJob?\nTutti i bot attivi verranno fermati.",
            )
            if confirm:
                self.service_controller.stop_all()
                # Esegue l'installer se c'è un aggiornamento pendente scaricato
                run_pending_installer()
                event.accept()
            else:
                event.ignore()
