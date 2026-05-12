"""
SyncroJob - Contabilità Stats Helper
Utility per il calcolo dei totali ore e statistiche basate sulla selezione delle tabelle.
"""

from contextlib import suppress
from typing import Any

from PySide6.QtWidgets import QTableWidget, QTreeWidget, QWidget


class ContabilitaStatsHelper:
    """Helper per l'estrazione di statistiche dalle tabelle di contabilità."""

    @staticmethod
    def calculate_selection_stats(widget: QWidget) -> tuple[int, str]:
        """
        Esegue il calcolo granulare delle ore selezionate filtrando le righe nascoste.
        Returns: (numero_righe, totale_ore_formattato)
        """
        with suppress(Exception):
            if isinstance(widget, QTreeWidget):
                return len(widget.selectedItems()), ""

            if not isinstance(widget, QTableWidget):
                return 0, "0"

            return ContabilitaStatsHelper._update_table_selection(widget)
        return 0, "0"

    @staticmethod
    def _update_table_selection(table: QTableWidget) -> tuple[int, str]:
        """Calcola i conteggi e il totale ore per un QTableWidget."""
        model = table.selectionModel()
        if not model:
            return 0, "0"

        indexes = model.selectedIndexes()
        if not indexes:
            return 0, "0"

        target_col = ContabilitaStatsHelper._find_ore_column(table)
        selected_rows = ContabilitaStatsHelper._get_unique_visible_rows(table, indexes)
        total_ore = ContabilitaStatsHelper._calculate_total_hours(table, selected_rows, target_col)

        return len(selected_rows), ContabilitaStatsHelper._format_hours(total_ore)

    @staticmethod
    def _get_unique_visible_rows(table: QTableWidget, indexes: list[Any]) -> set[int]:
        """Filtra gli indici per ottenere righe uniche, visibili e non di totale."""
        selected_rows = set()
        for idx in indexes:
            row = idx.row()
            item_0 = table.item(row, 0)
            is_total_row = item_0 and item_0.text() == "TOTALI"
            if not table.isRowHidden(row) and not is_total_row:
                selected_rows.add(row)
        return selected_rows

    @staticmethod
    def _calculate_total_hours(table: QTableWidget, rows: set[int], col: int) -> float:
        """Somma le ore nelle righe e colonna specificate."""
        total = 0.0
        if col == -1:
            return total

        for row in rows:
            if it := table.item(row, col):
                with suppress(Exception):
                    clean = str(it.text()).replace(".", "").replace(",", ".").strip()
                    if clean:
                        total += float(clean)
        return total

    @staticmethod
    def _format_hours(total: float) -> str:
        """Formatta il totale ore per la visualizzazione IT."""
        if total % 1 != 0:
            return f"{total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return str(int(total))

    @staticmethod
    def _find_ore_column(table: QTableWidget) -> int:
        """Individua l'indice della colonna contenente le ore in base all'header."""
        for c in range(table.columnCount()):
            h = table.horizontalHeaderItem(c)
            if h and ("ORE SP" in h.text().upper() or h.text().upper() == "ORE"):
                return c
        return -1
