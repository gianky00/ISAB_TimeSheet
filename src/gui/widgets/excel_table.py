"""
SyncroJob - Excel Table Widgets (Refactored)
Widget tabellari avanzati con integrazione AI Lyra e supporto mixin per Clipboard.
"""

from typing import Any

from PyQt6.QtCore import QPoint, Qt, pyqtSignal
from PyQt6.QtGui import QAction, QBrush, QColor, QKeySequence
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QGraphicsDropShadowEffect,
    QHeaderView,
    QMenu,
    QTableWidget,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.gui.styles import COLORS
from src.gui.widgets.core_widgets import FilterComboBox
from src.gui.widgets.effects import HoverPulseFrame
from src.gui.widgets.mixins.clipboard_mixin import ClipboardMixin
from src.gui.widgets.sortable_table_item import SortableTableWidgetItem
from src.utils.helpers import get_asset_path, get_colored_icon


class ExcelTableWidget(QTableWidget, ClipboardMixin):
    """
    QTableWidget con funzionalità Clipboard TSV e analisi AI Lyra.
    Supporta la formattazione semantica delle righe e l'interazione con l'intelligenza artificiale.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Inizializza la tabella configurando i trigger di modifica e la clipboard."""
        super().__init__(*args, **kwargs)
        self.auto_copy_headers = False
        self.setEditTriggers(
            QAbstractItemView.EditTrigger.DoubleClicked
            | QAbstractItemView.EditTrigger.EditKeyPressed
            | QAbstractItemView.EditTrigger.AnyKeyPressed
        )
        # Forza altezza riga per ospitare comodamente i widget (Enterprise Look)
        if v_header := self.verticalHeader():
            v_header.setDefaultSectionSize(34)
            v_header.setVisible(False)

    def set_row_status(self, row: int, status: str) -> None:
        """
        Imposta il colore semantico della riga in base allo stato.

        Args:
            row: Indice della riga.
            status: Stato della riga (es. 'completato', 'errore').
        """
        colors = {
            "completato": COLORS["table_success_bg"],
            "errore": COLORS["table_error_bg"],
            "in_corso": COLORS["table_warning_bg"],
            "da_processare": COLORS["bg_white"],
        }
        color = QColor(colors.get(status, COLORS["bg_white"]))
        for col in range(self.columnCount()):
            it = self.item(row, col)
            if it:
                it.setBackground(QBrush(color))
                it.setForeground(QBrush(QColor("black")))

    def keyPressEvent(self, event: Any) -> None:
        """Gestisce le scorciatoie da tastiera standard (Copia, Incolla, Canc)."""
        if event.matches(QKeySequence.StandardKey.Copy):
            self.copy_selection()
        elif event.matches(QKeySequence.StandardKey.Paste):
            self.paste_selection()
        elif event.key() == Qt.Key.Key_Delete:
            self.clear_selection()
        else:
            super().keyPressEvent(event)

    def clear_selection(self) -> None:
        """Svuota il contenuto delle celle selezionate."""
        for r in self.selectedRanges():
            for row in range(r.topRow(), r.bottomRow() + 1):
                for col in range(r.leftColumn(), r.rightColumn() + 1):
                    w = self.cellWidget(row, col)
                    if isinstance(w, FilterComboBox):
                        w.setCurrentIndex(0)
                    else:
                        it = self.item(row, col)
                        if it and (it.flags() & Qt.ItemFlag.ItemIsEditable):
                            it.setText("")

    def contextMenuEvent(self, event: Any) -> None:
        """Mostra il menu contestuale con opzioni di analisi AI e clipboard."""
        menu = QMenu(self)
        icon_color = COLORS["text_dark"]

        lyra_row = QAction(
            get_colored_icon(get_asset_path(Icons.SPARKLES), icon_color), "Analizza riga con Lyra", self
        )
        lyra_row.triggered.connect(lambda: self._analyze_row_at(event.pos()))

        lyra_sel = QAction(
            get_colored_icon(get_asset_path(Icons.SPARKLES), icon_color), "Analizza selezione con Lyra", self
        )
        lyra_sel.triggered.connect(self._analyze_selection)

        copy_act = QAction(get_colored_icon(get_asset_path(Icons.EDIT), icon_color), "Copia", self)
        copy_act.triggered.connect(self.copy_selection)

        for act in (lyra_row, lyra_sel, copy_act):
            menu.addAction(act)
        menu.exec(event.globalPos())

    def _analyze_row_at(self, pos: QPoint) -> None:
        """Invia i dati della riga corrente a Lyra AI per l'analisi."""
        it = self.itemAt(pos)
        if not it:
            return
        row = it.row()
        data = []
        for c in range(self.columnCount()):
            if self.isColumnHidden(c):
                continue
            h = self.horizontalHeaderItem(c)
            label = h.text() if h else f"Col {c}"
            val = self._get_cell_value(row, c)
            data.append(f"**{label}**: {val}")

        win = self.window()
        if hasattr(win, "analyze_with_lyra"):
            win.analyze_with_lyra(" | ".join(data))  # type: ignore

    def _analyze_selection(self) -> None:
        """Invia i dati delle celle selezionate a Lyra AI per l'analisi massiva."""
        ranges = self.selectedRanges()
        if not ranges:
            return
        rows_text = []
        for r in range(ranges[0].topRow(), ranges[0].bottomRow() + 1):
            line = []
            for c in range(self.columnCount()):
                if self.isColumnHidden(c):
                    continue
                h = self.horizontalHeaderItem(c)
                label = h.text() if h else f"Col {c}"
                line.append(f"{label}: {self._get_cell_value(r, c)}")
            rows_text.append(" | ".join(line))

        win = self.window()
        if hasattr(win, "analyze_with_lyra"):
            win.analyze_with_lyra("\n".join(rows_text))  # type: ignore


