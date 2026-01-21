"""
SyncroJob - Notifications Panel
Pannello per la visualizzazione delle notifiche e Audit Log Dashboard.
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from PyQt6.QtCore import QDate, Qt, QTimer
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QComboBox,
    QDialog,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QTableView,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from src.core.audit_manager import AuditManager
from src.core.constants import Icons
from src.core.notification_manager import NotificationManager
from src.gui.models.audit_model import AuditTableModel
from src.gui.widgets.calendar_date_edit import CalendarDateEdit
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


class AuditDetailDialog(QDialog):
    """Dialog per visualizzare i dettagli completi di un log."""

    def __init__(self, log_data, parent=None):
        super().__init__(parent)
        self.log_data = log_data  # Save for copy
        self.setWindowTitle("Dettagli Audit Log")
        self.setMinimumSize(700, 600)
        self._setup_ui(log_data)

    def _setup_ui(self, data):
        layout = QVBoxLayout(self)

        # Header Info
        ts = data.get("timestamp", "-")
        with suppress(ValueError):
            dt = datetime.fromisoformat(ts)
            ts = dt.strftime("%d/%m/%Y %H:%M:%S")

        dur_ms = data.get("duration_ms", 0) or 0
        dur_str = f"{dur_ms}ms" if dur_ms < 1000 else f"{dur_ms / 1000:.2f}s"

        err_code = data.get("error_code") or "Nessuno"
        module = data.get("module") or "Generico"

        info_text = f"""
        <table style="font-size: 14px; margin-bottom: 10px;" cellspacing="5">
            <tr><td><b>Data:</b></td><td>{ts}</td><td><b>Modulo:</b></td><td>{module}</td></tr>
            <tr><td><b>Utente:</b></td><td>{data.get("user_id", "-")}</td><td><b>Durata:</b></td><td>{dur_str}</td></tr>
            <tr><td><b>Azione:</b></td><td>{data.get("action", "-")}</td><td><b>Cod. Errore:</b></td><td>{err_code}</td></tr>
            <tr><td><b>Entità:</b></td><td>{data.get("entity", "-")}</td><td><b>Stato:</b></td><td>{data.get("status", "-")}</td></tr>
        </table>
        """
        lbl = QLabel(info_text)
        lbl.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(lbl)

        # JSON Viewer
        layout.addWidget(QLabel("<b>Dettagli Tecnici (JSON):</b>"))

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setStyleSheet(
            "font-family: Consolas, monospace; font-size: 13px; background-color: #f8f9fa;"
        )

        try:
            params_str = data.get("params", "{}")
            if isinstance(params_str, str):
                params_json = json.loads(params_str)
            else:
                params_json = params_str

            pretty_json = json.dumps(params_json, indent=4, ensure_ascii=False)
            self.text_edit.setText(pretty_json)
        except (json.JSONDecodeError, TypeError):
            self.text_edit.setText(str(data.get("params", "-")))

        layout.addWidget(self.text_edit)

        # Buttons Bar
        btn_layout = QHBoxLayout()

        # Copia JSON
        btn_copy = QPushButton("Copia JSON")
        btn_copy.setIcon(get_colored_icon(get_asset_path(Icons.FILE_TEXT), "#000000"))
        btn_copy.clicked.connect(self._copy_to_clipboard)
        btn_copy.setStyleSheet(
            """
            QPushButton {
                background-color: #e9ecef; border: 1px solid #ced4da;
                padding: 8px 15px; border-radius: 4px; font-weight: 600;
            }
            QPushButton:hover { background-color: #dee2e6; }
        """
        )
        btn_layout.addWidget(btn_copy)

        btn_layout.addStretch()

        # Chiudi
        btn_close = QPushButton("Chiudi")
        btn_close.clicked.connect(self.accept)
        btn_close.setStyleSheet(
            """
            QPushButton {
                background-color: #6c757d; color: white; border: none;
                padding: 8px 15px; border-radius: 4px; font-weight: bold;
            }
            QPushButton:hover { background-color: #5c636a; }
        """
        )
        btn_layout.addWidget(btn_close)

        layout.addLayout(btn_layout)

    def _copy_to_clipboard(self):
        cb = QGuiApplication.clipboard()
        cb.setText(self.text_edit.toPlainText())
        QMessageBox.information(self, "Copiato", "Dettagli copiati negli appunti!")


class AuditLogWidget(QWidget):
    """
    Dashboard avanzata per l'Audit Log V2.
    """

    PAGE_SIZE = 50

    def __init__(self, parent=None):
        super().__init__(parent)
        self.manager = AuditManager.instance()
        self.current_page = 0
        self.total_logs = 0

        # Timer per Live View
        self.live_timer = QTimer()
        self.live_timer.setInterval(5000)
        self.live_timer.timeout.connect(self._on_live_refresh)

        self._setup_ui()
        self._load_categories()
        self.refresh()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 0)
        layout.setSpacing(10)

        # --- TOP BAR ---
        top_bar = QHBoxLayout()
        info_lbl = QLabel("Dashboard Operazioni")
        info_lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: #212529;")
        top_bar.addWidget(info_lbl)

        self.integrity_icon = QLabel()
        self.integrity_icon.setFixedSize(18, 18)
        self.integrity_icon.setScaledContents(True)
        top_bar.addWidget(self.integrity_icon)

        self.integrity_lbl = QLabel("Verifica...")
        self.integrity_lbl.setStyleSheet(
            "color: #6c757d; font-size: 13px; font-weight: 600;"
        )
        top_bar.addWidget(self.integrity_lbl)

        top_bar.addStretch()

        self.live_check = QCheckBox("Live Mode")
        self.live_check.setToolTip("Aggiorna automaticamente ogni 5 secondi")
        self.live_check.stateChanged.connect(self._toggle_live_mode)
        top_bar.addWidget(self.live_check)
        layout.addLayout(top_bar)

        # --- FILTER BAR ---
        filter_frame = QFrame()
        filter_frame.setStyleSheet(
            "background-color: #f8f9fa; border-radius: 6px; border: 1px solid #dee2e6;"
        )
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setContentsMargins(10, 10, 10, 10)
        filter_layout.setSpacing(10)

        # Date Range
        self.date_from = CalendarDateEdit()
        self.date_from.setDate(QDate.currentDate().addDays(-7))
        self.date_from.setDisplayFormat("dd/MM/yyyy")
        self.date_from.setMinimumWidth(160)
        self.date_from.setMaximumWidth(200)

        self.date_to = CalendarDateEdit()
        self.date_to.setDate(QDate.currentDate())
        self.date_to.setDisplayFormat("dd/MM/yyyy")
        self.date_to.setMinimumWidth(160)
        self.date_to.setMaximumWidth(200)

        filter_layout.addWidget(QLabel("Dal:"))
        filter_layout.addWidget(self.date_from)
        filter_layout.addWidget(QLabel("Al:"))
        filter_layout.addWidget(self.date_to)

        # Categoria
        self.cat_combo = QComboBox()
        self.cat_combo.addItem("Tutte")
        self.cat_combo.setFixedWidth(150)
        filter_layout.addWidget(self.cat_combo)

        # Livello
        self.level_combo = QComboBox()
        self.level_combo.addItems(
            ["Tutti", "Info (Low)", "Warning (Med)", "Error (High)"]
        )
        self.level_combo.setFixedWidth(130)
        filter_layout.addWidget(self.level_combo)

        # Search
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Cerca nei log...")
        self.search_edit.setStyleSheet(
            "border: 1px solid #ced4da; border-radius: 4px; padding: 4px;"
        )
        filter_layout.addWidget(self.search_edit)

        # Btn Applica
        apply_btn = QPushButton("Filtra")
        apply_btn.setIcon(get_colored_icon(get_asset_path(Icons.SEARCH), "#ffffff"))
        apply_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #0d6efd; color: white; border: none;
                border-radius: 4px; padding: 6px 12px; font-weight: bold;
            }
            QPushButton:hover { background-color: #0b5ed7; }
        """
        )
        apply_btn.clicked.connect(lambda: self.refresh(reset_page=True))
        filter_layout.addWidget(apply_btn)

        layout.addWidget(filter_frame)

        # --- DATA GRID ---
        self.table_view = QTableView()
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.table_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_view.verticalHeader().setVisible(False)
        self.table_view.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Interactive
        )
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.setStyleSheet(
            """
            QTableView {
                border: 1px solid #dee2e6;
                border-radius: 6px;
                background-color: white;
                gridline-color: #f1f3f5;
            }
            QHeaderView::section {
                background-color: #e9ecef;
                padding: 8px;
                border: none;
                font-weight: bold;
                color: #495057;
            }
        """
        )

        self.model = AuditTableModel([])
        self.table_view.setModel(self.model)
        self.table_view.doubleClicked.connect(self._on_row_double_click)
        layout.addWidget(self.table_view)

        # --- PAGINATION ---
        pag_layout = QHBoxLayout()
        self.prev_btn = QPushButton("Precedente")
        self.prev_btn.setEnabled(False)
        self.prev_btn.clicked.connect(self._prev_page)

        self.page_lbl = QLabel("Pagina 1")
        self.page_lbl.setStyleSheet("font-weight: bold;")

        self.next_btn = QPushButton("Successiva")
        self.next_btn.setEnabled(False)
        self.next_btn.clicked.connect(self._next_page)

        pag_layout.addWidget(self.prev_btn)
        pag_layout.addStretch()
        pag_layout.addWidget(self.page_lbl)
        pag_layout.addStretch()
        pag_layout.addWidget(self.next_btn)
        layout.addLayout(pag_layout)

    def _load_categories(self):
        cats = self.manager.get_categories()
        self.cat_combo.addItems(cats)

    def _toggle_live_mode(self, state):
        if state == Qt.CheckState.Checked.value:
            self.refresh(reset_page=True)
            self.live_timer.start()
            self.date_from.setEnabled(False)
            self.date_to.setEnabled(False)
            self.prev_btn.setEnabled(False)
            self.next_btn.setEnabled(False)
        else:
            self.live_timer.stop()
            self.date_from.setEnabled(True)
            self.date_to.setEnabled(True)
            self.refresh()

    def _on_live_refresh(self):
        self.refresh(reset_page=True)

    def refresh(self, reset_page=False):
        if reset_page:
            self.current_page = 0

        start = self.date_from.date().toPyDate()
        end = self.date_to.date().toPyDate()
        start_dt = datetime.combine(start, datetime.min.time())
        end_dt = datetime.combine(end, datetime.max.time())

        cat = self.cat_combo.currentText()
        lvl_idx = self.level_combo.currentIndex()
        levels = None
        if lvl_idx == 1:
            levels = ["low"]
        elif lvl_idx == 2:
            levels = ["medium"]
        elif lvl_idx == 3:
            levels = ["high"]

        search = self.search_edit.text().strip()

        logs, total = self.manager.get_filtered_logs(
            start_date=start_dt,
            end_date=end_dt,
            category=cat,
            levels=levels,
            search_text=search,
            limit=self.PAGE_SIZE,
            offset=self.current_page * self.PAGE_SIZE,
        )

        self.total_logs = total
        self.model.update_data(logs)

        # Smart Resize
        self.table_view.resizeColumnsToContents()
        for i in range(self.model.columnCount() - 1):
            w = self.table_view.columnWidth(i)
            # Aumentiamo il buffer per leggibilità
            self.table_view.setColumnWidth(i, int(w * 1.15) + 15)

        self.table_view.horizontalHeader().setSectionResizeMode(
            self.model.columnCount() - 1, QHeaderView.ResizeMode.Stretch
        )

        self._update_pagination_ui()
        if self.current_page == 0:
            self._check_integrity()

    def _update_pagination_ui(self):
        total_pages = (self.total_logs + self.PAGE_SIZE - 1) // self.PAGE_SIZE
        if total_pages < 1:
            total_pages = 1
        disp = self.current_page + 1
        self.page_lbl.setText(
            f"Pagina {disp} di {total_pages} (Tot: {self.total_logs})"
        )
        self.prev_btn.setEnabled(self.current_page > 0)
        self.next_btn.setEnabled(disp < total_pages)

    def _next_page(self):
        self.current_page += 1
        self.refresh()

    def _prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.refresh()

    def _check_integrity(self):
        valid = self.manager.verify_integrity()
        if valid:
            self.integrity_icon.setPixmap(
                get_colored_icon(get_asset_path(Icons.SHIELD), "#198754").pixmap(18, 18)
            )
            self.integrity_lbl.setText("Integro")
            self.integrity_lbl.setStyleSheet("color: #198754; font-weight: bold;")
        else:
            self.integrity_icon.setPixmap(
                get_colored_icon(
                    get_asset_path(Icons.ALERT_TRIANGLE), "#dc3545"
                ).pixmap(18, 18)
            )
            # Fallimento atteso per vecchi record dopo update schema
            self.integrity_lbl.setText("Legacy/Manomesso")
            self.integrity_lbl.setStyleSheet("color: #dc3545; font-weight: bold;")

    def _on_row_double_click(self, index):
        log = self.model.get_log_at(index.row())
        if log:
            AuditDetailDialog(log, self).exec()


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
        from datetime import datetime

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
