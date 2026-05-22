"""SyncroJob - ODA Tree Widget.

Widget specializzato per la visualizzazione gerarchica degli Ordini di Acquisto.
"""

from PySide6.QtCore import QAbstractItemModel, QModelIndex, Qt, Signal
from PySide6.QtWidgets import QAbstractItemView, QHeaderView, QTreeView, QWidget

from src.gui.panels.storico_oda.oda_delegate import ChildDescriptionDelegate
from src.gui.styles import COLORS


class ODATreeView(QTreeView):
    """Vista gerarchica per Storico OdA con supporto Master-Detail.

    Inizializza la classe.
    """

    selection_changed_custom = Signal()
    row_double_clicked = Signal()
    context_menu_requested = Signal(object)  # pos

    def __init__(self, model: QAbstractItemModel, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setModel(model)
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.setAlternatingRowColors(True)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setUniformRowHeights(True)
        self.setIndentation(25)
        self.setAnimated(True)
        # Disabilitiamo l'espansione nativa per gestirla manualmente su tutte le colonne
        self.setExpandsOnDoubleClick(False)

        # Delegato per descrizioni posizioni
        self.setItemDelegate(ChildDescriptionDelegate(self))

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context_menu_requested.emit)

        # Gestione manuale doppio click su ogni colonna
        self.doubleClicked.connect(self._on_double_clicked)

        # Effetto animazione: scroll fluido all'espansione
        self.expanded.connect(self._on_expanded)

        if sel_model := self.selectionModel():
            sel_model.selectionChanged.connect(lambda _1, _2: self.selection_changed_custom.emit())

    def _on_double_clicked(self, index: QModelIndex) -> None:
        """Espande o comprime la riga al doppio click su qualsiasi colonna."""
        if not index.isValid():
            return

        # Se  un genitore (non ha parent), invertiamo l'espansione
        if not index.parent().isValid():
            if self.isExpanded(index):
                self.collapse(index)
            else:
                self.expand(index)

        self.row_double_clicked.emit()

    def _on_expanded(self, index: QModelIndex) -> None:
        """Scrolla in modo fluido per mostrare i figli appena espansi."""
        self.scrollTo(index, QAbstractItemView.ScrollHint.PositionAtTop)

        # Styling
        self.setStyleSheet(f"""
      QTreeView {{
        gridline-color: {COLORS["bg_alt"]};
        selection-background-color: {COLORS["table_selection_bg"]};
        selection-color: {COLORS["text_dark"]};
        border: 1px solid {COLORS["border_light"]};
        border-radius: 8px;
        background-color: {COLORS["bg_white"]};
      }}
      QHeaderView::section {{
        background-color: {COLORS["bg_light"]};
        color: {COLORS["text_dark"]};
        padding: 10px;
        font-weight: bold;
        border: none;
        border-bottom: 1px solid {COLORS["border_light"]};
      }}
    """)

    def configure_headers(self) -> None:
        """Configura le dimensioni e le modalità di ridimensionamento degli header."""
        h = self.header()
        if not h:
            return
        h.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        h.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        h.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        h.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        h.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        h.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        h.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        h.setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)

        self.setColumnWidth(0, 100)
        self.setColumnWidth(1, 90)
        self.setColumnWidth(2, 50)
        self.setColumnWidth(6, 80)
        self.setColumnWidth(7, 120)
