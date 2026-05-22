"""
SyncroJob - Main Window
Finestra principale dell'applicazione che coordina tutti i servizi, i controller e i componenti dell'interfaccia utente.
Refactored V9.0: Orchestration with modular Workflow and Monitoring Controllers.
"""

from __future__ import annotations

import logging
from typing import Any

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QMainWindow,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.core.app_updater import (
    run_pending_installer,
)
from src.core.audit_manager import AuditManager
from src.core.telegram_bridge import TelegramUIBridge
from src.core.telegram_manager import TelegramService
from src.core.version import __version__ as VERSION  # noqa: N812
from src.gui.components.animated_stack import SlidingStackedWidget
from src.gui.controllers.app_status_controller import AppStatusController
from src.gui.controllers.bot_controller import BotController
from src.gui.controllers.navigation_controller import NavigationController
from src.gui.controllers.search_controller import SearchController
from src.gui.controllers.service_controller import ServiceController
from src.gui.controllers.update_controller import UpdateController
from src.gui.dialogs.bug_report_dialog import BugReportDialog
from src.gui.dialogs.confirmation_dialog import ConfirmationDialog
from src.gui.styles import apply_theme
from src.gui.widgets.toast import ToastManager
from src.gui.workers.license_worker import LicenseWorker

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

    @property
    def page_stack(self) -> SlidingStackedWidget:
        """Alias per stacked_widget (retrocompatibilità test)."""
        return self.stacked_widget

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
        self.update_controller = UpdateController(self)
        self.app_status_controller = AppStatusController(self)

    def _init_ui_final(self) -> None:
        """Wiring finale, shortcuts e avvio servizi."""
        self.signal_connector = SignalConnector(self)
        self.signal_connector.connect_all()
        self.telegram_bridge.setup_connections()

        # Applica Tema Default
        app_instance = QApplication.instance()
        if isinstance(app_instance, QApplication):
            apply_theme(app_instance, config_manager.get_config_value("theme", "light"))

        self._setup_shortcuts()
        self.service_controller.start_all()
        self.navigation_controller.navigate_to(PageIndex.DASHBOARD)

        # License Heartbeat
        self._license_timer = QTimer(self)
        self._license_timer.timeout.connect(self._check_license_heartbeat)
        self._license_timer.start(14400000)

    def _check_license_heartbeat(self) -> None:
        """Esegue una sincronizzazione silente della licenza in background (Asincrono)."""
        if hasattr(self, "_license_worker") and self._license_worker and self._license_worker.isRunning():
            return

        self._license_worker = LicenseWorker()
        self._license_worker.finished_signal.connect(self._on_license_check_finished)
        self._license_worker.start()

    def _on_license_check_finished(self, success: bool, error_msg: str) -> None:
        """Gestisce l'esito della verifica licenza in background."""
        if not success and "REVOCATA" in error_msg:
            self._license_timer.stop()
            ConfirmationDialog.show_error(
                self,
                "Licenza Revocata",
                "La licenza è stata revocata dal server.\nL'applicazione verrà chiusa.",
            )
            self._force_quit = True
            QApplication.quit()
        elif success:
            logger.debug("Heartbeat licenza cloud completato con successo.")

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
            self.status_bar_component.footer_left.engine_clicked.connect(self._switch_engine)
            self.status_bar_component.footer_left.headless_clicked.connect(self._switch_headless)

            # Check for system tray support
            if not QSystemTrayIcon.isSystemTrayAvailable():
                logger.warning("System tray non disponibile su questo sistema.")

            # Check for updates on startup
            QTimer.singleShot(5000, self.update_controller.check_updates_startup)

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
        from src.gui.widgets.sidebar_widget import SidebarWidget

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
        """Controlla se ci sono aggiornamenti pendenti o nuovi al boot (Delegato)."""
        self.update_controller.check_updates_startup()

    def _show_update_banner(self, version_info: dict[str, Any]) -> None:
        """Mostra il banner di aggiornamento nella toolbar (Delegato)."""
        self.update_controller.show_update_banner(version_info)

    def _on_download_update_clicked(self, download_url: str) -> None:
        """Avvia il processo di download dell'aggiornamento (Delegato)."""
        self.update_controller.handle_download_update(download_url)

    def _on_update_error(self, message: str) -> None:
        """Gestisce errori durante lo scaricamento dell'aggiornamento (Delegato)."""
        self.update_controller.handle_update_error(message)

    def _on_update_downloaded(self, setup_path: str) -> None:
        """Gestisce il completamento del download dell'aggiornamento (Delegato)."""
        self.update_controller.handle_update_downloaded(setup_path)

    def show_background_notification(self, title: str, message: str, is_error: bool = False) -> None:
        """Mostra una notifica balloon se l'app è in background."""
        if hasattr(self, "tray_icon_component"):
            self.tray_icon_component.show_background_notification(title, message, is_error)

    def _switch_account(self, bot_type: str) -> None:
        """Ruota l'account attivo per il portale specificato (Delegato)."""
        self.app_status_controller.rotate_account(bot_type)

    def _switch_engine(self) -> None:
        """Ruota il motore di automazione attivo (Delegato)."""
        self.app_status_controller.switch_engine()

    def _switch_headless(self) -> None:
        """Ruota la modalità browser tra visibile e nascosta (Delegato)."""
        self.app_status_controller.switch_headless()

    def show_toast(self, message: str, level: str = "info") -> None:
        """
        Visualizza un messaggio toast.

        Args:
            message: Il messaggio da visualizzare.
            level: Livello del messaggio (info, success, warning, error).
        """
        ToastManager.instance().show(message, level)

    def show_settings(self) -> None:
        """Naviga alla pagina delle impostazioni globali."""
        self.navigation_controller.navigate_to(PageIndex.SETTINGS)

    def trigger_pdl_print(self, pdl_numbers: list[str]) -> None:
        """
        Coordina la stampa dei PDL selezionati navigando al bot di scarico.

        Args:
            pdl_numbers: Lista di numeri PDL da stampare.
        """
        if not pdl_numbers:
            return

        # Naviga al pannello Scarico PDL (Sotto-tab di Automazioni)
        self.navigation_controller.navigate_to_panel("scarico_pdl")

        # Recupera il pannello (già inizializzato dalla navigazione) e inietta i dati
        if hasattr(self, "pdl_panel") and self.pdl_panel:
            self.pdl_panel.set_pdl_list(pdl_numbers)
        else:
            # Fallback se non ancora registrato (molto improbabile dopo navigazione)
            from src.gui.main_window.page_index import PageIndex

            automazioni = self.navigation_controller.get_panel(PageIndex.AUTOMAZIONI)
            if automazioni and hasattr(automazioni, "panel_pdl"):
                automazioni.panel_pdl.set_pdl_list(pdl_numbers)

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
