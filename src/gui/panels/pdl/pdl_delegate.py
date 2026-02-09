from collections.abc import Sequence
from typing import Any

from PyQt6.QtCore import QModelIndex, Qt
from PyQt6.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem


class PDLDelegate(QStyledItemDelegate):
    """Delegate per gestire il wrap selettivo e l'allineamento nelle celle PDL."""

    def __init__(self, date_columns: Sequence[int], parent: Any | None = None) -> None:
        super().__init__(parent)
        self.date_columns = date_columns

    def initStyleOption(self, option: QStyleOptionViewItem | None, index: QModelIndex) -> None:
        super().initStyleOption(option, index)
        if not option:
            return
        # Abilita il wrap per tutte le colonne tranne quelle date
        if index.column() not in self.date_columns:
            option.features |= QStyleOptionViewItem.ViewItemFeature.HasDisplay
            option.displayAlignment = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
            option.textElideMode = Qt.TextElideMode.ElideNone
        else:
            # Date: riga singola
            option.textElideMode = Qt.TextElideMode.ElideRight
