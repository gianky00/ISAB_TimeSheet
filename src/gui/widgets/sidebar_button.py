"""
SyncroJob - Sidebar Button (Premium V6 - Ultra Optimized)
Rimosso QGraphicsDropShadowEffect per garantire 60fps costanti anche su hardware datato.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PySide6.QtGui import QDrag

from PySide6.QtCore import Property, QPoint, QSize, Qt, Signal
from PySide6.QtWidgets import QPushButton, QWidget

from src.gui.styles import COLORS
from src.gui.styles.palette_helpers import hex_to_rgba
from src.utils.helpers import get_colored_icon


class SidebarButton(QPushButton):
    """
    Pulsante ultra-moderno per la sidebar.
    Ottimizzato per la fluidit  estrema rimuovendo gli effetti grafici costosi.
    """

    text_opacity_changed = Signal(float)

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

        # OTTIMIZZAZIONE: Rimosso QGraphicsDropShadowEffect (Glow)
        # Gli effetti grafici causano lag massivo durante il ridimensionamento della sidebar.

        self._refresh_state()
        self._set_base_style()

    def get_text_opacity(self) -> float:
        """Restituisce l'opacit  del testo."""
        return self._text_opacity

    def set_text_opacity(self, value: float) -> None:
        """Imposta l'opacit  del testo."""
        if self._text_opacity != value:
            self._text_opacity = value
            self.text_opacity_changed.emit(value)
            # Qui potremmo aggiornare lo stile se necessario,
            # ma solitamente questa property  usata per animazioni di dissolvenza.

    text_opacity = Property(float, fget=get_text_opacity, fset=set_text_opacity, notify=text_opacity_changed)

    def set_collapsed(self, collapsed: bool, animated: bool = False) -> None:
        """Aggiorna lo stato visivo senza forzare ricaricamenti pesanti."""
        if self._collapsed == collapsed:
            return
        self._collapsed = collapsed
        self.setProperty("collapsed", collapsed)
        self._refresh_state()

        if style := self.style():
            style.unpolish(self)
            style.polish(self)

    def _refresh_state(self) -> None:
        """Sincronizza testo e icone."""
        base_text = f"  {self.label_text}"
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
        # Usiamo un bordo invece del glow per indicare lo stato attivo senza pesare sulla GPU
        active_border = f"1px solid {hex_to_rgba(COLORS['teal_accent'], 0.5)}"
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
        border: 1px solid transparent;
      }}
      QPushButton[collapsed="true"] {{
        padding: 0px;
        text-align: center;
        margin: 2px 4px;
      }}
      QPushButton:checked {{
        background-color: {active_bg};
        border: {active_border};
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
