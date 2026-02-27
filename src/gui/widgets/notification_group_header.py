"""
NotificationGroupHeader - Header collapsible per raggruppamenti di notifiche.
Supporta time-based, category-based e priority-based grouping.
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QWidget

from src.gui.styles import COLORS


class NotificationGroupHeader(QFrame):
    """
    Header collapsible per un gruppo di notifiche.

    Features:
    - Click per expand/collapse gruppo
    - Count badge
    - Icon emoji basato su tipo gruppo
    - Visual feedback su hover
    """

    # Signal
    toggled = pyqtSignal(str, bool)  # group_key, is_expanded

    def __init__(
        self,
        title: str,
        group_key: str,
        count: int = 0,
        icon: str = "📁",
        parent: QWidget | None = None,
    ):
        super().__init__(parent)
        self.group_key = group_key
        self._is_expanded = True  # Default: expanded
        self._count = count
        self._icon = icon
        self._title = title
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup layout e componenti."""
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(
            f"""
            NotificationGroupHeader {{
                background-color: {COLORS['bg_hover']};
                border-radius: 10px;
                border: 1px solid {COLORS['border_light']};
            }}
            NotificationGroupHeader:hover {{
                background-color: {COLORS['bg_light']};
                border-color: {COLORS['border_medium']};
            }}
        """
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(10)

        # Icon
        icon_lbl = QLabel(self._icon)
        icon_lbl.setStyleSheet("font-size: 18px; border: none; background: transparent;")
        layout.addWidget(icon_lbl)

        # Title
        self.title_lbl = QLabel(self._title)
        self.title_lbl.setStyleSheet(
            f"""
            QLabel {{
                font-weight: 800;
                font-size: 12px;
                color: {COLORS['text_dark']};
                text-transform: uppercase;
                letter-spacing: 1px;
                border: none;
                background: transparent;
            }}
        """
        )
        layout.addWidget(self.title_lbl)

        # Count badge
        self.count_lbl = QLabel(str(self._count))
        self.count_lbl.setStyleSheet(
            f"""
            QLabel {{
                font-weight: 700;
                font-size: 10px;
                color: white;
                background-color: {COLORS['text_muted']};
                padding: 2px 8px;
                border-radius: 10px;
                border: none;
            }}
        """
        )
        layout.addWidget(self.count_lbl)

        layout.addStretch()

        # Collapse/Expand arrow (moved to the right)
        self.arrow_btn = QLabel()
        self.arrow_btn.setText("SCENDI" if self._is_expanded else "ESPANDI")
        self.arrow_btn.setStyleSheet(
            f"""
            QLabel {{
                color: {COLORS['text_muted']};
                font-size: 9px;
                font-weight: 900;
                letter-spacing: 0.5px;
                border: none;
                background: transparent;
            }}
        """
        )
        layout.addWidget(self.arrow_btn)

    def mousePressEvent(self, event: QMouseEvent | None) -> None:
        """Toggle expanded state on click."""
        self._is_expanded = not self._is_expanded
        self.arrow_btn.setText("SCENDI" if self._is_expanded else "ESPANDI")
        self.toggled.emit(self.group_key, self._is_expanded)
        super().mousePressEvent(event)

    def set_count(self, count: int) -> None:
        """Update count badge."""
        self._count = count
        self.count_lbl.setText(str(count))

    def is_expanded(self) -> bool:
        """Check if group is expanded."""
        return self._is_expanded

    def set_expanded(self, expanded: bool) -> None:
        """Set expanded state programmatically."""
        self._is_expanded = expanded
        self.arrow_btn.setText("SCENDI" if expanded else "ESPANDI")
