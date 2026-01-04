"""
Bot TS - Main Window
Finestra principale dell'applicazione.
"""
import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QStackedWidget, QFrame, QSplashScreen, QApplication, QTabWidget,
    QProgressBar, QStatusBar, QLineEdit, QMenu
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPoint
from PyQt6.QtGui import QPixmap, QFont, QColor, QPainter, QKeySequence, QShortcut
from datetime import datetime

# Import Panels
from src.gui.panels import ScaricaTSPanel, CaricoTSPanel, DettagliOdAPanel, TimbratureBotPanel, TimbratureDBPanel, ScaricoPDLPanel
from src.gui.contabilita_panel import ContabilitaPanel
from src.gui.scarico_ore_panel import ScaricoOrePanel
from src.gui.settings_panel import SettingsPanel
from src.gui.help_panel import HelpPanel
from src.gui.dashboard_panel import DashboardPanel
from src.gui.lyra_panel import LyraPanel
from src.gui.notifications_panel import NotificationsPanel

# Import Core
from src.core.lyra_sentinel import LyraSentinel
from src.core.license_validator import get_license_info
from src.core import config_manager
from src.core.app_updater import check_for_updates
from src.core.notification_manager import NotificationManager
from src.core.backup_manager import BackupManager
from src.bots.portale_fornitori.timbrature.storage import TimbratureStorage

# Import UI/UX Components
from src.gui.widgets.toast import ToastManager
from src.gui.widgets.status_card import StatusCard
from src.gui.styles import apply_theme


