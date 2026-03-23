"""
PriorityBadge - Badge component per visualizzare la priorità di una notifica.
Supporta High (con pulse animation), Medium e Low.
"""

from typing import Any, ClassVar

from PyQt6.QtCore import QVariantAnimation, pyqtProperty  # type: ignore[attr-defined]
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QWidget

from src.gui.styles import COLORS


class PriorityBadge(QWidget):
    """
    Badge per priorità notifica con indicatore colorato e pulse animation.

    Levels:
    - high: Red dot + "Alta" label + pulse animation
    - medium: Orange dot + "Media" label
    - low: Green dot (no label, minimal)
    """

    # Color mapping
    PRIORITY_COLORS: ClassVar[dict[str, str]] = {
        "high": COLORS["error_red"],  # Red
        "medium": COLORS["warning_orange"],  # Orange
        "low": COLORS["success_dark"],  # Green
    }

    def __init__(self, priority: str = "low", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.priority = priority.lower()
        self._pulse_scale = 1.0
        self._setup_ui()

        # Start pulse animation for high priority
        if self.priority == "high":
            self._setup_pulse_animation()

    def _setup_ui(self) -> None:
        """Setup layout and components."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        # Color dot
        color = self.PRIORITY_COLORS.get(self.priority, self.PRIORITY_COLORS["low"])

        self.dot = QLabel()
        self.dot.setFixedSize(8, 8)
        self.dot.setStyleSheet(
            f"""
            QLabel {{
                background-color: {color};
                border-radius: 4px;
                border: none;
            }}
        """
        )
        layout.addWidget(self.dot)

        # Label (only for high and medium)
        if self.priority in ("high", "medium"):
            label_text = "Alta" if self.priority == "high" else "Media"
            self.label = QLabel(label_text)
            self.label.setStyleSheet(
                f"""
                QLabel {{
                    color: {color};
                    font-size: 11px;
                    font-weight: 700;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                    border: none;
                    background: transparent;
                }}
            """
            )
            layout.addWidget(self.label)

    def _setup_pulse_animation(self) -> None:
        """Setup pulse animation for high priority badge."""
        self.pulse_anim = QVariantAnimation(self)
        self.pulse_anim.setStartValue(1.0)
        self.pulse_anim.setKeyValueAt(0.5, 1.3)  # Scale up to 1.3x at midpoint
        self.pulse_anim.setEndValue(1.0)
        self.pulse_anim.setDuration(1000)  # 1 second per pulse
        self.pulse_anim.setLoopCount(-1)  # Infinite loop

        self.pulse_anim.valueChanged.connect(self._on_pulse_value_changed)
        self.pulse_anim.start()

    def _on_pulse_value_changed(self, value: Any) -> None:  # noqa: ANN401
        """Apply pulse scale to dot."""
        f_value = float(value)
        self._pulse_scale = f_value
        # Apply scale transformation to dot
        size = int(8 * f_value)
        self.dot.setFixedSize(size, size)

    def get_pulse_scale(self) -> float:
        """Get current pulse scale value."""
        return self._pulse_scale

    def set_pulse_scale(self, value: float) -> None:
        """Set pulse scale value."""
        self._pulse_scale = value
        size = int(8 * value)
        self.dot.setFixedSize(size, size)

    pulseScale = pyqtProperty(float, fget=get_pulse_scale, fset=set_pulse_scale)  # noqa: N815
