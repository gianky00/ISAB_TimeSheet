"""
Bot TS - Main Window
Finestra principale dell'applicazione.
"""
import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QStackedWidget, QFrame, QSplashScreen, QApplication
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont, QColor, QPainter

from src.gui.panels import ScaricaTSPanel, CaricoTSPanel, DettagliOdAPanel
from src.gui.settings_panel import SettingsPanel
from src.core.license_validator import get_license_info


class SidebarButton(QPushButton):
    """Pulsante personalizzato per la sidebar."""
    
    def __init__(self, text: str, icon: str = "", parent=None):
        super().__init__(parent)
        self.setText(f"{icon} {text}" if icon else text)
        self.setCheckable(True)
        self.setMinimumHeight(55)
        self.setMinimumWidth(180)
        self._update_style()
        self.toggled.connect(self._update_style)
    
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
        self.setWindowTitle("Bot TS - ISAB Timesheet Manager")
        self.setMinimumSize(1200, 800)
        
        self._current_page_index = 0
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        """Configura l'interfaccia."""
        # Widget centrale
        central_widget = QWidget()
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
            }
        """)
        sidebar_layout.addWidget(logo_label)
        
        subtitle = QLabel("ISAB Timesheet Manager")
        subtitle.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.7);
                font-size: 13px;
                padding-bottom: 20px;
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
        self.btn_scarico = SidebarButton("Scarico TS", "📥")
        self.btn_scarico.setChecked(True)
        sidebar_layout.addWidget(self.btn_scarico)
        
        self.btn_carico = SidebarButton("Carico TS", "📤")
        sidebar_layout.addWidget(self.btn_carico)
        
        self.btn_dettagli = SidebarButton("Dettagli OdA", "📋")
        sidebar_layout.addWidget(self.btn_dettagli)
        
        sidebar_layout.addStretch()

        # License Info
        license_info = get_license_info()
        if license_info:
            client = license_info.get("Cliente", "N/D")
            expiry = license_info.get("Scadenza Licenza", "N/D")
            license_text = f"Licenza: {client}\nScadenza: {expiry}"
        else:
            license_text = "Licenza non trovata"

        license_label = QLabel(license_text)
        license_label.setWordWrap(True)
        license_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.6);
                font-size: 13px;
                padding: 5px;
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
            }
        """)
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(version_label)
        
        main_layout.addWidget(sidebar)
        
        # === CONTENT AREA ===
        content_area = QWidget()
        content_area.setStyleSheet("background-color: #f8f9fa;")
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Stack per le pagine
        self.page_stack = QStackedWidget()
        
        # Crea i pannelli
        self.scarico_panel = ScaricaTSPanel()
        self.carico_panel = CaricoTSPanel()
        self.dettagli_panel = DettagliOdAPanel()
        self.settings_panel = SettingsPanel()
        
        # Aggiungi i pannelli allo stack
        self.page_stack.addWidget(self.scarico_panel)   # Index 0
        self.page_stack.addWidget(self.carico_panel)    # Index 1
        self.page_stack.addWidget(self.dettagli_panel)  # Index 2
        self.page_stack.addWidget(self.settings_panel)  # Index 3
        
        content_layout.addWidget(self.page_stack)
        
        main_layout.addWidget(content_area)
        
        # Lista pulsanti per gestione esclusiva
        self.nav_buttons = [
            self.btn_scarico, 
            self.btn_carico, 
            self.btn_dettagli, 
            self.btn_settings
        ]
    
    def _connect_signals(self):
        """Collega i segnali."""
        self.btn_scarico.clicked.connect(lambda: self._navigate_to(0))
        self.btn_carico.clicked.connect(lambda: self._navigate_to(1))
        self.btn_dettagli.clicked.connect(lambda: self._navigate_to(2))
        self.btn_settings.clicked.connect(lambda: self._navigate_to(3))

        # Aggiornamento live impostazioni
        self.settings_panel.settings_saved.connect(self._on_settings_saved)

    def _on_settings_saved(self):
        """Aggiorna i pannelli quando le impostazioni vengono salvate."""
        self.scarico_panel.refresh_fornitori()
        self.dettagli_panel.refresh_fornitori()
        # Aggiorna anche eventuali dati di default in futuro
    
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
        if self._current_page_index == 3:  # Settings page
            if self.settings_panel.has_unsaved_changes():
                can_proceed = self.settings_panel.prompt_save_if_needed()
                if not can_proceed:
                    # L'utente ha annullato - rimani sulla pagina corrente
                    self.nav_buttons[3].setChecked(True)
                    return
        
        # Procedi con la navigazione
        self._current_page_index = index
        self.page_stack.setCurrentIndex(index)
        
        # Aggiorna stato pulsanti
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)
        
        # Se arriviamo su Scarico TS, aggiorna la lista fornitori
        if index == 0:
            self.scarico_panel.refresh_fornitori()
    
    def show_settings(self):
        """Metodo pubblico per navigare alle impostazioni."""
        self._navigate_to(3)
    
    def closeEvent(self, event):
        """Gestisce la chiusura della finestra."""
        # Controlla modifiche non salvate nelle impostazioni
        if self.settings_panel.has_unsaved_changes():
            can_close = self.settings_panel.prompt_save_if_needed()
            if not can_close:
                event.ignore()
                return
        
        event.accept()


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
    
    return splash
