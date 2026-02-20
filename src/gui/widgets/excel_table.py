"""
SyncroJob - Excel Table Widgets
Widget tabellari avanzati con funzionalità di editing, copia/incolla e integrazione con l'AI Lyra.
"""

from collections.abc import Sequence
from typing import Any

from PyQt6.QtCore import QPoint, Qt, pyqtSignal
from PyQt6.QtGui import QAction, QBrush, QColor, QCursor, QKeySequence
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QComboBox,
    QFileDialog,
    QFrame,
    QGraphicsDropShadowEffect,
    QHeaderView,
    QMenu,
    QTableWidget,
    QTableWidgetItem,
    QToolTip,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.gui.widgets.sortable_table_item import SortableTableWidgetItem
from src.utils.helpers import get_asset_path, get_colored_icon


class ExcelTableWidget(QTableWidget):
    """
    QTableWidget potenziato con funzionalità avanzate:
    - Copia/Incolla intelligente (compatibile con Excel/TSV).
    - Gestione dello stato delle righe (colorazione semantica).
    - Integrazione con l'AI Lyra per l'analisi contestuale delle righe.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Inizializza la tabella e configura i trigger di editing."""
        super().__init__(*args, **kwargs)
        self.auto_copy_headers = False  # Flag per copiare automaticamente le intestazioni

        self.setEditTriggers(
            QAbstractItemView.EditTrigger.DoubleClicked
            | QAbstractItemView.EditTrigger.EditKeyPressed
            | QAbstractItemView.EditTrigger.AnyKeyPressed
        )

    def set_row_status(self, row: int, status: str) -> None:
        """
        Imposta il colore di sfondo della riga in base allo stato di avanzamento del bot.

        Args:
            row: Indice della riga.
            status: Stringa identificativa dello stato ('completato', 'errore', 'in_corso', 'da_processare').
        """
        color = {
            "completato": QColor("#C8E6C9"),  # Verde chiaro
            "errore": QColor("#FFCDD2"),  # Rosso chiaro
            "in_corso": QColor("#FFF9C4"),  # Giallo chiaro
            "da_processare": QColor("#FFFFFF"),  # Bianco
        }.get(status, QColor("white"))

        for col in range(self.columnCount()):
            item = self.item(row, col)
            if item:
                item.setBackground(QBrush(color))
                # Ripristina testo nero per contrasto
                item.setForeground(QBrush(QColor("black")))

    def keyPressEvent(self, event: Any) -> None:
        """Gestisce le scorciatoie da tastiera standard (Copia, Incolla, Cancella)."""
        if event.matches(QKeySequence.StandardKey.Copy):
            self.copy_selection()
        elif event.matches(QKeySequence.StandardKey.Paste):
            self.paste_selection()
        elif event.key() == Qt.Key.Key_Delete:
            self.clear_selection()
        else:
            super().keyPressEvent(event)

    def clear_selection(self) -> None:
        """Svuota il contenuto delle celle selezionate, gestendo sia testi che widget personalizzati."""
        ranges = self.selectedRanges()
        for r in ranges:
            for row in range(r.topRow(), r.bottomRow() + 1):
                for col in range(r.leftColumn(), r.rightColumn() + 1):
                    # Gestione Widget (es. ComboBox)
                    widget = self.cellWidget(row, col)
                    if isinstance(widget, QComboBox):
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

    def paste_selection(self) -> None:
        """Incolla i dati dagli appunti del sistema nella tabella a partire dalla cella corrente."""
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
        """Recupera il testo contenuto negli appunti."""
        clipboard = QApplication.clipboard()
        return clipboard.text() if clipboard else ""

    def _get_paste_start_pos(self) -> tuple[int, int]:
        """Restituisce la posizione di partenza (riga, colonna) per l'operazione di incolla."""
        r, c = self.currentRow(), self.currentColumn()
        return (max(0, r), max(0, c))

    def _paste_cell_data(self, row: int, col: int, text: str) -> None:
        """Aggiorna il contenuto di una singola cella con il testo fornito."""
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

    def contextMenuEvent(self, event: Any) -> None:
        """Genera il menu contestuale con opzioni di copia e analisi AI."""
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

        copy_action = QAction(get_colored_icon(get_asset_path(Icons.EDIT), "#000000"), "Copia", self)
        copy_action.triggered.connect(self.copy_selection)
        menu.addAction(copy_action)
        menu.exec(event.globalPos())

    def _analyze_row_at(self, pos: QPoint) -> None:
        """Estrae i dati della riga alla posizione specificata e li invia a Lyra."""
        item = self.itemAt(pos)
        if not item:
            return
        row = item.row()

        row_data: list[str] = []
        for c in range(self.columnCount()):
            if not self.isColumnHidden(c):
                header_item = self.horizontalHeaderItem(c)
                header = header_item.text() if header_item else f"Col {c}"
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
            win.analyze_with_lyra(context)  # type: ignore

    def _analyze_selection(self) -> None:
        """Invia il testo di tutte le celle selezionate all'AI Lyra."""
        selection = self.selectedRanges()
        if not selection:
            return

        rows_text: list[str] = []
        for r in range(selection[0].topRow(), selection[0].bottomRow() + 1):
            row_data = []
            for c in range(self.columnCount()):
                item = self.item(r, c)
                if item and not self.isColumnHidden(c):
                    header_item = self.horizontalHeaderItem(c)
                    header_text = header_item.text() if header_item else f"Col {c}"
                    row_data.append(f"{header_text}: {item.text()}")
            rows_text.append(" | ".join(row_data))

        context = "\n".join(rows_text)

        win = self.window()
        if hasattr(win, "analyze_with_lyra"):
            win.analyze_with_lyra(context)  # type: ignore

    def copy_selection(self) -> None:
        """Copia i dati selezionati in formato TSV negli appunti."""
        selection = self.selectedIndexes()
        if not selection:
            return

        rows, cols = self._get_selected_rows_cols(selection)
        if not rows or not cols:
            return

        tsv_rows: list[str] = []
        # 1. Header (se abilitato)
        if self.auto_copy_headers and len(self.selectedItems()) > 1:
            tsv_rows.append(self._build_header_tsv(cols))

        # 2. Data Rows
        tsv_rows.extend(self._get_row_as_tsv(r, cols) for r in rows if not self.isRowHidden(r))

        if tsv_rows:
            clipboard = QApplication.clipboard()
            if clipboard:
                clipboard.setText("\n".join(tsv_rows))
            QToolTip.showText(QCursor.pos(), "Copiato!", self)

    def _get_selected_rows_cols(self, ranges: Sequence[Any]) -> tuple[list[int], list[int]]:
        """Estrae indici univoci di riga e colonna da una sequenza di indici o range."""
        rows: set[int] = set()
        cols: set[int] = set()
        for item in ranges:
            if hasattr(item, "topRow"):  # QTableWidgetSelectionRange
                rows.update(range(item.topRow(), item.bottomRow() + 1))
                cols.update(range(item.leftColumn(), item.rightColumn() + 1))
            elif hasattr(item, "row"):  # QModelIndex
                rows.add(item.row())
                cols.add(item.column())
        return sorted(rows), sorted(cols)

    def _build_header_tsv(self, cols: list[int]) -> str:
        """Genera una stringa TSV contenente le intestazioni delle colonne specificate."""
        headers: list[str] = []
        for c in cols:
            if not self.isColumnHidden(c):
                it = self.horizontalHeaderItem(c)
                headers.append(it.text() if it else "")
        return "\t".join(headers)

    def _get_row_as_tsv(self, row: int, cols: list[int]) -> str:
        """Converte i dati di una riga in formato TSV per le colonne selezionate."""
        data: list[str] = []
        for c in cols:
            val = self._get_cell_value(row, c)
            data.append(val.replace("\t", " ").replace("\n", " "))
        return "\t".join(data)

    def _get_cell_value(self, row: int, col: int) -> str:
        """Estrae il valore testuale da una cella, gestendo anche widget interni."""
        widget = self.cellWidget(row, col)
        if isinstance(widget, QComboBox):
            return widget.currentText()
        it = self.item(row, col)
        return it.text() if it else ""


