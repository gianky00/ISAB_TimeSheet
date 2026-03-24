"""
SyncroJob - Editable Data Table
Widget universale per la visualizzazione e modifica di dati tabellari.
Implementa feedback visivo avanzato, menu contestuali e validazione.
"""

from __future__ import annotations

from typing import Any

from PyQt6.QtCore import QEvent, QPoint, Qt, pyqtSignal
from PyQt6.QtGui import QBrush, QColor, QEnterEvent, QPainter, QPaintEvent, QPen
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QMenu,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.gui.styles import COLORS
from src.gui.widgets.modern_card import ModernCard
from src.utils.helpers import get_asset_path, get_colored_icon


class EditableDataTable(QWidget):
    """
    Una tabella interattiva che consente la modifica diretta delle celle.
    Supporta il salvataggio automatico e fornisce segnali per il tracciamento dei cambiamenti.
    """

    data_changed = pyqtSignal()
    """Segnale emesso ogni volta che i dati nella tabella vengono modificati."""

    def __init__(self, columns: list[dict[str, Any]], parent: QWidget | None = None) -> None:
        """
        Inizializza la tabella con le colonne specificate.

        Args:
            columns: Lista di dizionari definenti le colonne (name, label, type, etc.).
            parent: Widget genitore.
        """
        super().__init__(parent)
        self.columns = columns
        self._is_hovered = False
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Configura il layout e lo stile della tabella."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Container Card per elevazione
        self.card = ModernCard(elevation=8)
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(2, 2, 2, 2)

        self.table = QTableWidget()
        self.table.setColumnCount(len(self.columns))
        self.table.setHorizontalHeaderLabels([col["label"] for col in self.columns])

        # Style & Configuration
        self.table.setFrameShape(QTableWidget.Shape.NoFrame)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.DoubleClicked | QAbstractItemView.EditTrigger.EditKeyPressed
        )
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)
        self.table.itemChanged.connect(lambda: self.data_changed.emit())

        header = self.table.horizontalHeader()
        if header:
            header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
            header.setStretchLastSection(True)

        card_layout.addWidget(self.table)
        layout.addWidget(self.card)

    def enterEvent(self, event: QEnterEvent | None) -> None:
        """Attiva l'effetto di evidenziazione della tabella."""
        self._is_hovered = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event: QEvent | None) -> None:
        """Disattiva l'effetto di evidenziazione."""
        self._is_hovered = False
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event: QPaintEvent | None) -> None:
        """Disegna un bordo sottile di accento se la tabella è in focus o hovered."""
        super().paintEvent(event)
        if self._is_hovered:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            pen = QPen(QColor(COLORS["primary_blue"]), 2)
            painter.setPen(pen)
            painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 12, 12)

    def _show_context_menu(self, pos: QPoint) -> None:
        """Visualizza il menu contestuale per l'aggiunta/rimozione di righe."""
        menu = QMenu(self)
        add_action = menu.addAction("Aggiungi Riga")
        if add_action:
            add_action.setIcon(get_colored_icon(get_asset_path(Icons.PLUS), COLORS["success_dark"]))

        remove_action = menu.addAction("Rimuovi Riga")
        if remove_action:
            remove_action.setIcon(get_colored_icon(get_asset_path(Icons.TRASH), COLORS["error_red"]))
            if not self.table.itemAt(pos):
                remove_action.setEnabled(False)

        viewport = self.table.viewport()
        if viewport:
            action = menu.exec(viewport.mapToGlobal(pos))
            if action == add_action:
                self.add_row()
            elif action == remove_action:
                item = self.table.itemAt(pos)
                if item:
                    self.remove_row(item.row())

    def add_row(self, data: dict[str, Any] | None = None) -> None:
        """Aggiunge una nuova riga alla tabella con dati opzionali."""
        row_idx = self.table.rowCount()
        self.table.insertRow(row_idx)

        for col_idx, col in enumerate(self.columns):
            val = data.get(col["name"], col.get("default", "")) if data else col.get("default", "")
            item = QTableWidgetItem(str(val))
            if col.get("readonly", False):
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                item.setForeground(QBrush(QColor(COLORS["text_muted"])))
            self.table.setItem(row_idx, col_idx, item)

        self.data_changed.emit()

    def remove_row(self, row_idx: int) -> None:
        """Rimuove la riga all'indice specificato."""
        self.table.removeRow(row_idx)
        self.data_changed.emit()

    def get_data(self) -> list[dict[str, Any]]:
        """Restituisce tutti i dati della tabella come lista di dizionari."""
        data_list = []
        for row in range(self.table.rowCount()):
            row_data = {}
            for col_idx, col in enumerate(self.columns):
                item = self.table.item(row, col_idx)
                row_data[col["name"]] = item.text() if item else ""
            data_list.append(row_data)
        return data_list

    def set_data(self, data_list: list[dict[str, Any]]) -> None:
        """Popola la tabella con la lista di dati fornita."""
        self.table.blockSignals(True)
        self.table.setRowCount(0)
        for data in data_list:
            self.add_row(data)
        self.table.blockSignals(False)
        self.data_changed.emit()

    def clear(self) -> None:
        """Svuota completamente la tabella."""
        self.table.setRowCount(0)
        self.data_changed.emit()

    def update_cell(self, row: int, col: int, value: str, emit_signal: bool = True) -> None:
        """Aggiorna il valore di una specifica cella."""
        item = self.table.item(row, col)
        if item:
            if not emit_signal:
                self.table.blockSignals(True)
            item.setText(value)
            if not emit_signal:
                self.table.blockSignals(False)

    def clear_status_columns(self) -> None:
        """Pulisce le colonne di sola lettura (solitamente usate per gli esiti)."""
        self.table.blockSignals(True)
        for row in range(self.table.rowCount()):
            for col_idx, col in enumerate(self.columns):
                if col.get("readonly", False) and (item := self.table.item(row, col_idx)):
                    item.setText("")
        self.table.blockSignals(False)
