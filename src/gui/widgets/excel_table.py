"""SyncroJob - Excel Table Widgets (Refactored).

Widget tabellari avanzati con supporto mixin per Clipboard.
"""

from typing import Any

from PySide6.QtCore import QPoint, Qt, Signal
from PySide6.QtGui import QAction, QBrush, QColor, QKeySequence, QPainter, QPaintEvent
from PySide6.QtWidgets import (
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
from src.gui.widgets.core_widgets import FilterComboBox, SortableTableWidgetItem
from src.gui.widgets.effects import HoverPulseFrame
from src.gui.widgets.mixins.clipboard_mixin import ClipboardMixin
from src.utils.helpers import get_asset_path, get_colored_icon


class ExcelTableWidget(QTableWidget):
    """QTableWidget con funzionalità Clipboard TSV.

    Supporta la formattazione semantica delle righe.

    Inizializza la tabella configurando i trigger di modifica e la clipboard.
    """

    # Safe Method Injection: Copia i metodi di ClipboardMixin per evitare crash da eredit  multipla su Windows
    copy_selection = ClipboardMixin.copy_selection
    paste_selection = ClipboardMixin.paste_selection
    _get_selected_rows_cols = ClipboardMixin._get_selected_rows_cols
    _build_header_tsv = ClipboardMixin._build_header_tsv
    _get_row_as_tsv = ClipboardMixin._get_row_as_tsv
    _get_cell_value = ClipboardMixin._get_cell_value
    _get_paste_start_pos = ClipboardMixin._get_paste_start_pos
    _paste_cell_data = ClipboardMixin._paste_cell_data

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.auto_copy_headers = False
        self._placeholder_text = ""
        self.setEditTriggers(
            QAbstractItemView.EditTrigger.DoubleClicked
            | QAbstractItemView.EditTrigger.EditKeyPressed
            | QAbstractItemView.EditTrigger.AnyKeyPressed
        )
        # Forza altezza riga per ospitare comodamente i widget (Enterprise Look)
        if v_header := self.verticalHeader():
            v_header.setDefaultSectionSize(34)
            v_header.setVisible(False)

    def setPlaceholderText(self, text: str) -> None:
        """Imposta il testo da visualizzare quando la tabella è vuota."""
        self._placeholder_text = text
        self.viewport().update()

    def smart_resize(self) -> None:
        """Esegue un ridimensionamento ottimizzato per evitare lag della UI."""
        from PySide6.QtCore import QTimer

        def _do_resize() -> None:
            if not self or self.rowCount() == 0:
                return
            self.setUpdatesEnabled(False)
            try:
                # Se la tabella è molto grande, ridimensioniamo solo le colonne.
                # Il ridimensionamento delle righe (O(N)) è il vero killer del frame rate.
                self.resizeColumnsToContents()
                if self.rowCount() < 500:
                    self.resizeRowsToContents()
            finally:
                self.setUpdatesEnabled(True)

        QTimer.singleShot(0, _do_resize)

    def paintEvent(self, event: QPaintEvent) -> None:
        """Override per disegnare il placeholder se la tabella è vuota."""
        super().paintEvent(event)
        if self.rowCount() == 0 and self._placeholder_text:
            painter = QPainter(self.viewport())
            painter.setPen(QColor(COLORS["text_light"]))
            font = self.font()
            font.setPointSize(10)
            painter.setFont(font)
            painter.drawText(
                self.viewport().rect(),
                Qt.AlignmentFlag.AlignCenter,
                self._placeholder_text,
            )

    def set_row_status(self, row: int, status: str) -> None:
        """Imposta il colore semantico della riga in base allo stato.

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
        """Mostra il menu contestuale con opzioni di clipboard."""
        # Se riceve un QPoint (da customContextMenuRequested), lo gestisce
        if hasattr(event, "globalPos"):
            pos = event.pos()
            global_pos = event.globalPos()
        else:
            pos = event
            global_pos = self.mapToGlobal(pos)

        menu = QMenu(self)
        icon_color = COLORS["text_dark"]

        copy_act = QAction(get_colored_icon(get_asset_path(Icons.EDIT), icon_color), "Copia", self)
        copy_act.triggered.connect(self.copy_selection)

        menu.addAction(copy_act)
        menu.exec(global_pos)


class EditableDataTable(QWidget):
    """Wrapper per ExcelTableWidget con gestione righe dinamica.

    Inizializza la tabella modificabile.

    Args:
      columns: Elenco di configurazioni per le colonne (nome, tipo, opzioni).
      parent: Widget genitore opzionale.
      initial_rows: Numero di righe vuote iniziali.

    Attributes:
        data_changed: Segnale o attributo della classe.
    """

    data_changed = Signal()

    def __init__(
        self, columns: list[dict[str, Any]], parent: QWidget | None = None, initial_rows: int = 20
    ) -> None:
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
        self.table.itemChanged.connect(lambda: self.data_changed.emit())

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

                combo.currentIndexChanged.connect(lambda: self.data_changed.emit())
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
            # Se nulla  selezionato, rimuovi l'ultima riga
            self.table.removeRow(self.table.rowCount() - 1)
        else:
            for row in rows:
                self.table.removeRow(row)
        self.data_changed.emit()

    def _show_context_menu(self, pos: QPoint) -> None:
        """Menu contestuale con opzioni di gestione riga."""
        global_pos = self.table.mapToGlobal(pos)
        menu = QMenu(self)
        icon_color = COLORS["text_dark"]

        add_act = QAction(get_colored_icon(get_asset_path(Icons.PLUS), icon_color), "Aggiungiàriga", self)
        add_act.triggered.connect(self._add_row)

        remove_act = QAction(
            get_colored_icon(get_asset_path(Icons.TRASH), icon_color), "Rimuovi riga/e", self
        )
        remove_act.triggered.connect(self._remove_row)

        copy_act = QAction(get_colored_icon(get_asset_path(Icons.EDIT), icon_color), "Copia", self)
        copy_act.triggered.connect(self.table.copy_selection)

        for act in (add_act, remove_act, copy_act):
            menu.addAction(act)
        menu.exec(global_pos)

    def get_data(self) -> list[dict[str, Any]]:
        """Estrae i dati dalla tabella in formato lista di dizionari."""
        data = []
        ignore_cols = {"ESITO", "ERRORE"}
        for r in range(self.table.rowCount()):
            row_data = {}
            has_content = False
            for c, col_def in enumerate(self.columns):
                val = self.table._get_cell_value(r, c)
                row_data[col_def["name"]] = val
                # Considera la riga valida solo se ha contenuto in una colonna non di servizio
                if val and col_def["name"].upper() not in ignore_cols:
                    has_content = True
            if has_content:
                data.append(row_data)
        return data

    def clear_status_columns(self) -> None:
        """Ripulisce le celle delle colonne ESITO e ERRORE, resettando il colore della riga."""
        target_cols = [
            c for c, col_def in enumerate(self.columns) if col_def["name"].upper() in {"ESITO", "ERRORE"}
        ]

        if not target_cols:
            return

        for r in range(self.table.rowCount()):
            self.set_row_status(r, "da_processare")
            for c in target_cols:
                item = self.table.item(r, c)
                if item:
                    item.setText("")

    def set_data(self, data: list[dict[str, Any]]) -> None:
        """Popola la tabella con i dati forniti.

        Utilizza un algoritmo di matching flessibile per le chiavi (ignora case, spazi e underscore).

        Args:
          data: Lista di dizionari contenenti i dati delle righe.
        """
        self.table.setRowCount(0)
        if not data:
            for _ in range(self.initial_rows):
                self._add_row()
            return

        for row_dict in data:
            self._add_row()
            row_idx = self.table.rowCount() - 1
            self._populate_row(row_idx, row_dict)

        # Padding per garantire sempre almeno 'initial_rows' righe a schermo
        while self.table.rowCount() < self.initial_rows:
            self._add_row()

    def _populate_row(self, row_idx: int, row_dict: dict[str, Any]) -> None:
        """Popola una singola riga mappando i dati del dizionario alle colonne."""
        for col_idx, col_def in enumerate(self.columns):
            val = self._find_matching_value(col_def["name"], row_dict)
            self._set_cell_value(row_idx, col_idx, val, col_def.get("type"))

    def _find_matching_value(self, col_name: str, row_dict: dict[str, Any]) -> str:
        """Cerca il valore nel dizionario con matching flessibile."""
        norm_col = self._normalize_key(col_name)
        for k, v in row_dict.items():
            if self._normalize_key(k) == norm_col:
                return str(v)
        return ""

    def _normalize_key(self, s: str) -> str:
        """Rimuove caratteri non alfanumerici e converte in minuscolo."""
        return "".join(c.lower() for c in s if c.isalnum())

    def _set_cell_value(self, row: int, col: int, value: str, col_type: str | None) -> None:
        """Imposta il valore di una cella (widget o item)."""
        if col_type == "combo":
            combo = self.table.cellWidget(row, col)
            if isinstance(combo, FilterComboBox):
                idx = combo.findText(value)
                if idx >= 0:
                    combo.setCurrentIndex(idx)
        else:
            item = self.table.item(row, col)
            if item:
                item.setText(value)

    def update_cell(self, row: int, col: int, value: str, emit_signal: bool = True) -> None:
        """Aggiorna il contenuto di una cella specifica.

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
                # Se  un widget (es. combo), non facciamo nulla o gestiamo se serve
                widget = self.table.cellWidget(row, col)
                if isinstance(widget, FilterComboBox):
                    idx = widget.findText(value)
                    if idx >= 0:
                        widget.setCurrentIndex(idx)
        finally:
            if not emit_signal:
                self.table.blockSignals(False)

    def setPlaceholderText(self, text: str) -> None:
        """Proxy per impostare il placeholder nella tabella sottostante."""
        self.table.setPlaceholderText(text)

    def set_row_status(self, row: int, status: str) -> None:
        """Proxy per impostare lo stato semantico della riga nella tabella.

        Args:
          row: Indice della riga.
          status: Stato della riga.
        """
        self.table.set_row_status(row, status)

    def update_column_options(self, col: int, options: list[str]) -> None:
        """Aggiorna le opzioni di una colonna di tipo 'combò per tutte le righe esistenti.

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
