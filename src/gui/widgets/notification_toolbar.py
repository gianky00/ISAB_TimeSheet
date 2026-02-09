"""
NotificationToolbar - Barra degli strumenti per filtrare, cercare e ordinare notifiche.
Include filter chips, search bar, sort dropdown e bulk actions menu.
"""

from typing import Any

from PyQt6.QtCore import QSize, Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QWidget,
)

from src.core.constants import Icons
from src.utils.helpers import get_asset_path, get_colored_icon


class FilterChip(QPushButton):
    """
    Filter chip button con stile Material Design 3.
    Mostra count e supporta stato active/inactive.
    """

    def __init__(
        self,
        label: str,
        key: str,
        icon: str | None = None,
        count: int = 0,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.key = key
        self._count = count
        self._is_active = False
        self._icon_path = icon

        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._update_text(label)
        self._apply_style()

        # Connect to update style on toggle
        self.toggled.connect(self._on_toggled)

    def _update_text(self, label: str) -> None:
        """Update button text with count badge."""
        text = f"{label} ({self._count})" if self._count > 0 else label

        self.setText(text)

        # Add icon if provided
        if self._icon_path:
            self.setIcon(
                get_colored_icon(
                    get_asset_path(self._icon_path),
                    "#ffffff" if self._is_active else "#6c757d",
                )
            )
            self.setIconSize(QSize(16, 16))

    def set_count(self, count: int) -> None:
        """Update count and refresh text."""
        self._count = count
        label = self.text().split(" (")[0]  # Extract label without count
        self._update_text(label)

    def _on_toggled(self, checked: bool) -> None:
        """Handle toggle state change."""
        self._is_active = checked
        self._apply_style()
        # Update icon color
        label = self.text().split(" (")[0]
        self._update_text(label)

    def _apply_style(self) -> None:
        """Apply style based on active state."""
        if self._is_active:
            # Active: filled with accent color
            self.setStyleSheet(
                """
                QPushButton {
                    background-color: #2196F3;
                    color: #ffffff;
                    border: none;
                    border-radius: 20px;
                    padding: 8px 16px;
                    font-size: 13px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
            """
            )
        else:
            self.setStyleSheet(
                """
                QPushButton {
                    background-color: transparent;
                    color: #6c757d;
                    border: 1px solid #ced4da;
                    border-radius: 20px;
                    padding: 8px 16px;
                    font-size: 13px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background-color: #f8f9fa;
                    border-color: #adb5bd;
                }
            """
            )


class NotificationToolbar(QWidget):
    """
    Toolbar con search, filter chips, sort dropdown e bulk actions.
    Emette signals per comunicare cambiamenti di stato.
    """

    # Signals
    search_query_changed = pyqtSignal(str)  # query
    filter_changed = pyqtSignal(str)  # filter_key (all, unread, error, warning, info)
    sort_changed = pyqtSignal(str)  # sort_key
    bulk_action_triggered = pyqtSignal(str)  # action_key

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._filter_chips: dict[str, FilterChip] = {}
        self._current_filter = "all"
        self._debounce_timer = QTimer()
        self._debounce_timer.setSingleShot(True)
        self._debounce_timer.timeout.connect(self._emit_search_query)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup layout e componenti."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        # === SEARCH BAR ===
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Cerca notifiche...")
        self.search_input.setFixedWidth(250)
        self.search_input.setStyleSheet(
            """
            QLineEdit {
                padding: 8px 12px;
                border: 1px solid #ced4da;
                border-radius: 8px;
                font-size: 13px;
                background: #ffffff;
            }
            QLineEdit:focus {
                border-color: #2196F3;
                outline: none;
            }
        """
        )
        self.search_input.textChanged.connect(self._on_search_text_changed)
        layout.addWidget(self.search_input)

        # === FILTER CHIPS ===
        filter_configs: list[dict[str, Any]] = [
            {"label": "Tutti", "key": "all", "icon": None},
            {"label": "Da leggere", "key": "unread", "icon": Icons.BELL},
            {"label": "Errori", "key": "error", "icon": Icons.X_CIRCLE},
            {"label": "Avvisi", "key": "warning", "icon": Icons.ALERT_TRIANGLE},
            {"label": "Info", "key": "info", "icon": Icons.INFO},
        ]

        for config in filter_configs:
            chip = FilterChip(
                label=str(config["label"]),
                key=str(config["key"]),
                icon=config["icon"],
                count=0,  # Will be updated dynamically
            )
            chip.clicked.connect(lambda checked, k=str(config["key"]): self._on_filter_clicked(k))
            self._filter_chips[str(config["key"])] = chip
            layout.addWidget(chip)

        # Set "Tutti" as default active
        self._filter_chips["all"].setChecked(True)

        layout.addStretch()

        # === SORT DROPDOWN ===
        sort_label = QLabel("Ordina:")
        sort_label.setStyleSheet("font-size: 13px; color: #6c757d; font-weight: 600;")
        layout.addWidget(sort_label)

        self.sort_combo = QComboBox()
        self.sort_combo.addItem("Data (recenti)", "date_desc")
        self.sort_combo.addItem("Data (vecchie)", "date_asc")
        self.sort_combo.addItem("Priorità", "priority")
        self.sort_combo.addItem("Livello", "level")
        self.sort_combo.setStyleSheet(
            """
            QComboBox {
                padding: 6px 12px;
                border: 1px solid #ced4da;
                border-radius: 6px;
                font-size: 13px;
                background: #ffffff;
                min-width: 140px;
            }
            QComboBox:hover {
                border-color: #adb5bd;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #ced4da;
                selection-background-color: #e7f3ff;
                background: #ffffff;
            }
        """
        )
        self.sort_combo.currentIndexChanged.connect(self._on_sort_changed)
        layout.addWidget(self.sort_combo)

    def _on_search_text_changed(self, text: str) -> None:
        """Handle search input change with debounce."""
        # Debounce: wait 300ms before emitting signal
        self._debounce_timer.stop()
        self._debounce_timer.start(300)

    def _emit_search_query(self) -> None:
        """Emit search query signal after debounce."""
        query = self.search_input.text().strip()
        self.search_query_changed.emit(query)

    def _on_filter_clicked(self, key: str) -> None:
        """Handle filter chip click."""
        # Deactivate all other chips
        for chip_key, chip in self._filter_chips.items():
            if chip_key != key:
                chip.setChecked(False)

        # Activate clicked chip
        self._filter_chips[key].setChecked(True)
        self._current_filter = key
        self.filter_changed.emit(key)

    def _on_sort_changed(self) -> None:
        """Handle sort dropdown change."""
        sort_key = str(self.sort_combo.currentData())
        self.sort_changed.emit(sort_key)

    def update_filter_counts(self, counts: dict[str, int]) -> None:
        """
        Update count badges on filter chips.

        Args:
            counts: Dict with keys 'all', 'unread', 'error', 'warning', 'info'
        """
        for key, chip in self._filter_chips.items():
            count = counts.get(key, 0)
            chip.set_count(count)

    def get_current_filter(self) -> str:
        """Get currently active filter key."""
        return self._current_filter

    def get_search_query(self) -> str:
        """Get current search query."""
        return self.search_input.text().strip()

    def get_sort_key(self) -> str:
        """Get current sort key."""
        return str(self.sort_combo.currentData())
