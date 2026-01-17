"""
Bot TS - Main Window
Finestra principale dell'applicazione SyncroJob.
Implementa Lazy Loading dei pannelli per prestazioni ottimali.
"""

from datetime import datetime
from enum import IntEnum
from pathlib import Path

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QStackedWidget,
    QStatusBar,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.core.backup_manager import BackupManager
from src.core.constants import Icons
from src.core.license_validator import get_license_info
from src.core.lyra_sentinel import LyraSentinel
from src.core.notification_manager import NotificationManager
from src.core.telegram_bridge import TelegramUIBridge
from src.core.telegram_manager import TelegramService
from src.gui.controllers.bot_controller import BotController
from src.gui.controllers.navigation_controller import NavigationController
from src.gui.controllers.search_controller import SearchController
from src.gui.controllers.service_controller import ServiceController
from src.gui.controllers.tray_controller import TrayController
from src.gui.styles import apply_theme
from src.gui.widgets.sidebar_widget import SidebarWidget
from src.gui.widgets.status_card import StatusCard
from src.gui.widgets.toast import ToastManager
from src.gui.widgets.update_banner import UpdateBanner


class PageIndex(IntEnum):
    """Indici delle pagine nello StackedWidget principale."""

    DASHBOARD = 0
    AUTOMAZIONI = 1
    LYRA = 2
    DATABASE = 3
    SETTINGS = 4
    HELP = 5
    NOTIFICATIONS = 6


