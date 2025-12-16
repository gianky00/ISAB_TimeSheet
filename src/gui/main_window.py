"""
Bot TS - Main Window
Finestra principale dell'applicazione.
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QStackedWidget, QSizePolicy, QMessageBox,
    QApplication, QSplashScreen
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QIcon, QPixmap, QPainter, QColor

from src.core import version, config_manager, license_validator, app_updater
from src.gui.panels import ScaricaTSPanel, CaricoTSPanel, DettagliOdAPanel
from src.gui.settings_panel import SettingsPanel
from src.utils import get_app_icon_path


class SidebarButton(QPushButton):
    """Pulsante della sidebar."""
    
    def __init__(self, text: str, icon: str = "", parent=None):
        super().__init__(parent)
        self.setText(f"{icon} {text}" if icon else text)
        self.setCheckable(True)
        self.setMinimumHeight(50)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        self.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 12px 20px;
                border: none;
                border-radius: 8px;
                font-size: 13px;
                color: #495057;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #e9ecef;
            }
            QPushButton:checked {
                background-color: #0d6efd;
                color: white;
                font-weight: bold;
            }
        """)


class MainWindow(QMainWindow):
    """Finestra principale dell'applicazione."""
    
    def __init__(self):
        super().__init__()
        self._setup_window()
        self._setup_ui()
        self._check_license()
        self._check_updates()
    
    def _setup_window(self):
        """Configura la finestra."""
        self.setWindowTitle(f"{version.__app_name__} v{version.__version__}")
        self.setMinimumSize(1100, 700)
        self.resize(1200, 750)
        
        # Icona
        icon_path = get_app_icon_path()
        if icon_path:
            self.setWindowIcon(QIcon(icon_path))
        
        # Centra la finestra
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
    
    def _setup_ui(self):
        """Configura l'interfaccia utente."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = self._create_sidebar()
        main_layout.addWidget(self.sidebar)
        
        # Content Area
        content_frame = QFrame()
        content_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
            }
        """)
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Stacked Widget per i pannelli
        self.stack = QStackedWidget()
        
        # Pannelli
        self.scarico_ts_panel = ScaricaTSPanel()
        self.carico_ts_panel = CaricoTSPanel()
        self.dettagli_oda_panel = DettagliOdAPanel()
        self.settings_panel = SettingsPanel()
        
        self.stack.addWidget(self.scarico_ts_panel)
        self.stack.addWidget(self.carico_ts_panel)
        self.stack.addWidget(self.dettagli_oda_panel)
        self.stack.addWidget(self.settings_panel)
        
        content_layout.addWidget(self.stack)
        
        main_layout.addWidget(content_frame, 1)
        
        # Connetti i segnali della sidebar
        self._connect_sidebar()
        
        # Seleziona il primo pannello
        self.sidebar_buttons[0].setChecked(True)
    
    def _create_sidebar(self) -> QFrame:
        """Crea la sidebar."""
        sidebar = QFrame()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: white;
                border-right: 1px solid #dee2e6;
            }
        """)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(15, 20, 15, 20)
        layout.setSpacing(8)
        
        # Logo/Header
        header = QLabel(version.__app_name__)
        header.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        header.setStyleSheet("color: #0d6efd; padding: 10px 0;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        version_label = QLabel(f"v{version.__version__}")
        version_label.setStyleSheet("color: #6c757d; font-size: 11px;")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)
        
        # Separatore
        sep1 = QFrame()
        sep1.setFrameShape(QFrame.Shape.HLine)
        sep1.setStyleSheet("background-color: #dee2e6;")
        sep1.setFixedHeight(1)
        layout.addWidget(sep1)
        layout.addSpacing(10)
        
        # Titolo sezione
        bots_label = QLabel("BOT DISPONIBILI")
        bots_label.setStyleSheet("color: #6c757d; font-size: 11px; font-weight: bold;")
        layout.addWidget(bots_label)
        
        # Pulsanti bot
        self.sidebar_buttons = []
        
        scarico_btn = SidebarButton("Scarico TS", "📥")
        self.sidebar_buttons.append(scarico_btn)
        layout.addWidget(scarico_btn)
        
        carico_btn = SidebarButton("Carico TS", "📤")
        self.sidebar_buttons.append(carico_btn)
        layout.addWidget(carico_btn)
        
        oda_btn = SidebarButton("Dettagli OdA", "📋")
        self.sidebar_buttons.append(oda_btn)
        layout.addWidget(oda_btn)
        
        layout.addStretch()
        
        # Separatore
        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setStyleSheet("background-color: #dee2e6;")
        sep2.setFixedHeight(1)
        layout.addWidget(sep2)
        layout.addSpacing(10)
        
        # Impostazioni
        settings_btn = SidebarButton("Impostazioni", "⚙️")
        self.sidebar_buttons.append(settings_btn)
        layout.addWidget(settings_btn)
        
        # Info licenza in fondo
        layout.addSpacing(10)
        
        license_info = QFrame()
        license_info.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        license_layout = QVBoxLayout(license_info)
        license_layout.setSpacing(2)
        
        is_valid, _ = license_validator.verify_license()
        client = license_validator.get_license_client()
        expiry = license_validator.get_license_expiry()
        
        if is_valid:
            status_icon = "✅"
            status_color = "#28a745"
        else:
            status_icon = "⚠️"
            status_color = "#dc3545"
        
        status_label = QLabel(f"{status_icon} {client}")
        status_label.setStyleSheet(f"color: {status_color}; font-size: 11px; font-weight: bold;")
        license_layout.addWidget(status_label)
        
        expiry_label = QLabel(f"Scade: {expiry}")
        expiry_label.setStyleSheet("color: #6c757d; font-size: 10px;")
        license_layout.addWidget(expiry_label)
        
        layout.addWidget(license_info)
        
        return sidebar
    
    def _connect_sidebar(self):
        """Connette i segnali della sidebar."""
        for i, btn in enumerate(self.sidebar_buttons):
            btn.clicked.connect(lambda checked, idx=i: self._on_sidebar_clicked(idx))
    
    def _on_sidebar_clicked(self, index: int):
        """Gestisce il click su un pulsante della sidebar."""
        # Deseleziona tutti
        for btn in self.sidebar_buttons:
            btn.setChecked(False)
        
        # Seleziona quello cliccato
        self.sidebar_buttons[index].setChecked(True)
        
        # Cambia pannello
        self.stack.setCurrentIndex(index)
    
    def _check_license(self):
        """Verifica la licenza all'avvio."""
        is_valid, message = license_validator.verify_license()
        
        if not is_valid:
            QMessageBox.warning(
                self,
                "Licenza non valida",
                f"⚠️ {message}\n\n"
                f"Alcune funzionalità potrebbero essere limitate.\n"
                f"Contatta l'amministratore per rinnovare la licenza."
            )
    
    def _check_updates(self):
        """Controlla aggiornamenti in background."""
        QTimer.singleShot(2000, lambda: app_updater.check_for_updates(silent=True))
    
    def closeEvent(self, event):
        """Gestisce la chiusura della finestra."""
        # Verifica se ci sono bot in esecuzione
        panels = [self.scarico_ts_panel, self.carico_ts_panel, self.dettagli_oda_panel]
        
        for panel in panels:
            if panel.worker and panel.worker.isRunning():
                reply = QMessageBox.question(
                    self,
                    "Bot in esecuzione",
                    "Un bot è ancora in esecuzione.\n"
                    "Vuoi davvero chiudere l'applicazione?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )
                
                if reply == QMessageBox.StandardButton.No:
                    event.ignore()
                    return
                else:
                    panel.worker.stop()
                    panel.worker.wait(3000)
        
        event.accept()


def create_splash_screen() -> QSplashScreen:
    """Crea lo splash screen."""
    # Crea un pixmap per lo splash
    splash_pixmap = QPixmap(400, 250)
    splash_pixmap.fill(QColor("#0d6efd"))
    
    # Disegna testo
    painter = QPainter(splash_pixmap)
    painter.setPen(QColor("white"))
    
    # Titolo
    font = QFont("Segoe UI", 24, QFont.Weight.Bold)
    painter.setFont(font)
    painter.drawText(splash_pixmap.rect(), Qt.AlignmentFlag.AlignCenter, version.__app_name__)
    
    # Versione
    font = QFont("Segoe UI", 12)
    painter.setFont(font)
    rect = splash_pixmap.rect()
    rect.setTop(rect.center().y() + 30)
    painter.drawText(rect, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop, 
                    f"v{version.__version__}")
    
    # Loading
    rect.setTop(rect.center().y() + 30)
    painter.drawText(rect, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
                    "Caricamento...")
    
    painter.end()
    
    splash = QSplashScreen(splash_pixmap)
    splash.setWindowFlags(Qt.WindowType.SplashScreen | Qt.WindowType.FramelessWindowHint)
    
    return splash
