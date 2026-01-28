from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar, QApplication, QFrame
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QFont
import os

class StartupDialog(QDialog):
    """Splash Screen avanzato con log dettagliati delle operazioni."""
    
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(500, 380)
        
        # Layout principale
        self.layout = QVBoxLayout(self)
        self.container = QFrame()
        self.container.setObjectName("StartupContainer")
        self.container.setStyleSheet("""
            #StartupContainer {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #1a1a1a, stop:1 #000000);
                border-radius: 12px;
                border: 1px solid #333333;
            }
            QLabel { color: #e0e0e0; font-family: 'Consolas', 'Segoe UI'; }
            #Title { font-size: 26px; font-weight: bold; color: #3498db; margin-bottom: 2px; }
            #Subtitle { font-size: 10px; color: #555555; text-transform: uppercase; letter-spacing: 2px; }
            #LogLine { font-size: 11px; color: #00ff00; }
            #OldLog { font-size: 10px; color: #666666; }
        """)
        
        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(35, 35, 35, 35)
        container_layout.setSpacing(10)

        # Header: Icona + Titolo
        header_layout = QVBoxLayout()
        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if os.path.exists("assets/app.ico"):
            self.logo_label.setPixmap(QIcon("assets/app.ico").pixmap(48, 48))
        header_layout.addWidget(self.logo_label)

        self.title_label = QLabel("SYNCROJOB ENTERPRISE")
        self.title_label.setObjectName("Title")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.title_label)

        self.subtitle = QLabel("Supplier Portal Automation Engine")
        self.subtitle.setObjectName("Subtitle")
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.subtitle)
        container_layout.addLayout(header_layout)

        container_layout.addSpacing(15)

        # Area LOG (Visualizza gli ultimi 4 messaggi)
        self.log_container = QVBoxLayout()
        self.log_container.setSpacing(4)
        self.log_labels = []
        for i in range(5):
            lbl = QLabel("")
            lbl.setObjectName("OldLog" if i < 4 else "LogLine")
            self.log_container.addWidget(lbl)
            self.log_labels.append(lbl)
        container_layout.addLayout(self.log_container)

        container_layout.addStretch()

        # Barra di progresso sottile
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: #222222;
                height: 4px;
                border-radius: 2px;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 2px;
            }
        """)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setRange(0, 100)
        container_layout.addWidget(self.progress_bar)

        # Footer
        from src.core.version import __version__
        footer = QLabel(f"INITIALIZING SYSTEM CORE v{__version__} ... READY")
        footer.setStyleSheet("font-size: 9px; color: #444444;")
        footer.setAlignment(Qt.AlignmentFlag.AlignRight)
        container_layout.addWidget(footer)

        self.layout.addWidget(self.container)
        self.current_logs = []

    def update_status(self, message: str, progress: int):
        """Aggiunge un log e aggiorna il progresso."""
        # Aggiungi prefisso stile console
        formatted_msg = f"> {message}"
        if progress == 100: formatted_msg = f"DONE: {message}"
        
        self.current_logs.append(formatted_msg)
        if len(self.current_logs) > 5:
            self.current_logs.pop(0)

        # Aggiorna le label (l'ultima è quella "attiva")
        for i in range(5):
            if i < len(self.current_logs):
                self.log_labels[i].setText(self.current_logs[i])
                # Effetto opacità per i log vecchi
                opacity = 0.2 + (i * 0.2)
                self.log_labels[i].setStyleSheet(f"color: rgba(0, 255, 0, {opacity});")
            else:
                self.log_labels[i].setText("")

        self.progress_bar.setValue(progress)
        QApplication.processEvents()