class EditableDataTable(QWidget):
    """
    Widget ad alto livello che incapsula una ExcelTableWidget.
    Fornisce menu contestuali per gestire righe (aggiunta/rimozione) e manipolare i dati.
    """

    data_changed = pyqtSignal()
    """Segnale emesso quando il contenuto della tabella viene modificato."""

    def __init__(self, columns: list[dict[str, Any]], parent: QWidget | None = None) -> None:
        """
        Inizializza la tabella editabile.

        Args:
            columns: Lista di dizionari che definiscono le colonne (name, type, options).
            parent: Widget genitore.
        """
        super().__init__(parent)
        self.columns = columns
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Configura il layout e la tabella interna con design Neon & Shadow."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 15)
        layout.setSpacing(0)

        # --- CONTAINER PRINCIPALE (Card con ombra e neon cyan) ---
        self.container = QFrame()
        self.container.setObjectName("tableContainer")
        self.container.setStyleSheet("""
            QFrame#tableContainer {
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                border-bottom: 3px solid #00E5FF; /* Cyan Neon */
                border-radius: 12px;
            }
            QTableWidget {
                background-color: transparent;
                border: none;
                gridline-color: #f1f3f5;
                selection-background-color: #E0F7FA;
                selection-color: #000000;
                outline: none;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                color: #424242;
                padding: 10px;
                font-weight: bold;
                border: none;
                border-bottom: 1px solid #dee2e6;
            }
        """)

        # Shadow Effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(8)
        shadow.setColor(QColor(0, 0, 0, 40))
        self.container.setGraphicsEffect(shadow)

        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(5, 5, 5, 5)

        self.table = ExcelTableWidget()
        self.table.setColumnCount(len(self.columns))
        self.table.setHorizontalHeaderLabels([str(c["name"]) for c in self.columns])

        header = self.table.horizontalHeader()
        if header is not None:
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            header.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)
        self.table.itemChanged.connect(self._on_item_changed)

        for _ in range(5):
            self._add_row()

        container_layout.addWidget(self.table)
        layout.addWidget(self.container)

    def _show_context_menu(self, position: QPoint) -> None:
        """Visualizza il menu contestuale per la gestione delle righe e dei dati."""
        menu = QMenu()

        lyra_action = QAction(
            get_colored_icon(get_asset_path(Icons.SPARKLES), "#000000"),
            "Analizza con Lyra",
            self,
        )
        lyra_action.triggered.connect(self.table._analyze_selection)
        menu.addAction(lyra_action)
        menu.addSeparator()

        copy_action = QAction(get_colored_icon(get_asset_path(Icons.EDIT), "#000000"), "Copia", self)
        copy_action.triggered.connect(self.table.copy_selection)
        menu.addAction(copy_action)

        paste_action = QAction(get_colored_icon(get_asset_path(Icons.UPLOAD), "#000000"), "Incolla", self)
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

        viewport = self.table.viewport()
        if viewport is not None:
            menu.exec(viewport.mapToGlobal(position))

    def _add_row(self) -> None:
        """Aggiunge una riga vuota alla fine della tabella."""
        row = self.table.rowCount()
        self.table.insertRow(row)
        self._populate_row(row)
        self.data_changed.emit()

    def _add_row_above(self) -> None:
        """Inserisce una riga vuota sopra la riga attualmente selezionata."""
        current_row = self.table.currentRow()
        if current_row < 0:
            current_row = 0

        self.table.insertRow(current_row)
        self._populate_row(current_row)
        self.data_changed.emit()

    def _populate_row(self, row: int) -> None:
        """Inizializza le celle di una riga con i widget appropriati (testo o combo)."""
        for col, column in enumerate(self.columns):
            col_type = column.get("type", "text")

            if col_type == "combo":
                combo = QComboBox()
                combo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
                combo.setStyleSheet(
                    """
                    QComboBox { border: none; background: transparent; color: black; padding-left: 5px; }
                    QComboBox QAbstractItemView { background-color: white; color: black; selection-background-color: #e7f1ff; selection-color: #0d6efd; }
                """
                )
                options = ["", *column.get("options", [])]
                combo.addItems(options)
                default_val = column.get("default", "")
                if default_val and default_val in options:
                    combo.setCurrentText(str(default_val))
                combo.currentTextChanged.connect(lambda text: self.data_changed.emit())
                self.table.setCellWidget(row, col, combo)
            else:
                default_val = column.get("default", "")
                item = SortableTableWidgetItem(default_val)
                self.table.setItem(row, col, item)

    def _remove_row(self) -> None:
        """Rimuove la riga attualmente selezionata."""
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.table.removeRow(current_row)
            self.data_changed.emit()

    def _clear_all(self) -> None:
        """Svuota completamente la tabella e ripristina una riga iniziale."""
        self.table.setRowCount(0)
        self._add_row()
        self.data_changed.emit()

    def _on_item_changed(self, item: QTableWidgetItem) -> None:
        """Emette il segnale di modifica dati quando un item cambia."""
        self.data_changed.emit()

    def get_data(self) -> list[dict[str, Any]]:
        """
        Estrae tutti i dati validi (righe non vuote) dalla tabella.

        Returns:
            list: Lista di dizionari con chiavi derivate dai nomi delle colonne.
        """
        data: list[dict[str, Any]] = []
        for row in range(self.table.rowCount()):
            row_data: dict[str, Any] = {}
            has_data = False
            for col, column in enumerate(self.columns):
                key = str(column["name"]).lower().replace(" ", "_")
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

    def set_data(self, data: list[dict[str, Any]]) -> None:
        """
        Popola la tabella con una lista di dati, resettando il contenuto precedente.

        Args:
            data: Lista di dizionari contenenti i valori per le colonne.
        """
        self.table.blockSignals(True)
        self.table.setRowCount(0)
        for row_data in data:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self._populate_row_from_data(row, row_data)
        if self.table.rowCount() == 0:
            while self.table.rowCount() < 5:
                self._add_row()
        self.table.blockSignals(False)

    def _populate_row_from_data(self, row: int, row_data: dict[str, Any]) -> None:
        """Popola una riga specifica utilizzando i dati forniti."""
        for col, column in enumerate(self.columns):
            col_type = column.get("type", "text")
            key = str(column["name"]).lower().replace(" ", "_")
            value = row_data.get(key, "")

            if col_type == "combo":
                combo = QComboBox()
                combo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
                combo.setStyleSheet(
                    """
                    QComboBox { border: none; background: transparent; color: black; padding-left: 5px; }
                    QComboBox QAbstractItemView { background-color: white; color: black; selection-background-color: #e7f1ff; selection-color: #0d6efd; }
                """
                )
                options = ["", *column.get("options", [])]
                combo.addItems(options)
                if value:
                    idx = combo.findText(str(value))
                    if idx >= 0:
                        combo.setCurrentIndex(idx)
                    else:
                        combo.setCurrentIndex(0)
                else:
                    combo.setCurrentIndex(0)
                combo.currentTextChanged.connect(lambda text: self.data_changed.emit())
                self.table.setCellWidget(row, col, combo)
            else:
                item = SortableTableWidgetItem(str(value))
                self.table.setItem(row, col, item)

    def update_column_options(self, column_name: str, new_options: list[str]) -> None:
        """
        Aggiorna dinamicamente le opzioni di una colonna di tipo ComboBox.

        Args:
            column_name: Nome esatto della colonna da aggiornare.
            new_options: Nuova lista di stringhe per il menu a tendina.
        """
        target_col_idx = -1
        for i, col in enumerate(self.columns):
            if col["name"] == column_name:
                col["options"] = new_options
                target_col_idx = i
                break

        if target_col_idx == -1:
            return

        self.table.blockSignals(True)
        for row in range(self.table.rowCount()):
            widget = self.table.cellWidget(row, target_col_idx)
            if isinstance(widget, QComboBox):
                current_text = widget.currentText()
                widget.clear()
                widget.addItems(["", *new_options])
                if current_text in new_options:
                    widget.setCurrentText(current_text)
                elif new_options:
                    widget.setCurrentIndex(0)
        self.table.blockSignals(False)
