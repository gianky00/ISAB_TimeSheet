from PyQt6.QtWidgets import (
    QVBoxLayout, QLabel, QFrame, QWidget
)
from src.gui.styles import COLORS
from src.gui.widgets.core_widgets import StandardInput

class FormUtils:
    @staticmethod
    def create_card(title_text: str) -> tuple[QFrame, QVBoxLayout]:
        card = QFrame()
        card.setStyleSheet(f"QFrame {{ background-color: {COLORS['bg_white']}; border-radius: 10px; border: 1px solid {COLORS['border_light']}; }}")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 15, 20, 20)
        layout.setSpacing(15)
        
        title_lbl = QLabel(title_text)
        title_lbl.setStyleSheet(f"font-weight: 800; font-size: 12px; letter-spacing: 0.5px; color: {COLORS['primary_dark']}; border: none;")
        layout.addWidget(title_lbl)
        
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet(f"background-color: {COLORS['bg_alt']}; border: none; min-height: 1px; max-height: 1px;")
        layout.addWidget(line)
        return card, layout

    @staticmethod
    def create_input_group(label_text: str, widget: QWidget, width: int = 0) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.setSpacing(4)
        lbl = QLabel(label_text)
        lbl.setStyleSheet(f"font-size: 11px; font-weight: 600; color: {COLORS['text_muted']}; border: none;")
        layout.addWidget(lbl)
        if width > 0:
            widget.setFixedWidth(width)
        if isinstance(widget, StandardInput):
            widget.setMinimumHeight(36)
            widget.setMaximumHeight(36)
        layout.addWidget(widget)
        return layout
