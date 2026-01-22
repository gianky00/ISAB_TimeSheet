"""
SyncroJob - Excel Table Widgets
Tabella potenziata con funzionalità stile Excel.
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction, QBrush, QColor, QCursor, QKeySequence
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QComboBox,
    QHeaderView,
    QMenu,
    QTableWidget,
    QToolTip,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.gui.widgets.sortable_table_item import SortableTableWidgetItem
from src.utils.helpers import get_asset_path, get_colored_icon


class ExcelTableWidget(QTableWidget):
    """QTableWidget potenziato con funzionalità copia stile Excel."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auto_copy_headers = (
            False  # Flag per copiare automaticamente le intestazioni
        )

        # Non impostiamo SelectionBehavior/Mode qui per permettere alle istanze di configurarlo
        # Assicura che il click selezioni anche se clicco su una cella non editabile
        self.setEditTriggers(
            QAbstractItemView.EditTrigger.DoubleClicked
            | QAbstractItemView.EditTrigger.EditKeyPressed
            | QAbstractItemView.EditTrigger.AnyKeyPressed
        )

    def set_row_status(self, row, status):
        """
        Imposta il colore di sfondo della riga in base allo stato.
        Status: 'completato', 'errore', 'in_corso', 'da_processare'
        """
        colors = {
            "completato": QColor("#C8E6C9"),  # Verde chiaro
            "errore": QColor("#FFCDD2"),  # Rosso chiaro
            "in_corso": QColor("#FFF9C4"),  # Giallo chiaro
            "da_processare": QColor("#FFFFFF"),  # Bianco
        }
        color = colors.get(status, QColor("white"))

        for col in range(self.columnCount()):
            item = self.item(row, col)
            if item:
                item.setBackground(QBrush(color))
                # Restore black text for contrast
                item.setForeground(QBrush(QColor("black")))

    def keyPressEvent(self, event):
        """Gestisce la pressione dei tasti (Copia/Incolla/Cancella)."""
        if event.matches(QKeySequence.StandardKey.Copy):
            self.copy_selection()
        elif event.matches(QKeySequence.StandardKey.Paste):
            self.paste_selection()
        elif event.key() == Qt.Key.Key_Delete:
            self.clear_selection()
        else:
            super().keyPressEvent(event)

    def clear_selection(self):
        """Cancella il contenuto delle celle selezionate (incluso reset ComboBox)."""
        ranges = self.selectedRanges()
        for r in ranges:
            for row in range(r.topRow(), r.bottomRow() + 1):
                for col in range(r.leftColumn(), r.rightColumn() + 1):
                    # Gestione Widget (es. ComboBox)
                    widget = self.cellWidget(row, col)
                    if isinstance(widget, QComboBox):
                        # Cerca opzione vuota o resetta
                        idx = widget.findText("")
                        if idx >= 0:
                            widget.setCurrentIndex(idx)
                        else:
                            widget.setCurrentIndex(-1)
                    else:
                        # Gestione Item Standard
                        item = self.item(row, col)
                        if item and (item.flags() & Qt.ItemFlag.ItemIsEditable):
                            item.setText("")

    def paste_selection(self):
        """Incolla il contenuto degli appunti nella tabella."""
        text = self._get_clipboard_text()
        if not text:
            return

        rows_data = text.split("\n")
        if rows_data and not rows_data[-1]:
            rows_data.pop()

        start_row, start_col = self._get_paste_start_pos()

        for r_idx, row_text in enumerate(rows_data):
            target_r = start_row + r_idx
            if target_r >= self.rowCount():
                break

            cols_data = row_text.split("\t")
            for c_idx, cell_text in enumerate(cols_data):
                target_c = start_col + c_idx
                if target_c >= self.columnCount() or self.isColumnHidden(target_c):
                    continue
                self._paste_cell_data(target_r, target_c, cell_text.strip())

    def _get_clipboard_text(self) -> str:
        clipboard = QApplication.clipboard()
        return clipboard.text() if clipboard else ""

    def _get_paste_start_pos(self) -> tuple[int, int]:
        r, c = self.currentRow(), self.currentColumn()
        return (max(0, r), max(0, c))

    def _paste_cell_data(self, row: int, col: int, text: str):
        """Aggiorna una cella specifica con il testo fornito."""
        widget = self.cellWidget(row, col)
        if isinstance(widget, QComboBox):
            idx = widget.findText(text)
            if idx >= 0:
                widget.setCurrentIndex(idx)
        else:
            item = self.item(row, col)
            if not item:
                item = SortableTableWidgetItem(text)
                self.setItem(row, col, item)
            else:
                item.setText(text)

    def contextMenuEvent(self, event):
        """Menu contestuale predefinito per copia veloce (per tabelle read-only)."""
        menu = QMenu(self)

        # Action: Analyze ROW with Lyra
        lyra_row_action = QAction(
            get_colored_icon(get_asset_path(Icons.SPARKLES), "#000000"),
            "Analizza riga con Lyra",
            self,
        )
        lyra_row_action.triggered.connect(lambda: self._analyze_row_at(event.pos()))
        menu.addAction(lyra_row_action)

        lyra_selection_action = QAction(
            get_colored_icon(get_asset_path(Icons.SPARKLES), "#000000"),
            "Analizza selezione con Lyra",
            self,
        )
        lyra_selection_action.triggered.connect(self._analyze_selection)
        menu.addAction(lyra_selection_action)

        copy_action = QAction(
            get_colored_icon(get_asset_path(Icons.EDIT), "#000000"), "Copia", self
        )
        copy_action.triggered.connect(self.copy_selection)
        menu.addAction(copy_action)
        menu.exec(event.globalPos())

    def _analyze_row_at(self, pos):
        """Analizza la riga specifica sotto il cursore."""
        item = self.itemAt(pos)
        if not item:
            return
        row = item.row()

        row_data = []
        for c in range(self.columnCount()):
            if not self.isColumnHidden(c):
                header = (
                    self.horizontalHeaderItem(c).text()
                    if self.horizontalHeaderItem(c)
                    else f"Col {c}"
                )
                widget = self.cellWidget(row, c)
                if isinstance(widget, QComboBox):
                    text = widget.currentText()
                else:
                    it = self.item(row, c)
                    text = it.text() if it else ""

                row_data.append(f"**{header}**: {text}")

        context = " | ".join(row_data)

        win = self.window()
        if hasattr(win, "analyze_with_lyra"):
            win.analyze_with_lyra(context)

    def _analyze_selection(self):
        """Invia la selezione a Lyra."""
        selection = self.selectedRanges()
        if not selection:
            return

        rows_text = []
        for r in range(selection[0].topRow(), selection[0].bottomRow() + 1):
            row_data = []
            for c in range(self.columnCount()):
                item = self.item(r, c)
                if item and not self.isColumnHidden(c):
                    row_data.append(
                        f"{self.horizontalHeaderItem(c).text()}: {item.text()}"
                    )
            rows_text.append(" | ".join(row_data))

        context = "\n".join(rows_text)

        win = self.window()
        if hasattr(win, "analyze_with_lyra"):
            win.analyze_with_lyra(context)

    def copy_selection(self):
        """Copia le celle selezionate negli appunti."""
        selection = self.selectedIndexes()
        if not selection:
            return

        rows, cols = self._get_selected_rows_cols(selection)
        if not rows or not cols:
            return

        tsv_rows = []
        # 1. Header (se abilitato)
        if self.auto_copy_headers and len(self.selectedItems()) > 1:
            tsv_rows.append(self._build_header_tsv(cols))

        # 2. Data Rows
        for r in rows:
            if not self.isRowHidden(r):
                tsv_rows.append(self._get_row_as_tsv(r, cols))

        if tsv_rows:
            QApplication.clipboard().setText("\n".join(tsv_rows))
            QToolTip.showText(QCursor.pos(), "Copiato!", self)

    def _get_selected_rows_cols(self, ranges) -> tuple[list[int], list[int]]:
        """Estrae gli indici unici di riga e colonna dalla selezione."""
        rows = set()
        cols = set()
        for item in ranges:
            if hasattr(item, "topRow"):  # QTableWidgetSelectionRange
                for r in range(item.topRow(), item.bottomRow() + 1):
                    rows.add(r)
                for c in range(item.leftColumn(), item.rightColumn() + 1):
                    cols.add(c)
            elif hasattr(item, "row"):  # QModelIndex
                rows.add(item.row())
                cols.add(item.column())
        return sorted(rows), sorted(cols)

    def _build_header_tsv(self, cols: list[int]) -> str:
        headers = []
        for c in cols:
            if not self.isColumnHidden(c):
                it = self.horizontalHeaderItem(c)
                headers.append(it.text() if it else "")
        return "\t".join(headers)

    def _get_row_as_tsv(self, row: int, cols: list[int]) -> str:
        data = []
        for c in cols:
            val = self._get_cell_value(row, c)
            data.append(val.replace("\t", " ").replace("\n", " "))
        return "\t".join(data)

    def _get_cell_value(self, row: int, col: int) -> str:
        widget = self.cellWidget(row, col)
        if isinstance(widget, QComboBox):
            return widget.currentText()
        it = self.item(row, col)
        return it.text() if it else ""


