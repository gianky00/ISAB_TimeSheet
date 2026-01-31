from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QStyledItemDelegate


class PDLDelegate(QStyledItemDelegate):
    """Delegate per gestire il wrap selettivo e l'allineamento nelle celle PDL."""

    def __init__(self, date_columns, parent=None):
        super().__init__(parent)
        self.date_columns = date_columns

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        # Abilita il wrap per tutte le colonne tranne quelle date
        if index.column() not in self.date_columns:
            option.features |= option.ViewItemFeature.HasDisplay
            option.displayAlignment = (
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
            )
            option.textElideMode = Qt.TextElideMode.ElideNone
        else:
            # Date: riga singola
            option.textElideMode = Qt.TextElideMode.ElideRight
