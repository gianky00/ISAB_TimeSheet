from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar, QApplication
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QPixmap, QIcon
import os

class StartupDialog(QDialog):
    """Finestra di avvio che mostra il progresso dell'inizializzazione."""
    
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(450, 300)
        
        # Layout principale con stile "Glassmorphism"
        self.layout = QVBoxLayout(self)
        self.container = QLabel()
        self.container.setObjectName("StartupContainer")
        self.container.setStyleSheet("""
            #StartupContainer {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #2c3e50, stop:1 #000000);
                border-radius: 15px;
                border: 1px solid #34495e;
            }
            QLabel { color: white; font-family: 'Segoe UI'; }
            #Title { font-size: 24px; font-weight: bold; margin-bottom: 5px; color: #3498db; }
            #Status { font-size: 13px; color: #bdc3c7; }
        """)
        
        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(30, 30, 30, 30)
        container_layout.setSpacing(15)

        # Logo/Icona se disponibile
        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Cerchiamo di caricare l'icona dell'app
        icon_path = "assets/app.ico"
        if os.path.exists(icon_path):
            self.logo_label.setPixmap(QIcon(icon_path).pixmap(64, 64))
        container_layout.addWidget(self.logo_label)

        # Titolo
        self.title_label = QLabel("SyncroJob")
        self.title_label.setObjectName("Title")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(self.title_label)

        # Sottotitolo/Status
        self.status_label = QLabel("Preparazione sistema...")
        self.status_label.setObjectName("Status")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(self.status_label)

        # Barra di progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: #34495e;
                height: 6px;
                border-radius: 3px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 3px;
            }
        """)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(10)
        container_layout.addWidget(self.progress_bar)

        # Versione
        from src.core.version import __version__
        self.ver_label = QLabel(f"Versione {__version__}")
        self.ver_label.setStyleSheet("font-size: 10px; color: #7f8c8d;")
        self.ver_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        container_layout.addStretch()
        container_layout.addWidget(self.ver_label)

        self.layout.addWidget(self.container)

    def update_status(self, message: str, progress: int):
        """Aggiorna il messaggio e la barra di progresso."""
        self.status_label.setText(message)
        self.progress_bar.setValue(progress)
        QApplication.processEvents() # Forza l'aggiornamento della UI
