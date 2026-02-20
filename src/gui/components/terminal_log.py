"""
Standard Terminal Log Widget per SyncroJob.
Sostituisce la vecchia timeline orizzontale con un visualizzatore testuale pulito e moderno.
"""

from PyQt6.QtWidgets import QPlainTextEdit, QVBoxLayout, QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QFont, QTextCharFormat, QColor, QTextCursor

class TerminalLogWidget(QWidget):
    """
    Console di log in stile terminale con evidenziazione dei livelli.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)

        # Header opzionale
        header_layout = QHBoxLayout()
        self.title_label = QLabel("LOG ATTIVITÀ")
        self.title_label.setStyleSheet("font-weight: bold; color: #808080; font-size: 10px;")
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        self.layout.addLayout(header_layout)

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
        
        self.layout.addWidget(self.editor)

    @pyqtSlot(str)
    @pyqtSlot(str, str)
    def append(self, message: str, level: str = "INFO"):
        """Aggiunge un messaggio colorato in base al livello."""
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
        self.editor.verticalScrollBar().setValue(self.editor.verticalScrollBar().maximum())

    def clear(self):
        self.editor.clear()
