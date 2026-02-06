"""
SyncroJob - Audit Log Widget
Widget riutilizzato per la visualizzazione dell'audit log.
Refactoring modulare V2.
"""

import logging

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from src.core.audit_manager import AuditManager
from src.core.constants import Icons
from src.gui.dialogs.audit_detail_dialog import AuditDetailDialog
from src.gui.models.audit_model import AuditTableModel
from src.gui.widgets.audit.audit_filter_bar import AuditFilterBar
from src.gui.widgets.audit.audit_pagination_bar import AuditPaginationBar
from src.utils.helpers import get_asset_path, get_colored_icon

logger = logging.getLogger(__name__)


class AuditLogWidget(QWidget):
    """
    Dashboard avanzata per l'Audit Log V2.
    Widget modulare con filtri, paginazione e Live Mode.
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
        self.filter_bar = AuditFilterBar()
        self.filter_bar.filters_applied.connect(lambda: self.refresh(reset_page=True))
        layout.addWidget(self.filter_bar)

        # --- DATA GRID ---
        self.table_view = QTableView()
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.table_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_view.verticalHeader().setVisible(False)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.setStyleSheet(
            """
            QTableView {
                border: 1px solid #dee2e6; border-radius: 6px;
                background-color: white; gridline-color: #f1f3f5;
            }
            QHeaderView::section {
                background-color: #e9ecef; padding: 8px; border: none;
                font-weight: bold; color: #495057;
            }
        """
        )

        self.model = AuditTableModel([])
        self.table_view.setModel(self.model)
        self.table_view.doubleClicked.connect(self._on_row_double_click)
        layout.addWidget(self.table_view)

        # --- PAGINATION ---
        self.pagination_bar = AuditPaginationBar()
        self.pagination_bar.page_changed.connect(self._on_page_changed)
        layout.addWidget(self.pagination_bar)

    def _load_categories(self):
        cats = self.manager.get_categories()
        self.filter_bar.set_categories(cats)

    def _toggle_live_mode(self, state):
        is_live = state in (Qt.CheckState.Checked, 2)  # Supporta sia Enum che Int
        if is_live:
            self.refresh(reset_page=True)
            self.live_timer.start()
        else:
            self.live_timer.stop()

        self.filter_bar.set_enabled_dates(not is_live)
        self.pagination_bar.setEnabled(not is_live)
        if not is_live:
            self.refresh()

    def _on_live_refresh(self):
        self.refresh(reset_page=True)

    def _on_page_changed(self, delta):
        self.current_page += delta
        self.refresh()

    def refresh(self, reset_page=False):
        if reset_page:
            self.current_page = 0

        filters = self.filter_bar.get_filters()
        logs, total = self.manager.get_filtered_logs(
            **filters,
            limit=self.PAGE_SIZE,
            offset=self.current_page * self.PAGE_SIZE,
        )

        self.total_logs = total
        self.model.update_data(logs)
        self.table_view.resizeColumnsToContents()
        self.pagination_bar.update_state(
            self.current_page, self.total_logs, self.PAGE_SIZE
        )

        if self.current_page == 0:
            self._check_integrity()

    def _check_integrity(self):
        valid = self.manager.verify_integrity()
        color = "#198754" if valid else "#dc3545"
        text = "Integro" if valid else "Legacy/Manomesso"
        icon = Icons.SHIELD if valid else Icons.ALERT_TRIANGLE

        self.integrity_icon.setPixmap(
            get_colored_icon(get_asset_path(icon), color).pixmap(18, 18)
        )
        self.integrity_lbl.setText(text)
        self.integrity_lbl.setStyleSheet(f"color: {color}; font-weight: bold;")

    def _on_row_double_click(self, index):
        log = self.model.get_log_at(index.row())
        if log:
            AuditDetailDialog(log, self).exec()
