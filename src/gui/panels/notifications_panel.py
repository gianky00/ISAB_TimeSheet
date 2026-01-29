"""
SyncroJob - Notifications Panel
Pannello per la visualizzazione delle notifiche e Audit Log Dashboard.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.core.notification_manager import NotificationManager
from src.gui.widgets.audit_log_widget import AuditLogWidget
from src.gui.widgets.modern_button import ModernButton
from src.gui.widgets.notification_card import NotificationCard
from src.gui.widgets.notification_group_header import NotificationGroupHeader
from src.gui.widgets.notification_toolbar import NotificationToolbar
from src.utils.helpers import get_asset_path, get_colored_icon


@dataclass
class FilterState:
    """State management for notification filters."""

    levels: list[str] = field(default_factory=lambda: ["all"])
    categories: list[str] = field(default_factory=list)
    priorities: list[str] = field(default_factory=list)
    date_range: Optional[tuple[datetime, datetime]] = None
    show_read: bool = True
    show_unread: bool = True
    show_archived: bool = False
    search_query: str = ""
    sort_by: str = "date_desc"
    group_by: str = "time"  # time, category, priority


# AuditDetailDialog e AuditLogWidget sono stati estratti in:
# src/gui/widgets/audit_log_widget.py


class NotificationsPanel(QWidget):
    """Pannello principale delle notifiche con schede Audit."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_filter = "all"
        self.current_search = ""
        self.current_sort = "date_desc"
        self.manager = NotificationManager.instance()
        self._group_widgets = {}  # Track group headers and their content
        self._cached_filter_result = None  # Cache filtered results
        self._last_filter_state = None  # Track filter state changes
        self._refresh_timer = QTimer()  # Debounce rapid refreshes
        self._refresh_timer.setSingleShot(True)
        self._refresh_timer.timeout.connect(self._do_refresh)
        self._setup_ui()
        self.manager.notifications_updated.connect(self._schedule_refresh)
        self.refresh_notifications()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        self.tabs = QTabWidget()
        self.tabs.setProperty("class", "Level2Tabs")
        main_layout.addWidget(self.tabs)

        # Tab Notifiche
        self.notif_tab = QWidget()
        nl = QVBoxLayout(self.notif_tab)
        nl.setContentsMargins(0, 10, 0, 0)
        nl.setSpacing(10)

        # === NEW: Toolbar con search, filter chips, sort ===
        self.toolbar = NotificationToolbar()
        self.toolbar.search_query_changed.connect(self._on_search_changed)
        self.toolbar.filter_changed.connect(self._on_filter_changed)
        self.toolbar.sort_changed.connect(self._on_sort_changed)
        nl.addWidget(self.toolbar)

        # Action buttons row (Segna letti, Svuota)
        actions_layout = QHBoxLayout()
        actions_layout.addStretch()

        mark_read = ModernButton(
            "Segna letti",
            variant=ModernButton.Variant.GHOST,
            size=ModernButton.Size.SMALL,
        )
        mark_read.setMinimumWidth(120)
        mark_read.setFixedHeight(40)
        mark_read.clicked.connect(self.manager.mark_all_as_read)
        actions_layout.addWidget(mark_read)

        clear = ModernButton(
            "Svuota", variant=ModernButton.Variant.DANGER, size=ModernButton.Size.SMALL
        )
        clear.setMinimumWidth(120)
        clear.setFixedHeight(40)
        clear.clicked.connect(self._clear_notifications)
        actions_layout.addWidget(clear)
        nl.addLayout(actions_layout)

        # Scroll area per notifiche
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet(
            "QScrollArea { background: transparent; border: none; }"
        )
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setSpacing(12)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.addStretch()
        self.scroll.setWidget(self.scroll_content)
        nl.addWidget(self.scroll)

        self.tabs.addTab(
            self.notif_tab,
            get_colored_icon(get_asset_path(Icons.BELL), "#546E7A"),
            "Notifiche",
        )

        # Tab Audit
        self.audit_tab = AuditLogWidget()
        self.tabs.addTab(
            self.audit_tab,
            get_colored_icon(get_asset_path(Icons.SHIELD), "#546E7A"),
            "Audit",
        )
        self.tabs.currentChanged.connect(self._on_tab_changed)

    def _on_tab_changed(self, index):
        if self.tabs.tabText(index) == "Audit":
            self.audit_tab.refresh()

    def _on_search_changed(self, query: str):
        """Handle search query change."""
        self.current_search = query.lower()
        self._invalidate_cache()
        self._schedule_refresh()

    def _on_filter_changed(self, filter_key: str):
        """Handle filter chip change."""
        self.current_filter = filter_key
        self._invalidate_cache()
        self._schedule_refresh()

    def _on_sort_changed(self, sort_key: str):
        """Handle sort dropdown change."""
        self.current_sort = sort_key
        self._invalidate_cache()
        self._schedule_refresh()

    def _schedule_refresh(self):
        """Schedule refresh with debounce to avoid rapid updates."""
        self._refresh_timer.stop()
        self._refresh_timer.start(50)  # 50ms debounce

    def _invalidate_cache(self):
        """Invalidate cached filter results."""
        self._cached_filter_result = None
        self._last_filter_state = None

    def _do_refresh(self):
        """Actual refresh implementation (called after debounce)."""
        self.refresh_notifications()

    def _clear_notifications(self):
        if (
            QMessageBox.question(self, "Conferma", "Vuoi svuotare i messaggi?")
            == QMessageBox.StandardButton.Yes
        ):
            self.manager.clear_all()

    def refresh_notifications(self):
        """Refresh notifications list with filtering, search, sorting and grouping (optimized)."""
        # Generate cache key from current filter state
        cache_key = (
            self.current_filter,
            self.current_search,
            self.current_sort,
            len(self.manager.notifications),  # Invalidate if data changes
        )

        # Use cached result if available
        if (
            self._last_filter_state == cache_key
            and self._cached_filter_result is not None
        ):
            notifs = self._cached_filter_result
        else:
            notifs = self._get_filtered_sorted_notifications()

            # Cache result
            self._cached_filter_result = notifs
            self._last_filter_state = cache_key

        # Update toolbar counts (lightweight operation)
        self._update_toolbar_counts()

        # Clear existing widgets ONLY if needed
        self._clear_scroll_area()

        # Show empty state if no notifications
        if not notifs:
            self._show_empty_state()
            return

        # Disable animations if too many notifications (performance optimization)
        disable_animations = len(notifs) > 30

        # Group notifications by time
        grouped = self._group_notifications_by_time(notifs)

        # Render groups
        self._render_groups(grouped, disable_animations)

    def _get_filtered_sorted_notifications(self) -> List[Dict[str, Any]]:
        """Restituisce le notifiche filtrate e ordinate."""
        # Get notifications based on filter
        if self.current_filter == "unread":
            notifs = self.manager.get_notifications(filter_unread=True)
        else:
            notifs = self.manager.get_notifications(filter_unread=False)

        # Apply level filter
        if self.current_filter == "error":
            notifs = [n for n in notifs if n.get("level") == "error"]
        elif self.current_filter == "warning":
            notifs = [n for n in notifs if n.get("level") == "warning"]
        elif self.current_filter == "info":
            notifs = [n for n in notifs if n.get("level") == "info"]

        # Apply search filter
        if self.current_search:
            notifs = [
                n
                for n in notifs
                if self.current_search in n.get("title", "").lower()
                or self.current_search in n.get("message", "").lower()
            ]

        # Sort notifications
        return self._sort_notifications(notifs)

    def _render_groups(
        self, grouped: Dict[str, Dict[str, Any]], disable_animations: bool
    ):
        """Renderizza i gruppi di notifiche nella scroll area."""
        for group_key, group_data in grouped.items():
            if not group_data["notifications"]:
                continue

            # Create group header
            header = NotificationGroupHeader(
                title=group_data["title"],
                group_key=group_key,
                count=len(group_data["notifications"]),
                icon=group_data["icon"],
            )
            header.toggled.connect(self._on_group_toggled)
            self.scroll_layout.insertWidget(self.scroll_layout.count() - 1, header)

            # Create container for group's notifications
            group_container = QWidget()
            group_layout = QVBoxLayout(group_container)
            group_layout.setContentsMargins(0, 0, 0, 0)
            group_layout.setSpacing(8)

            for notif in group_data["notifications"]:
                card = NotificationCard(notif, disable_animations=disable_animations)
                card.card_deleted.connect(self._invalidate_and_refresh)
                group_layout.addWidget(card)

            self.scroll_layout.insertWidget(
                self.scroll_layout.count() - 1, group_container
            )
            self._group_widgets[group_key] = {
                "header": header,
                "container": group_container,
            }

    def _clear_scroll_area(self):
        """Efficiently clear scroll area widgets."""
        # Clear group widgets tracking
        self._group_widgets.clear()

        # Remove all widgets except stretch
        while self.scroll_layout.count() > 1:
            item = self.scroll_layout.takeAt(0)
            if item and item.widget():
                widget = item.widget()
                widget.setParent(None)
                widget.deleteLater()

    def _invalidate_and_refresh(self):
        """Invalidate cache and schedule refresh."""
        self._invalidate_cache()
        self._schedule_refresh()

    def _sort_notifications(self, notifs: list) -> list:
        """Sort notifications based on current_sort."""
        if self.current_sort == "date_desc":
            return sorted(notifs, key=lambda n: n.get("timestamp", ""), reverse=True)
        elif self.current_sort == "date_asc":
            return sorted(notifs, key=lambda n: n.get("timestamp", ""))
        elif self.current_sort == "priority":
            priority_map = {"high": 3, "medium": 2, "low": 1}
            return sorted(
                notifs,
                key=lambda n: priority_map.get(n.get("priority", "low"), 1),
                reverse=True,
            )
        elif self.current_sort == "level":
            level_map = {"error": 4, "warning": 3, "success": 2, "info": 1}
            return sorted(
                notifs,
                key=lambda n: level_map.get(n.get("level", "info"), 1),
                reverse=True,
            )
        return notifs

    def _group_notifications_by_time(self, notifs: list) -> Dict[str, Dict[str, Any]]:
        """Group notifications by time buckets."""
        now = datetime.now()
        # Initialize with explicit types to satisfy mypy
        groups: Dict[str, Dict[str, Any]] = {
            "pinned": {"title": "Fissate", "icon": "📌", "notifications": []},
            "today": {"title": "Oggi", "icon": "📅", "notifications": []},
            "yesterday": {"title": "Ieri", "icon": "📆", "notifications": []},
            "week": {"title": "Ultimi 7 giorni", "icon": "📂", "notifications": []},
            "older": {"title": "Più vecchie", "icon": "🗂️", "notifications": []},
        }

        for notif in notifs:
            # Check if pinned
            if notif.get("pinned", False):
                # Explicit list append
                groups["pinned"]["notifications"].append(notif)
                continue

            try:
                ts = datetime.fromisoformat(notif.get("timestamp", ""))
                diff = now - ts

                if diff.days == 0:
                    groups["today"]["notifications"].append(notif)
                elif diff.days == 1:
                    groups["yesterday"]["notifications"].append(notif)
                elif diff.days <= 7:
                    groups["week"]["notifications"].append(notif)
                else:
                    groups["older"]["notifications"].append(notif)
            except Exception:
                groups["older"]["notifications"].append(notif)

        return groups

    def _on_group_toggled(self, group_key: str, is_expanded: bool):
        """Handle group header toggle."""
        if group_key in self._group_widgets:
            container = self._group_widgets[group_key]["container"]
            container.setVisible(is_expanded)

    def _update_toolbar_counts(self):
        """Update filter chip counts in toolbar (optimized)."""
        all_notifs = self.manager.notifications  # Direct access, already sorted

        # Count in single pass
        counts = {
            "all": len(all_notifs),
            "unread": 0,
            "error": 0,
            "warning": 0,
            "info": 0,
        }

        for n in all_notifs:
            if not n.get("read", False):
                counts["unread"] += 1

            level = n.get("level", "info")
            if level in counts:
                counts[level] += 1

        self.toolbar.update_filter_counts(counts)

    def _show_empty_state(self):
        """Show appropriate empty state based on current filter."""
        empty_widget = QWidget()
        empty_layout = QVBoxLayout(empty_widget)
        empty_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_layout.setSpacing(16)

        # Icon
        if self.current_filter == "all":
            icon_text = "📭"
            title = "Nessuna notifica"
            subtitle = "Le tue notifiche appariranno qui"
        elif self.current_filter == "unread":
            icon_text = "✅"
            title = "Tutto a posto!"
            subtitle = "Nessuna notifica da leggere"
        elif self.current_filter == "error":
            icon_text = "🎉"
            title = "Sistema funzionante!"
            subtitle = "Nessun errore registrato"
        else:
            icon_text = "📭"
            title = "Nessuna notifica"
            subtitle = f"Nessuna notifica di tipo {self.current_filter}"

        icon_lbl = QLabel(icon_text)
        icon_lbl.setStyleSheet("font-size: 64px; border: none;")
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_layout.addWidget(icon_lbl)

        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: #495057; border: none;"
        )
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_layout.addWidget(title_lbl)

        subtitle_lbl = QLabel(subtitle)
        subtitle_lbl.setStyleSheet("font-size: 14px; color: #6c757d; border: none;")
        subtitle_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        empty_layout.addWidget(subtitle_lbl)

        empty_widget.setStyleSheet("background: transparent;")
        self.scroll_layout.insertWidget(0, empty_widget)
