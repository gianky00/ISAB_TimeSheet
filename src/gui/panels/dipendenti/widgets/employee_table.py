"""
SyncroJob - Employee Table Widget
Widget specializzato per la visualizzazione della griglia anagrafica dipendenti.
"""

import logging
from typing import Any

from PyQt6.QtCore import QPoint, Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QMenu,
    QSizePolicy,
    QTableView,
    QWidget,
)

from src.core.constants import Icons
from src.gui.panels.dipendenti.shared import ColoredDotDelegate
from src.gui.styles import COLORS
from src.utils.helpers import get_asset_path, get_colored_icon

logger = logging.getLogger(__name__)


class EmployeeTableView(QTableView):
    """Tabella specializzata per l'anagrafica dipendenti con delegati e menu contestuale."""

    monitoring_toggled = pyqtSignal(str, bool)  # id_risorsa, enable
    employee_selected = pyqtSignal(int)  # row_idx

    def __init__(self, model: Any, parent: QWidget | None = None) -> None:
        """
        Inizializza la tabella dipendenti.

        Args:
            model: Il modello dati (FastTableModel).
            parent: Widget genitore opzionale.
        """
        super().__init__(parent)
        self.setModel(model)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Configura il comportamento della tabella, i delegati e lo stile."""
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

    def configure_columns(self, widths: list[int]) -> None:
        """
        Configura la larghezza fissa delle colonne.

        Args:
            widths: Lista di interi rappresentanti i pixel per ogni colonna.
        """
        header = self.horizontalHeader()
        if not header:
            return
        for i, w in enumerate(widths):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Fixed)
            self.setColumnWidth(i, w)
        total_w = sum(widths) + 20
        self.setFixedWidth(total_w)

    def _on_selection_internal(self, selected: Any, deselected: Any) -> None:
        """Emette il segnale di selezione dipendente quando cambia la riga attiva."""
        sel_model = self.selectionModel()
        if not sel_model:
            return
        indexes = sel_model.selectedRows()
        if indexes:
            self.employee_selected.emit(indexes[0].row())

    def _show_context_menu(self, position: QPoint) -> None:
        """
        Mostra il menu contestuale per attivare/disattivare il monitoraggio del dipendente.

        Args:
            position: Posizione del clic del mouse.
        """
        from PyQt6.QtGui import QAction  # noqa: PLC0415

        sel_model = self.selectionModel()
        if not sel_model:
            return

        indexes = sel_model.selectedRows()
        if not indexes:
            return

        row_idx = indexes[0].row()
        model = self.model()
        if not model:
            return

        # Recupero metadati via UserRole (senza query SQL sincrona)
        metadata = model.data(model.index(row_idx, 0), Qt.ItemDataRole.UserRole)

        if not metadata or "id_risorsa" not in metadata:
            return

        id_risorsa = metadata["id_risorsa"]
        is_monitored = metadata.get("is_monitored", True)

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
                "[OK] Riattiva monitoraggio",
                self,
            )
            act.triggered.connect(lambda: self.monitoring_toggled.emit(id_risorsa, True))

        menu.addAction(act)
        viewport = self.viewport()
        if viewport:
            viewport.update()
            menu.exec(viewport.mapToGlobal(position))
