"""
SyncroJob - Scarico Ore Table View
Widget tabellare specializzato per grandi volumi di dati con filtri Excel-style.
"""

import operator
from contextlib import suppress
from typing import Any

from PyQt6.QtCore import QItemSelection, Qt, pyqtSignal
from PyQt6.QtGui import QKeySequence
from PyQt6.QtWidgets import QApplication, QHeaderView, QTableView, QWidget

from src.gui.components.scarico_ore import FilterHeaderView, ScaricoOreTableModel


class ScaricoOreTableView(QTableView):
    """TableView ottimizzata per lo Scarico Ore con supporto a filtri e copia TSV."""

    selection_totals_changed = pyqtSignal(float)
    filter_changed = pyqtSignal(int, list)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._saved_selection_real_ids: set[int] = set()
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.setSortingEnabled(True)

        # Header filtrabile
        header = FilterHeaderView(Qt.Orientation.Horizontal, self)
        self.setHorizontalHeader(header)
        header.filterChanged.connect(self.filter_changed.emit)

    def set_source_model(self, model: ScaricoOreTableModel) -> None:
        """Collega il modello e configura le connessioni per la persistenza della selezione."""
        self.setModel(model)
        model.layoutAboutToBeChanged.connect(self._preserve_selection)
        model.layoutChanged.connect(self._restore_selection)

        if sel_model := self.selectionModel():
            sel_model.selectionChanged.connect(self._update_selection_totals)

    def _preserve_selection(self) -> None:
        """Salva gli ID reali delle righe selezionate prima di un cambio layout."""
        model = self.model()
        if not isinstance(model, ScaricoOreTableModel):
            return

        self._saved_selection_real_ids.clear()
        if (sel := self.selectionModel()) and sel.hasSelection():
            for idx in sel.selectedRows():
                if idx.isValid() and idx.row() < len(model._visible_indices):
                    self._saved_selection_real_ids.add(model._visible_indices[idx.row()])

    def _restore_selection(self) -> None:
        """Ripristina la selezione basandosi sugli ID reali salvati."""
        model = self.model()
        if not isinstance(model, ScaricoOreTableModel) or not self._saved_selection_real_ids:
            return

        real_to_vis = {real_id: vis_row for vis_row, real_id in enumerate(model._visible_indices)}
        new_sel = QItemSelection()
        for rid in self._saved_selection_real_ids:
            if rid in real_to_vis:
                vrow = real_to_vis[rid]
                new_sel.select(
                    model.index(vrow, 0),
                    model.index(vrow, model.columnCount() - 1),
                )
        if not new_sel.isEmpty() and (sel := self.selectionModel()):
            sel.select(new_sel, sel.SelectionFlag.ClearAndSelect | sel.SelectionFlag.Rows)
            self._update_selection_totals()

    def _update_selection_totals(self) -> None:
        """Calcola il totale delle ore selezionate."""
        try:
            if not (sel := self.selectionModel()) or not (idxs := sel.selectedIndexes()):
                self.selection_totals_changed.emit(0.0)
                return
            total = 0.0
            for idx in idxs:
                if idx.column() == 7:  # TOTALE ORE
                    with suppress(ValueError):
                        val = str(idx.data(Qt.ItemDataRole.DisplayRole)).replace(",", ".")
                        if val:
                            total += float(val)
            self.selection_totals_changed.emit(total)
        except Exception as e:
            print(f"Errore selezione: {e}")

    def resize_columns(self) -> None:
        """Configura le larghezze ottimali per le colonne."""
        h = self.horizontalHeader()
        if not h:
            return
        h.setMinimumHeight(80)
        h.setStretchLastSection(False)
        for i in range(11):
            h.setSectionResizeMode(i, QHeaderView.ResizeMode.Interactive)

        widths = [120, 150, 150, 100, 60, 75, 75, 90]
        for i, w in enumerate(widths):
            self.setColumnWidth(i, w)

        h.setSectionResizeMode(8, QHeaderView.ResizeMode.Stretch)
        self.setColumnWidth(9, 80)
        self.setColumnWidth(10, 130)

    def keyPressEvent(self, event: Any) -> None:
        """Gestisce Ctrl+C per la copia dei dati."""
        if event.matches(QKeySequence.StandardKey.Copy):
            self._copy_selection()
        else:
            super().keyPressEvent(event)

    def _copy_selection(self) -> None:
        """Copia i dati selezionati in formato TSV negli appunti."""
        if not (sel := self.selectionModel()) or not (idxs := sel.selectedIndexes()):
            return
        idxs.sort(key=lambda x: (x.row(), x.column()))
        rows: dict[int, list[tuple[int, str]]] = {}
        for idx in idxs:
            rows.setdefault(idx.row(), []).append((idx.column(), str(idx.data(Qt.ItemDataRole.DisplayRole))))

        lines = [
            "\t".join([x[1] for x in sorted(rows[r], key=operator.itemgetter(0))])
            for r in sorted(rows.keys())
        ]
        if cb := QApplication.clipboard():
            cb.setText("\n".join(lines))
