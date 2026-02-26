"""
SyncroJob - Message Bubble Widget
Widget per bolle di messaggio in chat, con supporto Markdown.
Estratto da lyra_panel.py per riutilizzabilità.
"""

import markdown
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from src.gui.styles import COLORS


class MessageBubble(QFrame):
    """
    Widget per una singola bolla di messaggio nella chat.

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
        super().__init__(parent)
        self.is_lyra = is_lyra
        self._setup_ui(sender, text)

    def _setup_ui(self, sender: str, text: str) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Container per l'allineamento
        container = QWidget()
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(10, 5, 10, 5)

        # La bolla effettiva
        bubble = QFrame()
        bubble_layout = QVBoxLayout(bubble)
        bubble_layout.setContentsMargins(15, 10, 15, 10)
        bubble_layout.setSpacing(5)

        # Colori e stili basati sul mittente
        if self.is_lyra:
            bg_color = COLORS["bg_alt"]
            text_color = COLORS["text_dark"]
            sender_color = COLORS["purple"]
            bubble.setStyleSheet(
                f"background-color: {bg_color}; "
                f"border-radius: 15px; "
                f"border-bottom-left-radius: 2px; "
                f"border: 1px solid {COLORS['border_light']};"
            )
            container_layout.addWidget(bubble)
            container_layout.addStretch()
        else:
            bg_color = COLORS["purple"]
            text_color = COLORS["bg_white"]
            sender_color = COLORS["bg_hover"]
            bubble.setStyleSheet(
                f"background-color: {bg_color}; border-radius: 15px; border-bottom-right-radius: 2px;"
            )
            container_layout.addStretch()
            container_layout.addWidget(bubble)

        # Shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 30))
        bubble.setGraphicsEffect(shadow)

        # Sender Label
        lbl_sender = QLabel(sender)
        lbl_sender.setStyleSheet(
            f"font-weight: bold; "
            f"font-size: 11px; "
            f"color: {sender_color}; "
            f"background: transparent; "
            f"border: none;"
        )
        bubble_layout.addWidget(lbl_sender)

        # Message Label (Markdown Support via RichText)
        lbl_msg = QLabel()
        lbl_msg.setWordWrap(True)
        lbl_msg.setTextFormat(Qt.TextFormat.RichText)
        lbl_msg.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        # Formattazione Markdown per HTML
        html_text = markdown.markdown(text, extensions=["tables", "fenced_code"])

        # Custom styles for table inside bubble
        if self.is_lyra:
            style_table = (
                'border="1" cellspacing="0" cellpadding="5" '
                'style="border-collapse: collapse; width: 100%; '
                f'margin-top: 5px; border-color: {COLORS["border_light"]};"'
            )
            html_text = html_text.replace("<table>", f"<table {style_table}>")

        lbl_msg.setText(
            f"<div style='color: {text_color}; font-size: 14px; line-height: 1.4;'>{html_text}</div>"
        )
        lbl_msg.setStyleSheet("background: transparent; border: none;")
        bubble_layout.addWidget(lbl_msg)

        layout.addWidget(container)
