"""SyncroJob - Notification Card (Refactored).

Widget moderno per la visualizzazione di una singola notifica.
Modularizzato per utilizzare il Notification Styling Engine.
"""

from datetime import UTC, datetime
from typing import Any

from PySide6.QtCore import QEasingCurve, QPropertyAnimation, Qt, Signal
from PySide6.QtGui import QMouseEvent, QShowEvent
from PySide6.QtWidgets import (
    QFrame,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.core.notification_manager import NotificationManager
from src.gui.styles import COLORS
from src.gui.styles.notification_styles import LEVEL_STYLES, get_notification_qss
from src.gui.widgets.core_widgets import IconButton
from src.gui.widgets.modern_button import ModernButton
from src.utils.helpers import get_asset_path, get_colored_icon


class NotificationCard(QFrame):
    """Widget moderno per la visualizzazione di una singola notifica.

    Utilizza stili dinamici basati sulla severit  e supporta animazioni di fade-in.

    Inizializza la card di notifica.

    Args:
      notification: Dizionario contenente i dati della notifica (id, titolo, messaggio, ecc.).
      parent: Widget genitore opzionale.
      disable_animations: Se True, disabilita l'effetto di fade-in iniziale.

    Attributes:
        action_triggered: Segnale o attributo della classe.
        card_clicked: Segnale o attributo della classe.
        card_deleted: Segnale o attributo della classe.
        pin_toggled: Segnale o attributo della classe.
    """

    # Signals
    card_clicked = Signal(str)
    card_deleted = Signal(str)
    pin_toggled = Signal(str, bool)
    action_triggered = Signal(str, str)

    def __init__(
        self,
        notification: dict[str, Any],
        parent: QWidget | None = None,
        disable_animations: bool = False,
    ) -> None:
        super().__init__(parent)
        self.notification = notification
        self.manager = NotificationManager.instance()
        self._disable_animations = disable_animations

        # UI Components
        self.pin_btn: QPushButton
        self.title_lbl: QLabel
        self.time_lbl: QLabel
        self.del_btn: QPushButton
        self.message_widget: QLabel | QTextBrowser
        self.opacity_effect: QGraphicsOpacityEffect
        self.fade_in_animation: QPropertyAnimation

        self._setup_ui()
        if not disable_animations:
            self._setup_animations()

    def _setup_ui(self) -> None:
        """Configura il layout, gli stili e gli elementi interattivi della card."""
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        level = self.notification.get("level", "info").lower()
        is_read = self.notification.get("read", False)

        # Applica lo stile dal motore esterno
        self.setStyleSheet(get_notification_qss(level, is_read))
        style_meta = LEVEL_STYLES.get(level, LEVEL_STYLES["info"])

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 10, 12, 10)
        main_layout.setSpacing(6)

        self._setup_header(main_layout, style_meta)
        self._setup_message(main_layout)
        self._setup_actions(main_layout)

    def _setup_header(self, layout: QVBoxLayout, style_meta: dict[str, Any]) -> None:
        """Configura l'area superiore della card con pin, icona e titoli."""
        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)

        self.pin_btn = IconButton()
        self.pin_btn.setText("  ")
        self.pin_btn.setFixedSize(24, 24)
        self.pin_btn.clicked.connect(self._toggle_pin)
        header_layout.addWidget(self.pin_btn)

        badge = QLabel()
        badge.setFixedSize(36, 36)
        badge.setPixmap(
            get_colored_icon(get_asset_path(style_meta["icon"]), style_meta["icon_color"]).pixmap(20, 22)
        )
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setStyleSheet(f"background: {style_meta['badge_bg']}; border-radius: 18px;")
        header_layout.addWidget(badge)

        info_v = QVBoxLayout()
        info_v.setSpacing(0)
        self.title_lbl = QLabel(self.notification.get("title", "Notifica"))
        self.title_lbl.setStyleSheet(f"font-weight: 800; font-size: 14px; color: {COLORS['text_dark']};")

        self.time_lbl = QLabel(self._format_timestamp(self.notification.get("timestamp")))
        self.time_lbl.setStyleSheet(f"font-size: 11px; color: {COLORS['text_muted']};")

        info_v.addWidget(self.title_lbl)
        info_v.addWidget(self.time_lbl)
        header_layout.addLayout(info_v, stretch=1)

        self.del_btn = IconButton()
        self.del_btn.setIcon(get_colored_icon(get_asset_path(Icons.TRASH), COLORS["text_muted"]))
        self.del_btn.setToolTip("Elimina")
        self.del_btn.clicked.connect(self._delete_notification)
        header_layout.addWidget(self.del_btn)
        layout.addLayout(header_layout)

    def _setup_message(self, layout: QVBoxLayout) -> None:
        """Inizializza il widget per il corpo del messaggio."""
        msg_text = self.notification.get("message", "")
        self.message_widget = QLabel(msg_text)
        self.message_widget.setWordWrap(True)
        self.message_widget.setStyleSheet(f"color: {COLORS['text_dark']}; font-size: 13px; padding: 2px 5px;")
        layout.addWidget(self.message_widget)

    def _setup_actions(self, layout: QVBoxLayout) -> None:
        """Aggiunge pulsanti di azione dinamici se presenti nella notifica."""
        actions = self.notification.get("actions", [])
        if actions:
            footer_lay = QHBoxLayout()
            footer_lay.setSpacing(8)
            footer_lay.addStretch()
            for act in actions:
                btn = ModernButton(
                    act["label"], variant=ModernButton.Variant.GHOST, size=ModernButton.Size.SMALL
                )
                btn.clicked.connect(
                    lambda _, k=act["key"]: self.action_triggered.emit(self.notification["id"], k)
                )
                footer_lay.addWidget(btn)
            layout.addLayout(footer_lay)

    def _format_timestamp(self, ts: Any) -> str:
        """Converte un timestamp in formato leggibile (HH:MM)."""
        if isinstance(ts, str):
            return ts
        if isinstance(ts, (int, float)):
            return datetime.fromtimestamp(ts, tz=UTC).astimezone().strftime("%H:%M")
        return datetime.now(UTC).astimezone().strftime("%H:%M")

    def _setup_animations(self) -> None:
        """Configura l'effetto di opacit  per l'animazione di ingresso."""
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.fade_in_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_in_animation.setDuration(400)
        self.fade_in_animation.setStartValue(0.0)
        self.fade_in_animation.setEndValue(1.0)
        self.fade_in_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    def showEvent(self, event: QShowEvent | None) -> None:
        """Avvia l'animazione di fade-in quando la card viene mostrata."""
        if not self._disable_animations:
            self.fade_in_animation.start()
        super().showEvent(event)  # type: ignore[arg-type]

    def _toggle_pin(self) -> None:
        """Gestisce il cambiamento di stato 'pinned' della notifica."""
        new_state = not self.notification.get("pinned", False)
        self.notification["pinned"] = new_state
        self.pin_btn.setText("  ")
        self.pin_toggled.emit(self.notification["id"], new_state)

    def _delete_notification(self) -> None:
        """Emette il segnale per la rimozione della notifica dal gestore."""
        self.card_deleted.emit(self.notification["id"])

    def mousePressEvent(self, event: QMouseEvent | None) -> None:
        """Emette il segnale di clic sulla card per contrassegnarla come letta."""
        if event and event.button() == Qt.MouseButton.LeftButton:
            self.card_clicked.emit(self.notification["id"])
        super().mousePressEvent(event)  # type: ignore[arg-type]
