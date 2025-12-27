"""
Pulsante moderno con varianti e stati.
"""
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, pyqtProperty
from ..design.colors import get_palette

class ModernButton(QPushButton):
    """Pulsante con animazioni e varianti."""

    class Variant:
        PRIMARY = "primary"
        SECONDARY = "secondary"
        SUCCESS = "success"
        DANGER = "danger"
        GHOST = "ghost"

    class Size:
        SMALL = "small"
        MEDIUM = "medium"
        LARGE = "large"

    def __init__(
        self,
        text: str = "",
        variant: str = Variant.PRIMARY,
        size: str = Size.MEDIUM,
        icon: str = None,
        parent=None
    ):
        super().__init__(text, parent)
        self._variant = variant
        self._size = size
        self._palette = get_palette()
        self._hover_opacity = 0.0

        self._setup_animation()
        self._apply_style()

        if icon:
            from PyQt6.QtGui import QIcon
            self.setIcon(QIcon(icon))
            # Increase padding for icon
            self.setStyleSheet(self.styleSheet() + "QPushButton { padding-left: 32px; text-align: left; }")


    def _setup_animation(self):
        self._anim = QPropertyAnimation(self, b"hoverOpacity")
        self._anim.setDuration(150)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    @pyqtProperty(float)
    def hoverOpacity(self):
        return self._hover_opacity

    @hoverOpacity.setter
    def hoverOpacity(self, value):
        self._hover_opacity = value
        self._apply_style()

    def enterEvent(self, event):
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(0.1)
        self._anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._anim.setStartValue(0.1)
        self._anim.setEndValue(0.0)
        self._anim.start()
        super().leaveEvent(event)

    def _get_colors(self):
        p = self._palette
        colors = {
            self.Variant.PRIMARY: (p.primary, p.on_primary),
            self.Variant.SECONDARY: (p.secondary, p.on_secondary),
            self.Variant.SUCCESS: (p.success, "#FFFFFF"),
            self.Variant.DANGER: (p.error, "#FFFFFF"),
            self.Variant.GHOST: ("transparent", p.primary),
        }
        return colors.get(self._variant, (p.primary, p.on_primary))

    def _get_size_styles(self):
        sizes = {
            self.Size.SMALL: ("8px 12px", "12px"),
            self.Size.MEDIUM: ("10px 20px", "14px"),
            self.Size.LARGE: ("14px 28px", "16px"),
        }
        return sizes.get(self._size, sizes[self.Size.MEDIUM])

    def _apply_style(self):
        bg_color, text_color = self._get_colors()
        padding, font_size = self._get_size_styles()

        # Calcola colore hover
        hover_overlay = f"rgba(255,255,255,{self._hover_opacity})"

        style = f"""
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                border: none;
                padding: {padding};
                font-size: {font_size};
                font-weight: 600;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 {hover_overlay},
                    stop:1 {bg_color}
                );
            }}
            QPushButton:pressed {{
                padding-top: 12px;
            }}
            QPushButton:disabled {{
                background-color: {self._palette.disabled};
                color: {self._palette.on_surface};
            }}
            QPushButton:focus {{
                outline: 2px solid {self._palette.focus};
                outline-offset: 2px;
            }}
        """
        # If ghost, add border
        if self._variant == self.Variant.GHOST:
            style += f"QPushButton {{ border: 1px solid {self._palette.primary}; }}"

        self.setStyleSheet(style)
