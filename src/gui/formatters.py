from PyQt6.QtCore import QAbstractTableModel, Qt


class FastTableModel(QAbstractTableModel):
    """
    Modello di dati ottimizzato per la massima reattività.
    Non crea widget per cella, ma fornisce i dati solo quando richiesto dalla vista.
    """
    def __init__(self, data=None, headers=None):
        super().__init__()
        self._data = data or []
        self._headers = headers or []

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data[index.row()][index.column()]
            return str(value) if value is not None else ""

        if role == Qt.ItemDataRole.TextAlignmentRole:
            # Allineamento predefinito
            return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter

        return None

    def headerData(self, section, orientation, role):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self._headers[section]
        return None

    def update_data(self, new_data):
        """Aggiorna i dati del modello in modo atomico."""
        self.beginResetModel()
        self._data = new_data
        self.endResetModel()
