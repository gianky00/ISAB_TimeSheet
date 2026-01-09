"""
Bot TS - Main Window
Finestra principale dell'applicazione SyncroJob.
Implementa Lazy Loading dei pannelli per prestazioni ottimali.
"""

from pathlib import Path

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
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
from src.gui.widgets.toast import ToastManager
from src.gui.widgets.update_banner import UpdateBanner


class MainWindow(QMainWindow):
    """Finestra principale dell'applicazione SyncroJob."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SyncroJob")
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
        self.navigation_controller.navigate_to(0)

        # Avvio automatico importazione contabilità se abilitato
        QTimer.singleShot(2000, self._check_and_start_contabilita_update)

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
        self.setStatusBar(self.status_bar)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMaximumWidth(200)
        self.status_bar.addPermanentWidget(self.progress_bar)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # SIDEBAR
        self.sidebar = SidebarWidget()
        self.sidebar.navigation_requested.connect(
            self.navigation_controller.navigate_to
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
            "🔍 Ricerca Universale (OdA, Dipendenti, Log...) - Ctrl+F"
        )
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
        NotificationManager.instance().unread_count_changed.connect(
            self.sidebar.btn_notifications.set_badge
        )
        self.sidebar.btn_notifications.set_badge(
            NotificationManager.instance().get_unread_count()
        )

    def _setup_shortcuts(self):
        """Configura le scorciatoie da tastiera globali."""
        self.shortcut_f5 = QShortcut(QKeySequence(Qt.Key.Key_F5), self)
        self.shortcut_f5.activated.connect(self._handle_f5)

        self.shortcut_search = QShortcut(QKeySequence("Ctrl+F"), self)
        self.shortcut_search.activated.connect(self._handle_ctrl_f)

    def _handle_f5(self):
        """Gestisce F5."""
        idx = self.page_stack.currentIndex()
        if idx == 0 and hasattr(self, "dashboard_panel"):
            self.dashboard_panel.refresh_data()
        elif idx == 3 and hasattr(self, "database_widget"):
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
        self.navigation_controller.navigate_to(5)
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
            self.navigation_controller.get_panel(3)
            self.contabilita_panel.start_import_process()

    def _on_download_update_clicked(self, url):
        import webbrowser

        webbrowser.open(url)

    # Wrapper per compatibilità
    def navigate_to_panel(self, panel_key: str):
        self.navigation_controller.navigate_to_panel(panel_key)

    def analyze_with_lyra(self, context_text: str):
        self.navigation_controller.analyze_with_lyra(context_text)

    def show_settings(self):
        self.navigation_controller.navigate_to(4)

    def closeEvent(self, event):
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
