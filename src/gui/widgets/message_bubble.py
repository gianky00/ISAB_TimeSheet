"""SyncroJob - Message Bubble Widget.

Widget per bolle di messaggio in chat, con supporto Markdown.
Estratto da lyra_panel.py per riutilizzabilit .
"""

import markdown
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from src.gui.styles import COLORS


class MessageBubble(QFrame):
    """Widget per una singola bolla di messaggio nella chat.

    Supporta:
    - Allineamento differenziato (AI a sinistra, utente a destra)
    - Rendering Markdown con supporto tabelle
    - Ombre e bordi arrotondati
    - Selezione testo

    Args:
      sender: Nome del mittente
      text: Testo del messaggio (supporta Markdown)
      is_lyra: True se messaggio AI (sinistra), False se utente (destra)
      parent: Widget parent opzionale
    """

    def __init__(self, sender: str, text: str, is_lyra: bool = True, parent: QWidget | None = None) -> None:
        """Inizializza la classe."""
        super().__init__(parent)
        self.is_lyra = is_lyra
        self._setup_ui(sender, text)

    def _setup_ui(self, sender: str, text: str) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Container per l'allineamento
        container = QWidget()
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(20, 8, 20, 8)
        container_layout.setSpacing(15)

        # La bolla effettiva
        bubble = QFrame()
        bubble.setObjectName("chatBubble")
        bubble_layout = QVBoxLayout(bubble)
        bubble_layout.setContentsMargins(18, 12, 18, 12)
        bubble_layout.setSpacing(6)

        # Avatar / Name Initials
        avatar = QLabel()
        avatar.setFixedSize(32, 32)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Colori e stili basati sul mittente
        if self.is_lyra:
            bg_color = "#f4f4f9"
            text_color = COLORS["text_dark"]

            avatar.setText("L")
            avatar.setStyleSheet(f"""
        background-color: {COLORS["purple"]};
        color: white;
        border-radius: 16px;
        font-weight: 900;
        font-size: 14px;
      """)

            bubble.setStyleSheet(f"""
        QFrame#chatBubble {{
          background-color: {bg_color};
          border-radius: 20px;
          border-top-left-radius: 4px;
          border: 1px solid {COLORS["border_light"]};
        }}
      """)

            container_layout.addWidget(avatar, alignment=Qt.AlignmentFlag.AlignTop)
            container_layout.addWidget(bubble)
            container_layout.addStretch()
        else:
            bg_color = COLORS["purple"]
            text_color = COLORS["bg_white"]

            avatar.setText("U")
            avatar.setStyleSheet(f"""
        background-color: {COLORS["text_muted"]};
        color: white;
        border-radius: 16px;
        font-weight: 900;
        font-size: 14px;
      """)

            bubble.setStyleSheet(f"""
        QFrame#chatBubble {{
          background-color: {bg_color};
          border-radius: 20px;
          border-top-right-radius: 4px;
        }}
      """)

            container_layout.addStretch()
            container_layout.addWidget(bubble)
            container_layout.addWidget(avatar, alignment=Qt.AlignmentFlag.AlignTop)

        # Message Label (Markdown Support via RichText)
        lbl_msg = QLabel()
        lbl_msg.setWordWrap(True)
        lbl_msg.setTextFormat(Qt.TextFormat.RichText)
        lbl_msg.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        # Formattazione Markdown per HTML
        html_text = markdown.markdown(text, extensions=["tables", "fenced_code", "nl2br"])

        # Custom styles for table inside bubble
        if self.is_lyra:
            style_table = (
                'border="1" cellspacing="0" cellpadding="8" '
                'style="border-collapse: collapse; width: 100%; '
                f'margin-top: 10px; border: 1px solid {COLORS["border_light"]}; border-radius: 8px;"'
            )
            html_text = html_text.replace("<table>", f"<table {style_table}>")

        lbl_msg.setText(
            f"<div style='color: {text_color}; font-size: 14px; line-height: 1.5;'>{html_text}</div>"
        )
        lbl_msg.setStyleSheet("background: transparent; border: none;")
        bubble_layout.addWidget(lbl_msg)

        layout.addWidget(container)
