"""SyncroJob - Audit Log Widget.

Widget riutilizzato per la visualizzazione dell'audit log.
Refactoring modulare V2.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import shiboken6
from PySide6.QtCore import (
    QModelIndex,
    Qt,
    QThreadPool,
    QTimer,
    Slot,
)
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFrame,
    QHBoxLayout,
    QLabel,
    QTableView,
    QVBoxLayout,
    QWidget,
)

if TYPE_CHECKING:
    from PySide6.QtGui import QShowEvent

from src.core.audit_manager import AuditManager
from src.core.constants import Icons
from src.gui.dialogs.audit_detail_dialog import AuditDetailDialog
from src.gui.models.audit_model import AuditTableModel
from src.gui.styles import COLORS
from src.gui.widgets.audit.audit_filter_bar import AuditFilterBar
from src.gui.widgets.audit.audit_pagination_bar import AuditPaginationBar
from src.gui.widgets.core_widgets import (
    StandardCheckBox,
)
from src.gui.widgets.modern_card import ModernCard
from src.gui.workers.integrity_worker import IntegrityWorker
from src.utils.helpers import get_asset_path, get_colored_icon

logger = logging.getLogger(__name__)


class AuditLogWidget(QWidget):
    """Dashboard avanzata per l'Audit Log V2.

    Widget modulare con filtri, paginazione e Live Mode.
    """

    PAGE_SIZE = 50

    def __init__(self, parent: QWidget | None = None) -> None:
        """Inizializza il widget."""
        super().__init__(parent)
        self.manager = AuditManager.instance()
        self.current_page = 0
        self.total_logs = 0
        self._first_refresh_done = False

        # Timer per Live View
        self.live_timer = QTimer()
        self.live_timer.setInterval(5000)
        self.live_timer.timeout.connect(self._on_live_refresh)

        self._setup_ui()
        self._load_categories()
        # Il refresh iniziale viene differito a showEvent per non bloccare lo startup

    def showEvent(self, event: QShowEvent) -> None:
        """Esegue il primo refresh solo quando il widget diventa visibile."""
        super().showEvent(event)
        if not self._first_refresh_done:
            self._first_refresh_done = True
            QTimer.singleShot(50, self.refresh)

    def _setup_ui(self) -> None:
        """Configura l'interfaccia utente."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        self._setup_header(layout)
        self._setup_filter_bar(layout)
        self._setup_data_grid(layout)
        self._setup_pagination(layout)

    def _setup_header(self, layout: QVBoxLayout) -> None:
        """Configura l'intestazione superiore."""
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 10)

        title_v = QVBoxLayout()
        title_v.setSpacing(2)
        title = QLabel("Dashboard Operazioni")
        title.setStyleSheet(f"font-size: 24px; font-weight: 900; color: {COLORS['text_dark']};")

        status_h = QHBoxLayout()
        status_h.setSpacing(8)
        self.integrity_icon = QLabel()
        self.integrity_icon.setFixedSize(16, 16)
        status_h.addWidget(self.integrity_icon)

        self.integrity_lbl = QLabel("Verifica integrità...")
        self.integrity_lbl.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 13px; font-weight: 600;")
        status_h.addWidget(self.integrity_lbl)
        status_h.addStretch()

        title_v.addWidget(title)
        title_v.addLayout(status_h)
        header_layout.addLayout(title_v)
        header_layout.addStretch()

        self.live_check = StandardCheckBox("Live Mode")
        self.live_check.setToolTip("Aggiorna automaticamente ogni 5 secondi")
        self.live_check.setStyleSheet(f"color: {COLORS['text_dark']}; font-weight: 600; font-size: 13px;")
        self.live_check.stateChanged.connect(self._toggle_live_mode)
        header_layout.addWidget(self.live_check, alignment=Qt.AlignmentFlag.AlignVCenter)

        layout.addLayout(header_layout)

    def _setup_filter_bar(self, layout: QVBoxLayout) -> None:
        """Inizializza la barra dei filtri."""
        self.filter_bar = AuditFilterBar()
        self.filter_bar.filters_applied.connect(lambda: self.refresh(reset_page=True))
        layout.addWidget(self.filter_bar)

    def _setup_data_grid(self, layout: QVBoxLayout) -> None:
        """Inizializza la tabella dei dati."""
        self.table_card = ModernCard(elevation=12)
        table_layout = QVBoxLayout(self.table_card)
        table_layout.setContentsMargins(5, 5, 5, 5)

        self.table_view = QTableView()
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_view.setFrameShape(QFrame.Shape.NoFrame)

        if v_header := self.table_view.verticalHeader():
            v_header.setVisible(False)
        if h_header := self.table_view.horizontalHeader():
            h_header.setStretchLastSection(True)

        self.model = AuditTableModel([])
        self.table_view.setModel(self.model)
        self.table_view.doubleClicked.connect(self._on_row_double_click)

        table_layout.addWidget(self.table_view)
        layout.addWidget(self.table_card)

    def _setup_pagination(self, layout: QVBoxLayout) -> None:
        """Inizializza la barra di paginazione."""
        self.pagination_bar = AuditPaginationBar()
        self.pagination_bar.page_changed.connect(self._on_page_changed)
        layout.addWidget(self.pagination_bar)

    def _load_categories(self) -> None:
        """Carica le categorie dal manager."""
        cats = self.manager.get_categories()
        self.filter_bar.set_categories(cats)

    def _toggle_live_mode(self, state: int | Qt.CheckState) -> None:
        """Attiva o disattiva la modalità live.

        Args:
          state: Stato della checkbox.
        """
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

    @Slot()
    def _on_live_refresh(self) -> None:
        """Esegue il refresh periodico in modalità live."""
        if shiboken6.isValid(self):
            self.refresh(reset_page=True)

    def _on_page_changed(self, delta: int) -> None:
        """Gestisce il cambio pagina.

        Args:
          delta: Spostamento pagina (+1 o -1).
        """
        self.current_page += delta
        self.refresh()

    def refresh(self, reset_page: bool = False) -> None:
        """Rinfresca i dati visualizzati applicando i filtri correnti.

        Args:
          reset_page: Se True, torna alla prima pagina.
        """
        if not shiboken6.isValid(self):
            return

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
        QTimer.singleShot(0, lambda: self.table_view.resizeColumnsToContents() if self.table_view else None)
        self.pagination_bar.update_state(self.current_page, self.total_logs, self.PAGE_SIZE)

        if self.current_page == 0:
            self._check_integrity()

    def _check_integrity(self) -> None:
        """Verifica l'integrità dei log in background e aggiorna l'interfaccia tramite segnali."""
        self.integrity_lbl.setText("Verifica integrità in corso...")
        self.integrity_lbl.setStyleSheet(f"color: {COLORS['text_muted']}; font-weight: 600;")

        worker = IntegrityWorker(self.manager)
        worker.signals.finished.connect(self._on_integrity_checked)
        if pool := QThreadPool.globalInstance():
            pool.start(worker)

    @Slot(bool)
    def _on_integrity_checked(self, valid: bool) -> None:
        """Callback al termine della verifica in background."""
        if not shiboken6.isValid(self):
            return

        color = COLORS["success_dark"] if valid else COLORS["error_red"]
        text = "Integro" if valid else "Legacy/Manomesso"
        icon = Icons.SHIELD if valid else Icons.ALERT_TRIANGLE

        self.integrity_icon.setPixmap(get_colored_icon(get_asset_path(icon), color).pixmap(18, 18))
        self.integrity_lbl.setText(text)
        self.integrity_lbl.setStyleSheet(f"color: {color}; font-weight: bold;")

    @Slot(QModelIndex)
    def _on_row_double_click(self, index: QModelIndex) -> None:
        """Gestisce il doppio click su una riga.

        Args:
          index: Indice della cella cliccata.
        """
        log = self.model.get_log_at(index.row())
        if log:
            AuditDetailDialog(log, self).exec()
