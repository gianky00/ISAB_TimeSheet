"""
NotificationGroupHeader - Header collapsible per raggruppamenti di notifiche.
Supporta time-based, category-based e priority-based grouping.
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QWidget


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

    def _setup_ui(self):
        """Setup layout e componenti."""
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(
            """
            NotificationGroupHeader {
                background-color: #f8f9fa;
                border-radius: 8px;
                border: 1px solid #e9ecef;
            }
            NotificationGroupHeader:hover {
                background-color: #e9ecef;
                border-color: #dee2e6;
            }
        """
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(8)

        # Collapse/Expand arrow
        self.arrow_btn = QLabel()
        self.arrow_btn.setText("▼" if self._is_expanded else "▶")
        self.arrow_btn.setStyleSheet(
            """
            QLabel {
                color: #6c757d;
                font-size: 12px;
                font-weight: bold;
                border: none;
                background: transparent;
            }
        """
        )
        layout.addWidget(self.arrow_btn)

        # Icon
        icon_lbl = QLabel(self._icon)
        icon_lbl.setStyleSheet(
            """
            QLabel {
                font-size: 16px;
                border: none;
                background: transparent;
            }
        """
        )
        layout.addWidget(icon_lbl)

        # Title
        self.title_lbl = QLabel(self._title)
        self.title_lbl.setStyleSheet(
            """
            QLabel {
                font-weight: 700;
                font-size: 13px;
                color: #495057;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                border: none;
                background: transparent;
            }
        """
        )
        layout.addWidget(self.title_lbl)

        # Count badge
        self.count_lbl = QLabel(f"({self._count})")
        self.count_lbl.setStyleSheet(
            """
            QLabel {
                font-weight: 600;
                font-size: 12px;
                color: #6c757d;
                border: none;
                background: transparent;
            }
        """
        )
        layout.addWidget(self.count_lbl)

        layout.addStretch()

    def mousePressEvent(self, event):
        """Toggle expanded state on click."""
        self._is_expanded = not self._is_expanded
        self.arrow_btn.setText("▼" if self._is_expanded else "▶")
        self.toggled.emit(self.group_key, self._is_expanded)
        super().mousePressEvent(event)

    def set_count(self, count: int):
        """Update count badge."""
        self._count = count
        self.count_lbl.setText(f"({count})")

    def is_expanded(self) -> bool:
        """Check if group is expanded."""
        return self._is_expanded

    def set_expanded(self, expanded: bool):
        """Set expanded state programmatically."""
        self._is_expanded = expanded
        self.arrow_btn.setText("▼" if expanded else "▶")
