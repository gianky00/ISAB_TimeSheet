from datetime import datetime

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.core.audit_manager import AuditManager
from src.core.constants import Icons
from src.utils.helpers import get_asset_path, get_colored_icon
from src.utils.log_humanizer import friendly_time_delta


class ActivityItem(QFrame):
    """
    Rappresenta una singola voce nella timeline orizzontale (Compact).
    """

    def __init__(self, log_entry: dict, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setStyleSheet(
            """
            QFrame {
                background-color: #ffffff;
                border-radius: 6px;
                border: 1px solid #e9ecef;
            }
            QFrame:hover {
                background-color: #f1f3f5;
                border-color: #ced4da;
            }
        """
        )
        self.setFixedWidth(280)  # Widen to accommodate more text

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(10)

        # 1. Icona Stato (Successo/Errore/Warning)
        status = log_entry.get("status", "success").lower()
        if status == "error":
            icon_color = "#dc3545"  # Rosso
            icon_path = Icons.ALERT_CIRCLE
        elif status == "warning":
            icon_color = "#ffc107"  # Giallo
            icon_path = Icons.ALERT_TRIANGLE
        else:
            icon_color = "#198754"  # Verde
            icon_path = Icons.CHECK_CIRCLE

        icon_lbl = QLabel()
        icon_lbl.setFixedSize(16, 16)
        icon_lbl.setPixmap(
            get_colored_icon(get_asset_path(icon_path), icon_color).pixmap(16, 16)
        )
        icon_lbl.setStyleSheet("border: none; background: transparent;")
        layout.addWidget(icon_lbl)

        # 2. Contenuto Testuale (Action + Time)
        text_layout = QVBoxLayout()
        text_layout.setSpacing(0)

        # Action (Full Specific Text)
        action_text = log_entry.get("action", "Azione")
        entity = log_entry.get("entity", "")

        if entity and entity != "-":
            full_text = f"{action_text} - {entity}"
        else:
            full_text = action_text

        action_lbl = QLabel(full_text)
        action_lbl.setStyleSheet(
            "font-weight: bold; font-size: 13px; color: #343a40; border: none; background: transparent;"
        )
        action_lbl.setWordWrap(True)  # NO TRUNCATION
        action_lbl.setToolTip(full_text)
        text_layout.addWidget(action_lbl)

        # Time
        ts_str = log_entry.get("timestamp", "")
        try:
            ts = datetime.fromisoformat(ts_str)
            time_str = friendly_time_delta(ts)
        except ValueError:
            time_str = "--"

        time_lbl = QLabel(time_str)
        time_lbl.setStyleSheet(
            "font-size: 11px; color: #adb5bd; border: none; background: transparent;"
        )
        text_layout.addWidget(time_lbl)

        layout.addLayout(text_layout)


class ActivityFeed(QWidget):
    """
    Widget che mostra una timeline orizzontale delle ultime attività.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(70)  # +40% (from 50px)
        self._setup_ui()

        self.timer = QTimer(self)
        self.timer.timeout.connect(
            self.refresh_feed
        )  # Refresh full feed to update logs
        self.timer.start(30000)

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # Label "Ultime Attività:"
        title = QLabel("Feed:")
        title.setStyleSheet(
            "font-size: 12px; font-weight: bold; color: #6c757d; margin-right: 5px;"
        )
        layout.addWidget(title)

        # Scroll Area Orizzontale
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setStyleSheet("background: transparent;")
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        self.feed_widget = QWidget()
        self.feed_layout = QHBoxLayout(self.feed_widget)  # Horizontal!
        self.feed_layout.setContentsMargins(0, 0, 0, 5)  # Padding for scrollbar
        self.feed_layout.setSpacing(10)
        self.feed_layout.addStretch()  # Align items to right (latest first?) or left? Let's align left.

        self.scroll_area.setWidget(self.feed_widget)
        layout.addWidget(self.scroll_area)

        self.refresh_feed()

    def refresh_feed(self):
        """Ricarica i log dall'AuditManager."""
        # Pulisci: remove all but stretch (last item)
        while self.feed_layout.count() > 1:
            item = self.feed_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Limit to 10 latest
        logs = AuditManager().get_logs(limit=10)

        if not logs:
            empty_lbl = QLabel("Nessuna attività recente.")
            empty_lbl.setStyleSheet("color: #adb5bd; font-size: 11px;")
            self.feed_layout.insertWidget(0, empty_lbl)
            return

        for log in logs:
            item = ActivityItem(log)
            # Insert at beginning (left)
            self.feed_layout.insertWidget(self.feed_layout.count() - 1, item)