class EditableDataTable(QWidget):
    """Wrapper per ExcelTableWidget con gestione righe dinamica."""

    data_changed = pyqtSignal()

    def __init__(self, columns: list[dict[str, Any]], parent: QWidget | None = None) -> None:
        """
        Inizializza la tabella modificabile.

        Args:
            columns: Elenco di configurazioni per le colonne (nome, tipo, opzioni).
            parent: Widget genitore opzionale.
        """
        super().__init__(parent)
        self.columns = columns
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Configura l'interfaccia, i frame e l'effetto ombra."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 15)
        layout.setSpacing(0)

        self.container = HoverPulseFrame(COLORS["text_dark"])
        self.container.setObjectName("tableContainer")
        self.container.setStyleSheet(f"""
            QFrame#tableContainer {{ background-color: {COLORS["bg_white"]}; border: 1px solid {COLORS["border_light"]}; border-radius: 12px; }}
            QTableWidget {{ background-color: transparent; border: none; gridline-color: {COLORS["bg_alt"]}; selection-background-color: {COLORS["table_selection_bg"]}; selection-color: {COLORS["text_dark"]}; outline: none; }}
            QHeaderView::section {{ background-color: {COLORS["bg_light"]}; color: {COLORS["text_dark"]}; padding: 10px; font-weight: bold; border: none; border-bottom: 1px solid {COLORS["border_light"]}; }}
        """)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setYOffset(8)
        shadow.setColor(QColor(0, 0, 0, 40))
        self.container.setGraphicsEffect(shadow)

        container_lay = QVBoxLayout(self.container)
        container_lay.setContentsMargins(5, 5, 5, 5)

        self.table = ExcelTableWidget()
        self.table.setColumnCount(len(self.columns))
        self.table.setHorizontalHeaderLabels([str(c["name"]) for c in self.columns])

        h = self.table.horizontalHeader()
        if h:
            h.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)
        self.table.itemChanged.connect(self.data_changed.emit)

        for _ in range(5):
            self._add_row()
        container_lay.addWidget(self.table)
        layout.addWidget(self.container)

    def _show_context_menu(self, pos: QPoint) -> None:
        """Mostra il menu contestuale per la gestione delle righe."""
        menu = QMenu()
        c = COLORS["text_dark"]

        lyra = QAction(get_colored_icon(get_asset_path(Icons.SPARKLES), c), "Analizza con Lyra", self)
        lyra.triggered.connect(self.table._analyze_selection)

        copy = QAction(get_colored_icon(get_asset_path(Icons.EDIT), c), "Copia", self)
        copy.triggered.connect(self.table.copy_selection)

        paste = QAction(get_colored_icon(get_asset_path(Icons.UPLOAD), c), "Incolla", self)
        paste.triggered.connect(self.table.paste_selection)

        add = QAction(get_colored_icon(get_asset_path(Icons.PLUS), c), "Aggiungi riga", self)
        add.triggered.connect(self._add_row)

        rem = QAction(get_colored_icon(get_asset_path(Icons.TRASH), c), "Rimuovi riga", self)
        rem.triggered.connect(self._remove_row)

        for a in (lyra, copy, paste, None, add, rem):
            if a is None:
                menu.addSeparator()
            else:
                menu.addAction(a)

        if viewport := self.table.viewport():
            menu.exec(viewport.mapToGlobal(pos))

    def update_column_options(self, col_index: int, new_options: list[str]) -> None:
        """
        Aggiorna dinamicamente le opzioni per una colonna di tipo 'combo'.

        Args:
            col_index: Indice della colonna da aggiornare.
            new_options: Nuova lista di stringhe per la combo box.
        """
        if col_index < 0 or col_index >= len(self.columns):
            return

        # Aggiorna la configurazione della colonna per le future righe
        self.columns[col_index]["options"] = new_options

        # Aggiorna i widget esistenti nelle righe correnti
        for row in range(self.table.rowCount()):
            container = self.table.cellWidget(row, col_index)
            if container:
                cb = container.findChild(FilterComboBox)
                if cb:
                    current_text = cb.currentText()
                    cb.blockSignals(True)
                    cb.clear()
                    cb.addItems(["", *new_options])
                    cb.setCurrentText(current_text)
                    cb.blockSignals(False)

    def _add_row(self, use_defaults: bool = True) -> None:
        """Aggiunge una nuova riga alla tabella, configurando eventuali widget combo."""
        row = self.table.rowCount()
        self.table.insertRow(row)
        for col, config in enumerate(self.columns):
            if config.get("type") == "combo":
                cb = FilterComboBox()
                cb.addItems(["", *config.get("options", [])])
                if use_defaults and config.get("default"):
                    cb.setCurrentText(str(config["default"]))
                cb.currentTextChanged.connect(lambda _: self.data_changed.emit())

                # Fix allineamento: rimuovi margini e centra il widget
                container = QWidget()
                container.setStyleSheet("background: transparent; border: none;")
                c_lay = QVBoxLayout(container)
                c_lay.setContentsMargins(1, 1, 1, 1)
                c_lay.setSpacing(0)
                c_lay.addWidget(cb)
                self.table.setCellWidget(row, col, container)
            else:
                val = str(config.get("default", "")) if use_defaults else ""
                item = SortableTableWidgetItem(val)
                if config.get("readonly"):
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    item.setBackground(QColor(COLORS["bg_alt"]))
                self.table.setItem(row, col, item)
        self.data_changed.emit()

    def update_cell(self, row: int, col: int, value: str, emit_signal: bool = True) -> None:
        """Aggiorna programmaticamente il valore di una cella specifica."""
        if 0 <= row < self.table.rowCount() and 0 <= col < self.table.columnCount():
            item = self.table.item(row, col)
            if item:
                item.setText(value)
            else:
                item = SortableTableWidgetItem(value)
                col_cfg = self.columns[col]
                if col_cfg.get("readonly"):
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    item.setBackground(QColor(COLORS["bg_alt"]))
                self.table.setItem(row, col, item)

            if emit_signal:
                self.data_changed.emit()

    def _remove_row(self) -> None:
        """Rimuove la riga attualmente selezionata."""
        r = self.table.currentRow()
        if r >= 0:
            self.table.removeRow(r)
            self.data_changed.emit()

    def clear(self) -> None:
        """Svuota la tabella e ripristina le righe predefinite."""
        self.table.blockSignals(True)
        self.table.setRowCount(0)
        for _ in range(5):
            self._add_row(use_defaults=False)
        self.table.blockSignals(False)
        self.data_changed.emit()

    def get_data(self) -> list[dict[str, Any]]:
        """Restituisce l'elenco dei dati contenuti nella tabella come lista di dizionari."""
        results = []
        for r in range(self.table.rowCount()):
            row_data = {}
            has_value = False
            for c, col_cfg in enumerate(self.columns):
                key = col_cfg["name"].lower().replace(" ", "_")
                val = self.table._get_cell_value(r, c)
                row_data[key] = val
                # Consideriamo la riga valida se ha almeno OdA o Contratto (prime 2 colonne)
                if c < 2 and val.strip():
                    has_value = True
            if has_value:
                results.append(row_data)
        return results

    def set_data(self, data: list[dict[str, Any]]) -> None:
        """Popola la tabella con un set di dati esistente."""
        self.table.blockSignals(True)
        self.table.setRowCount(0)
        for row_data in data:
            row = self.table.rowCount()
            self.table.insertRow(row)
            for c, col_cfg in enumerate(self.columns):
                key = col_cfg["name"].lower().replace(" ", "_")
                val = str(row_data.get(key, ""))
                if col_cfg.get("type") == "combo":
                    cb = FilterComboBox()
                    cb.addItems(["", *col_cfg.get("options", [])])
                    cb.setCurrentText(val)
                    cb.currentTextChanged.connect(lambda _: self.data_changed.emit())

                    # Fix allineamento: rimuovi margini e centra il widget
                    container = QWidget()
                    c_lay = QVBoxLayout(container)
                    c_lay.setContentsMargins(2, 2, 2, 2)
                    c_lay.addWidget(cb)
                    self.table.setCellWidget(row, c, container)
                else:
                    item = SortableTableWidgetItem(val)
                    if col_cfg.get("readonly"):
                        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                        item.setBackground(QColor(COLORS["bg_alt"]))
                    self.table.setItem(row, c, item)
        while self.table.rowCount() < 5:
            self._add_row(use_defaults=False)
        self.table.blockSignals(False)
