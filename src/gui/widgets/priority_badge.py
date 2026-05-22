"""Priority Badge Widget.

=====================
Badge animato che mostra un punto pulsante con intensità variabile.
"""

import contextlib
from typing import Any, ClassVar

from PySide6.QtCore import Property, QPropertyAnimation, Signal
from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget

from src.gui.styles import COLORS


class PriorityBadge(QWidget):
    """Badge circolare con animazione di pulsazione (glow)."""

    pulse_scale_changed = Signal(float)

    COLOR_MAP: ClassVar[dict[str, str]] = {
        "alta": COLORS["error_red"],
        "media": COLORS["warning_orange"],
        "bassa": COLORS["info_blue"],
        "completato": COLORS["success_green"],
    }

    def __init__(self, priority: str = "media", parent: QWidget | None = None) -> None:
        """Inizializza la classe."""
        super().__init__(parent)
        self.priority = priority.lower()
        self._pulse_scale = 1.0
        self._setup_ui()
        self._setup_animation()

    def _setup_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.dot = QLabel()
        color = self.COLOR_MAP.get(self.priority, COLORS["info_blue"])
        self.dot.setStyleSheet(
            f"background-color: {color}; border-radius: 4px; min-width: 8px; min-height: 8px;"
        )
        self.dot.setFixedSize(8, 8)
        layout.addWidget(self.dot)

    def _setup_animation(self) -> None:
        self.anim = QPropertyAnimation(self, b"pulse_scale")
        self.anim.setDuration(1200)
        self.anim.setStartValue(0.6)
        self.anim.setEndValue(1.1)
        self.anim.setLoopCount(-1)
        self.anim.start()

    def set_priority(self, priority: str) -> None:
        """Aggiorna il colore del badge in base alla priorità."""
        self.priority = priority.lower()
        color = self.COLOR_MAP.get(self.priority, COLORS["info_blue"])
        self.dot.setStyleSheet(
            f"background-color: {color}; border-radius: 4px; min-width: 8px; min-height: 8px;"
        )

    def stop_animation(self) -> None:
        """Ferma l'animazione in modo sicuro."""
        if hasattr(self, "anim") and self.anim:
            self.anim.stop()

    def hideEvent(self, event: Any) -> None:
        """Spegne l'animazione quando il widget non è visibile per risparmiare CPU."""
        self.stop_animation()
        super().hideEvent(event)

    def showEvent(self, event: Any) -> None:
        """Riprende l'animazione quando torna visibile."""
        if hasattr(self, "anim") and self.anim:
            self.anim.start()
        super().showEvent(event)

    def closeEvent(self, event: Any) -> None:
        """Cleanup finale."""
        self.stop_animation()
        super().closeEvent(event)

    def get_pulse_scale(self) -> float:
        """Getter per la scala di pulsazione."""
        return self._pulse_scale

    def set_pulse_scale(self, value: float) -> None:
        """Setter per la scala di pulsazione (usato dall'animazione)."""
        if self._pulse_scale != value:
            self._pulse_scale = value
            self.pulse_scale_changed.emit(value)
            # Applichiamo un effetto di ridimensionamento minimo o opacità
            with contextlib.suppress(Exception):
                if hasattr(self.dot, "setOpacity"):
                    self.dot.setOpacity(value)

            # In alternativa cambiamo la size
            size = int(8 * value)
            self.dot.setFixedSize(size, size)

    pulse_scale = Property(float, fget=get_pulse_scale, fset=set_pulse_scale, notify=pulse_scale_changed)
