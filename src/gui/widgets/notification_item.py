from datetime import datetime
from typing import Any

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from src.core.constants import Icons
from src.core.notification_manager import NotificationManager
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
        self.setFrameShape(QFrame.Shape.StyledPanel)

        # Determine colors based on level
        level = self.notification.get("level", "info").lower()
        bg_color = "#ffffff"
        border_color = "#dee2e6"
        icon_path = Icons.HELP

        if level == "success":
            border_color = "#198754"
            icon_path = Icons.CHECK_CIRCLE
        elif level == "warning":
            border_color = "#ffc107"
            icon_path = Icons.ALERT
        elif level == "error":
            border_color = "#dc3545"
            icon_path = Icons.X_CIRCLE

        if not self.notification.get("read", False):
            bg_color = "#f8f9fa"
            # Thicker border for unread
            self.setStyleSheet(
                f"""
                NotificationItem {{
                    background-color: {bg_color};
                    border: 1px solid {border_color};
                    border-left: 5px solid {border_color};
                    border-radius: 6px;
                }}
            """
            )
        else:
            self.setStyleSheet(
                f"""
                NotificationItem {{
                    background-color: {bg_color};
                    border: 1px solid {border_color};
                    border-radius: 6px;
                }}
            """
            )

        layout = QVBoxLayout(self)

        header_layout = QHBoxLayout()

        # Icon
        icon_lbl = QLabel()
        icon = get_colored_icon(get_asset_path(icon_path), "#000000")
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
        time_lbl.setStyleSheet("color: #6c757d; font-size: 12px; border: none; background: transparent;")
        header_layout.addWidget(time_lbl)

        # Delete Button
        del_btn = QPushButton()
        del_btn.setIcon(get_colored_icon(get_asset_path(Icons.TRASH), "#000000"))
        del_btn.setIconSize(QSize(14, 14))
        del_btn.setFixedSize(20, 20)
        del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        del_btn.setToolTip("Elimina")
        del_btn.setStyleSheet(
            """
            QPushButton {
                background: transparent;
                border: none;
                font-weight: bold;
                color: #adb5bd;
            }
            QPushButton:hover { color: #dc3545; }
        """
        )
        del_btn.clicked.connect(self._delete)
        header_layout.addWidget(del_btn)

        layout.addLayout(header_layout)

        # Message
        msg_lbl = QLabel(self.notification.get("message", ""))
        msg_lbl.setWordWrap(True)
        msg_lbl.setStyleSheet("color: #212529; border: none; margin-top: 5px; background: transparent;")
        layout.addWidget(msg_lbl)

    def mousePressEvent(self, event: QMouseEvent | None) -> None:
        """Segna la notifica come letta quando l'utente ci clicca sopra."""
        if not self.notification.get("read", False):
            self.manager.mark_as_read(self.notification["id"])
        super().mousePressEvent(event)

    def _delete(self) -> None:
        self.manager.delete_notification(self.notification["id"])
