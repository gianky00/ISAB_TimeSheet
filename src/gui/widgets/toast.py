"""Sistema di notifiche toast non-blocking con supporto hover e tempi differenziati."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, ClassVar

from PySide6.QtCore import (
    QEasingCurve,
    QEvent,
    QObject,
    QPropertyAnimation,
    QSize,
    Qt,
    QTimer,
    QVariantAnimation,
)
from PySide6.QtWidgets import (
    QApplication,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.gui.styles import COLORS
from src.gui.styles.constants import ANIMATION_TIMINGS
from src.utils.helpers import get_asset_path, get_colored_icon

from ..design.colors import get_palette
from ..design.spacing import BorderRadius

if TYPE_CHECKING:
    from PySide6.QtGui import QEnterEvent


@dataclass
class ToastParams:
    """Configurazione per la visualizzazione di un toast."""

    message: str
    toast_type: str = "info"
    duration: int = 3000
    pulse: bool = False
    is_rich_text: bool = False
    parent: QWidget | None = None
    position: str = "top"


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

    def __init__(self, params: ToastParams) -> None:
        """Inizializza il toast con i parametri di configurazione."""
        super().__init__(params.parent)
        self._duration = params.duration
        self._type = params.toast_type
        self._pulse = params.pulse
        self._palette = get_palette()
        self._msg_text = params.message
        self._is_rich_text = params.is_rich_text
        self._original_container_size: QSize | None = None

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Abilita il tracking del mouse per l'hover
        self.setMouseTracking(True)

        self._setup_ui(params.message)
        self._setup_animation()

        # Timer di chiusura persistente per permettere pausa/riavvio
        self._hide_timer = QTimer(self)
        self._hide_timer.setSingleShot(True)
        self._hide_timer.timeout.connect(self._fade_out.start)

    def _setup_ui(self, message: str) -> None:
        """Configura l'interfaccia utente del toast con icone e colori."""
        main_layout = QVBoxLayout(self)
        main_margin = 10
        main_layout.setContentsMargins(main_margin, main_margin, main_margin, main_margin)

        self.container = QWidget()
        container_layout = QHBoxLayout(self.container)
        cont_margin_h = 16
        cont_margin_v = 12
        container_layout.setContentsMargins(cont_margin_h, cont_margin_v, cont_margin_h, cont_margin_v)

        icon_path, color_key = self.TYPE_CONFIG.get(self._type, self.TYPE_CONFIG[Toast.Type.INFO])
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
        icon_res = get_colored_icon(get_asset_path(icon_path), COLORS["text_dark"])
        icon_size = 20
        icon_label.setPixmap(icon_res.pixmap(QSize(icon_size, icon_size)))
        icon_label.setStyleSheet("border: none; background: transparent;")
        container_layout.addWidget(icon_label)

        msg_label = QLabel()
        if self._is_rich_text:
            safe_msg = self._sanitize_html(message)
            msg_label.setTextFormat(Qt.TextFormat.RichText)
            msg_label.setText(safe_msg)
        else:
            msg_label.setTextFormat(Qt.TextFormat.PlainText)
            msg_label.setText(message)

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

    def _sanitize_html(self, html: str) -> str:
        """Rimuove tag pericolosi dall'HTML del toast."""
        clean = re.sub(r"<script.*?>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
        clean = re.sub(
            r"<(script|iframe|object|embed|applet|meta|link|style).*?>",
            "",
            clean,
            flags=re.IGNORECASE,
        )
        return re.sub(r"\son\w+?\s*=\s*['\"].*?['\"]", "", clean, flags=re.IGNORECASE)

    def _setup_animation(self) -> None:
        """Configura le animazioni di fade-in e fade-out."""
        self._opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self._opacity_effect)

        self._fade_in = QPropertyAnimation(self._opacity_effect, b"opacity")
        fade_in_duration = 200
        self._fade_in.setDuration(fade_in_duration)
        self._fade_in.setStartValue(0.0)
        self._fade_in.setEndValue(1.0)

        self._fade_out = QPropertyAnimation(self._opacity_effect, b"opacity")
        fade_out_duration = 300
        self._fade_out.setDuration(fade_out_duration)
        self._fade_out.setStartValue(1.0)
        self._fade_out.setEndValue(0.0)
        self._fade_out.finished.connect(self.deleteLater)

        if self._pulse:
            self._pulse_anim = QVariantAnimation(self)
            pulse_duration = 800
            self._pulse_anim.setDuration(pulse_duration)
            self._pulse_anim.setStartValue(1.0)
            self._pulse_anim.setKeyValueAt(0.5, 1.05)
            self._pulse_anim.setEndValue(1.0)
            self._pulse_anim.setEasingCurve(QEasingCurve.Type.InOutSine)
            self._pulse_anim.setLoopCount(-1)
            self._pulse_anim.valueChanged.connect(self._apply_scale)

    def _apply_scale(self, scale_factor: Any) -> None:
        """Applica la scala al container per l'effetto pulsazione."""
        if self._original_container_size is None:
            return
        f_scale = float(scale_factor)
        new_width = int(self._original_container_size.width() * f_scale)
        new_height = int(self._original_container_size.height() * f_scale)
        self.container.setFixedSize(new_width, new_height)

    def enterEvent(self, event: QEnterEvent) -> None:
        """Ferma il timer di chiusura quando il mouse entra nel toast."""
        if self._hide_timer.isActive():
            self._hide_timer.stop()
        super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        """Riavvia il timer di chiusura quando il mouse esce dal toast."""
        self._hide_timer.start(self._duration)
        super().leaveEvent(event)

    def show_at(self, x: int, y: int) -> None:
        """Visualizza il toast in una posizione specifica e avvia le animazioni."""
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
    """Singleton per la gestione del posizionamento e dello stacking dei toast."""

    _instance: ClassVar[ToastManager | None] = None
    _active_toasts: ClassVar[list[Toast]] = []

    @classmethod
    def instance(cls) -> ToastManager:
        """Restituisce l'istanza singleton di ToastManager."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def show(  # noqa: PLR0913
        self,
        message: str,
        toast_type: str = Toast.Type.INFO,
        duration: int = 3000,
        position: str = "top",
        pulse: bool = False,
        is_rich_text: bool = False,
    ) -> None:
        """Crea e visualizza un nuovo toast, calcolando la posizione corretta nello stack.

        Ottimizzato per limitare l'overhead di rendering su flussi massivi.
        """
        # Pulisce la lista dei toast non più visibili
        ToastManager._active_toasts = [t for t in ToastManager._active_toasts if t.isVisible()]

        # Protezione anti-jank: limite massimo di toast contemporanei
        if len(ToastManager._active_toasts) >= 3:
            return

        # Prevenzione duplicati identici (spam)
        for t in ToastManager._active_toasts:
            if hasattr(t, "_msg_text") and t._msg_text == message:
                return

        parent = QApplication.activeWindow()
        params = ToastParams(
            message=message,
            toast_type=toast_type,
            duration=duration,
            pulse=pulse,
            parent=parent,
            is_rich_text=is_rich_text,
        )
        toast = Toast(params)
        toast._msg_text = message  # Memorizza il testo per il filtro duplicati

        if parent:
            geo = parent.geometry()
            x = geo.x() + (geo.width() - toast.width()) // 2
            if position == "bottom":
                bottom_margin = 75
                y = geo.y() + geo.height() - bottom_margin - toast.height()
            else:
                stack_spacing = 10
                top_offset = 80
                offset_y = sum([t.height() + stack_spacing for t in ToastManager._active_toasts])
                y = geo.y() + top_offset + offset_y
        else:
            primary_screen = QApplication.primaryScreen()
            if primary_screen:
                screen = primary_screen.geometry()
                x = (screen.width() - toast.width()) // 2
                top_offset = 80
                bottom_offset = 150
                y = top_offset if position == "top" else (screen.height() - bottom_offset)
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
def toast_info(message: str, duration: int | None = None) -> None:
    """Visualizza un toast informativo."""
    d = duration or ANIMATION_TIMINGS["toast_info"]
    ToastManager.instance().show(message, Toast.Type.INFO, d, is_rich_text=("<" in message))


def toast_success(message: str, duration: int | None = None) -> None:
    """Visualizza un toast di successo (Veloce: 2s)."""
    d = duration or ANIMATION_TIMINGS["toast_success"]
    ToastManager.instance().show(message, Toast.Type.SUCCESS, d, is_rich_text=("<" in message))


def toast_warning(message: str, duration: int | None = None) -> None:
    """Visualizza un toast di avviso (Lungo: 10s)."""
    d = duration or ANIMATION_TIMINGS["toast_warning"]
    ToastManager.instance().show(message, Toast.Type.WARNING, d, is_rich_text=("<" in message))


def toast_error(message: str, duration: int | None = None) -> None:
    """Visualizza un toast di errore (Lungo: 10s)."""
    d = duration or ANIMATION_TIMINGS["toast_error"]
    ToastManager.instance().show(message, Toast.Type.ERROR, d, is_rich_text=("<" in message))
