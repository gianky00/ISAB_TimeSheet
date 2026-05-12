"""
SyncroJob - Shimmer Widget (Skeleton Loading)
Effetto pulsante per indicare il caricamento dei dati in modo elegante.
"""

from PySide6.QtCore import QEasingCurve, QPropertyAnimation
from PySide6.QtWidgets import QFrame, QGraphicsOpacityEffect, QVBoxLayout, QWidget

from src.gui.styles import COLORS


class ShimmerItem(QFrame):
    """Un singolo rettangolo pulsante che simula un contenuto in caricamento."""

    def __init__(self, height: int = 20, width: int | None = None, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        if width:
            self.setFixedWidth(width)
        self.setFixedHeight(height)
        self.setStyleSheet(f"""
      QFrame {{
        background-color: {COLORS["bg_hover"]};
        border-radius: {height // 2}px;
      }}
    """)

        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)

        self.anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim.setDuration(800)
        self.anim.setStartValue(0.3)
        self.anim.setEndValue(0.7)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.anim.setLoopCount(-1)
        self.anim.start()


class ShimmerSkeleton(QWidget):
    """Un set di ShimmerItem che simula una card o una riga di tabella."""

    def __init__(self, rows: int = 3, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        for _ in range(rows):
            layout.addWidget(ShimmerItem(height=15))
            layout.addWidget(ShimmerItem(height=15, width=200))
            layout.addSpacing(10)

        layout.addStretch()
