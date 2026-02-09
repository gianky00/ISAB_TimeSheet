"""
Sistema di notifiche toast non-blocking con supporto hover e tempi differenziati.
"""

from typing import Any, ClassVar, Optional

from PyQt6.QtCore import (
    QEasingCurve,
    QObject,
    QPropertyAnimation,
    QSize,
    Qt,
    QTimer,
    QVariantAnimation,
)
from PyQt6.QtGui import QEnterEvent
from PyQt6.QtWidgets import (
    QApplication,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.utils.helpers import get_asset_path, get_colored_icon

from ..design.colors import get_palette
from ..design.spacing import BorderRadius


class Toast(QWidget):
    """Notifica toast animata non bloccante con supporto pausa al passaggio del mouse."""

    class Type:
        """Costanti per il tipo di notifica."""

        INFO = "info"
        SUCCESS = "success"
        WARNING = "warning"
        ERROR = "error"

    TYPE_CONFIG: ClassVar[dict[str, tuple[str, str]]] = {
        Type.INFO: (Icons.HELP, "info"),
        Type.SUCCESS: (Icons.CHECK_CIRCLE, "success"),
        Type.WARNING: (Icons.ALERT, "warning"),
        Type.ERROR: (Icons.X_CIRCLE, "error"),
    }

    def __init__(
        self,
        message: str,
        toast_type: str = Type.INFO,
        duration: int = 3000,
        pulse: bool = False,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._duration = duration
        self._type = toast_type
        self._pulse = pulse
        self._palette = get_palette()
        self._original_container_size: QSize | None = None

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Abilita il tracking del mouse per l'hover
        self.setMouseTracking(True)

        self._setup_ui(message)
        self._setup_animation()

        # Timer di chiusura persistente per permettere pausa/riavvio
        self._hide_timer = QTimer(self)
        self._hide_timer.setSingleShot(True)
        self._hide_timer.timeout.connect(self._fade_out.start)

    def _setup_ui(self, message: str) -> None:
        """Configura l'interfaccia utente del toast con icone e colori."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)

        self.container = QWidget()
        container_layout = QHBoxLayout(self.container)
        container_layout.setContentsMargins(16, 12, 16, 12)

        icon_path, color_key = self.TYPE_CONFIG.get(self._type, self.TYPE_CONFIG[self.Type.INFO])
        accent = getattr(self._palette, color_key, self._palette.info)

        self.container.setStyleSheet(
            f"""
            QWidget {{
                background-color: {self._palette.surface};
                border: 1px solid {self._palette.border};
                border-left: 4px solid {accent};
                border-radius: {BorderRadius.md}px;
            }}
        """
        )

        icon_label = QLabel()
        icon = get_colored_icon(get_asset_path(icon_path), "#000000")
        icon_label.setPixmap(icon.pixmap(QSize(20, 20)))
        icon_label.setStyleSheet("border: none; background: transparent;")
        container_layout.addWidget(icon_label)

        msg_label = QLabel(message)
        msg_label.setStyleSheet(
            f"""
            color: {self._palette.on_surface};
            font-size: 14px;
            border: none;
            background: transparent;
        """
        )
        container_layout.addWidget(msg_label)

        main_layout.addWidget(self.container)
        self.adjustSize()

    def _setup_animation(self) -> None:
        """Configura le animazioni di fade-in e fade-out."""
        self._opacity = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self._opacity)

        self._fade_in = QPropertyAnimation(self._opacity, b"opacity")
        self._fade_in.setDuration(200)
        self._fade_in.setStartValue(0.0)
        self._fade_in.setEndValue(1.0)

        self._fade_out = QPropertyAnimation(self._opacity, b"opacity")
        self._fade_out.setDuration(300)
        self._fade_out.setStartValue(1.0)
        self._fade_out.setEndValue(0.0)
        self._fade_out.finished.connect(self.deleteLater)

        if self._pulse:
            self._pulse_anim = QVariantAnimation(self)
            self._pulse_anim.setDuration(800)
            self._pulse_anim.setStartValue(1.0)
            self._pulse_anim.setKeyValueAt(0.5, 1.05)
            self._pulse_anim.setEndValue(1.0)
            self._pulse_anim.setEasingCurve(QEasingCurve.Type.InOutSine)
            self._pulse_anim.setLoopCount(-1)
            self._pulse_anim.valueChanged.connect(self._apply_scale)

    def _apply_scale(self, scale_factor: Any) -> None:
        if self._original_container_size is None:
            return
        f_scale = float(scale_factor)
        new_width = int(self._original_container_size.width() * f_scale)
        new_height = int(self._original_container_size.height() * f_scale)
        self.container.setFixedSize(new_width, new_height)

    def enterEvent(self, event: QEnterEvent | None) -> None:
        """Ferma il timer di chiusura quando il mouse entra nel toast."""
        if self._hide_timer.isActive():
            self._hide_timer.stop()
        super().enterEvent(event)

    def leaveEvent(self, event: Any) -> None:
        """Riavvia il timer di chiusura quando il mouse esce dal toast."""
        self._hide_timer.start(self._duration)
        super().leaveEvent(event)

    def show_at(self, x: int, y: int) -> None:
        self.move(x, y)
        if self._pulse and hasattr(self, "_pulse_anim"):
            self.container.adjustSize()
            self._original_container_size = self.container.size()

        self.show()
        self._fade_in.start()

        if self._pulse and hasattr(self, "_pulse_anim"):
            self._pulse_anim.start()

        # Avvia timer di chiusura
        self._hide_timer.start(self._duration)


class ToastManager(QObject):
    """Singleton per la gestione dei toast."""

    _instance: ClassVar[Optional["ToastManager"]] = None
    _active_toasts: ClassVar[list[Toast]] = []

    @classmethod
    def instance(cls) -> "ToastManager":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def show(
        self,
        message: str,
        toast_type: str = Toast.Type.INFO,
        duration: int = 3000,
        position: str = "top",
        pulse: bool = False,
    ) -> None:
        parent = QApplication.activeWindow()
        toast = Toast(message, toast_type, duration, pulse, parent)
        # Update active toasts list using the class variable correctly
        ToastManager._active_toasts = [t for t in ToastManager._active_toasts if t.isVisible()]

        if parent:
            geo = parent.geometry()
            x = geo.x() + (geo.width() - toast.width()) // 2
            if position == "bottom":
                bottom_margin = 75
                y = geo.y() + geo.height() - bottom_margin - toast.height()
            else:
                offset_y = sum([t.height() + 10 for t in ToastManager._active_toasts])
                y = geo.y() + 80 + offset_y
        else:
            primary_screen = QApplication.primaryScreen()
            if primary_screen:
                screen = primary_screen.geometry()
                x = (screen.width() - toast.width()) // 2
                y = 80 if position == "top" else (screen.height() - 150)
            else:
                x, y = 0, 0

        ToastManager._active_toasts.append(toast)
        toast.destroyed.connect(
            lambda: ToastManager._active_toasts.remove(toast)
            if toast in ToastManager._active_toasts
            else None
        )
        toast.show_at(x, y)


# Funzioni helper globali con NUOVI TEMPI
def toast_info(message: str, duration: int = 3000) -> None:
    ToastManager.instance().show(message, Toast.Type.INFO, duration)


def toast_success(message: str, duration: int = 2000) -> None:
    """Visualizza un toast di successo (Veloce: 2s)."""
    ToastManager.instance().show(message, Toast.Type.SUCCESS, duration)


def toast_warning(message: str, duration: int = 10000) -> None:
    """Visualizza un toast di avviso (Lungo: 10s)."""
    ToastManager.instance().show(message, Toast.Type.WARNING, duration)


def toast_error(message: str, duration: int = 10000) -> None:
    """Visualizza un toast di errore (Lungo: 10s)."""
    ToastManager.instance().show(message, Toast.Type.ERROR, duration)
