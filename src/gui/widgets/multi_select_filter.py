"""
SyncroJob - MultiSelect Filter Widget
Widget professionale per la selezione multipla con ricerca e chip.
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.gui.widgets.modern_button import ModernButton
from src.utils.helpers import get_asset_path


class MultiSelectDialog(QDialog):
    """Dialogo di selezione multipla con ricerca."""

    def __init__(self, title: str, items: list[str], selected: list[str], parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumSize(400, 500)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Ricerca
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cerca...")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.textChanged.connect(self._filter_items)
        self.search_input.setStyleSheet(
            "padding: 8px; font-size: 13px; border: 1px solid #DDD; border-radius: 4px;"
        )
        layout.addWidget(self.search_input)

        # Toolbar
        toolbar = QHBoxLayout()
        self.btn_all = ModernButton("Tutti", variant=ModernButton.Variant.GHOST, size=ModernButton.Size.SMALL)
        self.btn_none = ModernButton(
            "Nessuno", variant=ModernButton.Variant.GHOST, size=ModernButton.Size.SMALL
        )
        self.btn_all.clicked.connect(lambda: self._set_all_checks(Qt.CheckState.Checked))
        self.btn_none.clicked.connect(lambda: self._set_all_checks(Qt.CheckState.Unchecked))
        toolbar.addWidget(self.btn_all)
        toolbar.addWidget(self.btn_none)
        toolbar.addStretch()
        layout.addLayout(toolbar)

        # Lista
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("border: 1px solid #DDD; border-radius: 4px; outline: none;")
        for text in items:
            item = QListWidgetItem(text)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            state = Qt.CheckState.Checked if text in selected else Qt.CheckState.Unchecked
            item.setCheckState(state)
            self.list_widget.addItem(item)
        layout.addWidget(self.list_widget)

        # Footer
        btns = QHBoxLayout()
        btns.addStretch()
        btn_cancel = ModernButton("Annulla", variant=ModernButton.Variant.GHOST)
        btn_confirm = ModernButton("Conferma", variant=ModernButton.Variant.PRIMARY)
        btn_cancel.clicked.connect(self.reject)
        btn_confirm.clicked.connect(self.accept)
        btns.addWidget(btn_cancel)
        btns.addWidget(btn_confirm)
        layout.addLayout(btns)

    def _filter_items(self, text: str):
        search_text = text.lower()
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item:
                item.setHidden(search_text not in item.text().lower())

    def _set_all_checks(self, state: Qt.CheckState):
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item and not item.isHidden():
                item.setCheckState(state)

    def get_selected(self) -> list[str]:
        selected = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item and item.checkState() == Qt.CheckState.Checked:
                selected.append(item.text())
        return selected


class MultiSelectFilter(QWidget):
    """Widget che mostra un pulsante di selezione e gestisce la multiselezione."""

    changed = pyqtSignal(list)

    def __init__(self, label: str, placeholder: str = "Seleziona...", parent: QWidget | None = None):
        super().__init__(parent)
        self.label_text = label
        self.placeholder = placeholder
        self.items: list[str] = []
        self.selected: list[str] = []

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.btn_select = ModernButton(
            placeholder, variant=ModernButton.Variant.GHOST, icon=get_asset_path(Icons.LIST)
        )
        self.btn_select.setStyleSheet("text-align: left; padding-left: 10px; border: 1px solid #ced4da;")
        self.btn_select.clicked.connect(self._open_dialog)
        layout.addWidget(self.btn_select)

    def set_items(self, items: list[str]):
        self.items = items
        # Rimuovi selezionati non più presenti
        self.selected = [s for s in self.selected if s in items]
        self._update_button_text()

    def set_selected(self, selected: list[str]):
        self.selected = selected
        self._update_button_text()

    def _update_button_text(self):
        if not self.selected:
            self.btn_select.setText(self.placeholder)
        else:
            self.btn_select.setText(f"{self.label_text}: {len(self.selected)} selezionati")

    def _open_dialog(self):
        dlg = MultiSelectDialog(f"Seleziona {self.label_text}", self.items, self.selected, self.window())
        if dlg.exec():
            self.selected = dlg.get_selected()
            self._update_button_text()
            self.changed.emit(self.selected)
