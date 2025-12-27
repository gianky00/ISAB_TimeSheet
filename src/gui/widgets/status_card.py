"""
Card per visualizzare stato con icona e animazioni.
"""
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QPropertyAnimation, pyqtProperty
from ..design.colors import get_palette
from ..design.spacing import Spacing, BorderRadius

class StatusCard(QFrame):
    """Card per mostrare stato operazione."""

    class Status:
        IDLE = "idle"
        RUNNING = "running"
        SUCCESS = "success"
        ERROR = "error"
        WARNING = "warning"

    STATUS_CONFIG = {
        Status.IDLE: ("⏸️", "In attesa", "secondary"),
        Status.RUNNING: ("⏳", "In esecuzione...", "info"),
        Status.SUCCESS: ("✅", "Completato", "success"),
        Status.ERROR: ("❌", "Errore", "error"),
        Status.WARNING: ("⚠️", "Attenzione", "warning"),
    }

    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)
        self._status = self.Status.IDLE
        self._palette = get_palette()
        self._pulse_opacity = 1.0

        self._setup_ui(title)
        self._setup_animation()
        self._apply_style()

    def _setup_ui(self, title: str):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(Spacing.md, Spacing.md, Spacing.md, Spacing.md)
        layout.setSpacing(Spacing.sm)

        # Icon
        self._icon_label = QLabel()
        self._icon_label.setFixedSize(32, 32)
        self._icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._icon_label.setStyleSheet("font-size: 20px; border: none; background: transparent;")
        layout.addWidget(self._icon_label)

        # Text container
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)

        self._title_label = QLabel(title)
        self._title_label.setStyleSheet(f"font-weight: 600; font-size: 14px; color: {self._palette.on_surface}; border: none; background: transparent;")

        self._status_label = QLabel()
        self._status_label.setStyleSheet(f"font-size: 12px; color: {self._palette.on_surface}; opacity: 0.7; border: none; background: transparent;")

        text_layout.addWidget(self._title_label)
        text_layout.addWidget(self._status_label)
        layout.addLayout(text_layout, 1)

        self._update_status_display()

    def _setup_animation(self):
        self._pulse_anim = QPropertyAnimation(self, b"pulseOpacity")
        self._pulse_anim.setDuration(1000)
        self._pulse_anim.setLoopCount(-1)  # Infinite
        self._pulse_anim.setStartValue(1.0)
        self._pulse_anim.setEndValue(0.5)

    @pyqtProperty(float)
    def pulseOpacity(self):
        return self._pulse_opacity

    @pulseOpacity.setter
    def pulseOpacity(self, value):
        self._pulse_opacity = value
        # Update just the icon opacity via stylesheet would be expensive,
        # so we trigger a repaint or set style on icon only if needed.
        # For simplicity, we just change window opacity or icon opacity style.
        # Changing QFrame opacity affects everything.
        # Let's change border-left color alpha or something.
        # Actually, let's just re-apply style with alpha if running.
        pass # Optimization: don't heavy re-style on loop.
        # Ideally we would use QGraphicsOpacityEffect on the icon.


    def setStatus(self, status: str, message: str = None):
        """Imposta lo stato della card."""
        self._status = status
        self._update_status_display(message)

        if status == self.Status.RUNNING:
            self._pulse_anim.start()
        else:
            self._pulse_anim.stop()
            self._pulse_opacity = 1.0

    def _update_status_display(self, custom_message: str = None):
        icon, default_msg, color_key = self.STATUS_CONFIG.get(
            self._status, self.STATUS_CONFIG[self.Status.IDLE]
        )
        self._icon_label.setText(icon)
        self._status_label.setText(custom_message or default_msg)
        self._apply_style()

    def _apply_style(self):
        _, _, color_key = self.STATUS_CONFIG.get(
            self._status, self.STATUS_CONFIG[self.Status.IDLE]
        )

        accent = getattr(self._palette, color_key, self._palette.primary)

        self.setStyleSheet(f"""
            StatusCard {{
                background-color: {self._palette.surface};
                border: 1px solid {self._palette.border};
                border-left: 4px solid {accent};
                border-radius: {BorderRadius.md}px;
            }}
        """)
