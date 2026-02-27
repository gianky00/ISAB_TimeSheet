"""
SyncroJob - Modern Card Widget
Un contenitore elegante con ombre morbide, angoli arrotondati e animazioni hover.
"""

from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QFrame, QGraphicsDropShadowEffect, QVBoxLayout, QWidget

from src.gui.styles import COLORS


class ModernCard(QFrame):
    """
    Una card moderna che gestisce automaticamente l'elevazione (ombra) e 
    gli effetti visivi quando l'utente ci passa sopra col mouse.
    """

    def __init__(self, parent: QWidget | None = None, elevation: int = 15) -> None:
        super().__init__(parent)
        self.elevation = elevation
        self._setup_base_style()
        self._setup_shadow()

    def _setup_base_style(self) -> None:
        self.setObjectName("modernCard")
        self.setStyleSheet(f"""
            QFrame#modernCard {{
                background-color: {COLORS["bg_white"]};
                border: 1px solid {COLORS["border_light"]};
                border-radius: 12px;
            }}
        """)

    def _setup_shadow(self) -> None:
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(self.elevation)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(4)
        self.shadow.setColor(QColor(0, 0, 0, 30))
        self.setGraphicsEffect(self.shadow)

        # Animazione per l'ombra (effetto sollevamento)
        self.shadow_anim = QPropertyAnimation(self.shadow, b"blurRadius")
        self.shadow_anim.setDuration(200)
        self.shadow_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def enterEvent(self, event) -> None:
        self.shadow_anim.setEndValue(self.elevation + 10)
        self.shadow_anim.start()
        self.setStyleSheet(f"""
            QFrame#modernCard {{
                background-color: {COLORS["bg_white"]};
                border: 1px solid {COLORS["primary_blue"]};
                border-radius: 12px;
            }}
        """)
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        self.shadow_anim.setEndValue(self.elevation)
        self.shadow_anim.start()
        self._setup_base_style()
        super().leaveEvent(event)


class ModernContentCard(ModernCard):
    """Card che include già un layout per i contenuti."""
    def __init__(self, parent: QWidget | None = None, elevation: int = 15) -> None:
        super().__init__(parent, elevation)
        self.content_layout = QVBoxLayout(self)
        self.content_layout.setContentsMargins(15, 15, 15, 15)
        self.content_layout.setSpacing(10)

    def addWidget(self, widget: QWidget) -> None:
        self.content_layout.addWidget(widget)
