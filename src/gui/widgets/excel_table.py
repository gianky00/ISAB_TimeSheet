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


class ExcelTableWidget(QTableWidget):
    """
    QTableWidget con funzionalità Clipboard TSV e analisi AI Lyra.
    Supporta la formattazione semantica delle righe e l'interazione con l'intelligenza artificiale.
    """

    # Safe Method Injection: Copia i metodi di ClipboardMixin per evitare crash da eredità multipla su Windows
    copy_selection = ClipboardMixin.copy_selection
    paste_selection = ClipboardMixin.paste_selection
    _get_selected_rows_cols = ClipboardMixin._get_selected_rows_cols
    _build_header_tsv = ClipboardMixin._build_header_tsv
    _get_row_as_tsv = ClipboardMixin._get_row_as_tsv
    _get_cell_value = ClipboardMixin._get_cell_value
    _get_paste_start_pos = ClipboardMixin._get_paste_start_pos
    _paste_cell_data = ClipboardMixin._paste_cell_data

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
            self.copy_selection()  # type: ignore
        elif event.matches(QKeySequence.StandardKey.Paste):
            self.paste_selection()  # type: ignore
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
        # Se riceve un QPoint (da customContextMenuRequested), lo gestisce
        if hasattr(event, "globalPos"):
            pos = event.pos()
            global_pos = event.globalPos()
        else:
            pos = event
            global_pos = self.mapToGlobal(pos)

        menu = QMenu(self)
        icon_color = COLORS["text_dark"]

        lyra_row = QAction(
            get_colored_icon(get_asset_path(Icons.SPARKLES), icon_color), "Analizza riga con Lyra", self
        )
        lyra_row.triggered.connect(lambda: self._analyze_row_at(pos))

        lyra_sel = QAction(
            get_colored_icon(get_asset_path(Icons.SPARKLES), icon_color), "Analizza selezione con Lyra", self
        )
        lyra_sel.triggered.connect(self._analyze_selection)

        copy_act = QAction(get_colored_icon(get_asset_path(Icons.EDIT), icon_color), "Copia", self)
        copy_act.triggered.connect(self.copy_selection)  # type: ignore

        for act in (lyra_row, lyra_sel, copy_act):
            menu.addAction(act)
        menu.exec(global_pos)

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
            val = self._get_cell_value(row, c)  # type: ignore
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
                line.append(f"{label}: {self._get_cell_value(r, c)}")  # type: ignore
            rows_text.append(" | ".join(line))

        win = self.window()
        if hasattr(win, "analyze_with_lyra"):
            win.analyze_with_lyra("\n".join(rows_text))  # type: ignore


