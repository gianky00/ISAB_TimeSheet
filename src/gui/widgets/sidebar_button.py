"""SyncroJob - Sidebar Button (Premium V6 - Ultra Optimized).

Rimosso QGraphicsDropShadowEffect per garantire 60fps costanti anche su hardware datato.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PySide6.QtGui import QDrag, QPaintEvent

from PySide6.QtCore import Property, QPoint, QSequentialAnimationGroup, QSize, Qt, Signal
from PySide6.QtWidgets import QPushButton, QWidget

from src.gui.styles import COLORS
from src.gui.styles.palette_helpers import hex_to_rgba
from src.utils.helpers import get_colored_icon


class SidebarButton(QPushButton):
    """Pulsante ultra-moderno per la sidebar.

    Ottimizzato per la fluidità estrema rimuovendo gli effetti grafici costosi.

    Inizializza la classe.
    """

    text_opacity_changed = Signal(float)

    def __init__(self, text: str, icon_path: str = "", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.label_text = text
        self.icon_path = icon_path
        self._collapsed = False
        self._badge_count = 0
        self._badge_text = ""
        self._text_opacity = 1.0
        self._drag_start_pos: QPoint | None = None
        self._current_drag: QDrag | None = None

        if icon_path:
            self.setIcon(get_colored_icon(icon_path, COLORS["bg_white"]))

        self.setCheckable(True)
        self.setMinimumHeight(48)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Inizializzazione animazione di pulsazione (lampeggio novità)
        self._pulse_alpha = 0.04
        self._is_pulsing = False
        self._pulse_anim: QSequentialAnimationGroup | None = None

        # OTTIMIZZAZIONE: Rimosso QGraphicsDropShadowEffect (Glow)
        # Gli effetti grafici causano lag massivo durante il ridimensionamento della sidebar.

        self._refresh_state()
        self._set_base_style()

    def get_text_opacity(self) -> float:
        """Restituisce l'opacità del testo."""
        return self._text_opacity

    def set_text_opacity(self, value: float) -> None:
        """Imposta l'opacità del testo."""
        if self._text_opacity != value:
            self._text_opacity = value
            self.text_opacity_changed.emit(value)
            # Qui potremmo aggiornare lo stile se necessario,
            # ma solitamente questa property è usata per animazioni di dissolvenza.

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
        display_text = f"{base_text} {self._badge_text}" if self._badge_text else base_text

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

    def get_pulse_alpha(self) -> float:
        """Restituisce il valore alpha corrente della pulsazione."""
        return self._pulse_alpha

    def set_pulse_alpha(self, val: float) -> None:
        """Imposta il valore alpha corrente della pulsazione e aggiorna il widget."""
        self._pulse_alpha = val
        self.update()

    pulse_alpha = Property(float, fget=get_pulse_alpha, fset=set_pulse_alpha)

    def setChecked(self, checked: bool) -> None:
        """Sovrascrive setChecked per interrompere la pulsazione quando attivo."""
        super().setChecked(checked)
        if checked:
            self._stop_pulse()
        elif self._badge_count > 0 or self._badge_text:
            self._start_pulse()

    def _start_pulse(self) -> None:
        """Avvia l'animazione di pulsazione premium del background."""
        if self._is_pulsing:
            return
        self._is_pulsing = True

        if not self._pulse_anim:
            from PySide6.QtCore import QEasingCurve, QPropertyAnimation

            anim_group = QSequentialAnimationGroup(self)

            anim_in = QPropertyAnimation(self, b"pulse_alpha")
            anim_in.setDuration(1200)  # Tempo di salita (1.2 secondi per un effetto morbidissimo)
            anim_in.setStartValue(0.04)
            anim_in.setEndValue(0.24)
            anim_in.setEasingCurve(QEasingCurve.Type.InOutQuad)

            anim_out = QPropertyAnimation(self, b"pulse_alpha")
            anim_out.setDuration(1200)  # Tempo di discesa
            anim_out.setStartValue(0.24)
            anim_out.setEndValue(0.04)
            anim_out.setEasingCurve(QEasingCurve.Type.InOutQuad)

            anim_group.addAnimation(anim_in)
            anim_group.addAnimation(anim_out)
            anim_group.setLoopCount(-1)
            self._pulse_anim = anim_group

        if self._pulse_anim:
            self._pulse_anim.start()

    def _stop_pulse(self) -> None:
        """Interrompe l'animazione di pulsazione."""
        if not self._is_pulsing:
            return
        self._is_pulsing = False
        if self._pulse_anim:
            self._pulse_anim.stop()
        self._pulse_alpha = 0.04
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        """Esegue il rendering del pulsante con l'overlay di lampeggio premium."""
        from PySide6.QtGui import QBrush, QColor, QPainter, QPen

        if self._is_pulsing and not self.isChecked():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            # Colore arancione caldo premium per catturare lo sguardo con eleganza
            base_color = QColor(COLORS["warning_light"])
            alpha = int(self._pulse_alpha * 255)
            base_color.setAlpha(alpha)

            rect = self.rect()
            margin_x = 8
            margin_y = 2
            if self._collapsed:
                margin_x = 4
                margin_y = 2

            adjusted_rect = rect.adjusted(margin_x, margin_y, -margin_x, -margin_y)

            painter.setBrush(QBrush(base_color))

            # Disegna un bordo pulsante coerente e sottile
            border_color = QColor(COLORS["warning_light"])
            border_alpha = int(min((self._pulse_alpha + 0.15), 1.0) * 255)
            border_color.setAlpha(border_alpha)
            painter.setPen(QPen(border_color, 1))

            painter.drawRoundedRect(adjusted_rect, 8, 8)
            painter.end()

        super().paintEvent(event)

    def set_badge(self, value: int | str) -> None:
        """Imposta un badge numerico o testuale sul pulsante e controlla il lampeggio."""
        if isinstance(value, int):
            self._badge_count = value
            self._badge_text = f"({value})" if value > 0 else ""
        else:
            self._badge_text = str(value)
            self._badge_count = 1 if value else 0
        self._refresh_state()

        if self._badge_count > 0 or self._badge_text:
            self._start_pulse()
        else:
            self._stop_pulse()
