"""
SyncroJob - Sidebar Button (Premium V6 - Optimized)
Ottimizzato per la fluidità: rimosso l'uso intensivo di setStyleSheet durante le animazioni.
"""

from typing import Any

from PyQt6.QtCore import QPoint, QSize, Qt, pyqtProperty  # type: ignore[attr-defined]
from PyQt6.QtGui import QColor, QDrag
from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QPushButton, QWidget

from src.gui.styles import COLORS
from src.gui.styles.palette_helpers import hex_to_rgba
from src.utils.helpers import get_colored_icon


class SidebarButton(QPushButton):
    """
    Pulsante ultra-moderno per la sidebar.
    Ottimizzato per la visibilità su sfondi scuri gradienti e performance elevate.
    """

    def __init__(self, text: str, icon_path: str = "", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.label_text = text
        self.icon_path = icon_path
        self._collapsed = False
        self._badge_count = 0
        self._text_opacity = 1.0
        self._drag_start_pos: QPoint | None = None
        self._current_drag: QDrag | None = None

        if icon_path:
            self.setIcon(get_colored_icon(icon_path, COLORS["bg_white"]))

        self.setCheckable(True)
        self.setMinimumHeight(48)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.glow = QGraphicsDropShadowEffect(self)
        self.glow.setBlurRadius(15)
        self.glow.setColor(QColor(0, 0, 0, 0))
        self.glow.setOffset(0, 0)
        self.setGraphicsEffect(self.glow)

        self._refresh_state()
        self._set_base_style()
        self.toggled.connect(self._on_toggled)

    @pyqtProperty(float)
    def text_opacity(self) -> float:
        """Restituisce l'opacità del testo."""
        return self._text_opacity

    @text_opacity.setter  # type: ignore[no-redef]
    def text_opacity(self, value: float) -> None:
        """Imposta l'opacità del testo (senza ricaricare lo stile intero)."""
        self._text_opacity = value
        # Non chiamiamo _update_style qui per performance

    def _on_toggled(self, checked: bool) -> None:
        if checked:
            c = QColor(COLORS["teal_accent"])
            c.setAlpha(180)
            self.glow.setColor(c)
        else:
            if self._badge_count == 0:
                self.glow.setColor(QColor(0, 0, 0, 0))

    def set_collapsed(self, collapsed: bool, animated: bool = False) -> None:
        """Aggiorna lo stato visivo senza forzare ricaricamenti pesanti."""
        if self._collapsed == collapsed:
            return
        self._collapsed = collapsed
        self.setProperty("collapsed", collapsed)
        self._refresh_state()
        
        # Invece di riscrivere tutto il QSS, aggiorniamo solo le proprietà necessarie
        if style := self.style():
            style.unpolish(self)
            style.polish(self)

    def _refresh_state(self) -> None:
        """Sincronizza testo e icone."""
        base_text = f"   {self.label_text}"
        display_text = f"{base_text} ({self._badge_count})" if self._badge_count > 0 else base_text

        if self._collapsed:
            self.setText("")
            self.setIconSize(QSize(22, 22))
        else:
            self.setText(display_text)
            self.setIconSize(QSize(18, 18))

    def _set_base_style(self) -> None:
        """Imposta lo stile QSS statico con selettori di stato."""
        active_bg = hex_to_rgba(COLORS["teal_accent"], 0.25)
        hover_bg = hex_to_rgba(COLORS["bg_white"], 0.1)
        text_color = COLORS["bg_white"]
        muted_text = hex_to_rgba(COLORS["bg_white"], 0.7)

        self.setStyleSheet(f"""
            QPushButton {{
                color: {muted_text};
                background-color: transparent;
                border-radius: 8px;
                padding: 12px 15px;
                text-align: left;
                font-size: 14px;
                font-weight: 500;
                margin: 2px 8px;
                border: none;
            }}
            QPushButton[collapsed="true"] {{
                padding: 0px;
                text-align: center;
            }}
            QPushButton:checked {{
                background-color: {active_bg};
                color: {text_color};
                font-weight: 800;
            }}
            QPushButton:hover {{
                background-color: {hover_bg};
                color: {text_color};
            }}
        """)

    def set_badge(self, count: int) -> None:
        """Imposta un badge numerico sul pulsante."""
        self._badge_count = count
        self._refresh_state()
        if count > 0 and not self.isChecked():
            self.glow.setColor(QColor(255, 152, 0, 100))
            self.glow.setBlurRadius(10)
        elif count == 0 and not self.isChecked():
            self.glow.setColor(QColor(0, 0, 0, 0))
