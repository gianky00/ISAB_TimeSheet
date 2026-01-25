import random
from contextlib import suppress

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.core.audit_manager import AuditManager
from src.core.auth_monitor import check_expiring_isab_authorizations
from src.core.lyra_sentinel import LyraSentinel
from src.core.telegram_bridge import TelegramUIBridge
from src.core.telegram_manager import TelegramService
from src.core.version import __version__ as VERSION
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
from .controllers.signal_connector import SignalConnector
from .page_index import PageIndex


class MainWindow(QMainWindow):
    """
    Finestra principale dell'applicazione (Facade).
    Coordina i componenti modulari e i controller.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"SyncroJob v{VERSION}")
        self.setMinimumSize(1200, 800)

        # Configurazione Stili
        self._load_styles()
        apply_theme(QApplication.instance(), "light")
        self.setAcceptDrops(True)

        self._current_page_index = -1
        self._force_quit = False

        # --- SERVIZI ---
        self.sentinel = LyraSentinel()
        self.telegram = TelegramService()
        self.telegram_bridge = TelegramUIBridge(self)
        self.telegram_bridge.setup_connections()

        # --- CONTROLLERS (High Level) ---
        # Note: Some controllers might expect the monolithic MainWindow attributes.
        # We need to ensure we expose what they need or update them.
        # For now, we attach components to self so they can be found if needed.

        # --- UI COMPONENTS ---
        # 1. Init Logic Controllers first (for dependencies)
        self.app_event_handler = AppEventHandler(self)
        self.signal_connector = SignalConnector(self)

        # 2. Init UI Components
        self.status_bar_component = StatusBarComponent(self)
        self.menu_bar_component = MenuBarComponent(self)  # Manages Command Palette
        self.tool_bar_component = ToolBarComponent(self)
        self.tray_icon_component = TrayIconComponent(self)  # Manages Tray

        # 3. Init Functional Controllers
        self.search_controller = SearchController(self)
        self.navigation_controller = NavigationController(self)

        # Tray Controller is wrapped in TrayIconComponent but we might need direct access
        self.tray_controller = self.tray_icon_component.controller

        # --- SIGNAL CONNECTIONS (UI) ---
        # Footer Left (Account Switch)
        if hasattr(self.status_bar_component, "footer_left"):
            self.status_bar_component.footer_left.portale_clicked.connect(
                lambda: self._switch_account("isab")
            )
            self.status_bar_component.footer_left.safework_clicked.connect(
                lambda: self._switch_account("safework")
            )

        # Footer Right (Status Cards)
        if hasattr(self.status_bar_component, "status_portale"):
            self.status_bar_component.status_portale.clicked.connect(
                lambda: self._switch_account("isab")
            )
        if hasattr(self.status_bar_component, "status_safework"):
            self.status_bar_component.status_safework.clicked.connect(
                lambda: self._switch_account("safework")
            )

        self.bot_controller = BotController(self, self.telegram)
        self.service_controller = ServiceController(self, self.telegram, self.sentinel)

        # --- UI SETUP ---
        self._setup_ui()

        # Connect Signals
        self.signal_connector.connect_global_signals()
        self.signal_connector.connect_sidebar_signals()  # Needs UI to be ready

        # Setup Shortcuts (delegated to components but F5/Ctrl+F handled here/delegated)
        self._setup_shortcuts()

        # Avvio servizi
        self.service_controller.start_all()

        # Navigazione iniziale (Dashboard)
        self.navigation_controller.navigate_to(PageIndex.DASHBOARD)

        # PRECARICAMENTO SILENZIOSO
        QTimer.singleShot(500, self._preload_background)
        QTimer.singleShot(10000, self._check_and_start_contabilita_update)

    def _load_styles(self):
        from pathlib import Path

        for qss in ["main_window.qss", "message_box.qss"]:
            path = Path(f"assets/styles/{qss}")
            if path.exists():
                self.setStyleSheet(self.styleSheet() + path.read_text(encoding="utf-8"))

    def _setup_ui(self):
        """Configura l'interfaccia assemblando i componenti."""
        # Status Bar is setup by component in its init

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # SIDEBAR (Created by ToolBarComponent)
        self.sidebar = self.tool_bar_component.setup_sidebar(main_layout)

        # CONTENT AREA
        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(20, 20, 20, 20)

        # Toolbar (Update Banner, Global Search)
        (
            self.update_banner,
            self.global_search,
        ) = self.tool_bar_component.setup_content_toolbar(content_layout)

        # Page Stack
        self.page_stack = QStackedWidget()
        for i in range(12):
            placeholder = QWidget()
            self.page_stack.addWidget(placeholder)
            setattr(self, f"_panel_initialized_{i}", False)

        content_layout.addWidget(self.page_stack)
        main_layout.addWidget(content_area)

    def _setup_shortcuts(self):
        # Delegate to MenuBarComponent for Palette
        # F5 and Ctrl+F
        from PyQt6.QtGui import QKeySequence, QShortcut

        self.shortcut_f5 = QShortcut(QKeySequence(Qt.Key.Key_F5), self)
        self.shortcut_f5.activated.connect(self.app_event_handler.handle_f5)

        self.shortcut_search = QShortcut(QKeySequence("Ctrl+F"), self)
        self.shortcut_search.activated.connect(self.app_event_handler.handle_ctrl_f)

        QApplication.instance().installEventFilter(self)

    # --- DELEGATED METHODS (Facade) ---
    def _toggle_footer_stats(self):
        self.status_bar_component._toggle_footer_stats()

    def _quit_application(self):
        self.app_event_handler.quit_application()

    def closeEvent(self, event):
        self.app_event_handler.handle_close_event(event)

    def show_toast(self, message: str, duration: int = 3000):
        ToastManager.instance().show(message, "info", duration)

    def _open_command_palette(self):
        self.menu_bar_component.open_command_palette()

    def _update_autopilot_status_ui(self):
        self.status_bar_component.update_autopilot_ui()

    def _on_download_update_clicked(self, url):
        import webbrowser

        webbrowser.open(url)

    # --- FACADE IMPLEMENTATION (Originally in MainWindow) ---
    # These methods are called by CommandPalette or Signals

    def _navigate_to(self, index: int):
        self.navigation_controller.navigate_to(index)

    def _handle_f5_action(self):
        """Logic for F5 refresh."""
        idx = self.page_stack.currentIndex()
        refresh_actions = {
            PageIndex.DASHBOARD: lambda: self.dashboard_panel.refresh_data()
            if hasattr(self, "dashboard_panel")
            else None,
            PageIndex.TIMBRATURE: lambda: self.timbrature_db_panel.refresh_data()
            if hasattr(self, "timbrature_db_panel")
            else None,
            PageIndex.STRUMENTALE: lambda: self.contabilita_panel.refresh_tabs()
            if hasattr(self, "contabilita_panel")
            else None,
            PageIndex.DATAEASE: lambda: self.scarico_ore_panel._start_update()
            if hasattr(self, "scarico_ore_panel")
            else None,
            PageIndex.ANAGRAFICHE: lambda: self.pdl_db_panel.refresh_data()
            if hasattr(self, "pdl_db_panel")
            else None,
            PageIndex.STORICO_ODA: lambda: self.storico_oda_panel.refresh_data()
            if hasattr(self, "storico_oda_panel")
            else None,
            PageIndex.DIPENDENTI: lambda: self.dipendenti_panel.refresh_data()
            if hasattr(self, "dipendenti_panel")
            else None,
        }
        action = refresh_actions.get(idx)
        if action:
            action()

    def _handle_f5(self):
        """Alias for backward compatibility (used by MenuBar)."""
        self._handle_f5_action()

    def _run_timbrature_bot(self, mode: str):
        # Ensure panel loaded
        if not hasattr(self, "timbrature_bot_panel"):
            self.navigation_controller.get_panel(PageIndex.AUTOMAZIONI)

        if hasattr(self, "timbrature_bot_panel"):
            # Connect signals if needed (logic from mono)
            if not getattr(self.timbrature_bot_panel, "_mw_signals_connected", False):
                with suppress(Exception):
                    self.timbrature_bot_panel.status_changed.connect(
                        lambda color,
                        msg: self.status_bar_component.footer_right.set_status(
                            msg, color
                        )
                    )
                    self.timbrature_bot_panel._mw_signals_connected = True

            from PyQt6.QtCore import QDate

            data_da = QDate.currentDate().toString("dd.MM.yyyy")
            data_a = QDate.currentDate().toString("dd.MM.yyyy")
            if mode == "ieri":
                data_da = QDate.currentDate().addDays(-1).toString("dd.MM.yyyy")
                data_a = QDate.currentDate().addDays(-1).toString("dd.MM.yyyy")
            elif mode == "mese":
                data_da = QDate.currentDate().toString("01.MM.yyyy")

            ToastManager.instance().show(f"🚀 Avvio Timbrature ({mode})...", "info")
            self.timbrature_bot_panel.run_externally(
                {"data_da": data_da, "data_a": data_a}
            )

    # --- Quick Action Inputs ---
    def _on_scarico_ts_input(self, args: list):
        if not args or not args[0]:
            return
        self.navigation_controller.navigate_to_panel("scarico_ts")
        if hasattr(self, "scarico_panel"):
            QTimer.singleShot(
                200,
                lambda: self.scarico_panel.run_externally(
                    {"single_item": {"numero_oda": args[0], "posizione_oda": ""}}
                ),
            )

    def _on_dettagli_oda_input(self, args: list):
        if not args or not args[0]:
            return
        self.navigation_controller.navigate_to_panel("dettagli_oda")
        if hasattr(self, "dettagli_panel"):
            QTimer.singleShot(
                200,
                lambda: self.dettagli_panel.run_externally(
                    {"single_item": {"Numero OdA": args[0], "numero_oda": args[0]}}
                ),
            )

    def _on_pdl_input(self, args: list):
        if not args or not args[0]:
            return
        self.navigation_controller.navigate_to_panel("scarico_pdl")
        if hasattr(self, "pdl_panel"):
            QTimer.singleShot(
                200,
                lambda: self.pdl_panel.run_externally(
                    {"single_item": {"numero_pdl": args[0]}}
                ),
            )

    def _on_prenota_bp_input(self, args: list):
        if not args or not args[0]:
            return
        self.navigation_controller.navigate_to_panel("prenota_bp")
        if hasattr(self, "prenota_panel"):
            QTimer.singleShot(
                200,
                lambda: self.prenota_panel.run_externally(
                    {"single_item": {"numero_bp": args[0]}}
                ),
            )

    def _run_carico_ts(self):
        self.navigation_controller.navigate_to_panel("carico_ts")
        if hasattr(self, "carico_panel"):
            QTimer.singleShot(200, lambda: self.carico_panel.run_externally({}))

    def _run_sync_dataease(self):
        self._navigate_to(PageIndex.DATAEASE)
        if hasattr(self, "scarico_ore_panel"):
            QTimer.singleShot(500, self.scarico_ore_panel._start_update)

    def _run_sync_strumentale(self):
        self._navigate_to(PageIndex.STRUMENTALE)
        if hasattr(self, "contabilita_panel"):
            QTimer.singleShot(500, self.contabilita_panel.start_import_process)

    def _handle_automation_tab_change(self, tab_index: int):
        self.navigation_controller.navigate_to(
            PageIndex.AUTOMAZIONI, sub_index=tab_index
        )
        if hasattr(self, "automazioni_widget"):
            self.automazioni_widget.setCurrentIndex(tab_index)

    def _handle_notifications_tab_change(self, tab_index: int):
        self.navigation_controller.navigate_to(
            PageIndex.NOTIFICATIONS, sub_index=tab_index
        )
        if hasattr(self, "notifications_panel"):
            self.notifications_panel.tabs.setCurrentIndex(tab_index)

    def _check_and_start_contabilita_update(self):
        config = config_manager.load_config()
        if config.get("enable_auto_update_contabilita", False):
            self.navigation_controller.get_panel(PageIndex.STRUMENTALE)
            if hasattr(self, "contabilita_panel"):
                self.contabilita_panel.start_import_process()

    def _switch_account(self, service_type: str):
        # Currently called by lambda in StatusBarComponent setup... wait.
        # StatusBarComponent creates FooterLeftWidget but connecting signal?
        # In StatusBarComponent: self.status_bar.addWidget(self.footer_left)
        # We need to access footer_left here to connect signals OR pass callback to component.
        # Let's fix this in __init__ after component init.

        success, new_user = config_manager.switch_default_account(service_type)
        if success:
            self.status_bar_component.footer_left.refresh_accounts()
            portal_name = "Portale Fornitori" if service_type == "isab" else "SafeWork"
            ToastManager.instance().show(
                f"Account {portal_name} cambiato in: {new_user}", "info"
            )
            if hasattr(self, "settings_panel") and self.settings_panel:
                self.settings_panel.load_settings()
            AuditManager.instance().log_action(
                "Switch Account", "config", portal_name, {"username": new_user}
            )
        else:
            self._navigate_to_settings_config()

    def _navigate_to_settings_config(self):
        _ = self.navigation_controller.get_panel(PageIndex.SETTINGS)
        self.navigation_controller.navigate_to(PageIndex.SETTINGS)
        if hasattr(self, "settings_panel") and self.settings_panel:
            QTimer.singleShot(50, lambda: self.settings_panel.tabs.setCurrentIndex(0))

    # --- Preload Logic (Main Orchestration) ---
    def _preload_background(self):
        # 1. VISUAL SETUP via Component
        self.status_bar_component.status_bar.setVisible(True)
        # ... logic to show StartupConsole etc is in StatusBarComponent, but we need to trigger it
        # Actually in Monolith it calls setVisible on widgets.
        # Let's assume StatusBarComponent sets them visible by default on creation?
        # Yes, in my StatusBarComponent implementation I set them visible=True.
        # But we need to switch from default to "Hacker Mode" if not already?
        # In Monolith: _preload_background hides footer_left, shows console.
        # I should probably expose a method `start_preload_visuals()` in StatusBarComponent.

        # Accessing widgets directly for speed in migration, though dirty.
        self.status_bar_component.footer_left.setVisible(False)
        self.status_bar_component.startup_console.setVisible(True)
        self.status_bar_component.boot_telemetry.setVisible(True)
        self.status_bar_component.footer_right.show_loading()
        self.status_bar_component.footer_right.set_global_progress(0)

        # Build Queue
        self._preload_tasks = []

        def mk_steps(action, label, ctx="SYS"):
            steps = []
            tx_id = f"{random.randint(0, 0xFFFF):04X}"
            steps.append(
                (None, f"[{ctx}] Resolving dependencies for {label} (TX-{tx_id})...")
            )
            steps.append((None, f"[{ctx}] Injecting service context into {label}..."))
            steps.append(
                (action, f"[{ctx}] Initializing worker threads for {label}...")
            )
            return steps

        # 1. CORE
        self._preload_tasks.extend(mk_steps(None, "Service Container", "CORE"))
        # 2. TIMBRATURE
        self._preload_tasks.extend(
            mk_steps(
                lambda: self.navigation_controller.get_panel(PageIndex.TIMBRATURE),
                "Timesheet Repository",
                "ORM",
            )
        )
        # 3. STRUMENTALE
        self._preload_tasks.extend(
            mk_steps(
                lambda: self.navigation_controller.get_panel(PageIndex.STRUMENTALE),
                "Asset Registry Module",
                "DATA",
            )
        )
        # 4. DATAEASE
        self._preload_tasks.extend(
            mk_steps(
                lambda: self.navigation_controller.get_panel(PageIndex.DATAEASE),
                "DataEase Sync Bridge",
                "IPC",
            )
        )
        # 5. ANAGRAFICHE
        self._preload_tasks.extend(
            mk_steps(
                lambda: self.navigation_controller.get_panel(PageIndex.ANAGRAFICHE),
                "HR Directory Service",
                "LDAP",
            )
        )
        # 5b. DIPENDENTI
        self._preload_tasks.extend(
            mk_steps(
                lambda: self.navigation_controller.get_panel(PageIndex.DIPENDENTI),
                "Employee Records",
                "HR",
            )
        )
        # 6. AUTOMAZIONI
        self._preload_tasks.extend(
            mk_steps(
                lambda: self.navigation_controller.get_panel(PageIndex.AUTOMAZIONI),
                "Task Scheduler Engine",
                "PROC",
            )
        )
        # 7. LYRA
        self._preload_tasks.extend(
            mk_steps(
                lambda: self.navigation_controller.get_panel(PageIndex.LYRA),
                "Lyra Analysis Engine",
                "AI",
            )
        )
        # 8. SETTINGS
        self._preload_tasks.extend(
            mk_steps(
                lambda: self.navigation_controller.get_panel(PageIndex.SETTINGS),
                "User Configuration",
                "CFG",
            )
        )

        self._preload_tasks.append((None, "[SYS] Pre-warming application cache..."))
        self._preload_tasks.append((None, "[SYS] Event Loop Started. SYSTEM READY."))

        self._total_preload = len(self._preload_tasks)
        self._completed_preload = 0
        QTimer.singleShot(50, self._process_next_preload)

    def _process_next_preload(self):
        from PyQt6 import sip

        if sip.isdeleted(self):
            return
        if not hasattr(self, "_preload_tasks") or not self._preload_tasks:
            self._finalize_preload()
            return

        action, description = self._preload_tasks.pop(0)
        self._completed_preload += 1

        # UI Updates via Component
        self.status_bar_component.startup_console.set_log(
            description, self._completed_preload, self._total_preload
        )
        pct = int((self._completed_preload / self._total_preload) * 100)
        self.status_bar_component.footer_right.set_global_progress(pct)

        delay = 30
        if action:
            try:
                action()
                delay = 50
            except Exception as e:
                print(f"Error during deep preload of {description}: {e}")

        QApplication.processEvents()
        QTimer.singleShot(delay, self._process_next_preload)

    def _finalize_preload(self):
        self.status_bar_component.show_operational_state()

        # Final Toast
        QTimer.singleShot(
            500,
            lambda: ToastManager.instance().show(
                "<center><b>Sistema inizializzato e pronto all'uso</b><br/>Tutti i moduli sono operativi. Enjoy!</center>",
                "success",
                5000,
                position="bottom",
                pulse=True,
            ),
        )

        # Connect Autopilot real-time updates if automation panel loaded
        if hasattr(self, "timbrature_bot_panel"):
            with suppress(Exception):
                self.timbrature_bot_panel.autopilot_changed.connect(
                    self._update_autopilot_status_ui
                )

        # Proactive Checks
        QTimer.singleShot(2000, self._check_isab_authorizations)
        self.auth_check_timer = QTimer(self)
        self.auth_check_timer.timeout.connect(self._check_isab_authorizations)
        self.auth_check_timer.start(4 * 3600 * 1000)

    def _check_isab_authorizations(self):
        try:
            expiring = check_expiring_isab_authorizations()
            if hasattr(self, "sidebar") and hasattr(self.sidebar, "btn_dipendenti"):
                self.sidebar.btn_dipendenti.set_badge(len(expiring))

            if not expiring:
                return

            scaduti = [d for d in expiring if d["stato"] == "SCADUTA"]
            in_scadenza = [d for d in expiring if d["stato"] == "IN SCADENZA"]
            msg = "<b>Monitoraggio Abilitazioni ISAB</b><br/>"
            if scaduti:
                msg += f"🔴 {len(scaduti)} Abilitazioni SCADUTE (>30 gg)<br/>"
            if in_scadenza:
                msg += f"🟠 {len(in_scadenza)} In scadenza (20-30 gg)<br/>"
            msg += (
                "<br/><small>Controlla la tabella 'Dipendenti' per i dettagli.</small>"
            )
            ToastManager.instance().show(
                msg, "warning" if in_scadenza or scaduti else "info", 8000
            )
        except Exception as e:
            print(f"Errore monitoraggio autorizzazioni: {e}")

    def _on_anomalies_found(self, count):
        """Gestisce le anomalie trovate da Lyra."""
        if hasattr(self, "sidebar"):
            self.sidebar.btn_lyra.set_badge(count)
        if count > 0:
            ToastManager.instance().show(
                f"⚠️ Lyra ha rilevato {count} anomalie", "warning"
            )

    def _show_update_banner(self, new_version, download_url, changelog):
        """Mostra un banner informativo per la nuova versione."""
        if hasattr(self, "update_banner"):
            self.update_banner.show_update(new_version, download_url, changelog)

        # Notifica tray tramite component/controller
        if hasattr(self, "tray_icon_component"):
            self.tray_icon_component.show_update_message(new_version)

    def _on_settings_saved(self):
        if hasattr(self, "scarico_panel"):
            self.scarico_panel.refresh_fornitori()
        if hasattr(self, "dettagli_panel"):
            self.dettagli_panel.refresh_fornitori()
        if hasattr(self, "timbrature_bot_panel"):
            self.timbrature_bot_panel.refresh_fornitori()

        self.telegram.start_service()
        self._update_autopilot_status_ui()

        # Aggiorna account visualizzati nel footer sinistro
        if hasattr(self, "status_bar_component") and hasattr(
            self.status_bar_component, "footer_left"
        ):
            self.status_bar_component.footer_left.refresh_accounts()

        ToastManager.instance().show("Impostazioni salvate!", "success")

    def _on_help_requested(self, section_title):
        self.navigation_controller.navigate_to(PageIndex.HELP)
        if hasattr(self, "help_panel"):
            self.help_panel.open_section(section_title)

    def analyze_with_lyra(self, context_text: str):
        """Passa al contesto Lyra."""
        # TODO: Implement if needed, was empty in source
        pass

    def show_settings(self):
        """Mostra il pannello delle impostazioni."""
        self.navigation_controller.navigate_to(PageIndex.SETTINGS)

    def show_background_notification(
        self, title: str, message: str, is_error: bool = False
    ):
        """Mostra una notifica di sistema (Toast) se l'applicazione non è attiva."""
        if hasattr(self, "tray_icon_component"):
            self.tray_icon_component.show_background_notification(
                title, message, is_error
            )

    # --- COMPATIBILITY PROPERTIES (Facade -> Component) ---
    @property
    def footer_left(self):
        return self.status_bar_component.footer_left

    @property
    def footer_right(self):
        return self.status_bar_component.footer_right

    @property
    def status_portale(self):
        return self.status_bar_component.status_portale

    @property
    def status_safework(self):
        return self.status_bar_component.status_safework

    @property
    def startup_console(self):
        return self.status_bar_component.startup_console

    @property
    def boot_telemetry(self):
        return self.status_bar_component.boot_telemetry
