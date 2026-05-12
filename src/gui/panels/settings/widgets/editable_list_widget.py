"""
SyncroJob - Editable List Widget
Widget riutilizzabile per la gestione di liste testuali semplici (Aggiungi, Modifica, Rimuovi).
"""

from collections.abc import Sequence
from typing import Any

from PySide6.QtCore import QPoint, Qt, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMenu,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.gui.dialogs.confirmation_dialog import ConfirmationDialog
from src.gui.dialogs.standard_input_dialog import StandardInputDialog
from src.gui.panels.settings.shared import (
    create_group_box,
    list_style,
    style_mini_button,
)
from src.gui.styles import COLORS
from src.gui.widgets.core_widgets import (
    IconButton,
    StandardListWidget,
)
from src.utils.helpers import get_asset_path, get_colored_icon


class EditableListWidget(QWidget):
    """
    Widget che gestisce una lista di stringhe con controlli CRUD.
    Supporta l'interazione tramite pulsanti dedicati o menu contestuale.
    """

    changed = Signal()

    def __init__(self, title: str, input_label: str, parent: QWidget | None = None) -> None:
        """
        Inizializza il widget lista modificabile.

        Args:
          title: Titolo del gruppo visualizzato.
          input_label: Etichetta da mostrare nel dialogo di input.
          parent: Widget genitore opzionale.
        """
        super().__init__(parent)
        self.title = title
        self.input_label = input_label
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Configura il layout, la lista e i pulsanti d'azione."""
        self.group = create_group_box(self.title)
        layout = QVBoxLayout(self.group)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.group)

        self.list_widget = StandardListWidget()
        self.list_widget.setMinimumHeight(100)
        self.list_widget.setStyleSheet(list_style())
        self.list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self._show_menu)
        layout.addWidget(self.list_widget)

        btns = QHBoxLayout()
        self._add_btn(btns, Icons.PLUS, COLORS["success_green"], self.add_item, "Aggiungi")
        self._add_btn(btns, Icons.EDIT, COLORS["primary_blue"], self.edit_item, "Modifica")
        self._add_btn(btns, Icons.TRASH, COLORS["error_red"], self.remove_item, "Rimuovi")
        btns.addStretch()
        layout.addLayout(btns)

    def _add_btn(self, layout: QHBoxLayout, icon: str, color: str, callback: Any, tooltip: str) -> None:
        """Helper per aggiungere un pulsante icona alla barra delle azioni."""
        btn = IconButton()
        btn.setIcon(get_colored_icon(get_asset_path(icon), COLORS["text_dark"]))
        btn.setToolTip(tooltip)
        btn.clicked.connect(callback)
        style_mini_button(btn, color)
        layout.addWidget(btn)

    def _show_menu(self, pos: QPoint) -> None:
        """Mostra il menu contestuale per l'elemento selezionato."""
        menu = QMenu()
        item = self.list_widget.itemAt(pos)
        menu.addAction("Aggiungi", self.add_item)
        if item:
            self.list_widget.setCurrentItem(item)
            menu.addSeparator()
            menu.addAction("Modifica", self.edit_item)
            menu.addAction("Rimuovi", self.remove_item)

        viewport = self.list_widget.viewport()
        if viewport:
            menu.exec(viewport.mapToGlobal(pos))

    def add_item(self) -> None:
        """Apre il dialogo di input per aggiungere una nuova stringa alla lista."""
        text, ok = StandardInputDialog.get_input(self, "Aggiungi", self.input_label)
        if ok and text:
            self.list_widget.addItem(text)
            self.changed.emit()

    def edit_item(self) -> None:
        """Apre il dialogo di input per modificare l'elemento selezionato."""
        item = self.list_widget.currentItem()
        if item:
            text, ok = StandardInputDialog.get_input(self, "Modifica", self.input_label, text=item.text())
            if ok and text:
                item.setText(text)
                self.changed.emit()

    def remove_item(self) -> None:
        """Rimuove l'elemento selezionato previa conferma dell'utente."""
        row = self.list_widget.currentRow()
        item = self.list_widget.item(row)
        if item and ConfirmationDialog.confirm(self, "Conferma", f"Rimuovere '{item.text()}'?"):
            self.list_widget.takeItem(row)
            self.changed.emit()

    def get_items(self) -> list[str]:
        """Restituisce l'elenco di tutte le stringhe contenute nella lista."""
        items = []
        for i in range(self.list_widget.count()):
            it = self.list_widget.item(i)
            if it:
                items.append(it.text())
        return items

    def set_items(self, items: Sequence[str]) -> None:
        """
        Popola la lista con le stringhe fornite.

        Args:
          items: Sequenza di stringhe da aggiungere.
        """
        self.list_widget.clear()
        self.list_widget.addItems(items)
