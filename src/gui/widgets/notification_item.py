from datetime import datetime
from typing import Any

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from src.core.constants import Icons
from src.core.notification_manager import NotificationManager
from src.gui.styles import COLORS
from src.gui.widgets.core_widgets import (
    IconButton,
)
from src.utils.helpers import get_asset_path, get_colored_icon


# Widget per singola notifica
class NotificationItem(QFrame):
    """
    Widget grafico per la visualizzazione di una singola notifica nel centro notifiche.
    Supporta diversi livelli di severità (info, success, warning, error).
    """

    def __init__(self, notification: dict[str, Any], parent: QWidget | None = None) -> None:
        """Inizializza l'item con i dati della notifica."""
        super().__init__(parent)
        self.notification = notification
        self.manager = NotificationManager.instance()
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Configura il layout e gli stili dell'item."""
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self._apply_base_style()

        layout = QVBoxLayout(self)
        self._setup_header(layout)
        self._setup_body(layout)

    def _apply_base_style(self) -> None:
        """Determina e applica lo stile base (colori, bordi)."""
        level = self.notification.get("level", "info").lower()
        bg_color = COLORS["bg_white"]
        border_color = COLORS["border_light"]

        if level == "success":
            border_color = COLORS["success_dark"]
        elif level == "warning":
            border_color = COLORS["warning_yellow"]
        elif level == "error":
            border_color = COLORS["error_red"]

        if not self.notification.get("read", False):
            bg_color = COLORS["bg_light"]
            left_border = f"5px solid {border_color}"
        else:
            left_border = f"1px solid {border_color}"

        self.setStyleSheet(
            f"""
            NotificationItem {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-left: {left_border};
                border-radius: 6px;
            }}
        """
        )

    def _setup_header(self, layout: QVBoxLayout) -> None:
        """Inizializza l'header con icona, titolo, timestamp e pulsante elimina."""
        header_layout = QHBoxLayout()
        level = self.notification.get("level", "info").lower()
        icon_path = {
            "success": Icons.CHECK_CIRCLE,
            "warning": Icons.ALERT,
            "error": Icons.X_CIRCLE,
        }.get(level, Icons.HELP)

        # Icon
        icon_lbl = QLabel()
        icon = get_colored_icon(get_asset_path(icon_path), COLORS["text_dark"])
        icon_lbl.setPixmap(icon.pixmap(QSize(18, 18)))
        icon_lbl.setStyleSheet("border: none; background: transparent;")
        header_layout.addWidget(icon_lbl)

        title_lbl = QLabel(self.notification.get("title", "Notifica"))
        title_lbl.setStyleSheet("font-weight: bold; font-size: 14px; border: none; background: transparent;")
        header_layout.addWidget(title_lbl)

        header_layout.addStretch()

        # Timestamp
        try:
            ts = datetime.fromisoformat(self.notification.get("timestamp") or "")
            time_str = ts.strftime("%d/%m %H:%M")
        except Exception:
            time_str = ""

        time_lbl = QLabel(time_str)
        time_lbl.setStyleSheet(
            f"color: {COLORS['text_muted']}; font-size: 12px; border: none; background: transparent;"
        )
        header_layout.addWidget(time_lbl)

        # Delete Button
        del_btn = IconButton()
        del_btn.setIcon(get_colored_icon(get_asset_path(Icons.TRASH), COLORS["text_dark"]))
        del_btn.setIconSize(QSize(14, 14))
        del_btn.setFixedSize(20, 20)
        del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        del_btn.setToolTip("Elimina")
        del_btn.setStyleSheet(
            f"""
            QPushButton {{
                background: transparent;
                border: none;
                font-weight: bold;
                color: {COLORS["text_light"]};
            }}
            QPushButton:hover {{ color: {COLORS["error_red"]}; }}
        """
        )
        del_btn.clicked.connect(self._delete)
        header_layout.addWidget(del_btn)

        layout.addLayout(header_layout)

    def _setup_body(self, layout: QVBoxLayout) -> None:
        """Configura il corpo del messaggio."""
        msg_lbl = QLabel(self.notification.get("message", ""))
        msg_lbl.setWordWrap(True)
        msg_lbl.setStyleSheet(
            f"color: {COLORS['text_dark']}; border: none; margin-top: 5px; background: transparent;"
        )
        layout.addWidget(msg_lbl)

    def mousePressEvent(self, event: QMouseEvent | None) -> None:
        """Segna la notifica come letta quando l'utente ci clicca sopra."""
        if not self.notification.get("read", False):
            self.manager.mark_as_read(self.notification["id"])
        super().mousePressEvent(event)

    def _delete(self) -> None:
        self.manager.delete_notification(self.notification["id"])
