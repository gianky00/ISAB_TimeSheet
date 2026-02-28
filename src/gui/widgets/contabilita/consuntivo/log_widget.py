"""
SyncroJob - Consuntivo Operations Log Widget
Console dark per il tracciamento delle operazioni in tempo reale.
"""

from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)


class OperationLogWidget(QFrame):
    """Console dark per i log delle operazioni."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("logWidget")
        self.setStyleSheet("""
            QFrame#logWidget {
                background-color: #1e1e2e;
                border: 1px solid #313244;
                border-radius: 16px;
            }
        """)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(12)
        shadow.setOffset(0, 3)
        shadow.setColor(QColor(0, 0, 0, 20))
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)

        header_row = QHBoxLayout()
        header_label = QLabel("🖥️ Console Operazioni")
        header_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        header_label.setStyleSheet("color: #cdd6f4;")
        header_row.addWidget(header_label)
        header_row.addStretch()

        clear_btn = QPushButton("Pulisci")
        clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        clear_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255,255,255,0.08); color: #bac2de;
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 6px; padding: 4px 12px; font-size: 11px;
            }
            QPushButton:hover { background: rgba(255,255,255,0.15); }
        """)
        clear_btn.clicked.connect(self.clear)
        header_row.addWidget(clear_btn)
        layout.addLayout(header_row)

        self._log_text = QTextEdit()
        self._log_text.setReadOnly(True)
        self._log_text.setFont(QFont("Cascadia Code", 10))
        self._log_text.setStyleSheet("""
            QTextEdit {
                background: transparent; color: #a6e3a1; border: none;
                selection-background-color: rgba(137, 180, 250, 0.3);
            }
            QScrollBar:vertical { border: none; background: transparent; width: 6px; }
            QScrollBar::handle:vertical { background: rgba(255,255,255,0.15); border-radius: 3px; }
        """)
        layout.addWidget(self._log_text)

    def append_log(self, message: str, level: str = "info") -> None:
        colors = {
            "info": "#89b4fa",
            "success": "#a6e3a1",
            "warning": "#f9e2af",
            "error": "#f38ba8",
            "step": "#cba6f7",
        }
        color = colors.get(level, colors["info"])
        time_str = datetime.now().strftime("%H:%M:%S")
        self._log_text.append(
            f'<span style="color:#585b70;">[{time_str}]</span> <span style="color:{color};">{message}</span>'
        )
        self._log_text.ensureCursorVisible()

    def clear(self) -> None:
        self._log_text.clear()
