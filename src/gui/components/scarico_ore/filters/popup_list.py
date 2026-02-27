from collections.abc import Sequence
from typing import Any

from src.gui.widgets.core_widgets import (PrimaryButton, SecondaryButton, DangerButton, GhostButton, IconButton, SearchInput, StandardInput, StandardTextEdit, FilterComboBox, StandardCheckBox, StandardSpinBox, StandardTable, StandardListWidget, StandardTreeWidget, StandardGroupBox, StandardProgressBar)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QListView,
    QMenu,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ListFilterPopupWidget(QWidget):
    """
    Widget di popup per il filtraggio di liste di valori unici.
    Include una barra di ricerca e opzioni di selezione rapida.
    """

    def __init__(self, values: Sequence[Any], selected_values: Sequence[str] | None = None) -> None:
        super().__init__()
        self.values = values
        self.all_values = {str(v).lower() for v in values}
        self.applied = False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        self.search_edit = SearchInput()
        self.search_edit.setPlaceholderText("Cerca...")
        self.search_edit.textChanged.connect(self._filter_list)
        layout.addWidget(self.search_edit)

        btn_layout = QHBoxLayout()
        btn_all = PrimaryButton("Tutti")
        btn_none = PrimaryButton("Nessuno")
        btn_ok = PrimaryButton("OK")
        for btn in (btn_all, btn_none, btn_ok):
            btn.setStyleSheet("font-size: 11px; padding: 2px;")

        btn_all.clicked.connect(self.select_all)
        btn_none.clicked.connect(self.select_none)
        btn_ok.clicked.connect(self.apply_filter)

        btn_layout.addWidget(btn_all)
        btn_layout.addWidget(btn_none)
        btn_layout.addWidget(btn_ok)
        layout.addLayout(btn_layout)

        self.list_view = QListView()
        self.model = QStandardItemModel()
        self.model.itemChanged.connect(self._on_item_changed)

        is_all_selected = selected_values is None
        selected_set = set()
        if selected_values:
            selected_set = {v.lower() for v in selected_values}

        for val in values:
            item = QStandardItem(str(val))
            item.setCheckable(True)
            if is_all_selected or (str(val).lower() in selected_set):
                item.setCheckState(Qt.CheckState.Checked)
            else:
                item.setCheckState(Qt.CheckState.Unchecked)
            self.model.appendRow(item)

        self.list_view.setModel(self.model)
        self.list_view.setFixedHeight(250)
        self.list_view.setMinimumWidth(250)
        layout.addWidget(self.list_view)

        self.original_rows = [self.model.item(i) for i in range(self.model.rowCount())]

    def _filter_list(self, text: str) -> None:
        text = text.lower()
        for i in range(self.model.rowCount()):
            item = self.model.item(i)
            if item is not None:
                if text in item.text().lower():
                    self.list_view.setRowHidden(i, False)
                else:
                    self.list_view.setRowHidden(i, True)

    def select_all(self) -> None:
        """Seleziona tutti i valori visibili nella lista."""
        self.model.blockSignals(True)
        for i in range(self.model.rowCount()):
            if not self.list_view.isRowHidden(i):
                item = self.model.item(i)
                if item is not None:
                    item.setCheckState(Qt.CheckState.Checked)
        self.model.blockSignals(False)
        self.model.layoutChanged.emit()

    def select_none(self) -> None:
        """Deseleziona tutti i valori visibili nella lista."""
        self.model.blockSignals(True)
        for i in range(self.model.rowCount()):
            if not self.list_view.isRowHidden(i):
                item = self.model.item(i)
                if item is not None:
                    item.setCheckState(Qt.CheckState.Unchecked)
        self.model.blockSignals(False)
        self.model.layoutChanged.emit()

    def _on_item_changed(self, item: QStandardItem) -> None:
        """Gestore eventi per il cambio di stato di un elemento (placeholder)."""

    def apply_filter(self) -> None:
        """Marca il filtro come applicato e chiude il menu."""
        self.applied = True
        self._close_menu()

    def get_selected_values(self) -> list[str] | None:
        """
        Ottiene i valori selezionati dal modello.

        Returns:
            list[str] | None: Lista di stringhe selezionate o None se tutti gli elementi sono selezionati.
        """
        selected: list[str] = []
        all_checked = True

        for i in range(self.model.rowCount()):
            item = self.model.item(i)
            if item is not None:
                if item.checkState() == Qt.CheckState.Checked:
                    selected.append(item.text())
                else:
                    all_checked = False

        if all_checked:
            return None
        return selected

    def _close_menu(self) -> None:
        parent = self.parent()
        while parent:
            if isinstance(parent, QMenu):
                parent.close()
                break
            parent = parent.parent()