class SidebarButton(QPushButton):
    """Pulsante personalizzato per la sidebar."""
    
    def __init__(self, text: str, icon: str = "", parent=None):
        super().__init__(parent)
        self.setText(f"{icon} {text}" if icon else text)
        self.setCheckable(True)
        self.setMinimumHeight(55)
        self.setMinimumWidth(180)
        self._original_text = f"{icon} {text}" if icon else text
        self._update_style()
        self.toggled.connect(self._update_style)
    
    def set_badge(self, count: int):
        """Imposta un badge di notifica."""
        if count > 0:
            self.setText(f"{self._original_text} 🔴 {count}")
        else:
            self.setText(self._original_text)

    def _update_style(self):
        """Aggiorna lo stile in base allo stato."""
        if self.isChecked():
            self.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 255, 255, 0.25);
                    color: #ffffff;
                    border: 1px solid rgba(255, 255, 255, 0.3);
                    border-radius: 8px;
                    padding: 12px 18px;
                    text-align: left;
                    font-weight: bold;
                    font-size: 16px;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #ffffff;
                    border: 1px solid transparent;
                    border-radius: 8px;
                    padding: 12px 18px;
                    text-align: left;
                    font-size: 16px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0.15);
                    color: white;
                }
            """)


class MainWindow(QMainWindow):
    """Finestra principale dell'applicazione Bot TS."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bot TS - Timesheet Manager")
        self.setMinimumSize(1200, 800)
        
        # Apply Global Theme
        apply_theme(QApplication.instance(), "light")

        # Abilita Drag & Drop
        self.setAcceptDrops(True)

        self._current_page_index = 0
        self._setup_ui()
        self._connect_signals()
        self._setup_shortcuts()

        # Toast notification system is now global via ToastManager
        # We can still expose a helper if needed, but components use ToastManager directly.

        # Lyra Sentinel (Monitoraggio Anomalie)
        self.sentinel = LyraSentinel()
        self.sentinel.anomalies_found.connect(self._on_anomalies_found)
        QTimer.singleShot(2000, self.sentinel.start) # Ritarda leggermente l'avvio

        # Avvio automatico importazione contabilità se abilitato
        QTimer.singleShot(1000, self._check_and_start_contabilita_update)

        # Controllo aggiornamenti applicazione (dopo 3 secondi)
        QTimer.singleShot(3000, self._check_updates)
    
    def _check_updates(self):
        """Avvia il controllo aggiornamenti in background."""
        # silent=True significa che mostra popup SOLO se trova un aggiornamento
        check_for_updates(parent=self, silent=True)
    
    def _on_anomalies_found(self, count):
        """Gestisce le anomalie trovate da Lyra."""
        self.btn_lyra.set_badge(count)
        if count > 0:
            ToastManager.instance().show(f"⚠️ Lyra ha rilevato {count} anomalie", "warning")

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

        if idx == 0: # Dashboard
            self.dashboard_panel.refresh_data()
            self.show_toast("Dashboard aggiornata")
        # Database Page (Index 3)
        elif idx == 3:
            tab_idx = self.database_widget.currentIndex()
            if tab_idx == 0: # Timbrature
                self.timbrature_db_panel.refresh_data()
                self.show_toast("Dati aggiornati")
            elif tab_idx == 1: # Contabilità
                self.contabilita_panel.refresh_tabs()
                self.show_toast("Contabilità aggiornata (Vista)")
            elif tab_idx == 2: # Scarico Ore
                self.scarico_ore_panel._start_update()

    def _handle_ctrl_f(self):
        """Gestisce Ctrl+F per il focus sulla ricerca."""
        idx = self.page_stack.currentIndex()

        # Database Page
        if idx == 3:
            tab_idx = self.database_widget.currentIndex()
            if tab_idx == 0: # Timbrature
                self.timbrature_db_panel.search_input.setFocus()
                self.timbrature_db_panel.search_input.selectAll()
            elif tab_idx == 1: # Contabilità
                if self.contabilita_panel.search_input.isVisible():
                    self.contabilita_panel.search_input.setFocus()
                    self.contabilita_panel.search_input.selectAll()
            elif tab_idx == 2: # Scarico Ore
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
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        self.progress_bar.setMaximumWidth(200)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #ced4da;
                border-radius: 4px;
                text-align: center;
                color: black;
            }
            QProgressBar::chunk {
                background-color: #0d6efd;
            }
        """)
        self.status_bar.addPermanentWidget(self.progress_bar)

        # Widget centrale
        central_widget = QWidget()
        # Force light theme for the main window content area if needed, or rely on specific widgets
        # central_widget.setStyleSheet("background-color: #f8f9fa; color: #212529;")
        # Removed explicit style to let QSS handle it
        self.setCentralWidget(central_widget)
        
        # Layout principale orizzontale
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # === SIDEBAR ===
        sidebar = QFrame()
        sidebar.setFixedWidth(240)
        sidebar.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
            }
        """)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(15, 20, 15, 20)
        sidebar_layout.setSpacing(10)
        
        # Logo/Titolo
        logo_label = QLabel("🤖 Bot TS")
        logo_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 28px;
                font-weight: bold;
                padding: 10px 0;
                background: transparent;
            }
        """)
        sidebar_layout.addWidget(logo_label)
        
        subtitle = QLabel("Timesheet Manager")
        subtitle.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.7);
                font-size: 13px;
                padding-bottom: 20px;
                background: transparent;
            }
        """)
        sidebar_layout.addWidget(subtitle)
        
        # Separatore
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: rgba(255, 255, 255, 0.2);")
        sidebar_layout.addWidget(separator)
        
        sidebar_layout.addSpacing(15)
        
        # Pulsanti navigazione
        self.btn_home = SidebarButton("Home", "🏠")
        self.btn_home.setChecked(True)
        sidebar_layout.addWidget(self.btn_home)

        self.btn_automazioni = SidebarButton("Automazioni", "🤖")
        sidebar_layout.addWidget(self.btn_automazioni)

        self.btn_database = SidebarButton("Database", "🗄️")
        sidebar_layout.addWidget(self.btn_database)
        
        sidebar_layout.addStretch()

        self.btn_lyra = SidebarButton("Lyra AI", "✨")
        sidebar_layout.addWidget(self.btn_lyra)

        self.btn_notifications = SidebarButton("Notifiche", "🔔")
        sidebar_layout.addWidget(self.btn_notifications)

        self.btn_help = SidebarButton("Guida", "❓")
        sidebar_layout.addWidget(self.btn_help)

        sidebar_layout.addSpacing(10)

        # License Info
        license_info = get_license_info()
        if license_info:
            client = license_info.get("Cliente", "N/D")
            expiry = license_info.get("Scadenza Licenza", "N/D")

            # Get last login from config
            config = config_manager.load_config()
            last_login = config.get("last_login_date", "N/D")

            # Update last login date to NOW for next time
            now_str = datetime.now().strftime("%d/%m/%Y %H:%M")
            config_manager.set_config_value("last_login_date", now_str)

            license_text = f"Licenza: {client}\nScadenza: {expiry}\nUltimo accesso: {last_login}"
        else:
            license_text = "Licenza non trovata"

        license_label = QLabel(license_text)
        license_label.setWordWrap(True)
        license_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.6);
                font-size: 13px;
                padding: 5px;
                background: transparent;
            }
        """)
        sidebar_layout.addWidget(license_label)
        
        # Separatore
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.Shape.HLine)
        separator2.setStyleSheet("background-color: rgba(255, 255, 255, 0.2);")
        sidebar_layout.addWidget(separator2)
        
        sidebar_layout.addSpacing(10)
        
        # Impostazioni
        self.btn_settings = SidebarButton("Impostazioni", "⚙️")
        sidebar_layout.addWidget(self.btn_settings)
        
        # Versione
        from src.core.version import __version__
        version_label = QLabel(f"v{__version__}")
        version_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.5);
                font-size: 13px;
                padding-top: 10px;
                background: transparent;
            }
        """)
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(version_label)
        
        main_layout.addWidget(sidebar)
        
        # === CONTENT AREA ===
        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # --- GLOBAL SEARCH BAR ---
        search_container = QHBoxLayout()
        search_container.setContentsMargins(0, 0, 0, 10)
        
        self.global_search = QLineEdit()
        self.global_search.setPlaceholderText("🔍 Ricerca Universale (OdA, Dipendenti, Log...) - Ctrl+F")
        self.global_search.setMinimumHeight(40)
        self.global_search.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ced4da;
                border-radius: 20px;
                padding: 5px 20px;
                background-color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #0d6efd;
                background-color: #f8f9fa;
            }
        """)
        # Connect search logic
        self.global_search.returnPressed.connect(self._perform_global_search)
        
        search_container.addWidget(self.global_search)
        content_layout.addLayout(search_container)
        
        # Stack per le pagine principali (Automazioni, Database, Settings)
        self.page_stack = QStackedWidget()
        
        # Crea i pannelli individuali
        self.dashboard_panel = DashboardPanel()
        self.scarico_panel = ScaricaTSPanel()
        self.carico_panel = CaricoTSPanel()
        self.dettagli_panel = DettagliOdAPanel()
        self.pdl_panel = ScaricoPDLPanel() # NEW
        self.timbrature_bot_panel = TimbratureBotPanel()
        self.timbrature_db_panel = TimbratureDBPanel()
        self.contabilita_panel = ContabilitaPanel()
        self.scarico_ore_panel = ScaricoOrePanel() # NEW: Scarico Ore Panel
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
        self.global_status_card.setMaximumHeight(40) # Ensure it fits in tab bar
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
        for panel in [self.dettagli_panel, self.scarico_panel, self.timbrature_bot_panel, 
                      self.carico_panel, self.pdl_panel]:
            if hasattr(panel, 'status_changed'):
                panel.status_changed.connect(self._on_panel_status_changed)

        # --- Page 3: Database (Tab Widget) ---
        self.database_widget = QTabWidget()
        self.database_widget.addTab(self.timbrature_db_panel, "Timbrature Isab")
        self.database_widget.addTab(self.contabilita_panel, "Strumentale")
        self.database_widget.addTab(self.scarico_ore_panel, "DataEase") # Renamed from "Scarico Ore Cantiere"

        # Aggiungi le pagine allo stack
        # 0: Dashboard
        # 1: Automazioni
        # 2: Lyra
        # 3: Database
        # 4: Settings
        # 5: Help
        # 6: Notifications
        self.page_stack.addWidget(self.dashboard_panel)    # Index 0
        self.page_stack.addWidget(self.automazioni_widget) # Index 1
        self.page_stack.addWidget(self.lyra_panel)         # Index 2
        self.page_stack.addWidget(self.database_widget)    # Index 3
        self.page_stack.addWidget(self.settings_panel)     # Index 4
        self.page_stack.addWidget(self.help_panel)         # Index 5
        self.page_stack.addWidget(self.notifications_panel) # Index 6
        
        content_layout.addWidget(self.page_stack)
        
        main_layout.addWidget(content_area)
        
        # Lista pulsanti per gestione esclusiva
        self.nav_buttons = [
            self.btn_home,
            self.btn_automazioni,
            self.btn_lyra,
            self.btn_database,
            self.btn_settings,
            self.btn_help,
            self.btn_notifications
        ]
    
    def _perform_global_search(self):
        """Esegue la ricerca globale estesa su tutti i moduli."""
        query = self.global_search.text().strip()
        if not query or len(query) < 2: return

        results_menu = QMenu(self)
        results_menu.setStyleSheet("""
            QMenu { background-color: white; border: 1px solid #dee2e6; padding: 5px; min-width: 450px; }
            QMenu::item { padding: 8px 25px; font-size: 13px; }
            QMenu::item:selected { background-color: #0d6efd; color: white; }
            QMenu::separator { height: 1px; background: #e9ecef; margin: 5px 0; }
        """)

        found_count = 0

        # --- 1. Contabilità Strumentale (OdA) ---
        try:
            from src.core.contabilita_manager import ContabilitaManager
            oda_matches = ContabilitaManager.search_oda(query)
            if oda_matches:
                results_menu.addAction("📊 CONTABILITÀ STRUMENTALE (OdA):").setEnabled(False)
                for oda in oda_matches[:20]:
                    text = f"OdA {oda['codice_oda']} - {oda['descrizione'][:50]}..." # Increased trunc limit
                    action = results_menu.addAction(text)
                    action.triggered.connect(lambda _, o=oda['codice_oda']: self._navigate_to_oda(o))
                    found_count += 1
                results_menu.addSeparator()
        except: pass

        # --- 2. Contabilità Estesa (Giornaliere, Cantiere, Certificati) ---
        try:
            ext_matches = ContabilitaManager.search_extended(query)
            
            # Giornaliere
            if ext_matches.get("GIORNALIERE"):
                results_menu.addAction("📂 GIORNALIERE:").setEnabled(False)
                for g in ext_matches["GIORNALIERE"][:20]:
                    text = f"{g['data']} - {g['personale']} - {g['descrizione'][:40]}..."
                    action = results_menu.addAction(text)
                    action.triggered.connect(lambda _, q=query: self._navigate_to_extended(1, q)) # Tab 1 = Giornaliere
                    found_count += 1
                results_menu.addSeparator()

            # Cantiere (Scarico Ore)
            if ext_matches.get("CANTIERE"):
                results_menu.addAction("🏗️ CANTIERE (Scarico Ore):").setEnabled(False)
                for c in ext_matches["CANTIERE"][:20]:
                    text = f"{c['data']} - {c['personale']} - {c['commessa']}"
                    action = results_menu.addAction(text)
                    action.triggered.connect(lambda _, q=query: self._navigate_to_dataease(q))
                    found_count += 1
                results_menu.addSeparator()

            # Certificati
            if ext_matches.get("CERTIFICATI"):
                results_menu.addAction("📜 CERTIFICATI:").setEnabled(False)
                for c in ext_matches["CERTIFICATI"][:20]:
                    text = f"{c['matricola']} - {c['modello']} ({c['costruttore']})"
                    action = results_menu.addAction(text)
                    action.triggered.connect(lambda _, q=query: self._navigate_to_extended(3, q)) # Tab 3 = Certificati
                    found_count += 1
                results_menu.addSeparator()

        except: pass

        # --- 3. Dipendenti (Timbrature) ---
        try:
            emp_matches = TimbratureStorage().search_employees(query)
            if emp_matches:
                results_menu.addAction("👥 DIPENDENTI:").setEnabled(False)
                for emp in emp_matches[:20]:
                    text = f"{emp['cognome']} {emp['nome']}"
                    action = results_menu.addAction(text)
                    # Navigate to Timbrature DB and filter
                    action.triggered.connect(lambda _, q=text: self._navigate_to_timbrature(q))
                    found_count += 1
                results_menu.addSeparator()
        except: pass

        # --- 4. Audit Log ---
        try:
            from src.core.audit_manager import AuditManager
            audit_logs = AuditManager().get_logs(limit=100)
            matches = [l for l in audit_logs if query.lower() in str(l['action']).lower() or query.lower() in str(l['entity']).lower()]
            if matches:
                results_menu.addAction("🛡️ AUDIT LOG:").setEnabled(False)
                for log in matches[:3]:
                    action = results_menu.addAction(f"{log['action']} - {log['entity']}")
                    action.triggered.connect(lambda: self._navigate_to(6))
                    found_count += 1
        except: pass

        if found_count == 0:
            results_menu.addAction("❌ Nessun risultato trovato").setEnabled(False)

        pos = self.global_search.mapToGlobal(QPoint(0, self.global_search.height()))
        results_menu.exec(pos)

    def _navigate_to_extended(self, tab_idx, query):
        """Naviga a un tab specifico di Contabilità e imposta il filtro."""
        self._navigate_to(3) # Database
        self.database_widget.setCurrentIndex(1) # Contabilità
        self.contabilita_panel.main_tabs.setCurrentIndex(tab_idx)
        self.contabilita_panel.set_search_query(query)

    def _navigate_to_dataease(self, query):
        """Naviga a Scarico Ore (DataEase)."""
        self._navigate_to(3)
        self.database_widget.setCurrentIndex(2) # DataEase
        self.scarico_ore_panel.search_input.setText(query)

    def _navigate_to_timbrature(self, query):
        """Naviga a Timbrature DB."""
        self._navigate_to(3)
        self.database_widget.setCurrentIndex(0) # Timbrature
        self.timbrature_db_panel.search_input.setText(query)

    def _navigate_to_oda(self, oda_code):
        """Naviga al pannello contabilità e filtra per OdA."""
        self._navigate_to(3) # Database
        self.database_widget.setCurrentIndex(1) # Contabilità
        self.contabilita_panel.set_search_query(oda_code)

    def _get_active_bot_panel(self):
        """Recupera il pannello bot attualmente visibile."""
        main_idx = self.automazioni_widget.currentIndex()
        if main_idx == 0: # Portale Fornitori
            return self.tab_fornitori.currentWidget()
        elif main_idx == 1: # SafeWork
            return self.tab_safework.currentWidget()
        return None

    def _update_global_status(self):
        """Aggiorna la card di stato globale in base al pannello attivo."""
        panel = self._get_active_bot_panel()
        if panel and hasattr(panel, 'get_current_status'):
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
        self.btn_home.clicked.connect(lambda: self._navigate_to(0))
        self.btn_automazioni.clicked.connect(lambda: self._navigate_to(1))
        self.btn_lyra.clicked.connect(lambda: self._navigate_to(2))
        self.btn_database.clicked.connect(lambda: self._navigate_to(3))
        self.btn_settings.clicked.connect(lambda: self._navigate_to(4))
        self.btn_help.clicked.connect(lambda: self._navigate_to(5))
        self.btn_notifications.clicked.connect(lambda: self._navigate_to(6))

        # Notification Badge
        NotificationManager.instance().unread_count_changed.connect(self.btn_notifications.set_badge)
        # Init badge
        self.btn_notifications.set_badge(NotificationManager.instance().get_unread_count())

        # Aggiornamento live impostazioni
        self.settings_panel.settings_saved.connect(self._on_settings_saved)

    def _on_settings_saved(self):
        """Aggiorna i pannelli quando le impostazioni vengono salvate."""
        self.scarico_panel.refresh_fornitori()
        self.dettagli_panel.refresh_fornitori()
        self.timbrature_bot_panel.refresh_fornitori()

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
            self.nav_buttons[index].setChecked(True)
            return
        
        # Se stiamo lasciando la pagina delle impostazioni, controlla le modifiche
        if self._current_page_index == 4:  # Settings page is now index 4
            if self.settings_panel.has_unsaved_changes():
                can_proceed = self.settings_panel.prompt_save_if_needed()
                if not can_proceed:
                    # L'utente ha annullato - rimani sulla pagina corrente
                    self.nav_buttons[4].setChecked(True)
                    return
        
        # Procedi con la navigazione
        self._current_page_index = index
        self.page_stack.setCurrentIndex(index)
        
        # Aggiorna stato pulsanti
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)
        
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
            "scarico_pdl": (1, 0)
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
        db_map = {
            "db_timbrature": 0,
            "db_strumentale": 1,
            "db_dataease": 2
        }

        if panel_key in db_map:
            self._navigate_to(3)
            self.database_widget.setCurrentIndex(db_map[panel_key])
            return

    def analyze_with_lyra(self, context_text: str):
        """Passa alla vista Lyra e analizza il contesto fornito."""
        self._navigate_to(2) # Switch to Lyra
        self.lyra_panel.ask_lyra("Analizza questi dati e dimmi se ci sono anomalie o punti di attenzione.", context_text)
    
    def closeEvent(self, event):
        """Gestisce la chiusura della finestra."""
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

    # --- Drag & Drop ---
    def dragEnterEvent(self, event):
        """Accetta file Excel trascinati."""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and urls[0].toLocalFile().endswith(('.xlsx', '.xls')):
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
                ToastManager.instance().show("Tipo file non riconosciuto. Rinominare con 'Timbrature' o 'Contabilita'.", "warning")

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
    painter.drawText(sub_rect, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop, 
                    "ISAB Timesheet Manager\nCaricamento...")
    
    painter.end()
    
    splash = QSplashScreen(splash_pixmap)
    splash.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
    
    splash.show() # Ensure it's shown if created
    return splash
