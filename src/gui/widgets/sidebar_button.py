"""
SyncroJob - Sidebar Button (Premium)
Pulsante avanzato con supporto per Glassmorphism, Glow effect e animazioni di stato.
"""

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QPushButton, QWidget

from src.utils.helpers import get_colored_icon


class SidebarButton(QPushButton):
    """
    Pulsante d'élite per la sidebar.
    Integra effetti di luce e animazioni per comunicare lo stato dell'app.
    """

    def __init__(self, text: str, icon_path: str = "", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.label_text = text
        self.icon_path = icon_path
        self._collapsed = False
        self._badge_count = 0

        if icon_path:
            self.setIcon(get_colored_icon(icon_path, "#ffffff"))

        self.setCheckable(True)
        self.setMinimumHeight(48)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Effetto Glow (Bagliore)
        self.glow = QGraphicsDropShadowEffect(self)
        self.glow.setBlurRadius(15)
        self.glow.setColor(QColor(0, 150, 136, 0))
        self.glow.setOffset(0, 0)
        self.setGraphicsEffect(self.glow)

        self._refresh_state()
        self._update_style()
        self.toggled.connect(self._on_toggled)

    def _on_toggled(self, checked: bool) -> None:
        if checked:
            self.glow.setColor(QColor(0, 150, 136, 180)) # Teal glow
        else:
            if self._badge_count == 0:
                self.glow.setColor(QColor(0, 150, 136, 0))
        self._update_style()

    def set_collapsed(self, collapsed: bool) -> None:
        self._collapsed = collapsed
        self._refresh_state()
        self._update_style()

    def _refresh_state(self) -> None:
        base_text = f"   {self.label_text}"
        display_text = f"{base_text} ({self._badge_count})" if self._badge_count > 0 else base_text

        if self._collapsed:
            self.setText("")
            self.setIconSize(QSize(22, 22))
            tooltip = self.label_text
            if self._badge_count > 0:
                tooltip += f" ({self._badge_count} notifiche)"
            self.setToolTip(tooltip)
        else:
            self.setText(display_text)
            self.setIconSize(QSize(18, 18))
            self.setToolTip("")

    def set_badge(self, count: int) -> None:
        self._badge_count = count
        self._refresh_state()
        if count > 0 and not self.isChecked():
            self.glow.setColor(QColor(255, 152, 0, 100)) # Orange soft glow
            self.glow.setBlurRadius(10)
        elif count == 0 and not self.isChecked():
            self.glow.setColor(QColor(0, 0, 0, 0))

    def set_status_glow(self, active: bool, color: str = "#009688"):
        if active:
            self.glow.setColor(QColor(color))
            self.glow.setBlurRadius(20)
        else:
            self._on_toggled(self.isChecked())

    def _update_style(self) -> None:
        align = "center" if self._collapsed else "left"
        padding = "0px" if self._collapsed else "12px 15px"

        # Sfondo premium per selezione
        bg_color = "rgba(255, 255, 255, 0.12)" if self.isChecked() else "transparent"
        text_color = "#ffffff" if self.isChecked() else "rgba(255, 255, 255, 0.65)"
        font_weight = "700" if self.isChecked() else "500"

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
                background-color: rgba(255, 255, 255, 0.08);
                color: #ffffff;
            }}
        """)
