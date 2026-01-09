"""
Bot TS - Main Window
Finestra principale dell'applicazione.
"""

import os
from pathlib import Path

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import (
    QColor,
    QFont,
    QKeySequence,
    QPainter,
    QPixmap,
    QShortcut,
)
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QSplashScreen,
    QStackedWidget,
    QStatusBar,
    QSystemTrayIcon,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.core.app_updater import check_for_updates
from src.core.backup_manager import BackupManager

# Import Core
from src.core.lyra_sentinel import LyraSentinel
from src.core.notification_manager import NotificationManager
from src.core.telegram_bridge import TelegramUIBridge
from src.core.telegram_manager import TelegramService
from src.gui.contabilita_panel import ContabilitaPanel
from src.gui.controllers.bot_controller import BotController
from src.gui.controllers.navigation_controller import NavigationController
from src.gui.controllers.search_controller import SearchController
from src.gui.controllers.service_controller import ServiceController
from src.gui.controllers.tray_controller import TrayController
from src.gui.dashboard_panel import DashboardPanel
from src.gui.help_panel import HelpPanel
from src.gui.lyra_panel import LyraPanel
from src.gui.notifications_panel import NotificationsPanel

# Import Panels
from src.gui.panels import (
    CaricoTSPanel,
    DettagliOdAPanel,
    ScaricaTSPanel,
    ScaricoPDLPanel,
    TimbratureBotPanel,
    TimbratureDBPanel,
)
from src.gui.scarico_ore_panel import ScaricoOrePanel
from src.gui.settings_panel import SettingsPanel
from src.gui.styles import apply_theme
from src.gui.widgets.sidebar_widget import SidebarWidget
from src.gui.widgets.status_card import StatusCard

# Import UI/UX Components
from src.gui.widgets.toast import ToastManager
from src.gui.widgets.update_banner import UpdateBanner


