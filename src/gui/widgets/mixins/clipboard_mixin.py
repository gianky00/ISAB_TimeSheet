"""SyncroJob - Clipboard Mixin.

Aggiunge funzionalit  di copia/incolla standard Excel alle tabelle.
"""

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QComboBox as QtQComboBox

from src.gui.widgets.core_widgets import SortableTableWidgetItem

if TYPE_CHECKING:
    from PySide6.QtWidgets import QTableWidget

    Base = QTableWidget
else:
    Base = object


class ClipboardMixin(Base):
    """Mixin per aggiungere supporto copia/incolla (TSV) compatibile con Excel."""

    def copy_selection(self: Any) -> None:
        """Copia la selezione corrente negli appunti in formato TSV."""
        selection = self.selectedIndexes()
        if not selection:
            return

        rows, cols = self._get_selected_rows_cols(selection)

        # Costruisci stringa TSV (Header + Dati)
        tsv_parts = [self._build_header_tsv(cols)]
        tsv_parts.extend(self._get_row_as_tsv(r, cols) for r in rows)

        clipboard = QGuiApplication.clipboard()
        if clipboard:
            clipboard.setText("\n".join(tsv_parts))

    def paste_selection(self: Any) -> None:
        """Incolla i dati dagli appunti partendo dalla cella corrente."""
        clipboard = QGuiApplication.clipboard()
        text = clipboard.text() if clipboard else ""
        if not text:
            return

        rows_data = text.split("\n")
        if rows_data and not rows_data[-1]:
            rows_data.pop()

        r_start, c_start = self._get_paste_start_pos()

        for r_idx, row_text in enumerate(rows_data):
            target_r = r_start + r_idx
            if target_r >= self.rowCount():
                break

            cols_data = row_text.split("\t")
            for c_idx, cell_text in enumerate(cols_data):
                target_c = c_start + c_idx
                if target_c >= self.columnCount() or self.isColumnHidden(target_c):
                    continue
                self._paste_cell_data(target_r, target_c, cell_text.strip())

    def _get_selected_rows_cols(self: Any, selection: Sequence[Any]) -> tuple[list[int], list[int]]:
        rows, cols = set(), set()
        for idx in selection:
            rows.add(idx.row())
            cols.add(idx.column())
        return sorted(rows), sorted(cols)

    def _build_header_tsv(self: Any, cols: list[int]) -> str:
        headers = []
        for c in cols:
            it = self.horizontalHeaderItem(c)
            headers.append(it.text() if it else f"Col {c}")
        return "\t".join(headers)

    def _get_row_as_tsv(self: Any, row: int, cols: list[int]) -> str:
        data = []
        for c in cols:
            val = self._get_cell_value(row, c)
            data.append(val.replace("\t", " ").replace("\n", " "))
        return "\t".join(data)

    def _get_cell_value(self: Any, row: int, col: int) -> str:
        widget = self.cellWidget(row, col)
        if widget:
            # Se è direttamente una QComboBox
            if isinstance(widget, QtQComboBox):
                return str(widget.currentText())
            # Se è un container che ospita una QComboBox
            cb = widget.findChild(QtQComboBox)
            if cb:
                return str(cb.currentText())

        it = self.item(row, col)
        return it.text() if it else ""

    def _get_paste_start_pos(self: Any) -> tuple[int, int]:
        return (max(0, self.currentRow()), max(0, self.currentColumn()))

    def _paste_cell_data(self: Any, row: int, col: int, text: str) -> None:
        widget = self.cellWidget(row, col)
        if isinstance(widget, QtQComboBox):
            idx = widget.findText(text)
            if idx >= 0:
                widget.setCurrentIndex(idx)
        else:
            item = self.item(row, col)
            if not item:
                self.setItem(row, col, SortableTableWidgetItem(text))
            else:
                item.setText(text)
