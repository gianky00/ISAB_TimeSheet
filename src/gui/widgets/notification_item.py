from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout

from src.core.notification_manager import NotificationManager


# Widget per singola notifica
class NotificationItem(QFrame):
    def __init__(self, notification):
        super().__init__()
        self.notification = notification
        self.manager = NotificationManager.instance()
        self._setup_ui()

    def _setup_ui(self):
        self.setFrameShape(QFrame.Shape.StyledPanel)

        # Determine colors based on level
        level = self.notification.get("level", "info").lower()
        bg_color = "#ffffff"
        border_color = "#dee2e6"
        icon = "ℹ️"

        if level == "success":
            border_color = "#198754"
            icon = "✅"
        elif level == "warning":
            border_color = "#ffc107"
            icon = "⚠️"
        elif level == "error":
            border_color = "#dc3545"
            icon = "❌"

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

        # Header: Icon + Title + Timestamp + Close
        header_layout = QHBoxLayout()

        title_lbl = QLabel(f"{icon} {self.notification.get('title', 'Notifica')}")
        title_lbl.setStyleSheet("font-weight: bold; font-size: 14px; border: none; background: transparent;")
        header_layout.addWidget(title_lbl)

        header_layout.addStretch()

        # Timestamp
        try:
            ts = datetime.fromisoformat(self.notification.get("timestamp"))
            time_str = ts.strftime("%d/%m %H:%M")
        except:
            time_str = ""

        time_lbl = QLabel(time_str)
        time_lbl.setStyleSheet("color: #6c757d; font-size: 12px; border: none; background: transparent;")
        header_layout.addWidget(time_lbl)

        # Delete Button
        del_btn = QPushButton("×")
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

    def mousePressEvent(self, event):
        if not self.notification.get("read", False):
            self.manager.mark_as_read(self.notification["id"])
        super().mousePressEvent(event)

    def _delete(self):
        self.manager.delete_notification(self.notification["id"])
