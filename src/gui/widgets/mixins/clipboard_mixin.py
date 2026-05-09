"""
SyncroJob - Clipboard Mixin
Fornisce funzionalità avanzate di Copia/Incolla in formato TSV (Excel-compatible).
"""

from collections.abc import Sequence
from typing import Any, cast

from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QApplication, QComboBox as QtQComboBox, QToolTip

from src.gui.widgets.sortable_table_item import SortableTableWidgetItem


class ClipboardMixin:
    """Mixin per aggiungere capacità di Copia/Incolla TSV ai widget tabellari."""

    def copy_selection(self) -> None:
        """Copia i dati selezionati in formato TSV negli appunti."""
        if not hasattr(self, "selectedIndexes"):
            return
        selection = self.selectedIndexes()
        if not selection:
            return

        rows, cols = self._get_selected_rows_cols(selection)
        if not rows or not cols:
            return

        tsv_rows: list[str] = []
        # Header (se abilitato e se selezione multipla)
        if getattr(self, "auto_copy_headers", False) and len(selection) > 1:
            tsv_rows.append(self._build_header_tsv(cols))

        # Data Rows
        for r in rows:
            if hasattr(self, "isRowHidden") and self.isRowHidden(r):
                continue
            tsv_rows.append(self._get_row_as_tsv(r, cols))

        if tsv_rows:
            clipboard = QApplication.clipboard()
            if clipboard:
                clipboard.setText("\n".join(tsv_rows))
            QToolTip.showText(QCursor.pos(), "Copiato!", cast("Any", self))

    def paste_selection(self) -> None:
        """Incolla i dati dagli appunti nella tabella."""
        clipboard = QApplication.clipboard()
        text = clipboard.text() if clipboard else ""
        if not text:
            return

        rows_data = text.split("\n")
        if rows_data and not rows_data[-1]:
            rows_data.pop()

        r_start, c_start = self._get_paste_start_pos()

        for r_idx, row_text in enumerate(rows_data):
            target_r = r_start + r_idx
            if target_r >= self.rowCount():  # type: ignore
                break

            cols_data = row_text.split("\t")
            for c_idx, cell_text in enumerate(cols_data):
                target_c = c_start + c_idx
                if target_c >= self.columnCount() or self.isColumnHidden(target_c):  # type: ignore
                    continue
                self._paste_cell_data(target_r, target_c, cell_text.strip())

    def _get_selected_rows_cols(self, selection: Sequence[Any]) -> tuple[list[int], list[int]]:
        rows, cols = set(), set()
        for idx in selection:
            rows.add(idx.row())
            cols.add(idx.column())
        return sorted(rows), sorted(cols)

    def _build_header_tsv(self, cols: list[int]) -> str:
        headers = []
        for c in cols:
            it = self.horizontalHeaderItem(c)  # type: ignore
            headers.append(it.text() if it else f"Col {c}")
        return "\t".join(headers)

    def _get_row_as_tsv(self, row: int, cols: list[int]) -> str:
        data = []
        for c in cols:
            val = self._get_cell_value(row, c)
            data.append(val.replace("\t", " ").replace("\n", " "))
        return "\t".join(data)

    def _get_cell_value(self, row: int, col: int) -> str:
        widget = self.cellWidget(row, col)  # type: ignore
        if widget:
            # Se  direttamente una QComboBox
            if isinstance(widget, QtQComboBox):
                return str(widget.currentText())
            # Se  un container che ospita una QComboBox
            cb = widget.findChild(QtQComboBox)
            if cb:
                return str(cb.currentText())

        it = self.item(row, col)  # type: ignore
        return it.text() if it else ""

    def _get_paste_start_pos(self) -> tuple[int, int]:
        return (max(0, self.currentRow()), max(0, self.currentColumn()))  # type: ignore

    def _paste_cell_data(self, row: int, col: int, text: str) -> None:
        widget = self.cellWidget(row, col)  # type: ignore
        if isinstance(widget, QtQComboBox):
            idx = widget.findText(text)
            if idx >= 0:
                widget.setCurrentIndex(idx)
        else:
            item = self.item(row, col)  # type: ignore
            if not item:
                self.setItem(row, col, SortableTableWidgetItem(text))  # type: ignore
            else:
                item.setText(text)
