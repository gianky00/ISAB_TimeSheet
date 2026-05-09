# mypy: disable-error-code="no-untyped-def, no-untyped-call, unused-ignore, arg-type"
"""
SyncroJob - PDL Programmazione Table Widget
Componente specializzato per la visualizzazione della griglia di programmazione.
"""

import logging
from typing import Any

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
)

from src.core.database.pdl_queries import PDLQueries
from src.gui.styles import COLORS
from src.gui.widgets.core_widgets import StandardTable
from src.gui.widgets.pdl.status_bar_widget import ProgrammingStatusWidget

logger = logging.getLogger(__name__)


class ProgrammazioneTableWidget(StandardTable):
    """Tabella specializzata per la programmazione PDL con supporto per espansione Timeline."""

    row_expanded = Signal(int, bool)  # row, is_expanded
    selection_changed_custom = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(0, 0, parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.setColumnCount(12)
        self.setAlternatingRowColors(True)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.setStyleSheet(f"QTableWidget {{ border: none; background-color: {COLORS['bg_white']}; }}")

        v_header = self.verticalHeader()
        if v_header:
            v_header.setVisible(False)
            v_header.setDefaultSectionSize(42)

        h_header = self.horizontalHeader()
        if h_header:
            h_header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
            h_header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
            h_header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
            h_header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
            h_header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
            h_header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
            h_header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
            for i in range(5, 12):
                h_header.setSectionResizeMode(i, QHeaderView.ResizeMode.Fixed)
                self.setColumnWidth(i, 85)

        self.cellDoubleClicked.connect(self._handle_double_click)
        self.cellClicked.connect(self.selection_changed_custom.emit)

    def _handle_double_click(self, row: int, column: int) -> None:
        from src.gui.widgets.pdl_timeline import PDLTimelineWidget

        # Se la riga sotto  già una timeline, la rimuoviamo (collasso)
        next_row = row + 1
        if next_row < self.rowCount():
            next_widget = self.cellWidget(next_row, 0)
            if isinstance(next_widget, PDLTimelineWidget):
                self.removeRow(next_row)
                self.row_expanded.emit(row, False)
                return

        # Espansione: recupera dati e inserisci riga
        pdl_item = self.item(row, 3)
        if not pdl_item:
            return
        pdl_code = pdl_item.text()

        self.insertRow(next_row)
        try:
            interventions = PDLQueries.get_pdl_interventions(pdl_code)
        except Exception as e:
            logger.exception(f"Errore timeline PDL {pdl_code}", exc=e)
            interventions = []

        timeline = PDLTimelineWidget(interventions)
        self.setSpan(next_row, 0, 1, self.columnCount())
        self.setCellWidget(next_row, 0, timeline)
        self.setRowHeight(next_row, timeline.sizeHint().height())
        self.row_expanded.emit(row, True)

    def populate_results(self, results: list[dict[str, Any]], today_idx: int = -1) -> None:
        """Popola la tabella con i risultati forniti."""
        self.setRowCount(len(results))
        for row_idx, res in enumerate(results):
            self.setItem(row_idx, 0, QTableWidgetItem(res["richiedente"]))
            self.setItem(row_idx, 1, QTableWidgetItem(res.get("area", "")))
            self.setItem(row_idx, 2, QTableWidgetItem(res.get("unita", "")))

            pdl_item = QTableWidgetItem(res["pdl"])
            pdl_item.setData(Qt.ItemDataRole.UserRole, res["pdl"])
            pdl_item.setToolTip("Doppio click per cronologiàinterventi")
            self.setItem(row_idx, 3, pdl_item)

            self.setItem(row_idx, 4, QTableWidgetItem(res.get("descrizione", "")))

            prog_list = res["programmazione"]
            for i, prog in enumerate(prog_list):
                is_full = prog["tcl"] and prog["tgo"]
                conn_left = i > 0 and is_full and prog_list[i - 1]["tcl"] and prog_list[i - 1]["tgo"]
                conn_right = (
                    i < len(prog_list) - 1 and is_full and prog_list[i + 1]["tcl"] and prog_list[i + 1]["tgo"]
                )

                status_widget = ProgrammingStatusWidget(
                    prog["tcl"],
                    prog["tgo"],
                    connect_left=conn_left,
                    connect_right=conn_right,
                    is_today=(i == today_idx),
                )
                self.setCellWidget(row_idx, 5 + i, status_widget)
