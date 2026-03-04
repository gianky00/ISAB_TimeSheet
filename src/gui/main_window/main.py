"""
SyncroJob - Main Window
Finestra principale dell'applicazione che coordina tutti i servizi, i controller e i componenti dell'interfaccia utente.
Refactored V9.0: Orchestration with modular Workflow and Monitoring Controllers.
"""

import webbrowser
from contextlib import suppress
from pathlib import Path
from typing import Any

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.core.audit_manager import AuditManager
from src.core.lyra_sentinel import LyraSentinel
from src.core.telegram_bridge import TelegramUIBridge
from src.core.telegram_manager import TelegramService
from src.core.version import __version__ as VERSION
from src.gui.components.animated_stack import SlidingStackedWidget
from src.gui.controllers.bot_controller import BotController
from src.gui.controllers.navigation_controller import NavigationController
from src.gui.controllers.search_controller import SearchController
from src.gui.controllers.service_controller import ServiceController
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


class MainWindow(QMainWindow):
    """
    Finestra principale dell'applicazione (Facade).
    Coordina i componenti modulari e i controller, fungendo da punto centrale di orchestrazione.
    """

    def __init__(self) -> None:
        """Inizializza la finestra principale, carica gli stili e configura i controller."""
        super().__init__()
        self.setWindowTitle(f"SyncroJob v{VERSION}")
        self.setMinimumSize(1200, 800)

        # Configurazione Stili
        self._load_styles()
        if app := QApplication.instance():
            apply_theme(app, "light")  # type: ignore[arg-type]
        self.setAcceptDrops(True)

        self._current_page_index = -1
        self._force_quit = False
        self._is_initializing = True

        # --- SERVIZI ---
        self.sentinel = LyraSentinel()
        self.telegram = TelegramService()
        self.telegram_bridge = TelegramUIBridge(self)
        self.telegram_bridge.setup_connections()

        # --- CONTROLLERS ---
        self.app_event_handler = AppEventHandler(self)
        self.signal_connector = SignalConnector(self)

        # --- UI COMPONENTS ---
        self.status_bar_component = StatusBarComponent(self)
        self.menu_bar_component = MenuBarComponent(self)
        self.tool_bar_component = ToolBarComponent(self)
        self.tray_icon_component = TrayIconComponent(self)

        # --- Functional Controllers ---
        self.search_controller = SearchController(self)
        self.navigation_controller = NavigationController(self)
        self.tray_controller = self.tray_icon_component.controller
        self.bot_controller = BotController(self, self.telegram)
        self.service_controller = ServiceController(self, self.telegram, self.sentinel)

        # Modular Workflow and Monitoring Controllers
        self.workflow_controller = WorkflowController(self)
        self.monitoring_controller = MonitoringController(self)

        # --- UI SETUP ---
        self._setup_ui()

        # Connect Signals
        self.signal_connector.connect_global_signals()
        self.signal_connector.connect_sidebar_signals()

        # Shortcuts
        self._setup_shortcuts()

        # Avvio servizi
        self.service_controller.start_all()

        # Navigazione iniziale (Dashboard)
        self.navigation_controller.navigate_to(PageIndex.DASHBOARD)

    def finalize_init(self) -> None:
        """Metodo chiamato per finalizzare l'inizializzazione dopo la visualizzazione della finestra."""
        import logging

        logger = logging.getLogger("MainWindow")

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

            # --- Eager Loading & Background Checks (Differiti per massime prestazioni UI) ---
            QTimer.singleShot(200, self._deferred_finalize)
            logger.info("finalize_init sequence triggered")
        except Exception as e:
            logger.critical(f"Error in finalize_init: {e}", exc_info=True)
            raise

    def _deferred_finalize(self) -> None:
        """Esegue le operazioni pesanti di inizializzazione senza bloccare l'avvio immediato."""
        # 1. Pre-caricamento pannelli critici
        self.navigation_controller.get_panel(PageIndex.CONSUNTIVO)

        # 2. Reset flag per abilitare i toast utente
        self._is_initializing = False

        # 3. Start Monitoring
        self.monitoring_controller.start_monitoring()

        # 4. Connect Autopilot real-time updates
        if hasattr(self, "timbrature_bot_panel"):
            with suppress(Exception):
                self.timbrature_bot_panel.autopilot_changed.connect(self._update_autopilot_status_ui)

        # 5. Show final system-ready toast
        ToastManager.instance().show(
            "<center><b>Sistema inizializzato e pronto all'uso</b><br/>Tutti i moduli sono operativi. Enjoy!</center>",
            "success",
            5000,
            position="bottom",
            pulse=True,
        )

    def _load_styles(self) -> None:
        """Carica i file QSS degli stili."""
        # Forza i tooltip in Light Mode a livello globale
        global_tooltip_style = """
            QToolTip {
                background-color: #FFFFFF;
                color: #212121;
                border: 1px solid #BBBBBB;
                border-radius: 6px;
                padding: 8px 12px;
            }
        """
        self.setStyleSheet(global_tooltip_style)

        for qss in ("main_window.qss", "message_box.qss"):
            path = Path("assets") / "styles" / qss
            if path.exists():
                self.setStyleSheet(self.styleSheet() + path.read_text(encoding="utf-8"))

    def _setup_ui(self) -> None:
        """Configura il layout e i componenti UI principali usando un overlay per la sidebar."""
        from PyQt6.QtWidgets import QGridLayout

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QGridLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Content Area
        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(10, 10, 10, 10)

        self.page_stack = SlidingStackedWidget()
        for i in range(13):
            placeholder = QWidget()
            self.page_stack.addWidget(placeholder)
            setattr(self, f"_panel_initialized_{i}", False)

        (
            self.update_banner,
            self.global_search,
        ) = self.tool_bar_component.setup_content_toolbar(content_layout)

        content_layout.addWidget(self.page_stack)
        main_layout.addWidget(content_area, 0, 0)

        # 2. Sidebar come Overlay
        self.sidebar = self.tool_bar_component.setup_sidebar(central_widget)
        main_layout.addWidget(self.sidebar, 0, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.sidebar.raise_()

    def _setup_shortcuts(self) -> None:
        """Configura le scorciatoie da tastiera globali."""
        from PyQt6.QtGui import QKeySequence, QShortcut

        self.shortcut_f5 = QShortcut(QKeySequence(Qt.Key.Key_F5), self)
        self.shortcut_f5.activated.connect(self._handle_f5)
        self.shortcut_search = QShortcut(QKeySequence("Ctrl+F"), self)
        self.shortcut_search.activated.connect(self.app_event_handler.handle_ctrl_f)
        if app := QApplication.instance():
            app.installEventFilter(self)

    # --- DELEGATED TO CONTROLLERS ---
    def _handle_f5(self) -> None:
        """Refresh action delegata al NavigationController."""
        self.navigation_controller.refresh_current_page()

    def _switch_account(self, service_type: str) -> None:
        """Passa all'account successivo per il servizio specificato."""
        success, new_user = config_manager.switch_default_account(service_type)
        if success:
            self.status_bar_component.footer_left.refresh_accounts()
            portal_name = "Portale Fornitori" if service_type == "isab" else "SafeWork"
            ToastManager.instance().show(f"Account {portal_name} cambiato in: {new_user}", "info")
            if hasattr(self, "settings_panel") and self.settings_panel:
                self.settings_panel.load_settings()
            AuditManager.instance().log_action(
                "Switch Account", "config", portal_name, {"username": new_user}
            )
        else:
            self._navigate_to_settings_config()

    def _navigate_to_settings_config(self) -> None:
        """Naviga alla pagina di configurazione account nelle impostazioni."""
        self.navigation_controller.navigate_to(PageIndex.SETTINGS)
        if hasattr(self, "settings_panel") and self.settings_panel:
            QTimer.singleShot(50, lambda: self.settings_panel.tabs.setCurrentIndex(0))

    # --- UI HELPERS & OVERRIDES ---
    def _toggle_footer_stats(self) -> None:
        """Alterna la visibilità delle statistiche nel footer."""
        self.status_bar_component._toggle_footer_stats()

    def _quit_application(self) -> None:
        """Chiude l'applicazione in modo sicuro."""
        self.app_event_handler.quit_application()

    def closeEvent(self, event: Any) -> None:
        """Gestisce l'evento di chiusura della finestra."""
        self.app_event_handler.handle_close_event(event)

    def show_toast(self, message: str, duration: int = 3000) -> None:
        """Mostra un messaggio toast a video."""
        ToastManager.instance().show(message, "info", duration)

    def _open_command_palette(self) -> None:
        """Apre la palette dei comandi rapidi."""
        self.menu_bar_component.open_command_palette()

    def _update_autopilot_status_ui(self) -> None:
        """Aggiorna lo stato visivo dell'autopilot nella barra di stato."""
        self.status_bar_component.update_autopilot_ui()

    def _on_download_update_clicked(self, url: str) -> None:
        """Apre il browser per il download di un aggiornamento."""
        webbrowser.open(url)

    def _navigate_to(self, index: int) -> None:
        """Naviga verso una pagina specifica tramite indice."""
        self.navigation_controller.navigate_to(index)

    def _show_update_banner(self, new_version: str, download_url: str, changelog: str) -> None:
        """Mostra il banner di aggiornamento disponibile."""
        if hasattr(self, "update_banner"):
            self.update_banner.show_update(new_version, download_url, changelog)
        if hasattr(self, "tray_icon_component"):
            self.tray_icon_component.show_update_message(new_version)

    def trigger_pdl_print(self, pdl_numbers: list[str]) -> None:
        """
        Riceve una lista di numeri PDL dal database e li invia al pannello di scarico PDL
        per l'avvio automatico del bot di stampa.
        """
        if not pdl_numbers:
            return

        # 1. Forza l'inizializzazione del pannello Automazioni (che contiene scarico_pdl)
        self.navigation_controller.navigate_to_panel("scarico_pdl")

        # 2. Recupera l'istanza del pannello Scarico PDL tramite AutomazioniWidget
        if hasattr(self, "automazioni_widget"):
            # Scarico PDL è nel tab 1 (SafeWork), bot 0
            pdl_panel = self.automazioni_widget.get_bot_panel(1, 0)
            if pdl_panel and hasattr(pdl_panel, "set_pdl_list"):
                pdl_panel.set_pdl_list(pdl_numbers)

    def _on_settings_saved(self) -> None:
        """Callback eseguita al salvataggio delle impostazioni (Hot Reload Globale)."""
        # 1. Riavvia servizi dipendenti dalle credenziali/token
        self.telegram.start_service()
        self._update_autopilot_status_ui()

        # 2. Refresh account nel footer (Account Portale/SafeWork)
        if hasattr(self, "status_bar_component") and hasattr(self.status_bar_component, "footer_left"):
            self.status_bar_component.footer_left.refresh_accounts()

        # 3. Hot Reload in tutti i pannelli inizializzati
        for i in range(self.page_stack.count()):
            panel = self.page_stack.widget(i)
            if not panel or panel is self.page_stack:
                continue

            # Refresh Anagrafiche (Fornitori, Contratti)
            if hasattr(panel, "refresh_contracts"):
                panel.refresh_contracts()
            if hasattr(panel, "refresh_fornitori"):
                panel.refresh_fornitori()

            # Refresh Percorsi e Dati Salvati
            if hasattr(panel, "_load_saved_data"):
                try:
                    panel._load_saved_data()
                except Exception as e:
                    import logging
                    logging.getLogger("MainWindow").warning(f"Errore hot-reload dati in {panel}: {e}")

            # Refresh Database se visibili
            if hasattr(panel, "refresh_data"):
                try:
                    panel.refresh_data()
                except Exception as e:
                    import logging
                    logging.getLogger("MainWindow").debug(f"Salto refresh database silente per {panel}: {e}")

        # 4. Feedback utente
        if not getattr(self, "_is_initializing", False):
            ToastManager.instance().show(
                "<center><b>Hot Reload Completato</b><br/>Tutte le impostazioni sono ora attive.</center>",
                "success"
            )

    def _on_help_requested(self, section_title: str) -> None:
        """Naviga alla sezione di aiuto specificata."""
        self.navigation_controller.navigate_to(PageIndex.HELP)
        if hasattr(self, "help_panel"):
            self.help_panel.open_section(section_title)

    def open_bug_report_dialog(self) -> None:
        """Apre il dialogo per la segnalazione di un bug."""
        from src.gui.dialogs.bug_report_dialog import BugReportDialog

        dlg = BugReportDialog(self)
        dlg.exec()

    def show_settings(self) -> None:
        """Naviga alla pagina delle impostazioni."""
        self.navigation_controller.navigate_to(PageIndex.SETTINGS)

    def show_background_notification(self, title: str, message: str, is_error: bool = False) -> None:
        """Mostra una notifica di sistema (Toast/Tray) in background."""
        if hasattr(self, "tray_icon_component"):
            self.tray_icon_component.show_background_notification(title, message, is_error)

    # --- Properties per compatibilità ---
    @property
    def footer_left(self) -> Any:
        """Restituisce il componente sinistro del footer."""
        return self.status_bar_component.footer_left

    @property
    def footer_right(self) -> Any:
        """Restituisce il componente destro del footer."""
        return self.status_bar_component.footer_right

    @property
    def status_portale(self) -> Any:
        """Restituisce l'indicatore di stato del Portale ISAB."""
        return self.status_bar_component.status_portale

    @property
    def status_safework(self) -> Any:
        """Restituisce l'indicatore di stato di SafeWork."""
        return self.status_bar_component.status_safework

    @property
    def startup_console(self) -> Any:
        """Restituisce la console di avvio."""
        return self.status_bar_component.startup_console

    @property
    def boot_telemetry(self) -> Any:
        """Restituisce il monitor di telemetria boot."""
        return self.status_bar_component.boot_telemetry