from src.core.version import __version__ as VERSION  # Importo la versione

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
        # Coda di caricamento: (Azione, Descrizione)
        self._preload_tasks = [
            (
                lambda: self.navigation_controller.get_panel(PageIndex.DATABASE),
                "Inizializzazione Database",
            ),
            (
                lambda: self.timbrature_db_panel.refresh_data(),
                "Popolamento Timbrature Isab",
            ),
            (
                lambda: self.contabilita_panel.refresh_tabs(),
                "Caricamento Registro Strumentale",
            ),
            (
                lambda: self.scarico_ore_panel._start_update(),
                "Sincronizzazione DataEase",
            ),
            (
                lambda: self.navigation_controller.get_panel(PageIndex.AUTOMAZIONI),
                "Preparazione Motori Automazione",
            ),
            (
                lambda: self.navigation_controller.get_panel(PageIndex.LYRA),
                "Avvio Analisi Lyra",
            ),
            (
                lambda: self.navigation_controller.get_panel(PageIndex.SETTINGS),
                "Configurazione Preferenze",
            ),
            (
                lambda: self.navigation_controller.get_panel(PageIndex.NOTIFICATIONS),
                "Centro Notifiche",
            ),
            (
                lambda: self.navigation_controller.get_panel(PageIndex.HELP),
                "Guida e Documentazione",
            ),
        ]
        self._total_preload = len(self._preload_tasks)

        # Attiva indicatori
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, self._total_preload)
        self.progress_bar.setValue(0)

        # Avvia la catena
        QTimer.singleShot(100, self._process_next_preload)

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

        # Feedback Utente
        self.status_bar.showMessage(f"Ottimizzazione: {description}...")
        self.progress_bar.setValue(self._total_preload - len(self._preload_tasks))

        # Esegui azione (Safe)
        try:
            action()
        except Exception as e:
            print(f"Error during deep preload of {description}: {e}")

        # TRUCCO PER REATTIVITÀ: Forza l'app a gestire i click e il mouse PRIMA del prossimo task
        QApplication.processEvents()

        # Pianifica il prossimo step con un delay leggermente superiore per fluidità
        QTimer.singleShot(300, self._process_next_preload)

    def _finalize_preload(self):
        """Conclude la sequenza di caricamento."""
        from PyQt6 import sip

        if sip.isdeleted(self):
            return

        self.progress_bar.setVisible(False)
        self._update_license_status_bar()
        self.status_bar.showMessage("SyncroJob è pronto. Tutti i servizi attivi.", 3000)

    def _update_license_status_bar(self):
        """Aggiorna le etichette della licenza nella status bar."""
        license_info = get_license_info()
        if license_info:
            client = license_info.get("Cliente", "N/D")
            expiry = license_info.get("Scadenza Licenza", "N/D")
            config = config_manager.load_config()
            last_login = config.get("last_login_date", "N/D")

            # Update last login date
            now_str = datetime.now().strftime("%d/%m/%Y %H:%M")
            config_manager.set_config_value("last_login_date", now_str)

            self.lbl_license.setText(f"Licenza: {client}")
            self.lbl_expiry.setText(f"Scadenza: {expiry}")
            self.lbl_last_login.setText(f"Ultimo accesso: {last_login}")

            for lbl in [self.lbl_license, self.lbl_expiry, self.lbl_last_login]:
                lbl.setVisible(True)

    def _on_anomalies_found(self, count):
        """Gestisce le anomalie trovate da Lyra."""
        if hasattr(self, "sidebar"):
            self.sidebar.btn_lyra.set_badge(count)
        if count > 0:
            ToastManager.instance().show(f"⚠️ Lyra ha rilevato {count} anomalie", "warning")

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

    def show_background_notification(self, title: str, message: str, is_error: bool = False):
        """
        Mostra una notifica di sistema (Toast) se l'applicazione non è attiva.
        """
        is_active = self.isActiveWindow() and not self.isMinimized()

        if not is_active and hasattr(self, "tray_controller"):
            icon = (
                QSystemTrayIcon.MessageIcon.Critical if is_error else QSystemTrayIcon.MessageIcon.Information
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
        self.setStatusBar(self.status_bar)

        # License info in status bar (inizialmente nascoste)
        self.lbl_license = QLabel()
        self.lbl_expiry = QLabel()
        self.lbl_last_login = QLabel()

        for lbl in [self.lbl_license, self.lbl_expiry, self.lbl_last_login]:
            lbl.setVisible(False)
            lbl.setStyleSheet("color: #495057; font-size: 12px; margin-right: 15px;")
            self.status_bar.addWidget(lbl)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMaximumWidth(200)
        self.status_bar.addPermanentWidget(self.progress_bar)

        # Status Cards Separate
        self.status_portale = StatusCard("Portale Fornitori")
        self.status_portale.setMinimumWidth(180)
        self.status_bar.addPermanentWidget(self.status_portale)

        self.status_safework = StatusCard("SafeWork")
        self.status_safework.setMinimumWidth(180)
        self.status_bar.addPermanentWidget(self.status_safework)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # SIDEBAR
        self.sidebar = SidebarWidget()
        self.sidebar.navigation_requested.connect(self.navigation_controller.navigate_to)
        main_layout.addWidget(self.sidebar)

        # CONTENT AREA
        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(20, 20, 20, 20)

        self.update_banner = UpdateBanner()
        self.update_banner.download_requested.connect(self._on_download_update_clicked)
        content_layout.addWidget(self.update_banner)

        self.global_search = QLineEdit()
        self.global_search.setPlaceholderText("🔍 Ricerca Universale (OdA, Dipendenti, Log...) - Ctrl+F")
        self.global_search.setMinimumHeight(40)
        self.global_search.returnPressed.connect(
            lambda: self.search_controller.perform_search(self.global_search.text())
        )
        content_layout.addWidget(self.global_search)

        # Page Stack con Placeholder
        self.page_stack = QStackedWidget()
        for i in range(7):
            placeholder = QWidget()
            # Inseriamo un layout per indicare il caricamento se necessario
            self.page_stack.addWidget(placeholder)
            setattr(self, f"_panel_initialized_{i}", False)

        content_layout.addWidget(self.page_stack)
        main_layout.addWidget(content_area)

    def _connect_signals(self):
        """Collega i segnali globali."""
        NotificationManager.instance().unread_count_changed.connect(self.sidebar.btn_notifications.set_badge)
        self.sidebar.btn_notifications.set_badge(NotificationManager.instance().get_unread_count())

    def _setup_shortcuts(self):
        """Configura le scorciatoie da tastiera globali."""
        self.shortcut_f5 = QShortcut(QKeySequence(Qt.Key.Key_F5), self)
        self.shortcut_f5.activated.connect(self._handle_f5)

        self.shortcut_search = QShortcut(QKeySequence("Ctrl+F"), self)
        self.shortcut_search.activated.connect(self._handle_ctrl_f)

    def _handle_f5(self):
        """Gestisce F5."""
        idx = self.page_stack.currentIndex()
        if idx == PageIndex.DASHBOARD and hasattr(self, "dashboard_panel"):
            self.dashboard_panel.refresh_data()
        elif idx == PageIndex.DATABASE and hasattr(self, "database_widget"):
            tab_idx = self.database_widget.currentIndex()
            if tab_idx == 0:
                self.timbrature_db_panel.refresh_data()
            elif tab_idx == 1:
                self.contabilita_panel.refresh_tabs()
            elif tab_idx == 2:
                self.scarico_ore_panel._start_update()

    def _handle_ctrl_f(self):
        """Gestisce Ctrl+F."""
        self.global_search.setFocus()
        self.global_search.selectAll()

    def _on_help_requested(self, section_title):
        self.navigation_controller.navigate_to(PageIndex.HELP)
        self.help_panel.open_section(section_title)

    def _on_settings_saved(self):
        if hasattr(self, "scarico_panel"):
            self.scarico_panel.refresh_fornitori()
        if hasattr(self, "dettagli_panel"):
            self.dettagli_panel.refresh_fornitori()
        if hasattr(self, "timbrature_bot_panel"):
            self.timbrature_bot_panel.refresh_fornitori()
        self.telegram.start_service()
        ToastManager.instance().show("Impostazioni salvate!", "success")

    def _check_and_start_contabilita_update(self):
        config = config_manager.load_config()
        if config.get("enable_auto_update_contabilita", False):
            # Assicuriamoci che il pannello sia caricato se dobbiamo avviarlo
            self.navigation_controller.get_panel(PageIndex.DATABASE)
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
        self.navigation_controller.navigate_to(PageIndex.DATABASE)
        # Il pannello database ha diversi tab (Timbrature, Contabilità, Scarico Ore)
        # Assumiamo che tab 1 sia Contabilità (da verificare nel widget)
        if hasattr(self, "database_widget"):
            self.database_widget.setCurrentIndex(1)
            if hasattr(self, "contabilita_panel"):
                self.contabilita_panel.set_search_query(oda_code)

    def _navigate_to_extended(self, tab_idx: int, query: str):
        """Naviga verso un sub-tab specifico del pannello Contabilità."""
        self.navigation_controller.navigate_to(PageIndex.DATABASE)
        if hasattr(self, "database_widget"):
            self.database_widget.setCurrentIndex(1)
            if hasattr(self, "contabilita_panel"):
                self.contabilita_panel.main_tabs.setCurrentIndex(tab_idx)
                self.contabilita_panel.set_search_query(query)

    def _navigate_to_dataease(self, query: str):
        """Naviga verso il pannello Scarico Ore (DataEase)."""
        self.navigation_controller.navigate_to(PageIndex.DATABASE)
        if hasattr(self, "database_widget"):
            self.database_widget.setCurrentIndex(2)
            if hasattr(self, "scarico_ore_panel"):
                self.scarico_ore_panel.set_search_query(query)

    def _navigate_to_timbrature(self, query: str):
        """Naviga verso il database Timbrature."""
        self.navigation_controller.navigate_to(PageIndex.DATABASE)
        if hasattr(self, "database_widget"):
            self.database_widget.setCurrentIndex(0)
            if hasattr(self, "timbrature_db_panel"):
                self.timbrature_db_panel.search_input.setText(query)

    def analyze_with_lyra(self, context_text: str):
        """Passa il contesto a Lyra e naviga verso il pannello AI."""
        self.navigation_controller.analyze_with_lyra(context_text)

    def show_settings(self):
        """Mostra il pannello delle impostazioni."""
        self.navigation_controller.navigate_to(PageIndex.SETTINGS)

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
