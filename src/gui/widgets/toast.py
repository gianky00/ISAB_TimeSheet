"""
Sistema di notifiche toast non-blocking.
"""
from PyQt6.QtWidgets import QLabel, QWidget, QHBoxLayout, QGraphicsOpacityEffect, QApplication
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QPoint
from ..design.colors import get_palette
from ..design.spacing import BorderRadius

class Toast(QWidget):
    """Notifica toast animata."""

    class Type:
        INFO = "info"
        SUCCESS = "success"
        WARNING = "warning"
        ERROR = "error"

    TYPE_CONFIG = {
        Type.INFO: ("ℹ️", "info"),
        Type.SUCCESS: ("✅", "success"),
        Type.WARNING: ("⚠️", "warning"),
        Type.ERROR: ("❌", "error"),
    }

    def __init__(self, message: str, toast_type: str = Type.INFO, duration: int = 3000, parent=None):
        super().__init__(parent)
        self._duration = duration
        self._type = toast_type
        self._palette = get_palette()

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self._setup_ui(message)
        self._setup_animation()

    def _setup_ui(self, message: str):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)

        icon, color_key = self.TYPE_CONFIG.get(self._type, self.TYPE_CONFIG[self.Type.INFO])
        accent = getattr(self._palette, color_key, self._palette.info)

        # Container
        self.setStyleSheet(f"""
            Toast {{
                background-color: {self._palette.surface};
                border: 1px solid {self._palette.border};
                border-left: 4px solid {accent};
                border-radius: {BorderRadius.md}px;
            }}
        """)

        # Icon
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 18px; border: none; background: transparent;")
        layout.addWidget(icon_label)

        # Message
        msg_label = QLabel(message)
        msg_label.setStyleSheet(f"""
            color: {self._palette.on_surface};
            font-size: 14px;
            border: none;
            background: transparent;
        """)
        layout.addWidget(msg_label)

        self.adjustSize()

    def _setup_animation(self):
        # Opacity effect
        self._opacity = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self._opacity)

        # Fade in animation
        self._fade_in = QPropertyAnimation(self._opacity, b"opacity")
        self._fade_in.setDuration(200)
        self._fade_in.setStartValue(0.0)
        self._fade_in.setEndValue(1.0)

        # Fade out animation
        self._fade_out = QPropertyAnimation(self._opacity, b"opacity")
        self._fade_out.setDuration(300)
        self._fade_out.setStartValue(1.0)
        self._fade_out.setEndValue(0.0)
        self._fade_out.finished.connect(self.deleteLater)

    def show_at(self, x: int, y: int):
        """Mostra toast in posizione specifica."""
        self.move(x, y)
        self.show()
        self._fade_in.start()

        # Auto-hide
        QTimer.singleShot(self._duration, self._fade_out.start)

class ToastManager:
    """Gestisce posizionamento e stacking toast."""

    _instance = None
    _active_toasts = []

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def show(self, message: str, toast_type: str = Toast.Type.INFO, duration: int = 3000):
        """Mostra un toast."""

        parent = QApplication.activeWindow()
        toast = Toast(message, toast_type, duration, parent)

        # Clean up closed toasts from list
        self._active_toasts = [t for t in self._active_toasts if t.isVisible()]

        # Posiziona in basso a destra
        if parent:
            # Map parent geometry to global
            geo = parent.geometry()
            x = geo.x() + geo.width() - toast.width() - 20
            # Stack upwards
            offset_y = sum([t.height() + 10 for t in self._active_toasts])
            y = geo.y() + geo.height() - toast.height() - 20 - offset_y
        else:
            screen = QApplication.primaryScreen().geometry()
            x = screen.width() - toast.width() - 20
            offset_y = sum([t.height() + 10 for t in self._active_toasts])
            y = screen.height() - toast.height() - 60 - offset_y

        self._active_toasts.append(toast)
        # Remove from list when destroyed
        toast.destroyed.connect(lambda: self._active_toasts.remove(toast) if toast in self._active_toasts else None)

        toast.show_at(x, y)

# Funzioni helper globali
def toast_info(message: str, duration: int = 3000):
    ToastManager.instance().show(message, Toast.Type.INFO, duration)

def toast_success(message: str, duration: int = 3000):
    ToastManager.instance().show(message, Toast.Type.SUCCESS, duration)

def toast_warning(message: str, duration: int = 3000):
    ToastManager.instance().show(message, Toast.Type.WARNING, duration)

def toast_error(message: str, duration: int = 5000):
    ToastManager.instance().show(message, Toast.Type.ERROR, duration)
