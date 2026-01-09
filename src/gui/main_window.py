"""
Bot TS - Main Window
Finestra principale dell'applicazione.
"""

import os
from pathlib import Path

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import (
    QAction,
    QColor,
    QFont,
    QIcon,
    QKeySequence,
    QPageLayout,
    QPageSize,
    QPainter,
    QPixmap,
    QShortcut,
    QTextDocument,
)
from PyQt6.QtPrintSupport import QPrinter
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QMenu,
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
from src.gui.controllers.search_controller import SearchController
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
from src.utils.helpers import get_app_icon_path


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
        self._force_quit = False  # NEW: Controllo chiusura definitiva
        self._setup_ui()
        self._setup_tray_icon()  # NEW: Tray Icon
        self._connect_signals()
        self._setup_shortcuts()

        # Toast notification system is now global via ToastManager
        # We can still expose a helper if needed, but components use ToastManager directly.

        # Lyra Sentinel (Monitoraggio Anomalie)
        self.sentinel = LyraSentinel()
        self.sentinel.anomalies_found.connect(self._on_anomalies_found)
        QTimer.singleShot(2000, self.sentinel.start)  # Ritarda leggermente l'avvio

        # Telegram Service
        self.telegram = TelegramService()
        self.telegram_bridge = TelegramUIBridge(self)
        self.telegram_bridge.setup_connections()
        self.search_controller = SearchController(self)
        QTimer.singleShot(1000, self.telegram.start_service)

        # Inoltro notifiche a Telegram
        NotificationManager.instance().notification_added.connect(self._forward_notification_to_telegram)

        # Avvio automatico importazione contabilità se abilitato
        QTimer.singleShot(1000, self._check_and_start_contabilita_update)

        # Controllo aggiornamenti applicazione (dopo 3 secondi)
        QTimer.singleShot(3000, self._check_updates)

    def _handle_bot_results(self, bot_id, results):
        """Gestisce i risultati prodotti dai bot (es. file scaricati) e li invia a Telegram."""
        if bot_id == "scarico_pdl":
            for file_path in results:
                if os.path.exists(file_path):
                    self.telegram.send_document_sync(
                        file_path, caption=f"📄 **PDL Scaricato**\nFile: `{os.path.basename(file_path)}`"
                    )

    def _generate_pdf_from_html(self, html_content: str, output_path: str):
        """Genera un PDF da contenuto HTML."""
        doc = QTextDocument()

        # Aggiungi stili CSS globali per garantire leggibilità
        header_style = """
        <style>
            body { font-family: Arial, sans-serif; font-size: 18pt; }
            h2 { font-size: 30pt; color: #333; }
            h3 { font-size: 24pt; color: #0d6efd; margin-top: 20px; }
            p { font-size: 18pt; color: #555; }
            table { width: 100%; border-collapse: collapse; margin-top: 15px; }
            th { background-color: #f2f2f2; color: #333; font-weight: bold; padding: 12px; font-size: 16pt; border: 1px solid #ddd; }
            td { padding: 10px; font-size: 16pt; border: 1px solid #ddd; color: #000; }
        </style>
        """
        doc.setHtml(header_style + html_content)

        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        printer.setOutputFileName(output_path)
        printer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
        printer.setPageOrientation(QPageLayout.Orientation.Landscape) # Landscape per tabelle larghe

        doc.print(printer)

    def _forward_notification_to_telegram(self, notification):
        """Inoltra notifiche importanti a Telegram (tranne quelle generate da Telegram stesso)."""
        if notification.get("title") == "Telegram":
            return

        level = notification.get("level", "info")
        # Inoltriamo solo successi, errori e avvisi (evitiamo spam di info generiche)
        if level in ["success", "error", "warning"]:
            title = notification.get("title", "Notifica")
            msg = notification.get("message", "")
            icon = "✅" if level == "success" else "❌" if level == "error" else "⚠️"

            text = f"{icon} *{title}*\n{msg}"
            self.telegram.send_message_sync(text)

    def _setup_tray_icon(self):
        """Configura l'icona nella system tray."""
        self.tray_icon = QSystemTrayIcon(self)

        icon_path = get_app_icon_path()
        if icon_path:
            self.tray_icon.setIcon(QIcon(icon_path))

        # Tray Menu
        tray_menu = QMenu()
        show_action = QAction("🖥️ Mostra SyncroJob", self)
        show_action.triggered.connect(self.showMaximized)
        show_action.triggered.connect(self.activateWindow)
        tray_menu.addAction(show_action)

        tray_menu.addSeparator()

        def force_quit_app():
            self._force_quit = True
            QApplication.instance().quit()

        quit_action = QAction("❌ Esci", self)
        quit_action.triggered.connect(force_quit_app)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self._handle_tray_activation)
        self.tray_icon.show()

    def _handle_tray_activation(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.isVisible():
                self.hide()
            else:
                self.showMaximized()
                self.activateWindow()

    def _check_updates(self):
        """Avvia il controllo aggiornamenti in background."""
        # Usa il nuovo sistema a banner invece del popup bloccante
        check_for_updates(parent=self, silent=True, callback=self._show_update_banner)

    def _show_update_banner(self, new_version, download_url, changelog):
        """Mostra un banner informativo per la nuova versione."""
        self.update_banner.show_update(new_version, download_url, changelog)

        # Notifica tray
        self.tray_icon.showMessage(
            "Aggiornamento Disponibile",
            f"È uscita la versione {new_version}. Clicca qui per scaricarla.",
            QSystemTrayIcon.MessageIcon.Information,
            5000,
        )

    def _on_anomalies_found(self, count):
        """Gestisce le anomalie trovate da Lyra."""
        self.sidebar.btn_lyra.set_badge(count)
        if count > 0:
            ToastManager.instance().show(f"⚠️ Lyra ha rilevato {count} anomalie", "warning")

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
            self.tray_icon.showMessage(title, message, icon, 5000)

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
        self.progress_bar.setObjectName("progressBar")  # Assegna objectName
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
        self.sidebar.navigation_requested.connect(self._navigate_to)
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
        self.global_search.setObjectName("globalSearchInput")  # Assegna objectName
        self.global_search.setPlaceholderText("🔍 Ricerca Universale (OdA, Dipendenti, Log...) - Ctrl+F")
        self.global_search.setMinimumHeight(40)
        # Connect search logic
        self.global_search.returnPressed.connect(
            lambda: self.search_controller.perform_search(self.global_search.text())
        )

        search_container.addWidget(self.global_search)
        content_layout.addLayout(search_container)

        # Stack per le pagine principali (Automazioni, Database, Settings)
        self.page_stack = QStackedWidget()

        # Crea i pannelli individuali
        self.dashboard_panel = DashboardPanel()
        self.scarico_panel = ScaricaTSPanel()
        self.carico_panel = CaricoTSPanel()
        self.dettagli_panel = DettagliOdAPanel()
        self.pdl_panel = ScaricoPDLPanel()  # NEW
        self.pdl_panel.bot_results_ready.connect(self._handle_bot_results)
        self.timbrature_bot_panel = TimbratureBotPanel()
        self.timbrature_db_panel = TimbratureDBPanel()
        self.contabilita_panel = ContabilitaPanel()
        self.scarico_ore_panel = ScaricoOrePanel()  # NEW: Scarico Ore Panel
        self.settings_panel = SettingsPanel()
        self.help_panel = HelpPanel()
        self.lyra_panel = LyraPanel()
        self.notifications_panel = NotificationsPanel()

        # Collega il segnale di update dal bot al database
        self.timbrature_bot_panel.data_updated.connect(self.timbrature_db_panel.refresh_data)

        # --- Page 1: Automazioni (Main Groups) ---
        self.automazioni_widget = QTabWidget()

        # Global Status Card (Corner Widget)
        self.global_status_card = StatusCard("Stato Attività")
        self.global_status_card.setMinimumWidth(350)
        self.global_status_card.setMaximumHeight(40)  # Ensure it fits in tab bar
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

        # Connect signals for Global Status Update
        self.automazioni_widget.currentChanged.connect(self._update_global_status)
        self.tab_fornitori.currentChanged.connect(self._update_global_status)
        self.tab_safework.currentChanged.connect(self._update_global_status)

        # Connect panel status changes
        for panel in [
            self.dettagli_panel,
            self.scarico_panel,
            self.timbrature_bot_panel,
            self.carico_panel,
            self.pdl_panel,
        ]:
            if hasattr(panel, "status_changed"):
                panel.status_changed.connect(self._on_panel_status_changed)

        # --- Page 3: Database (Tab Widget) ---
        self.database_widget = QTabWidget()
        self.database_widget.addTab(self.timbrature_db_panel, "Timbrature Isab")
        self.database_widget.addTab(self.contabilita_panel, "Strumentale")
        self.database_widget.addTab(self.scarico_ore_panel, "DataEase")  # Renamed from "Scarico Ore Cantiere"

        # Aggiungi le pagine allo stack
        # 0: Dashboard
        # 1: Automazioni
        # 2: Lyra
        # 3: Database
        # 4: Settings
        # 5: Help
        # 6: Notifications
        self.page_stack.addWidget(self.dashboard_panel)  # Index 0
        self.page_stack.addWidget(self.automazioni_widget)  # Index 1
        self.page_stack.addWidget(self.lyra_panel)  # Index 2
        self.page_stack.addWidget(self.database_widget)  # Index 3
        self.page_stack.addWidget(self.settings_panel)  # Index 4
        self.page_stack.addWidget(self.help_panel)  # Index 5
        self.page_stack.addWidget(self.notifications_panel)  # Index 6

        content_layout.addWidget(self.page_stack)

        main_layout.addWidget(content_area)

    def _navigate_to_extended(self, tab_idx, query):
        """Naviga a un tab specifico di Contabilità e imposta il filtro."""
        self._navigate_to(3)  # Database
        self.database_widget.setCurrentIndex(1)  # Contabilità
        self.contabilita_panel.main_tabs.setCurrentIndex(tab_idx)
        self.contabilita_panel.set_search_query(query)

    def _navigate_to_dataease(self, query):
        """Naviga a Scarico Ore (DataEase)."""
        self._navigate_to(3)
        self.database_widget.setCurrentIndex(2)  # DataEase
        self.scarico_ore_panel.search_input.setText(query)

    def _navigate_to_timbrature(self, query):
        """Naviga a Timbrature DB."""
        self._navigate_to(3)
        self.database_widget.setCurrentIndex(0)  # Timbrature
        self.timbrature_db_panel.search_input.setText(query)

    def _navigate_to_oda(self, oda_code):
        """Naviga al pannello contabilità e filtra per OdA."""
        self._navigate_to(3)  # Database
        self.database_widget.setCurrentIndex(1)  # Contabilità
        self.contabilita_panel.set_search_query(oda_code)

    def _get_active_bot_panel(self):
        """Recupera il pannello bot attualmente visibile."""
        main_idx = self.automazioni_widget.currentIndex()
        if main_idx == 0:  # Portale Fornitori
            return self.tab_fornitori.currentWidget()
        elif main_idx == 1:  # SafeWork
            return self.tab_safework.currentWidget()
        return None

    def _update_global_status(self):
        """Aggiorna la card di stato globale in base al pannello attivo."""
        panel = self._get_active_bot_panel()
        if panel and hasattr(panel, "get_current_status"):
            status, message = panel.get_current_status()
            self.global_status_card.setStatus(status, message)

            # Change Global Status Card Title based on Panel Name?
            # User request: "Stato Attività" title constant.
            # But maybe we want to know WHICH activity.
            # "Stato Attività" is generic enough.
            # self.global_status_card._title_label.setText(f"Stato: {panel.bot_name}")
            # Let's keep "Stato Attività" as per request.

    def _on_panel_status_changed(self, status, message):
        """Callback quando un pannello cambia stato."""
        sender = self.sender()
        active_panel = self._get_active_bot_panel()

        # Aggiorna solo se il segnale arriva dal pannello attivo
        if sender == active_panel:
            self.global_status_card.setStatus(status, message)

    def _connect_signals(self):
        """Collega i segnali."""
        # Note: Navigation signals are handled by SidebarWidget and connected in _setup_ui

        # Notification Badge
        NotificationManager.instance().unread_count_changed.connect(self.sidebar.btn_notifications.set_badge)
        # Init badge
        self.sidebar.btn_notifications.set_badge(NotificationManager.instance().get_unread_count())

        # Aggiornamento live impostazioni
        self.settings_panel.settings_saved.connect(self._on_settings_saved)
        self.settings_panel.request_help_section.connect(self._on_help_requested)

    def _on_help_requested(self, section_title):
        """Gestisce la richiesta di apertura di una sezione specifica della guida."""
        self._navigate_to(5)  # Index della pagina Help
        self.help_panel.open_section(section_title)

    def _on_settings_saved(self):
        """Aggiorna i pannelli quando le impostazioni vengono salvate."""
        self.scarico_panel.refresh_fornitori()
        self.dettagli_panel.refresh_fornitori()
        self.timbrature_bot_panel.refresh_fornitori()

        # Riavvia il servizio Telegram per applicare eventuali nuovi token
        self.telegram.start_service()

        # Feedback Toast
        ToastManager.instance().show("Impostazioni salvate con successo!", "success")

    def _navigate_to(self, index: int):
        """
        Naviga alla pagina specificata.

        Controlla se ci sono modifiche non salvate nelle impostazioni
        prima di cambiare pagina.
        """
        # Se stiamo già sulla pagina richiesta, non fare nulla
        if index == self._current_page_index:
            # Assicura che il pulsante sia checked
            self.sidebar.set_active_button(index)
            return

        # Se stiamo lasciando la pagina delle impostazioni, controlla le modifiche
        if self._current_page_index == 4:  # Settings page is now index 4
            if self.settings_panel.has_unsaved_changes():
                can_proceed = self.settings_panel.prompt_save_if_needed()
                if not can_proceed:
                    # L'utente ha annullato - rimani sulla pagina corrente
                    self.sidebar.set_active_button(4)
                    return

        # Procedi con la navigazione
        self._current_page_index = index
        self.page_stack.setCurrentIndex(index)

        # Aggiorna stato pulsanti
        self.sidebar.set_active_button(index)

        # Se arriviamo su Automazioni (Index 1), potremmo voler aggiornare i fornitori
        if index == 1:
            self.scarico_panel.refresh_fornitori()

    def _check_and_start_contabilita_update(self):
        """Controlla la configurazione e avvia l'update contabilità se abilitato."""
        config = config_manager.load_config()
        if config.get("enable_auto_update_contabilita", False):
            self.contabilita_panel.start_import_process()

    def show_settings(self):
        """Metodo pubblico per navigare alle impostazioni."""
        self._navigate_to(4)

    def navigate_to_panel(self, panel_key: str):
        """
        Naviga a un pannello specifico (usato dalla Dashboard).
        Keys: 'dettagli_oda', 'scarico_ts', 'timbrature', 'carico_ts'
              'db_timbrature', 'db_strumentale', 'db_dataease'
        """
        # --- Automazioni (Index 1) ---
        # Map: key -> (MainTab Index, SubTab Index)
        # MainTab 0: Portale Fornitori
        # MainTab 1: SafeWork

        bot_map = {
            "dettagli_oda": (0, 0),
            "scarico_ts": (0, 1),
            "timbrature": (0, 2),
            "carico_ts": (0, 3),
            "scarico_pdl": (1, 0),
        }

        if panel_key in bot_map:
            main_idx, sub_idx = bot_map[panel_key]
            self._navigate_to(1)
            self.automazioni_widget.setCurrentIndex(main_idx)
            if main_idx == 0:
                self.tab_fornitori.setCurrentIndex(sub_idx)
            elif main_idx == 1:
                self.tab_safework.setCurrentIndex(sub_idx)
            return

        # --- Database (Index 3) ---
        db_map = {"db_timbrature": 0, "db_strumentale": 1, "db_dataease": 2}

        if panel_key in db_map:
            self._navigate_to(3)
            self.database_widget.setCurrentIndex(db_map[panel_key])
            return

    def analyze_with_lyra(self, context_text: str):
        """Passa alla vista Lyra e analizza il contesto fornito."""
        self._navigate_to(2)  # Switch to Lyra
        self.lyra_panel.ask_lyra(
            "Analizza questi dati e dimmi se ci sono anomalie o punti di attenzione.", context_text
        )

    def _on_download_update_clicked(self, url):
        """Gestisce il click sul pulsante scarica del banner."""
        import webbrowser

        webbrowser.open(url)
        ToastManager.instance().show("Download avviato nel browser", "success")

    def closeEvent(self, event):
        """Gestisce la chiusura della finestra: minimizza nella tray se non è force_quit."""
        if self._force_quit:
            # Ferma servizi in background in modo bloccante
            if self.telegram:
                self.telegram.stop_service()

            # Auto Backup
            config = config_manager.load_config()
            if config.get("auto_backup", True):
                BackupManager.create_backup()

            # Controlla modifiche non salvate nelle impostazioni
            if self.settings_panel.has_unsaved_changes():
                can_close = self.settings_panel.prompt_save_if_needed()
                if not can_close:
                    event.ignore()
                    return

            event.accept()
            return

        # Altrimenti minimizza nella tray
        if self.isVisible():
            self.hide()

            # Mostra messaggio solo la prima volta
            config = config_manager.load_config()
            if not config.get("tray_hint_shown", False):
                self.tray_icon.showMessage(
                    "SyncroJob è ancora attivo",
                    "L'applicazione continua a lavorare in background.\nUsa il tasto destro sull'icona per chiudere definitivamente.",
                    QSystemTrayIcon.MessageIcon.Information,
                    5000,
                )
                config_manager.set_config_value("tray_hint_shown", True)

            event.ignore()

    # --- Drag & Drop ---
    def dragEnterEvent(self, event):
        """Accetta file Excel trascinati."""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and urls[0].toLocalFile().endswith((".xlsx", ".xls")):
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()

    def dropEvent(self, event):
        """Gestisce il drop del file."""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            file_path = urls[0].toLocalFile()

            lower_path = file_path.lower()
            if "timbrature" in lower_path:
                self._import_timbrature(file_path)
            elif "contabilita" in lower_path or "consuntivo" in lower_path:
                self._import_contabilita(file_path)
            else:
                ToastManager.instance().show(
                    "Tipo file non riconosciuto. Rinominare con 'Timbrature' o 'Contabilita'.", "warning"
                )

    def _import_timbrature(self, path):
        # Usa il metodo statico del bot timbrature
        try:
            from src.bots.portale_fornitori.timbrature.bot import TimbratureBot

            db_path = config_manager.CONFIG_DIR / "data" / "timbrature_Isab.db"
            success = TimbratureBot.import_to_db_static(path, db_path, lambda x: None)
            if success:
                self.timbrature_db_panel.refresh_data()
                ToastManager.instance().show("Timbrature importate con successo!", "success")
            else:
                ToastManager.instance().show("Errore importazione Timbrature.", "error")
        except Exception as e:
            ToastManager.instance().show(f"Errore: {e}", "error")

    def _import_contabilita(self, path):
        # Usa il manager contabilità
        try:
            from src.core.contabilita_manager import ContabilitaManager

            success, msg = ContabilitaManager.import_data_from_excel(path)
            if success:
                self.contabilita_panel.refresh_tabs()
                ToastManager.instance().show("Contabilità importata con successo!", "success")
            else:
                ToastManager.instance().show(f"Errore: {msg}", "error")
        except Exception as e:
            ToastManager.instance().show(f"Errore: {e}", "error")


def create_splash_screen() -> QSplashScreen:
    """Crea e restituisce una splash screen."""
    # Crea un pixmap per la splash
    splash_pixmap = QPixmap(400, 250)
    splash_pixmap.fill(QColor("#667eea"))

    painter = QPainter(splash_pixmap)
    painter.setPen(QColor("white"))

    # Titolo
    font_title = QFont("Arial", 28, QFont.Weight.Bold)
    painter.setFont(font_title)
    painter.drawText(splash_pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "🤖 Bot TS")

    # Sottotitolo
    font_sub = QFont("Arial", 12)
    painter.setFont(font_sub)
    painter.setPen(QColor(255, 255, 255, 180))
    sub_rect = splash_pixmap.rect()
    sub_rect.setTop(sub_rect.center().y() + 30)
    painter.drawText(
        sub_rect,
        Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
        "ISAB Timesheet Manager\nCaricamento...",
    )

    painter.end()

    splash = QSplashScreen(splash_pixmap)
    splash.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

    splash.show()  # Ensure it's shown if created
    return splash
