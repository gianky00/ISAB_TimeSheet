import markdown
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.gui.widgets.message_bubble import MessageBubble


class ChatArea(QScrollArea):
    """Area di visualizzazione dei messaggi della chat."""

    table_detected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setStyleSheet("background-color: white; border: 1px solid #dee2e6; border-radius: 8px;")

        self.container = QWidget()
        self.container.setStyleSheet("background-color: white;")
        self.chat_layout = QVBoxLayout(self.container)
        self.chat_layout.setContentsMargins(5, 10, 5, 10)
        self.chat_layout.setSpacing(5)
        self.chat_layout.addStretch()

        self.setWidget(self.container)

    def append_message(self, sender, text):
        """Aggiunge una bolla di messaggio alla chat."""
        is_lyra = sender == "Lyra"
        bubble = MessageBubble(sender, text, is_lyra=is_lyra)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, bubble)

        # Scroll to bottom
        QApplication.processEvents()
        sb = self.verticalScrollBar()
        sb.setValue(sb.maximum())

        # Rilevamento tabelle per l'esportazione Excel
        if "<table>" in markdown.markdown(text, extensions=["tables"]):
            self.table_detected.emit(text)

    def clear(self):
        """Rimuove tutti i messaggi dalla chat."""
        while self.chat_layout.count() > 1:
            item = self.chat_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
