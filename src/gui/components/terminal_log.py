"""
Standard Terminal Log Widget per SyncroJob.
Sostituisce la vecchia timeline orizzontale con un visualizzatore testuale pulito e moderno.
"""

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QColor, QFont, QTextCharFormat, QTextCursor
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPlainTextEdit, QVBoxLayout, QWidget


class TerminalLogWidget(QWidget):
    """
    Console di log in stile terminale con evidenziazione dei livelli.
    Fornisce una visualizzazione testuale moderna e pulita delle attività del bot.
    """

    def __init__(self, parent=None):
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
        self.title_label.setStyleSheet("font-weight: bold; color: #808080; font-size: 10px;")
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        self.main_layout.addLayout(header_layout)

        # Area di testo
        self.editor = QPlainTextEdit()
        self.editor.setReadOnly(True)
        self.editor.setMaximumBlockCount(1000)  # Limite per performance

        # Styling Cyber-Console
        self.editor.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1E1E1E;
                color: #D4D4D4;
                border: 1px solid #333333;
                border-radius: 4px;
                padding: 5px;
            }
        """)

        font = QFont("Consolas", 10)
        if not font.exactMatch():
            font = QFont("Courier New", 10)
        self.editor.setFont(font)

        self.main_layout.addWidget(self.editor)

    @pyqtSlot(str)
    @pyqtSlot(str, str)
    def append(self, message: str, level: str = "INFO"):
        """
        Aggiunge un messaggio colorato alla console in base al livello di logging.

        Args:
            message: Testo del messaggio da loggare.
            level: Livello del log (es. INFO, ERROR, WARN, SUCCESS).
        """
        from datetime import datetime

        timestamp = datetime.now().strftime("%H:%M:%S")

        self.editor.moveCursor(QTextCursor.MoveOperation.End)

        # Formattazione per livello
        color = "#D4D4D4"

        level_upper = level.upper()
        if "ERROR" in level_upper or "❌" in message:
            color = "#F44336"
        elif "WARN" in level_upper or "⚠️" in message:
            color = "#FFB300"
        elif "SUCCESS" in level_upper or "✅" in message:
            color = "#4CAF50"

        # Costruisce la riga
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))

        # Inserisce timestamp grigio
        ts_fmt = QTextCharFormat()
        ts_fmt.setForeground(QColor("#606060"))
        self.editor.setCurrentCharFormat(ts_fmt)
        self.editor.insertPlainText(f"[{timestamp}] ")

        # Inserisce il resto con il colore del livello
        self.editor.setCurrentCharFormat(fmt)
        self.editor.insertPlainText(f"{message}\n")

        # Auto-scroll
        v_scroll = self.editor.verticalScrollBar()
        if v_scroll:
            v_scroll.setValue(v_scroll.maximum())

    def clear(self):
        """Pulisce tutto il contenuto della console di log."""
        self.editor.clear()
