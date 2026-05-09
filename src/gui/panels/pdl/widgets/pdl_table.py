"""
SyncroJob - PDL Table Widget
Widget specializzato per la visualizzazione della griglia PDL SafeWork.
"""

from PySide6.QtCore import QAbstractItemModel, Qt, Signal
from PySide6.QtWidgets import QAbstractItemView, QHeaderView, QTableView, QWidget

from src.gui.panels.pdl.pdl_delegate import PDLDelegate


class PDLTableView(QTableView):
    """Tabella specializzata per il Database PDL con Master-Detail support."""

    header_clicked = Signal(int)
    row_double_clicked = Signal()
    selection_changed_custom = Signal()
    context_menu_requested = Signal(object)  # pos

    def __init__(self, model: QAbstractItemModel, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setModel(model)
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.setWordWrap(True)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)

        # Delegato per colonne specifiche (es. date)
        self.setItemDelegate(PDLDelegate([0], self))

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context_menu_requested.emit)
        self.doubleClicked.connect(lambda _: self.row_double_clicked.emit())
        if sel_model := self.selectionModel():
            sel_model.selectionChanged.connect(self.selection_changed_custom.emit)

        v_header = self.verticalHeader()
        if v_header:
            v_header.setVisible(False)

        h_header = self.horizontalHeader()
        if h_header:
            h_header.setSectionsClickable(True)
            h_header.sectionClicked.connect(self.header_clicked.emit)

    def optimize_columns(self, headers_count: int) -> None:
        """Ottimizza la larghezza delle colonne basandosi sul contenuto."""
        h = self.horizontalHeader()
        if not h:
            return
        for i in range(headers_count):
            h.setSectionResizeMode(i, QHeaderView.ResizeMode.Interactive)

        self.resizeColumnsToContents()
        # Limita larghezze troppo ampie tranne l'ultima (descrizione)
        for i in range(headers_count):
            if i != 6 and h.sectionSize(i) > 200:
                h.resizeSection(i, 200)

        h.setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)
