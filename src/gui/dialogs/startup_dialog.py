from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QApplication, QFrame, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QIcon, QColor
import os
import random

class StartupDialog(QDialog):
    """Splash Screen raffinato e pulito."""
    
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(550, 350)
        
        # Layout principale
        self.layout = QVBoxLayout(self)
        self.container = QFrame()
        self.container.setObjectName("MainFrame")
        self.container.setStyleSheet("""
            #MainFrame {
                background-color: #0a0a0a;
                border-radius: 15px;
                border: 1px solid #1e1e1e;
            }
            QLabel { color: #ffffff; font-family: 'Segoe UI', 'Consolas'; }
            #MainTitle { font-size: 32px; font-weight: 900; color: #ffffff; letter-spacing: 1px; }
            #VersionLabel { font-size: 12px; color: #3498db; font-weight: bold; margin-top: -5px; }
            #LogArea { background-color: #050505; border-radius: 8px; border: 1px solid #151515; }
        """)
        
        # Shadow Effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(40)
        shadow.setColor(QColor(52, 152, 219, 60))
        shadow.setOffset(0, 0)
        self.container.setGraphicsEffect(shadow)

        main_layout = QVBoxLayout(self.container)
        main_layout.setContentsMargins(45, 45, 45, 45)
        main_layout.setSpacing(15)

        # --- HEADER ---
        header_layout = QHBoxLayout()
        
        # Logo
        self.logo_label = QLabel()
        if os.path.exists("assets/app.ico"):
            self.logo_label.setPixmap(QIcon("assets/app.ico").pixmap(64, 64))
        header_layout.addWidget(self.logo_label)

        title_vbox = QVBoxLayout()
        title_vbox.setSpacing(0)
        self.title_label = QLabel('SYNCRO<span style="color:#3498db;">JOB</span>')
        self.title_label.setObjectName("MainTitle")
        self.title_label.setTextFormat(Qt.TextFormat.RichText)
        
        from src.core.version import __version__
        self.version_label = QLabel(f"VERSION {__version__}")
        self.version_label.setObjectName("VersionLabel")
        
        title_vbox.addWidget(self.title_label)
        title_vbox.addWidget(self.version_label)
        header_layout.addLayout(title_vbox)
        header_layout.addStretch()
        
        main_layout.addLayout(header_layout)

        # --- LOG CONSOLE ---
        self.log_frame = QFrame()
        self.log_frame.setObjectName("LogArea")
        log_vbox = QVBoxLayout(self.log_frame)
        log_vbox.setContentsMargins(20, 15, 20, 15)
        log_vbox.setSpacing(4)
        
        self.log_labels = []
        for i in range(5):
            lbl = QLabel("")
            lbl.setStyleSheet(f"font-size: 11px; color: rgba(255, 255, 255, {0.2 + (i*0.2)}); font-family: 'Consolas';")
            log_vbox.addWidget(lbl)
            self.log_labels.append(lbl)
        
        main_layout.addWidget(self.log_frame)

        # --- PROGRESS BAR ---
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(3)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: #111111;
                border-radius: 1px;
            }
            QProgressBar::chunk {
                background-color: #3498db;
            }
        """)
        self.progress_bar.setTextVisible(False)
        main_layout.addWidget(self.progress_bar)

        # --- FOOTER ---
        footer_layout = QHBoxLayout()
        self.status_text = QLabel("INITIALIZING...")
        self.status_text.setStyleSheet("font-size: 10px; color: #444; font-weight: bold; letter-spacing: 1px;")
        
        footer_layout.addWidget(self.status_text)
        footer_layout.addStretch()
        main_layout.addLayout(footer_layout)

        self.layout.addWidget(self.container)
        
        # Variabili di stato
        self.current_logs = []
        
        # Animazione Fade-In
        self.setWindowOpacity(0.0)
        self.fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self.fade_anim.setDuration(600)
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.fade_anim.start()

    def update_status(self, message: str, progress: int):
        """Aggiorna lo stato con log bianchi e testo pulito."""
        # Footer status
        self.status_text.setText(f"{message.upper()}")
        
        # Log Rolling
        self.current_logs.append(f"> {message}")
        if len(self.current_logs) > 5:
            self.current_logs.pop(0)

        # Update labels (Bianchi con opacità variabile)
        for i in range(5):
            if i < len(self.current_logs):
                self.log_labels[i].setText(self.current_logs[i])
                opacity = 0.3 if i < len(self.current_logs) - 1 else 1.0
                self.log_labels[i].setStyleSheet(f"color: rgba(255, 255, 255, {opacity}); font-family: 'Consolas';")
            else:
                self.log_labels[i].setText("")

        self.progress_bar.setValue(progress)
        QApplication.processEvents()