class EditableDataTable(QWidget):
    """Tabella editabile con menu contestuale."""

    data_changed = pyqtSignal()

    def __init__(self, columns: list, parent=None):
        super().__init__(parent)
        self.columns = columns
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.table = ExcelTableWidget()
        self.table.setColumnCount(len(self.columns))
        self.table.setHorizontalHeaderLabels([c["name"] for c in self.columns])

        # Removed hardcoded stylesheet to rely on global light.qss
        # This ensures selection colors and borders are consistent app-wide

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setDefaultAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )

        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)
        self.table.itemChanged.connect(self._on_item_changed)

        for _ in range(5):
            self._add_row()

        layout.addWidget(self.table)

    def _show_context_menu(self, position):
        menu = QMenu()

        lyra_action = QAction(
            get_colored_icon(get_asset_path(Icons.SPARKLES), "#000000"),
            "Analizza con Lyra",
            self,
        )
        lyra_action.triggered.connect(self.table._analyze_selection)
        menu.addAction(lyra_action)
        menu.addSeparator()

        copy_action = QAction(
            get_colored_icon(get_asset_path(Icons.EDIT), "#000000"), "Copia", self
        )
        copy_action.triggered.connect(self.table.copy_selection)
        menu.addAction(copy_action)

        paste_action = QAction(
            get_colored_icon(get_asset_path(Icons.UPLOAD), "#000000"), "Incolla", self
        )
        paste_action.triggered.connect(self.table.paste_selection)
        menu.addAction(paste_action)

        menu.addSeparator()

        add_action = QAction(
            get_colored_icon(get_asset_path(Icons.PLUS), "#000000"),
            "Aggiungi riga",
            self,
        )
        add_action.triggered.connect(self._add_row)
        menu.addAction(add_action)

        add_above_action = QAction(
            get_colored_icon(get_asset_path(Icons.PLUS), "#000000"),
            "Aggiungi riga sopra",
            self,
        )
        add_above_action.triggered.connect(self._add_row_above)
        menu.addAction(add_above_action)

        menu.addSeparator()

        remove_action = QAction(
            get_colored_icon(get_asset_path(Icons.TRASH), "#000000"),
            "Rimuovi riga",
            self,
        )
        remove_action.triggered.connect(self._remove_row)
        menu.addAction(remove_action)

        clear_action = QAction(
            get_colored_icon(get_asset_path(Icons.TRASH), "#000000"),
            "Pulisci tutto",
            self,
        )
        clear_action.triggered.connect(self._clear_all)
        menu.addAction(clear_action)

        menu.exec(self.table.viewport().mapToGlobal(position))

    def _add_row(self):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self._populate_row(row)
        self.data_changed.emit()

    def _add_row_above(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            current_row = 0

        self.table.insertRow(current_row)
        self._populate_row(current_row)
        self.data_changed.emit()

    def _populate_row(self, row: int):
        for col, column in enumerate(self.columns):
            col_type = column.get("type", "text")

            if col_type == "combo":
                combo = QComboBox()
                combo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
                combo.setStyleSheet(
                    """
                    QComboBox {
                        border: none;
                        background: transparent;
                        color: black;
                        padding-left: 5px;
                    }
                    QComboBox QAbstractItemView {
                        background-color: white;
                        color: black;
                        selection-background-color: #e7f1ff;
                        selection-color: #0d6efd;
                    }
                """
                )
                options = [""] + column.get("options", [])
                combo.addItems(options)
                default_val = column.get("default", "")
                if default_val and default_val in options:
                    combo.setCurrentText(default_val)
                combo.currentTextChanged.connect(lambda text: self.data_changed.emit())
                self.table.setCellWidget(row, col, combo)
            else:
                default_val = column.get("default", "")
                item = SortableTableWidgetItem(default_val)
                self.table.setItem(row, col, item)

    def _remove_row(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.table.removeRow(current_row)
            self.data_changed.emit()

    def _clear_all(self):
        self.table.setRowCount(0)
        self._add_row()
        self.data_changed.emit()

    def _on_item_changed(self, item):
        self.data_changed.emit()

    def get_data(self) -> list:
        """Estrae tutti i dati dalla tabella come lista di dizionari."""
        data = []
        for row in range(self.table.rowCount()):
            row_data = {}
            has_data = False
            for col, column in enumerate(self.columns):
                key = column["name"].lower().replace(" ", "_")
                widget = self.table.cellWidget(row, col)
                if isinstance(widget, QComboBox):
                    value = widget.currentText()
                else:
                    item = self.table.item(row, col)
                    value = item.text() if item else ""
                row_data[key] = value
                if value:
                    has_data = True
            if has_data:
                data.append(row_data)
        return data

    def set_data(self, data: list):
        """
        Popola la tabella con i dati forniti.

        Args:
            data: Lista di dizionari contenenti i valori per le colonne.
        """
        self.table.blockSignals(True)
        self.table.setRowCount(0)
        for row_data in data:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self._populate_row(row)
            for col, column in enumerate(self.columns):
                key = column["name"].lower().replace(" ", "_")
                value = row_data.get(key, "")
                widget = self.table.cellWidget(row, col)
                if isinstance(widget, QComboBox):
                    if value:
                        idx = widget.findText(str(value))
                        if idx >= 0:
                            widget.setCurrentIndex(idx)
                        else:
                            # Se il valore non c'è, lo aggiungiamo? No, per le combo fisse meglio di no
                            # Ma se è un valore ad-hoc?
                            # Nel dubbio, proviamo a selezionarlo se c'è, altrimenti lasciamo vuoto (idx 0)
                            widget.setCurrentIndex(0)
                else:
                    item = self.table.item(row, col)
                    if item:
                        item.setText(str(value))
        if self.table.rowCount() == 0:
            while self.table.rowCount() < 5:
                self._add_row()
        self.table.blockSignals(False)

    def update_column_options(self, column_name: str, new_options: list):
        """Aggiorna le opzioni per una colonna di tipo combo."""
        # 1. Aggiorna definizione colonna
        target_col_idx = -1
        for i, col in enumerate(self.columns):
            if col["name"] == column_name:
                col["options"] = new_options
                target_col_idx = i
                break

        if target_col_idx == -1:
            return

        # 2. Aggiorna widget esistenti
        self.table.blockSignals(True)
        for row in range(self.table.rowCount()):
            widget = self.table.cellWidget(row, target_col_idx)
            if isinstance(widget, QComboBox):
                current_text = widget.currentText()
                widget.clear()
                # Aggiungi sempre opzione vuota
                widget.addItems([""] + new_options)

                # Tenta di ripristinare il valore
                if current_text in new_options:
                    widget.setCurrentText(current_text)
                elif new_options:
                    widget.setCurrentIndex(0)
        self.table.blockSignals(False)
