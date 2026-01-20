"""
Bot TS - Main Window
Finestra principale dell'applicazione SyncroJob.
Implementa Lazy Loading dei pannelli per prestazioni ottimali.
"""

import random  # NEW IMPORT
from datetime import datetime
from enum import IntEnum
from pathlib import Path

from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, QSize, Qt, QTimer
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import (
    QApplication,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QStatusBar,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.core.auth_monitor import check_expiring_isab_authorizations
from src.core.backup_manager import BackupManager
from src.core.license_validator import get_license_info
from src.core.lyra_sentinel import LyraSentinel
from src.core.notification_manager import NotificationManager
from src.core.telegram_bridge import TelegramUIBridge
from src.core.telegram_manager import TelegramService
from src.core.version import __version__ as VERSION  # Importo la versione
from src.gui.controllers.bot_controller import BotController
from src.gui.controllers.navigation_controller import NavigationController
from src.gui.controllers.search_controller import SearchController
from src.gui.controllers.service_controller import ServiceController
from src.gui.controllers.tray_controller import TrayController
from src.gui.styles import apply_theme
from src.gui.widgets.footer_stats import (  # NEW IMPORT
    BootTelemetryWidget,
    FooterLeftWidget,
    FooterRightWidget,
    StartupConsole,
)
from src.gui.widgets.sidebar_widget import SidebarWidget
from src.gui.widgets.status_card import StatusCard
from src.gui.widgets.toast import ToastManager
from src.gui.widgets.update_banner import UpdateBanner


class PageIndex(IntEnum):
    """Indici delle pagine nello StackedWidget principale."""

    DASHBOARD = 0
    AUTOMAZIONI = 1
    LYRA = 2
    TIMBRATURE = 3
    STRUMENTALE = 4
    DATAEASE = 5
    ANAGRAFICHE = 6
    SETTINGS = 7
    HELP = 8
    NOTIFICATIONS = 9
    STORICO_ODA = 10
    DIPENDENTI = 11


class MainWindow(QMainWindow):
    """
    Finestra principale dell'applicazione.
    Coordina i controller, la navigazione e il caricamento dei pannelli.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"SyncroJob v{VERSION}")  # Titolo con Versione
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

        # --- CONTROLLERS ---
        self.tray_controller = TrayController(self)
        self.search_controller = SearchController(self)
        self.navigation_controller = NavigationController(self)

        # --- GESTIONE TOAST MULTI-THREAD ---
        NotificationManager.instance().request_toast.connect(
            lambda msg, t, d: ToastManager.instance().show(msg, t, d)
        )
        self.bot_controller = BotController(self, self.telegram)
        self.service_controller = ServiceController(self, self.telegram, self.sentinel)

        # --- UI SETUP ---
        self._setup_ui()
        self._connect_signals()
        self._setup_shortcuts()

        # Avvio servizi
        self.service_controller.start_all()

        # Navigazione iniziale (Dashboard)
        self.navigation_controller.navigate_to(PageIndex.DASHBOARD)

        # PRECARICAMENTO SILENZIOSO: Carica i moduli pesanti in background dopo l'avvio
        QTimer.singleShot(500, self._preload_background)

        # Avvio automatico importazione contabilità (ritardato per stabilità)
        QTimer.singleShot(10000, self._check_and_start_contabilita_update)

    def _preload_background(self):
        """Avvia la sequenza di caricamento incrementale PROFONDO con feedback visivo."""
        # Nascondi i widget del footer standard (FASE 2)
        self.footer_left.setVisible(False)

        # Mostra i widget "Hacker Mode" (FASE 1)
        self.startup_console.setVisible(True)
        self.boot_telemetry.setVisible(True)

        # Mostra la progress bar (FASE 1)
        self.footer_right.setVisible(True)
        self.footer_right.show_loading()
        self.footer_right.set_global_progress(0)

        # Helper per creare filler logs "Professional Engineering"
        def mk_steps(action, label, ctx="SYS"):
            steps = []
            # Genera ID transazione esadecimale (realistico per tracing)
            tx_id = f"{random.randint(0, 0xFFFF):04X}"

            steps.append(
                (None, f"[{ctx}] Resolving dependencies for {label} (TX-{tx_id})...")
            )
            steps.append((None, f"[{ctx}] Injecting service context into {label}..."))
            steps.append(
                (action, f"[{ctx}] Initializing worker threads for {label}...")
            )
            return steps

        # Coda di caricamento: Lista di (Azione/None, Messaggio)
        self._preload_tasks = []

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

        # 8. SETTINGS & FINAL
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

        # Avvia la catena (Molto rapida)
        QTimer.singleShot(50, self._process_next_preload)

    def _process_next_preload(self):
        """Esegue il prossimo task di precaricamento senza bloccare la UI."""
        from PyQt6 import sip

        if sip.isdeleted(self):
            return

        if not hasattr(self, "_preload_tasks") or not self._preload_tasks:
            self._finalize_preload()
            return

        # Estrai il prossimo task
        action, description = self._preload_tasks.pop(0)
        self._completed_preload += 1

        # Aggiorna Console e Progress Bar
        self.startup_console.set_log(
            description, self._completed_preload, self._total_preload
        )
        progress_pct = int((self._completed_preload / self._total_preload) * 100)
        self.footer_right.set_global_progress(progress_pct)

        # Esegui azione (se presente)
        delay = 30  # Default delay (molto veloce per effetto scrolling)
        if action:
            try:
                action()
                delay = 50  # Un po' più lento per le azioni vere
            except Exception as e:
                print(f"Error during deep preload of {description}: {e}")

        # TRUCCO PER REATTIVITÀ: Forza l'app a gestire i click e il mouse PRIMA del prossimo task
        QApplication.processEvents()

        # Pianifica il prossimo step
        QTimer.singleShot(delay, self._process_next_preload)

    def _finalize_preload(self):
        """Conclude la sequenza di caricamento."""
        from PyQt6 import sip

        if sip.isdeleted(self):
            return

        # Ripristina Footer Standard (FASE 2) con animazioni fade-out/fade-in
        # Animazione fade-out per startup_console
        console_effect = QGraphicsOpacityEffect(self.startup_console)
        self.startup_console.setGraphicsEffect(console_effect)
        console_anim = QPropertyAnimation(console_effect, b"opacity")
        console_anim.setDuration(600)
        console_anim.setStartValue(1.0)
        console_anim.setEndValue(0.0)
        console_anim.setEasingCurve(QEasingCurve.Type.InCubic)
        console_anim.finished.connect(lambda: self.startup_console.setVisible(False))
        console_anim.start()

        # Animazione fade-out per boot_telemetry con reset opacity al termine
        telemetry_effect = QGraphicsOpacityEffect(self.boot_telemetry)
        self.boot_telemetry.setGraphicsEffect(telemetry_effect)
        telemetry_anim = QPropertyAnimation(telemetry_effect, b"opacity")
        telemetry_anim.setDuration(600)
        telemetry_anim.setStartValue(1.0)
        telemetry_anim.setEndValue(0.0)
        telemetry_anim.setEasingCurve(QEasingCurve.Type.InCubic)

        def hide_and_reset_telemetry():
            self.boot_telemetry.setVisible(False)
            # Rimuovi l'effect e reset opacity per permettere toggle futuro
            self.boot_telemetry.setGraphicsEffect(None)
            # Stop timer per risparmiare risorse
            if self.boot_telemetry.timer.isActive():
                self.boot_telemetry.timer.stop()

        telemetry_anim.finished.connect(hide_and_reset_telemetry)
        telemetry_anim.start()

        # Mantieni le animazioni come attributi per evitare garbage collection
        self._console_anim = console_anim
        self._telemetry_anim = telemetry_anim

        self.status_bar.clearMessage()
        self.footer_right.show_operational()  # Nascondi progress bar, mostra status cards

        self._update_license_status_bar()

        # Animazione fade-in per il footer sinistro
        self.footer_left.fade_in(400)

        # Assicura che lo stato del toggle sia corretto (footer_left visibile)
        self._footer_stats_mode = False

        # FINAL: Show visible TOAST instead of status bar message
        # Delay increased to 500ms to ensure UI is stable and Toast appears ON TOP
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

        # Connect Autopilot Real-time updates
        if hasattr(self, "timbrature_bot_panel"):
            try:
                self.timbrature_bot_panel.autopilot_changed.connect(
                    self._update_autopilot_status_ui
                )
            except Exception:
                pass

        # Monitoraggio Abilitazioni ISAB (Proattivo)
        QTimer.singleShot(2000, self._check_isab_authorizations)

    def _check_isab_authorizations(self):
        """Verifica dipendenti con abilitazione ISAB in scadenza e mostra notifica."""
        try:
            expiring = check_expiring_isab_authorizations()

            # Aggiorna Badge Sidebar Dipendenti (Somma di Scaduti + In Scadenza)
            total_alerts = len(expiring)
            if hasattr(self, "sidebar") and hasattr(self.sidebar, "btn_dipendenti"):
                self.sidebar.btn_dipendenti.set_badge(total_alerts)

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
                msg,
                "warning" if in_scadenza or scaduti else "info",
                8000,
                position="bottom_right",
            )

        except Exception as e:
            print(f"Errore monitoraggio autorizzazioni: {e}")

    def _update_license_status_bar(self):
        """Aggiorna le etichette della licenza nella status bar."""
        license_info = get_license_info()
        if license_info:
            client = license_info.get("Cliente", "N/D")
            expiry = license_info.get("Scadenza Licenza", "N/D")
            hw_id = license_info.get("Hardware ID", "N/D")
            config = config_manager.load_config()
            last_login = config.get("last_login_date", "N/D")

            # Update last login date
            now_str = datetime.now().strftime("%d/%m/%Y %H:%M")
            config_manager.set_config_value("last_login_date", now_str)

            # Usa il nuovo widget grafico sinistro
            self.footer_left.update_info(client, expiry, last_login, hw_id)
            self.footer_left.setVisible(True)

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

        # Notifica tray tramite controller
        if hasattr(self, "tray_controller"):
            self.tray_controller.show_message(
                "Aggiornamento Disponibile",
                f"È uscita la versione {new_version}. Clicca qui per scaricarla.",
            )

    def show_background_notification(
        self, title: str, message: str, is_error: bool = False
    ):
        """
        Mostra una notifica di sistema (Toast) se l'applicazione non è attiva.
        """
        is_active = self.isActiveWindow() and not self.isMinimized()

        if not is_active and hasattr(self, "tray_controller"):
            icon = (
                QSystemTrayIcon.MessageIcon.Critical
                if is_error
                else QSystemTrayIcon.MessageIcon.Information
            )
            self.tray_controller.show_message(title, message, icon, 5000)
            QApplication.alert(self, 0)

    def show_toast(self, message: str, duration: int = 3000):
        """Mostra una notifica toast."""
        ToastManager.instance().show(message, "info", duration)

    def _load_styles(self):
        """Carica i fogli di stile QSS."""
        for qss in ["main_window.qss", "message_box.qss"]:
            path = Path(f"assets/styles/{qss}")
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    self.setStyleSheet(self.styleSheet() + f.read())

    def _setup_ui(self):
        """Configura l'interfaccia con Placeholders per Lazy Loading."""
        self.status_bar = QStatusBar()
        # Footer con gradiente sfumato e bordo superiore accentuato
        self.status_bar.setStyleSheet(
            """
            QStatusBar {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FFFFFF,
                    stop:1 #F5F5F5
                );
                border-top: 2px solid qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #E0E0E0,
                    stop:0.5 #BDBDBD,
                    stop:1 #E0E0E0
                );
                min-height: 65px;
            }
        """
        )
        self.setStatusBar(self.status_bar)

        # Toggle Button per Footer Stats (sinistra)
        from src.core.constants import Icons
        from src.utils.helpers import get_asset_path, get_colored_icon

        self.footer_toggle_btn = QPushButton()
        self.footer_toggle_btn.setIcon(
            get_colored_icon(get_asset_path(Icons.ACTIVITY), "#000000")
        )
        self.footer_toggle_btn.setIconSize(QSize(20, 20))
        self.footer_toggle_btn.setFixedSize(40, 40)
        self.footer_toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.footer_toggle_btn.setToolTip("Toggle System Metrics / License Info")
        self.footer_toggle_btn.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 8px;
                margin: 0 5px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.05);
            }
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 0.1);
            }
        """
        )
        self.footer_toggle_btn.clicked.connect(self._toggle_footer_stats)
        self.status_bar.addWidget(self.footer_toggle_btn)

        # Stato toggle: False = footer_left visibile, True = boot_telemetry visibile
        self._footer_stats_mode = False

        # 1. LEFT: Mega Widget (Cliente, Scadenza, Login, Accounts)
        self.footer_left = FooterLeftWidget()
        self.footer_left.setVisible(True)
        # Connessione click per navigare a Impostazioni -> Configurazione
        self.footer_left.portale_clicked.connect(self._navigate_to_settings_config)
        self.footer_left.safework_clicked.connect(self._navigate_to_settings_config)
        self.status_bar.addWidget(self.footer_left)

        # 1b. LEFT: Boot Telemetry (Hacker Mode)
        self.boot_telemetry = BootTelemetryWidget()
        self.boot_telemetry.setVisible(True)
        self.status_bar.addWidget(self.boot_telemetry)

        # 3. STARTUP CONSOLE (Centrale)
        self.startup_console = StartupConsole()
        self.startup_console.setVisible(True)
        self.status_bar.addWidget(self.startup_console, 1)

        # 2. RIGHT: Status Cards (Contenute in FooterRightWidget)
        self.status_portale = StatusCard("Portale Fornitori")
        self.status_safework = StatusCard("SafeWork")

        # Connessione click per navigare a Impostazioni -> Configurazione
        self.status_portale.clicked.connect(self._navigate_to_settings_config)
        self.status_safework.clicked.connect(self._navigate_to_settings_config)

        self.footer_right = FooterRightWidget(self.status_portale, self.status_safework)
        self.status_bar.addPermanentWidget(self.footer_right)

        # Initial Autopilot Status Update
        self._update_autopilot_status_ui()

        # Timer per il countdown Autopilot (aggiorna ogni 5 secondi)
        self.autopilot_timer = QTimer(self)
        self.autopilot_timer.timeout.connect(self._update_autopilot_status_ui)
        self.autopilot_timer.start(5000)  # 5 secondi

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # SIDEBAR
        self.sidebar = SidebarWidget()
        self.sidebar.navigation_requested.connect(
            self.navigation_controller.navigate_to
        )
        self.sidebar.automation_tab_requested.connect(
            self._handle_automation_tab_change
        )
        self.sidebar.notifications_tab_requested.connect(
            self._handle_notifications_tab_change
        )
        main_layout.addWidget(self.sidebar)

        # CONTENT AREA
        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(20, 20, 20, 20)

        self.update_banner = UpdateBanner()
        self.update_banner.download_requested.connect(self._on_download_update_clicked)
        content_layout.addWidget(self.update_banner)

        self.global_search = QLineEdit()
        self.global_search.setPlaceholderText(
            "Ricerca Universale (OdA, Dipendenti, Log...) - Ctrl+F"
        )
        self.global_search.setMinimumHeight(40)
        self.global_search.returnPressed.connect(
            lambda: self.search_controller.perform_search(self.global_search.text())
        )
        content_layout.addWidget(self.global_search)

        # Page Stack con Placeholder
        self.page_stack = QStackedWidget()
        for i in range(12):  # Increased range for new pages
            placeholder = QWidget()
            # Inseriamo un layout per indicare il caricamento se necessario
            self.page_stack.addWidget(placeholder)
            setattr(self, f"_panel_initialized_{i}", False)

        content_layout.addWidget(self.page_stack)
        main_layout.addWidget(content_area)

    def _connect_signals(self):
        """Collega i segnali globali."""
        NotificationManager.instance().unread_count_changed.connect(
            self.sidebar.group_notifiche.header_btn.set_badge
        )
        self.sidebar.group_notifiche.header_btn.set_badge(
            NotificationManager.instance().get_unread_count()
        )

    def _setup_shortcuts(self):
        """Configura le scorciatoie da tastiera globali."""
        self.shortcut_f5 = QShortcut(QKeySequence(Qt.Key.Key_F5), self)
        self.shortcut_f5.activated.connect(self._handle_f5)

        self.shortcut_search = QShortcut(QKeySequence("Ctrl+F"), self)
        self.shortcut_search.activated.connect(self._handle_ctrl_f)

    def _handle_f5(self):
        """Gestisce F5 tramite dispatch map."""
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

    def _handle_ctrl_f(self):
        """Gestisce Ctrl+F."""
        self.global_search.setFocus()
        self.global_search.selectAll()

    def _on_help_requested(self, section_title):
        self.navigation_controller.navigate_to(PageIndex.HELP)
        self.help_panel.open_section(section_title)

    def _update_autopilot_status_ui(self):
        """Aggiorna le card di stato con il countdown del task più imminente."""
        from PyQt6.QtCore import QTime

        config = config_manager.load_config()

        # Lista di tutti i task autopilot possibili
        # (Sito, Nome Display, Enabled Key, Time Key)
        tasks = [
            (
                "PF",
                "TIMBRATURE",
                "timbrature_autopilot_enabled",
                "timbrature_autopilot_time",
            ),
            (
                "PF",
                "SCARICO ODA",
                "scarico_oda_generale_autopilot_enabled",
                "scarico_oda_generale_autopilot_time",
            ),
            (
                "SW",
                "RICERCA PDL",
                "ricerca_pdl_autopilot_enabled",
                "ricerca_pdl_autopilot_time",
            ),
        ]

        now = QTime.currentTime()
        # Monitoriamo il task più imminente per OGNI sito
        imminent_pf = None  # (nome, secondi)
        imminent_sw = None  # (nome, secondi)
        min_secs_pf = float("inf")
        min_secs_sw = float("inf")

        for site, name, enabled_key, time_key in tasks:
            if config.get(enabled_key, False):
                target_time_str = config.get(time_key, "09:00")
                # Supporto sia per "09:00" che per "9:00"
                target_time = QTime.fromString(target_time_str, "HH:mm")
                if not target_time.isValid():
                    target_time = QTime.fromString(target_time_str, "H:mm")

                if not target_time.isValid():
                    continue

                secs_to = now.secsTo(target_time)
                if secs_to < 0:
                    secs_to += 24 * 3600

                if site == "PF":
                    if secs_to < min_secs_pf:
                        min_secs_pf = secs_to
                        imminent_pf = (name, secs_to)
                elif site == "SW":
                    if secs_to < min_secs_sw:
                        min_secs_sw = secs_to
                        imminent_sw = (name, secs_to)

        # Helper per formattare il countdown
        def format_countdown(name, secs):
            hours = secs // 3600
            mins = (secs % 3600) // 60
            countdown_text = f"TRA {hours}H {mins}M" if hours > 0 else f"TRA {mins}M"
            return f"{name}: {countdown_text}"

        # Aggiorna Portale Fornitori
        if imminent_pf:
            self.status_portale.setAutopilot(True, format_countdown(*imminent_pf))
        else:
            self.status_portale.setAutopilot(False)

        # Aggiorna SafeWork
        if imminent_sw:
            self.status_safework.setAutopilot(True, format_countdown(*imminent_sw))
        else:
            self.status_safework.setAutopilot(False)

    def _on_settings_saved(self):
        if hasattr(self, "scarico_panel"):
            self.scarico_panel.refresh_fornitori()
        if hasattr(self, "dettagli_panel"):
            self.dettagli_panel.refresh_fornitori()
        if hasattr(self, "timbrature_bot_panel"):
            self.timbrature_bot_panel.refresh_fornitori()

        self.telegram.start_service()
        self._update_autopilot_status_ui()  # Update UI cards

        # Aggiorna account visualizzati nel footer sinistro
        if hasattr(self, "footer_left"):
            self.footer_left.refresh_accounts()

        ToastManager.instance().show("Impostazioni salvate!", "success")

    def _check_and_start_contabilita_update(self):
        config = config_manager.load_config()
        if config.get("enable_auto_update_contabilita", False):
            # Assicuriamoci che il pannello sia caricato se dobbiamo avviarlo
            self.navigation_controller.get_panel(PageIndex.STRUMENTALE)
            if hasattr(self, "contabilita_panel"):
                self.contabilita_panel.start_import_process()

    def _on_download_update_clicked(self, url):
        import webbrowser

        webbrowser.open(url)

    # Wrapper per compatibilità
    def navigate_to_panel(self, panel_key: str):
        """Naviga verso il pannello specificato tramite chiave stringa."""
        self.navigation_controller.navigate_to_panel(panel_key)

    def _navigate_to(self, index: int):
        """Naviga verso un indice di pagina specifico."""
        self.navigation_controller.navigate_to(index)

    def _navigate_to_oda(self, oda_code: str):
        """Naviga verso la contabilità e cerca un OdA specifico."""
        self.navigation_controller.navigate_to(PageIndex.STRUMENTALE)
        if hasattr(self, "contabilita_panel"):
            self.contabilita_panel.set_search_query(oda_code)

    def _navigate_to_extended(self, tab_idx: int, query: str):
        """Naviga verso un sub-tab specifico del pannello Contabilità."""
        self.navigation_controller.navigate_to(PageIndex.STRUMENTALE)
        if hasattr(self, "contabilita_panel"):
            self.contabilita_panel.main_tabs.setCurrentIndex(tab_idx)
            self.contabilita_panel.set_search_query(query)

    def _navigate_to_dataease(self, query: str):
        """Naviga verso il pannello Scarico Ore (DataEase)."""
        self.navigation_controller.navigate_to(PageIndex.DATAEASE)
        if hasattr(self, "scarico_ore_panel"):
            self.scarico_ore_panel.set_search_query(query)

    def _navigate_to_timbrature(self, query: str):
        """Naviga verso il database Timbrature."""
        self.navigation_controller.navigate_to(PageIndex.TIMBRATURE)
        if hasattr(self, "timbrature_db_panel"):
            self.timbrature_db_panel.search_input.setText(query)

    def _handle_automation_tab_change(self, tab_index: int):
        """Gestisce il cambio tab interno per il pannello Automazioni."""
        # 1. Naviga al pannello Automazioni se non ci siamo già
        self.navigation_controller.navigate_to(PageIndex.AUTOMAZIONI)

        # 2. Imposta il tab corretto
        if hasattr(self, "automazioni_widget"):
            self.automazioni_widget.setCurrentIndex(tab_index)

    def _handle_notifications_tab_change(self, tab_index: int):
        """Gestisce il cambio tab interno per il pannello Notifiche."""
        # 1. Naviga al pannello Notifiche se non ci siamo già
        self.navigation_controller.navigate_to(PageIndex.NOTIFICATIONS)

        # 2. Imposta il tab corretto (0: Notifiche, 1: Audit)
        if hasattr(self, "notifications_panel"):
            self.notifications_panel.tabs.setCurrentIndex(tab_index)

    def analyze_with_lyra(self, context_text: str):
        """Passa al contesto Lyra."""

    def show_settings(self):
        """Mostra il pannello delle impostazioni."""
        self.navigation_controller.navigate_to(PageIndex.SETTINGS)

    def _navigate_to_settings_config(self):
        """Naviga al pannello Impostazioni -> tab Configurazione."""
        # STEP 1: Forza il caricamento del pannello PRIMA di navigare
        _ = self.navigation_controller.get_panel(PageIndex.SETTINGS)

        # STEP 2: Naviga al pannello (ora sicuramente caricato)
        self.navigation_controller.navigate_to(PageIndex.SETTINGS)

        # STEP 3: Imposta il tab immediatamente (il pannello è già caricato)
        if hasattr(self, "settings_panel") and self.settings_panel is not None:
            # Usa QTimer per assicurare che l'UI sia aggiornata prima di cambiare tab
            QTimer.singleShot(50, lambda: self.settings_panel.tabs.setCurrentIndex(0))

    def _toggle_footer_stats(self):
        """Toggle tra System Metrics (boot_telemetry) e License Info (footer_left)."""
        self._footer_stats_mode = not self._footer_stats_mode

        if self._footer_stats_mode:
            # Mostra boot_telemetry, nascondi footer_left
            self.footer_left.setVisible(False)
            self.boot_telemetry.setVisible(True)
            # Assicura che non ci siano effetti residui di opacity
            self.boot_telemetry.setGraphicsEffect(None)
            # Restart timer e forza update immediato
            if not self.boot_telemetry.timer.isActive():
                self.boot_telemetry.timer.start(1000)
            self.boot_telemetry._update_stats()  # Update immediato
        else:
            # Mostra footer_left, nascondi boot_telemetry
            self.boot_telemetry.setVisible(False)
            self.footer_left.setVisible(True)
            # Stop timer per risparmiare risorse
            if self.boot_telemetry.timer.isActive():
                self.boot_telemetry.timer.stop()

    def closeEvent(self, event):
        """
        Gestisce l'evento di chiusura della finestra.
        Se non forzata, nasconde l'applicazione nel tray.
        """
        if self._force_quit:
            if self.telegram:
                self.telegram.stop_service()
            config = config_manager.load_config()
            if config.get("auto_backup", True):
                BackupManager.create_backup()
            event.accept()
            return
        if self.isVisible():
            self.hide()
            event.ignore()
