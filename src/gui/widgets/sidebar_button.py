"""
SyncroJob - Sidebar Button (Premium V6)
Risoluzione contrasto: Sfondo selezione più scuro e opacità testo migliorata.
"""

from PyQt6.QtCore import QPropertyAnimation, QRect, QSize, Qt, pyqtProperty
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QGraphicsOpacityEffect, QPushButton, QWidget

from src.utils.helpers import get_colored_icon


class SidebarButton(QPushButton):
    """
    Pulsante ultra-moderno per la sidebar.
    Ottimizzato per la visibilità su sfondi scuri gradienti.
    """

    def __init__(self, text: str, icon_path: str = "", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.label_text = text
        self.icon_path = icon_path
        self._collapsed = False
        self._badge_count = 0
        self._text_opacity = 1.0 # Default a 1.0 per visibilità immediata

        if icon_path:
            self.setIcon(get_colored_icon(icon_path, "#ffffff"))

        self.setCheckable(True)
        self.setMinimumHeight(48)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.glow = QGraphicsDropShadowEffect(self)
        self.glow.setBlurRadius(15)
        self.glow.setColor(QColor(0, 150, 136, 0))
        self.glow.setOffset(0, 0)
        self.setGraphicsEffect(self.glow)

        self._refresh_state()
        self._update_style()
        self.toggled.connect(self._on_toggled)

    @pyqtProperty(float)
    def text_opacity(self) -> float:
        return self._text_opacity

    @text_opacity.setter
    def text_opacity(self, value: float) -> None:
        self._text_opacity = value
        self._update_style()

    def _on_toggled(self, checked: bool) -> None:
        if checked:
            self.glow.setColor(QColor(0, 150, 136, 180))
        else:
            if self._badge_count == 0:
                self.glow.setColor(QColor(0, 150, 136, 0))
        self._update_style()

    def set_collapsed(self, collapsed: bool, animated: bool = False) -> None:
        self._collapsed = collapsed
        self._refresh_state()
        self._update_style()

    def _refresh_state(self) -> None:
        base_text = f"   {self.label_text}"
        display_text = f"{base_text} ({self._badge_count})" if self._badge_count > 0 else base_text

        if self._collapsed:
            self.setText("")
            self.setIconSize(QSize(22, 22))
        else:
            self.setText(display_text)
            self.setIconSize(QSize(18, 18))

    def _update_style(self) -> None:
        align = "center" if self._collapsed else "left"
        padding = "0px" if self._collapsed else "12px 15px"
        
        # Sfondo selezione più deciso (Teal scuro trasparente) per contrasto con testo bianco
        if self.isChecked():
            bg_color = "rgba(0, 150, 136, 0.25)" 
            text_color = "#ffffff"
            font_weight = "800"
        else:
            bg_color = "transparent"
            text_color = f"rgba(255, 255, 255, {max(0.4, self._text_opacity)})" # Mai sotto 0.4 se visibile
            font_weight = "500"

        self.setStyleSheet(f"""
            QPushButton {{
                color: {text_color};
                background-color: {bg_color};
                border-radius: 8px;
                padding: {padding};
                text-align: {align};
                font-size: 14px;
                font-weight: {font_weight};
                margin: 2px 8px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 0.1);
                color: #ffffff;
            }}
        """)

    def set_badge(self, count: int) -> None:
        self._badge_count = count
        self._refresh_state()
        if count > 0 and not self.isChecked():
            self.glow.setColor(QColor(255, 152, 0, 100))
            self.glow.setBlurRadius(10)
        elif count == 0 and not self.isChecked():
            self.glow.setColor(QColor(0, 0, 0, 0))
