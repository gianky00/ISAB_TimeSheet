"""
SyncroJob - Employee Table Widget
Widget specializzato per la visualizzazione della griglia anagrafica dipendenti.
"""

import logging

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QAbstractItemView, QHeaderView, QMenu, QSizePolicy, QTableView

from src.core.constants import Icons
from src.core.database import db_manager
from src.gui.panels.dipendenti.shared import ColoredDotDelegate
from src.gui.styles import COLORS
from src.utils.helpers import get_asset_path, get_colored_icon

logger = logging.getLogger(__name__)


class EmployeeTableView(QTableView):
    """Tabella specializzata per l'anagrafica dipendenti con delegati e menu contestuale."""

    monitoring_toggled = pyqtSignal(str, bool)  # id_risorsa, enable
    employee_selected = pyqtSignal(int)  # row_idx

    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.setModel(model)
        self._setup_ui()

    def _setup_ui(self):
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        v_header = self.verticalHeader()
        if v_header:
            v_header.setVisible(False)

        # Menu contestuale
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

        # Delegato per pallino stato
        self.setItemDelegateForColumn(0, ColoredDotDelegate(self))

        # Connessione selezione
        if sel_model := self.selectionModel():
            sel_model.selectionChanged.connect(self._on_selection_internal)

        # Styling
        self.setStyleSheet(f"""
            QTableView {{
                border: 1px solid {COLORS["border_light"]};
                border-radius: 8px;
                background-color: {COLORS["bg_white"]};
            }}
        """)

    def configure_columns(self, widths: list[int]):
        header = self.horizontalHeader()
        if not header:
            return
        for i, w in enumerate(widths):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Fixed)
            self.setColumnWidth(i, w)
        total_w = sum(widths) + 20
        self.setFixedWidth(total_w)

    def _on_selection_internal(self, selected, _):
        sel_model = self.selectionModel()
        if not sel_model:
            return
        indexes = sel_model.selectedRows()
        if indexes:
            self.employee_selected.emit(indexes[0].row())

    def _show_context_menu(self, position):
        from PyQt6.QtGui import QAction

        sel_model = self.selectionModel()
        if not sel_model:
            return

        indexes = sel_model.selectedRows()
        if not indexes:
            return

        row_idx = indexes[0].row()
        model = self.model()
        if not hasattr(model, "_data"):
            return

        id_risorsa = model._data[row_idx][1]  # type: ignore

        query = "SELECT monitoraggio_attivo FROM dipendenti WHERE id_risorsa = ?"
        result = db_manager.execute_query(db_manager.DB_DIPENDENTI, query, (id_risorsa,))
        is_monitored = result[0][0] if result and result[0][0] is not None else 1

        menu = QMenu(self)
        if is_monitored:
            act = QAction(
                get_colored_icon(get_asset_path(Icons.X_CIRCLE), COLORS["error_red"]),
                "🚫 Escludi da monitoraggio",
                self,
            )
            act.triggered.connect(lambda: self.monitoring_toggled.emit(id_risorsa, False))
        else:
            act = QAction(
                get_colored_icon(get_asset_path(Icons.CHECK_CIRCLE), COLORS["success_dark"]),
                "✅ Riattiva monitoraggio",
                self,
            )
            act.triggered.connect(lambda: self.monitoring_toggled.emit(id_risorsa, True))

        menu.addAction(act)
        viewport = self.viewport()
        if viewport:
            viewport.update()
            menu.exec(viewport.mapToGlobal(position))