class EditableDataTable(QWidget):
    """Wrapper per ExcelTableWidget con gestione righe dinamica."""

    data_changed = pyqtSignal()

    def __init__(self, columns: list[dict[str, Any]], parent: QWidget | None = None, initial_rows: int = 20) -> None:
        """
        Inizializza la tabella modificabile.

        Args:
            columns: Elenco di configurazioni per le colonne (nome, tipo, opzioni).
            parent: Widget genitore opzionale.
            initial_rows: Numero di righe vuote iniziali.
        """
        super().__init__(parent)
        self.columns = columns
        self.initial_rows = initial_rows
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
        self.table.setHorizontalHeaderLabels([str(c.get("label", c["name"])) for c in self.columns])

        h = self.table.horizontalHeader()
        if h:
            h.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)
        self.table.itemChanged.connect(self.data_changed.emit)

        # Standard: righe predefinite
        for _ in range(self.initial_rows):
            self._add_row()
        container_lay.addWidget(self.table)
        layout.addWidget(self.container)

    def _add_row(self, use_defaults: bool = True) -> None:
        """Aggiunge una riga vuota alla tabella con i widget appropriati."""
        row = self.table.rowCount()
        self.table.insertRow(row)
        for col, col_def in enumerate(self.columns):
            default_val = str(col_def.get("default", "")) if use_defaults else ""

            if col_def.get("type") == "combo":
                combo = FilterComboBox()
                options = col_def.get("options", [])
                # Assicurati che ci sia un'opzione vuota
                if "" not in options:
                    options = ["", *list(options)]
                combo.addItems(options)

                if default_val:
                    combo.setCurrentText(default_val)
                else:
                    combo.setCurrentIndex(0)

                combo.currentIndexChanged.connect(self.data_changed.emit)
                self.table.setCellWidget(row, col, combo)
            else:
                item = SortableTableWidgetItem(default_val)
                if col_def.get("readonly"):
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row, col, item)

    def _remove_row(self) -> None:
        """Rimuove la riga corrente o le righe selezionate."""
        rows = sorted({index.row() for index in self.table.selectedIndexes()}, reverse=True)
        if not rows and self.table.rowCount() > 0:
            # Se nulla è selezionato, rimuovi l'ultima riga
            self.table.removeRow(self.table.rowCount() - 1)
        else:
            for row in rows:
                self.table.removeRow(row)
        self.data_changed.emit()

    def _show_context_menu(self, pos: QPoint) -> None:
        """Menu contestuale con opzioni di gestione riga e Lyra."""
        global_pos = self.table.mapToGlobal(pos)
        menu = QMenu(self)
        icon_color = COLORS["text_dark"]

        add_act = QAction(
            get_colored_icon(get_asset_path(Icons.PLUS), icon_color), "Aggiungi riga", self
        )
        add_act.triggered.connect(self._add_row)

        remove_act = QAction(
            get_colored_icon(get_asset_path(Icons.TRASH), icon_color), "Rimuovi riga/e", self
        )
        remove_act.triggered.connect(self._remove_row)

        lyra_row = QAction(
            get_colored_icon(get_asset_path(Icons.SPARKLES), icon_color), "Analizza riga con Lyra", self
        )
        lyra_row.triggered.connect(lambda: self.table._analyze_row_at(pos))

        lyra_sel = QAction(
            get_colored_icon(get_asset_path(Icons.SPARKLES), icon_color), "Analizza selezione con Lyra", self
        )
        lyra_sel.triggered.connect(self.table._analyze_selection)

        copy_act = QAction(get_colored_icon(get_asset_path(Icons.EDIT), icon_color), "Copia", self)
        copy_act.triggered.connect(self.table.copy_selection)  # type: ignore

        for act in (add_act, remove_act, lyra_row, lyra_sel, copy_act):
            menu.addAction(act)
        menu.exec(global_pos)

    def get_data(self) -> list[dict[str, Any]]:
        """Estrae i dati dalla tabella in formato lista di dizionari."""
        data = []
        for r in range(self.table.rowCount()):
            row_data = {}
            has_content = False
            for c, col_def in enumerate(self.columns):
                val = self.table._get_cell_value(r, c)  # type: ignore
                row_data[col_def["name"]] = val
                if val:
                    has_content = True
            if has_content:
                data.append(row_data)
        return data

    def set_data(self, data: list[dict[str, Any]]) -> None:
        """
        Popola la tabella con i dati forniti.
        Utilizza un algoritmo di matching flessibile per le chiavi (ignora case, spazi e underscore).

        Args:
            data: Lista di dizionari contenenti i dati delle righe.
        """
        self.table.setRowCount(0)
        if not data:
            for _ in range(self.initial_rows):
                self._add_row()
            return

        def normalize(s: str) -> str:
            return "".join(c.lower() for c in s if c.isalnum())

        for row_dict in data:
            self._add_row()
            row_idx = self.table.rowCount() - 1
            for col_idx, col_def in enumerate(self.columns):
                col_name = col_def["name"]
                norm_col = normalize(col_name)

                # Cerca il valore nel dizionario con matching flessibile
                val = ""
                for k, v in row_dict.items():
                    if normalize(k) == norm_col:
                        val = str(v)
                        break

                if col_def.get("type") == "combo":
                    combo = self.table.cellWidget(row_idx, col_idx)
                    if isinstance(combo, FilterComboBox):
                        idx = combo.findText(val)
                        if idx >= 0:
                            combo.setCurrentIndex(idx)
                else:
                    item = self.table.item(row_idx, col_idx)
                    if item:
                        item.setText(val)

        # Padding per garantire sempre almeno 'initial_rows' righe a schermo
        while self.table.rowCount() < self.initial_rows:
            self._add_row()

    def update_cell(self, row: int, col: int, value: str, emit_signal: bool = True) -> None:
        """
        Aggiorna il contenuto di una cella specifica.

        Args:
            row: Indice della riga.
            col: Indice della colonna.
            value: Nuovo valore testuale.
            emit_signal: Se True, emette il segnale data_changed.
        """
        if row >= self.table.rowCount() or col >= self.table.columnCount():
            return

        if not emit_signal:
            self.table.blockSignals(True)

        try:
            item = self.table.item(row, col)
            if item:
                item.setText(value)
            else:
                # Se è un widget (es. combo), non facciamo nulla o gestiamo se serve
                widget = self.table.cellWidget(row, col)
                if isinstance(widget, FilterComboBox):
                    idx = widget.findText(value)
                    if idx >= 0:
                        widget.setCurrentIndex(idx)
        finally:
            if not emit_signal:
                self.table.blockSignals(False)

    def set_row_status(self, row: int, status: str) -> None:
        """
        Proxy per impostare lo stato semantico della riga nella tabella.

        Args:
            row: Indice della riga.
            status: Stato della riga.
        """
        self.table.set_row_status(row, status)

    def update_column_options(self, col: int, options: list[str]) -> None:
        """
        Aggiorna le opzioni di una colonna di tipo 'combo' per tutte le righe esistenti.
        Aggiorna anche la definizione della colonna per le future righe.

        Args:
            col: Indice della colonna.
            options: Nuova lista di opzioni.
        """
        if col < 0 or col >= len(self.columns):
            return

        # Aggiorna la definizione
        self.columns[col]["options"] = options

        # Aggiorna i widget esistenti
        for row in range(self.table.rowCount()):
            widget = self.table.cellWidget(row, col)
            if isinstance(widget, FilterComboBox):
                current_text = widget.currentText()
                widget.blockSignals(True)
                widget.clear()
                # Assicurati che ci sia un'opzione vuota
                final_options = ["", *[o for o in options if o]] if "" not in options else options
                widget.addItems(final_options)

                # Ripristina il valore se ancora valido
                idx = widget.findText(current_text)
                if idx >= 0:
                    widget.setCurrentIndex(idx)
                else:
                    widget.setCurrentIndex(0)
                widget.blockSignals(False)

    def clear(self) -> None:
        """Svuota la tabella e ripristina le righe iniziali."""
        self.table.setRowCount(0)
        for _ in range(self.initial_rows):
            self._add_row(use_defaults=False)
