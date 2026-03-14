"""
SyncroJob - Consuntivo Operations Log Widget
Console chiara per il tracciamento delle operazioni in tempo reale.
"""

from datetime import UTC, datetime

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
    QWidget,
)

from src.gui.styles import COLORS


class OperationLogWidget(QFrame):
    """Console professionale in Light Mode per i log delle operazioni."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Inizializza la console di log.

        Args:
            parent: Widget genitore opzionale.
        """
        super().__init__(parent)
        self.setObjectName("logWidget")
        self.setStyleSheet(f"""
            QFrame#logWidget {{
                background-color: {COLORS["bg_white"]};
                border: 1px solid {COLORS["border_light"]};
                border-radius: 12px;
            }}
        """)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)
        shadow.setOffset(0, 2)
        shadow.setColor(QColor(0, 0, 0, 15))
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(8)

        header_row = QHBoxLayout()
        header_label = QLabel("Console Operazioni")
        header_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        header_label.setStyleSheet(
            f"color: {COLORS['text_dark']}; text-transform: uppercase; letter-spacing: 0.5px;"
        )
        header_row.addWidget(header_label)
        header_row.addStretch()

        clear_btn = QPushButton("Pulisci")
        clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        clear_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS["bg_light"]};
                color: {COLORS["text_muted"]};
                border: 1px solid {COLORS["border_light"]};
                border-radius: 6px;
                padding: 4px 12px;
                font-size: 11px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {COLORS["border_light"]};
                color: {COLORS["text_dark"]};
            }}
        """)
        clear_btn.clicked.connect(self.clear)
        header_row.addWidget(clear_btn)
        layout.addLayout(header_row)

        self._log_text = QTextEdit()
        self._log_text.setReadOnly(True)
        self._log_text.setFont(QFont("Cascadia Code", 10))
        self._log_text.setStyleSheet(f"""
            QTextEdit {{
                background-color: {COLORS["bg_light"]};
                color: {COLORS["text_dark"]};
                border: 1px solid {COLORS["border_light"]};
                border-radius: 8px;
                padding: 5px;
                selection-background-color: {COLORS["primary_blue"]}4D;
            }}
            QScrollBar:vertical {{ border: none; background: transparent; width: 6px; }}
            QScrollBar::handle:vertical {{ background: {COLORS["border_medium"]}; border-radius: 3px; }}
        """)
        layout.addWidget(self._log_text)

    def append_log(self, message: str, level: str = "info") -> None:
        """
        Aggiunge una riga alla console con formattazione semantica.

        Args:
            message: Il testo da visualizzare.
            level: Il livello di severità per la colorazione (info, success, warning, error, step).
        """
        colors = {
            "info": COLORS["primary_blue"],
            "success": COLORS["success_dark"],
            "warning": COLORS["warning_orange"],
            "error": COLORS["error_red"],
            "step": COLORS["purple"],
        }
        color = colors.get(level, colors["info"])
        time_str = datetime.now(UTC).astimezone().strftime("%H:%M:%S")
        self._log_text.append(
            f'<span style="color:{COLORS["text_muted"]};">[{time_str}]</span> '
            f'<span style="color:{color}; font-weight: 500;">{message}</span>'
        )
        self._log_text.ensureCursorVisible()

    def clear(self) -> None:
        """Svuota completamente il contenuto della console."""
        self._log_text.clear()
