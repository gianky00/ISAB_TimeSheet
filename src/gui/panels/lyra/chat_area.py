import markdown
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.gui.styles import COLORS
from src.gui.widgets.message_bubble import MessageBubble


class TypingIndicator(QWidget):
    """Widget che simula Lyra che sta scrivendo."""

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 5, 20, 5)

        self.container = QFrame()
        self.container.setStyleSheet(
            f"background: #f4f4f9; border-radius: 15px; border: 1px solid {COLORS['border_light']};"
        )
        c_layout = QHBoxLayout(self.container)
        c_layout.setContentsMargins(15, 8, 15, 8)

        self.label = QLabel("Lyra sta scrivendo...")
        self.label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 12px; font-style: italic;")
        c_layout.addWidget(self.label)

        layout.addWidget(self.container)
        layout.addStretch()


class ChatArea(QScrollArea):
    """Area di visualizzazione dei messaggi della chat."""

    table_detected = pyqtSignal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setStyleSheet("background-color: transparent;")

        self.container = QWidget()
        self.container.setStyleSheet("background-color: transparent;")
        self.chat_layout = QVBoxLayout(self.container)
        self.chat_layout.setContentsMargins(10, 20, 10, 20)
        self.chat_layout.setSpacing(10)
        self.chat_layout.addStretch()

        self.setWidget(self.container)
        self.typing_indicator: TypingIndicator | None = None

    def set_typing(self, is_typing: bool) -> None:
        """Mostra o nasconde l'indicatore di digitazione."""
        if is_typing:
            if self.typing_indicator is None:
                self.typing_indicator = TypingIndicator()
                self.chat_layout.insertWidget(self.chat_layout.count() - 1, self.typing_indicator)
        else:
            if self.typing_indicator is not None:
                self.chat_layout.removeWidget(self.typing_indicator)
                self.typing_indicator.deleteLater()
                self.typing_indicator = None
        self.scroll_to_bottom()

    def append_message(self, sender: str, text: str) -> None:
        """Aggiunge una bolla di messaggio alla chat."""
        # Se Lyra sta scrivendo, rimuoviamo l'indicatore prima di mettere il messaggio reale
        if sender == "Lyra":
            self.set_typing(False)

        is_lyra = sender == "Lyra"
        bubble = MessageBubble(sender, text, is_lyra=is_lyra)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, bubble)

        self.scroll_to_bottom()

        # Rilevamento tabelle per l'esportazione Excel
        if "<table>" in markdown.markdown(text, extensions=["tables"]):
            self.table_detected.emit(text)

    def scroll_to_bottom(self) -> None:
        """Scrolla l'area verso il basso."""
        QApplication.processEvents()
        sb = self.verticalScrollBar()
        if sb is not None:
            sb.setValue(sb.maximum())

    def remove_last_message(self) -> None:
        """Rimuove l'ultima bolla inserita (prima dello stretch)."""
        if self.chat_layout.count() > 1:
            # L'ultimo item (count-1) è lo stretch, quindi prendiamo count-2
            item = self.chat_layout.takeAt(self.chat_layout.count() - 2)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

    def clear(self) -> None:
        """Rimuove tutti i messaggi dalla chat."""
        while self.chat_layout.count() > 1:
            item = self.chat_layout.takeAt(0)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