class MainWindow(QMainWindow):
    """Finestra principale dell'applicazione SyncroJob."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SyncroJob")
        self.setMinimumSize(1200, 800)

        # Load main_window.qss
        style_file_path = Path("assets/styles/main_window.qss")
        if style_file_path.exists():
            with open(style_file_path, "r", encoding="utf-8") as f:
                main_window_qss = f.read()
                self.setStyleSheet(main_window_qss)
        else:
            print(f"Warning: {style_file_path} not found.")

        # Load message_box.qss
        message_box_style_path = Path("assets/styles/message_box.qss")
        if message_box_style_path.exists():
            with open(message_box_style_path, "r", encoding="utf-8") as f:
                message_box_qss = f.read()
                # Append to existing stylesheet
                self.setStyleSheet(self.styleSheet() + message_box_qss)
        else:
            print(f"Warning: {message_box_style_path} not found.")

        # Apply Global Theme (light.qss)
        apply_theme(QApplication.instance(), "light")

        # Abilita Drag & Drop
        self.setAcceptDrops(True)

        self._current_page_index = 0
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

        # --- REMAINING INIT ---
        # Registrazione pannelli bot
        self.bot_controller.register_panels([
            self.dettagli_panel,
            self.scarico_panel,
            self.timbrature_bot_panel,
            self.carico_panel,
            self.pdl_panel
        ])

        # Avvio servizi
        self.service_controller.start_all()

        # Avvio automatico importazione contabilità se abilitato
        QTimer.singleShot(1000, self._check_and_start_contabilita_update)

    def _on_anomalies_found(self, count):
        """Gestisce le anomalie trovate da Lyra."""
        self.sidebar.btn_lyra.set_badge(count)
        if count > 0:
            ToastManager.instance().show(f"⚠️ Lyra ha rilevato {count} anomalie", "warning")

    def _show_update_banner(self, new_version, download_url, changelog):
        """Mostra un banner informativo per la nuova versione."""
        self.update_banner.show_update(new_version, download_url, changelog)

        # Notifica tray tramite controller
        self.tray_controller.show_message(
            "Aggiornamento Disponibile",
            f"È uscita la versione {new_version}. Clicca qui per scaricarla.",
        )

    def show_background_notification(self, title: str, message: str, is_error: bool = False):
        """
        Mostra una notifica di sistema (Toast) se l'applicazione non è attiva (in background o minimizzata).
        """
        # Controlla se l'applicazione è in primo piano
        is_active = self.isActiveWindow() and not self.isMinimized()

        if not is_active:
            icon = (
                QSystemTrayIcon.MessageIcon.Critical if is_error else QSystemTrayIcon.MessageIcon.Information
            )
            self.tray_controller.show_message(title, message, icon, 5000)

            # Flash Taskbar come avviso visivo aggiuntivo
            QApplication.alert(self, 0)

    def show_toast(self, message: str, duration: int = 3000):
        """Mostra una notifica toast (Wrapper for backward compatibility)."""
        ToastManager.instance().show(message, "info", duration)

    def _setup_shortcuts(self):
        """Configura le scorciatoie da tastiera globali."""
        # F5 - Aggiorna / Avvia
        self.shortcut_f5 = QShortcut(QKeySequence(Qt.Key.Key_F5), self)
        self.shortcut_f5.activated.connect(self._handle_f5)

        # Ctrl+F - Cerca
        self.shortcut_search = QShortcut(QKeySequence("Ctrl+F"), self)
        self.shortcut_search.activated.connect(self._handle_ctrl_f)

        # Ctrl+S - Salva Impostazioni
        self.shortcut_save = QShortcut(QKeySequence("Ctrl+S"), self)
        self.shortcut_save.activated.connect(self._handle_ctrl_s)

    def _handle_f5(self):
        """Gestisce F5 in base alla vista corrente."""
        idx = self.page_stack.currentIndex()

        if idx == 0:  # Dashboard
            self.dashboard_panel.refresh_data()
            self.show_toast("Dashboard aggiornata")
        # Database Page (Index 3)
        elif idx == 3:
            tab_idx = self.database_widget.currentIndex()
            if tab_idx == 0:  # Timbrature
                self.timbrature_db_panel.refresh_data()
                self.show_toast("Dati aggiornati")
            elif tab_idx == 1:  # Contabilità
                self.contabilita_panel.refresh_tabs()
                self.show_toast("Contabilità aggiornata (Vista)")
            elif tab_idx == 2:  # Scarico Ore
                self.scarico_ore_panel._start_update()

    def _handle_ctrl_f(self):
        """Gestisce Ctrl+F per il focus sulla ricerca."""
        idx = self.page_stack.currentIndex()

        # Database Page
        if idx == 3:
            tab_idx = self.database_widget.currentIndex()
            if tab_idx == 0:  # Timbrature
                self.timbrature_db_panel.search_input.setFocus()
                self.timbrature_db_panel.search_input.selectAll()
            elif tab_idx == 1:  # Contabilità
                if self.contabilita_panel.search_input.isVisible():
                    self.contabilita_panel.search_input.setFocus()
                    self.contabilita_panel.search_input.selectAll()
            elif tab_idx == 2:  # Scarico Ore
                self.scarico_ore_panel.search_input.setFocus()
                self.scarico_ore_panel.search_input.selectAll()

    def _handle_ctrl_s(self):
        """Gestisce Ctrl+S per salvare le impostazioni."""
        if self.page_stack.currentIndex() == 4:
            self.settings_panel.save_btn.click()

    def _setup_ui(self):
        """Configura l'interfaccia."""
        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Global Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progressBar")
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        self.progress_bar.setMaximumWidth(200)
        self.status_bar.addPermanentWidget(self.progress_bar)

        # Widget centrale
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principale orizzontale
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # === SIDEBAR ===
        self.sidebar = SidebarWidget()
        self.sidebar.navigation_requested.connect(self.navigation_controller.navigate_to)
        main_layout.addWidget(self.sidebar)

        # === CONTENT AREA ===
        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(20, 20, 20, 20)

        # --- UPDATE BANNER ---
        self.update_banner = UpdateBanner()
        self.update_banner.download_requested.connect(self._on_download_update_clicked)
        content_layout.addWidget(self.update_banner)

        # --- GLOBAL SEARCH BAR ---
        search_container = QHBoxLayout()
        search_container.setContentsMargins(0, 0, 0, 10)

        self.global_search = QLineEdit()
        self.global_search.setObjectName("globalSearchInput")
        self.global_search.setPlaceholderText("🔍 Ricerca Universale (OdA, Dipendenti, Log...) - Ctrl+F")
        self.global_search.setMinimumHeight(40)
        self.global_search.returnPressed.connect(
            lambda: self.search_controller.perform_search(self.global_search.text())
        )

        search_container.addWidget(self.global_search)
        content_layout.addLayout(search_container)

        # Stack per le pagine principali
        self.page_stack = QStackedWidget()

        # Crea i pannelli individuali
        self.dashboard_panel = DashboardPanel()
        self.scarico_panel = ScaricaTSPanel()
        self.carico_panel = CaricoTSPanel()
        self.dettagli_panel = DettagliOdAPanel()
        self.pdl_panel = ScaricoPDLPanel()
        self.timbrature_bot_panel = TimbratureBotPanel()
        self.timbrature_db_panel = TimbratureDBPanel()
        self.contabilita_panel = ContabilitaPanel()
        self.scarico_ore_panel = ScaricoOrePanel()
        self.settings_panel = SettingsPanel()
        self.help_panel = HelpPanel()
        self.lyra_panel = LyraPanel()
        self.notifications_panel = NotificationsPanel()

        # Collega il segnale di update dal bot al database
        self.timbrature_bot_panel.data_updated.connect(self.timbrature_db_panel.refresh_data)

        # --- Page 1: Automazioni ---
        self.automazioni_widget = QTabWidget()

        # Global Status Card
        self.global_status_card = StatusCard("Stato Attività")
        self.global_status_card.setMinimumWidth(350)
        self.global_status_card.setMaximumHeight(40)
        self.automazioni_widget.setCornerWidget(self.global_status_card, Qt.Corner.TopRightCorner)

        # Group 1: Portale Fornitori
        self.tab_fornitori = QTabWidget()
        self.tab_fornitori.addTab(self.dettagli_panel, "📋 Dettagli OdA")
        self.tab_fornitori.addTab(self.scarico_panel, "📥 Scarico TS")
        self.tab_fornitori.addTab(self.timbrature_bot_panel, "⏱️ Timbrature")
        self.tab_fornitori.addTab(self.carico_panel, "📤 Carico TS")

        # Group 2: SafeWork
        self.tab_safework = QTabWidget()
        self.tab_safework.addTab(self.pdl_panel, "🛡️ Scarico PDL")

        self.automazioni_widget.addTab(self.tab_fornitori, "Portale Fornitori")
        self.automazioni_widget.addTab(self.tab_safework, "SafeWork")

        # --- Page 3: Database ---
        self.database_widget = QTabWidget()
        self.database_widget.addTab(self.timbrature_db_panel, "Timbrature Isab")
        self.database_widget.addTab(self.contabilita_panel, "Strumentale")
        self.database_widget.addTab(self.scarico_ore_panel, "DataEase")

        # Aggiungi le pagine allo stack
        self.page_stack.addWidget(self.dashboard_panel)  # 0
        self.page_stack.addWidget(self.automazioni_widget)  # 1
        self.page_stack.addWidget(self.lyra_panel)  # 2
        self.page_stack.addWidget(self.database_widget)  # 3
        self.page_stack.addWidget(self.settings_panel)  # 4
        self.page_stack.addWidget(self.help_panel)  # 5
        self.page_stack.addWidget(self.notifications_panel)  # 6

        content_layout.addWidget(self.page_stack)
        main_layout.addWidget(content_area)

    def _connect_signals(self):
        """Collega i segnali."""
        # Notification Badge
        NotificationManager.instance().unread_count_changed.connect(self.sidebar.btn_notifications.set_badge)
        self.sidebar.btn_notifications.set_badge(NotificationManager.instance().get_unread_count())

        # Aggiornamento live impostazioni
        self.settings_panel.settings_saved.connect(self._on_settings_saved)
        self.settings_panel.request_help_section.connect(self._on_help_requested)

        # Segnali di navigazione tab interni (delegati a bot_controller)
        self.automazioni_widget.currentChanged.connect(self.bot_controller.update_global_status)
        self.tab_fornitori.currentChanged.connect(self.bot_controller.update_global_status)
        self.tab_safework.currentChanged.connect(self.bot_controller.update_global_status)

    def _on_help_requested(self, section_title):
        """Gestisce la richiesta di apertura di una sezione specifica della guida."""
        self.navigation_controller.navigate_to(5)
        self.help_panel.open_section(section_title)

    def _on_settings_saved(self):
        """Aggiorna i pannelli quando le impostazioni vengono salvate."""
        self.scarico_panel.refresh_fornitori()
        self.dettagli_panel.refresh_fornitori()
        self.timbrature_bot_panel.refresh_fornitori()
        self.telegram.start_service()
        ToastManager.instance().show("Impostazioni salvate con successo!", "success")

    def _check_and_start_contabilita_update(self):
        """Controlla la configurazione e avvia l'update contabilità se abilitato."""
        config = config_manager.load_config()
        if config.get("enable_auto_update_contabilita", False):
            self.contabilita_panel.start_import_process()

    def _on_download_update_clicked(self, url):
        """Gestisce il click sul pulsante scarica del banner."""
        import webbrowser
        webbrowser.open(url)
        ToastManager.instance().show("Download avviato nel browser", "success")

    # --- WRAPPERS DI COMPATIBILITÀ ---
    def navigate_to_panel(self, panel_key: str):
        self.navigation_controller.navigate_to_panel(panel_key)

    def analyze_with_lyra(self, context_text: str):
        self.navigation_controller.analyze_with_lyra(context_text)

    def show_settings(self):
        self.navigation_controller.navigate_to(4)

    def closeEvent(self, event):
        """Gestisce la chiusura della finestra."""
        if self._force_quit:
            if self.telegram:
                self.telegram.stop_service()
            config = config_manager.load_config()
            if config.get("auto_backup", True):
                BackupManager.create_backup()
            if self.settings_panel.has_unsaved_changes():
                if not self.settings_panel.prompt_save_if_needed():
                    event.ignore()
                    return
            event.accept()
            return

        if self.isVisible():
            self.hide()
            event.ignore()
