"""
Standard Terminal Log Widget per SyncroJob.
Sostituisce la vecchia timeline orizzontale con un visualizzatore testuale pulito e moderno in Light Mode.
"""

from datetime import UTC, datetime

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QColor, QFont, QTextCharFormat, QTextCursor
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPlainTextEdit, QVBoxLayout, QWidget

from src.gui.styles import COLORS


class TerminalLogWidget(QWidget):
    """
    Console di log in stile terminale chiaro con evidenziazione dei livelli.
    Fornisce una visualizzazione testuale moderna e pulita delle attività del bot.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Inizializza il widget del terminale e configura l'editor di testo.

        Args:
            parent: Widget genitore.
        """
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(5)

        # Header opzionale
        header_layout = QHBoxLayout()
        self.title_label = QLabel("LOG ATTIVITÀ")
        self.title_label.setStyleSheet(
            f"font-weight: bold; color: {COLORS['text_muted']}; font-size: 10px; letter-spacing: 1px;"
        )
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        self.main_layout.addLayout(header_layout)

        # Area di testo
        self.editor = QPlainTextEdit()
        self.editor.setReadOnly(True)
        self.editor.setMaximumBlockCount(1000)

        # Styling Enterprise Light Console
        self.editor.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {COLORS["bg_light"]};
                color: {COLORS["text_dark"]};
                border: 1px solid {COLORS["border_light"]};
                border-radius: 8px;
                padding: 8px;
            }}
        """)

        font = QFont("Consolas", 10)
        if not font.exactMatch():
            font = QFont("Courier New", 10)
        self.editor.setFont(font)

        self.main_layout.addWidget(self.editor)

    @pyqtSlot(str)
    @pyqtSlot(str, str)
    def append(self, message: str, level: str = "INFO") -> None:
        """
        Aggiunge un messaggio colorato alla console in base al livello di logging.

        Args:
            message: Testo del messaggio da loggare.
            level: Livello del log (es. INFO, ERROR, WARN, SUCCESS).
        """
        timestamp = datetime.now(UTC).astimezone().strftime("%H:%M:%S")

        self.editor.moveCursor(QTextCursor.MoveOperation.End)

        # Formattazione per livello (Colori ad alto contrasto per Light Mode)
        color = COLORS["text_dark"]

        level_upper = level.upper()
        if "ERROR" in level_upper or "❌" in message:
            color = COLORS["error_red"]
        elif "WARN" in level_upper or "⚠️" in message:
            color = COLORS["warning_orange"]
        elif "SUCCESS" in level_upper or "✅" in message:
            color = COLORS["success_dark"]
        elif "INFO" in level_upper:
            color = COLORS["primary_blue"]

        # Costruisce la riga
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))
        fmt.setFontWeight(600 if level_upper != "INFO" else 400)

        # Inserisce timestamp grigio
        ts_fmt = QTextCharFormat()
        ts_fmt.setForeground(QColor(COLORS["text_muted"]))
        self.editor.setCurrentCharFormat(ts_fmt)
        self.editor.insertPlainText(f"[{timestamp}] ")

        # Inserisce il resto con il colore del livello
        self.editor.setCurrentCharFormat(fmt)
        self.editor.insertPlainText(f"{message}\n")

        # Auto-scroll
        v_scroll = self.editor.verticalScrollBar()
        if v_scroll:
            v_scroll.setValue(v_scroll.maximum())

    def clear(self) -> None:
        """Pulisce tutto il contenuto della console di log."""
        self.editor.clear()
