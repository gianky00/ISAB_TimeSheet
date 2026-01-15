"""
Sistema di notifiche toast non-blocking.
"""

from PyQt6.QtCore import QPropertyAnimation, Qt, QTimer
from PyQt6.QtWidgets import (
    QApplication,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QLabel,
    QWidget,
)

from ..design.colors import get_palette
from ..design.spacing import BorderRadius


class Toast(QWidget):
    """Notifica toast animata non bloccante."""

    class Type:
        """Costanti per il tipo di notifica."""

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

    def __init__(
        self,
        message: str,
        toast_type: str = Type.INFO,
        duration: int = 3000,
        parent=None,
    ):
        """
        Inizializza il toast.

        Args:
            message: Il messaggio da visualizzare.
            toast_type: Tipo di toast (info, success, warning, error).
            duration: Durata della visualizzazione in millisecondi.
            parent: Widget genitore.
        """
        super().__init__(parent)
        self._duration = duration
        self._type = toast_type
        self._palette = get_palette()

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self._setup_ui(message)
        self._setup_animation()

    def _setup_ui(self, message: str):
        """Configura l'interfaccia utente del toast con icone e colori."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)

        icon, color_key = self.TYPE_CONFIG.get(
            self._type, self.TYPE_CONFIG[self.Type.INFO]
        )
        accent = getattr(self._palette, color_key, self._palette.info)

        # Container
        self.setStyleSheet(
            f"""
            Toast {{
                background-color: {self._palette.surface};
                border: 1px solid {self._palette.border};
                border-left: 4px solid {accent};
                border-radius: {BorderRadius.md}px;
            }}
        """
        )

        # Icon
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(
            "font-size: 18px; border: none; background: transparent;"
        )
        layout.addWidget(icon_label)

        # Message
        msg_label = QLabel(message)
        msg_label.setStyleSheet(
            f"""
            color: {self._palette.on_surface};
            font-size: 14px;
            border: none;
            background: transparent;
        """
        )
        layout.addWidget(msg_label)

        self.adjustSize()

    def _setup_animation(self):
        """Configura le animazioni di fade-in e fade-out."""
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
        """
        Visualizza il toast in una posizione specifica e avvia il timer di auto-chiusura.

        Args:
            x: Coordinata X globale.
            y: Coordinata Y globale.
        """
        self.move(x, y)
        self.show()
        self._fade_in.start()

        # Auto-hide
        QTimer.singleShot(self._duration, self._fade_out.start)


class ToastManager:
    """
    Singleton per la gestione del posizionamento e dello stacking dei toast.
    Assicura che i toast multipli non si sovrappongano.
    """

    _instance = None
    _active_toasts: list[Toast] = []

    @classmethod
    def instance(cls):
        """Restituisce l'istanza singleton di ToastManager."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def show(
        self, message: str, toast_type: str = Toast.Type.INFO, duration: int = 3000
    ):
        """
        Crea e visualizza un nuovo toast, calcolando la posizione corretta nello stack.

        Args:
            message: Messaggio da mostrare.
            toast_type: Tipo di notifica.
            duration: Durata in ms.
        """

        parent = QApplication.activeWindow()
        toast = Toast(message, toast_type, duration, parent)

        # Clean up closed toasts from list
        self._active_toasts = [t for t in self._active_toasts if t.isVisible()]

        # Posiziona in ALTO CENTRALE
        if parent:
            # Map parent geometry to global
            geo = parent.geometry()
            x = geo.x() + (geo.width() - toast.width()) // 2
            # Stack downwards
            offset_y = sum([t.height() + 10 for t in self._active_toasts])
            y = geo.y() + 80 + offset_y  # Margine dall'alto (sotto header)
        else:
            primary_screen = QApplication.primaryScreen()
            if primary_screen:
                screen = primary_screen.geometry()
                x = (screen.width() - toast.width()) // 2
                offset_y = sum([t.height() + 10 for t in self._active_toasts])
                y = 80 + offset_y
            else:
                x, y = 0, 0  # Fallback

        self._active_toasts.append(toast)
        # Remove from list when destroyed
        toast.destroyed.connect(
            lambda: self._active_toasts.remove(toast)
            if toast in self._active_toasts
            else None
        )

        toast.show_at(x, y)


# Funzioni helper globali
def toast_info(message: str, duration: int = 3000):
    """Visualizza un toast informativo."""
    ToastManager.instance().show(message, Toast.Type.INFO, duration)


def toast_success(message: str, duration: int = 3000):
    """Visualizza un toast di successo."""
    ToastManager.instance().show(message, Toast.Type.SUCCESS, duration)


def toast_warning(message: str, duration: int = 3000):
    """Visualizza un toast di avviso."""
    ToastManager.instance().show(message, Toast.Type.WARNING, duration)


def toast_error(message: str, duration: int = 5000):
    """Visualizza un toast di errore."""
    ToastManager.instance().show(message, Toast.Type.ERROR, duration)
