"""
SyncroJob - UI Effects Manager
Centralizza la gestione delle animazioni e degli effetti visivi (Shadows, Fades, Slides).
"""

from typing import Any

from PySide6.QtCore import QEasingCurve, QPropertyAnimation
from PySide6.QtWidgets import QGraphicsDropShadowEffect, QWidget


class UIEffectsManager:
    """Manager centralizzato per effetti UI moderni."""

    @staticmethod
    def apply_shadow(widget: QWidget, blur: int = 15, color: str = "#20000000") -> None:
        """Applica un'ombra morbida a un widget."""
        shadow = QGraphicsDropShadowEffect(widget)
        shadow.setBlurRadius(blur)
        shadow.setOffset(0, 3)
        # hex_to_rgba non è disponibile qui, usiamo stringa diretta per ora
        shadow.setColor(color)
        widget.setGraphicsEffect(shadow)

    @staticmethod
    def animate_fade(widget: QWidget, duration: int = 300) -> None:
        """Animazione di dissolvenza in entrata."""
        anim = QPropertyAnimation(widget, b"windowOpacity")
        anim.setDuration(duration)
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        anim.start()

    @staticmethod
    def animate_geometry(widget: QWidget, start_rect: Any, end_rect: Any, duration: int = 400) -> None:
        """Animazione slide di un widget."""
        anim = QPropertyAnimation(widget, b"geometry")
        anim.setDuration(duration)
        anim.setStartValue(start_rect)
        anim.setEndValue(end_rect)
        anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        anim.start()
