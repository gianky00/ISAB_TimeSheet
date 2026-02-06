import os
from contextlib import suppress
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QFont
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QMenu,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.core.constants import Icons
from src.core.contabilita_manager import ContabilitaManager
from src.gui.formatters import format_date_it, format_number_smart
from src.gui.widgets import ExcelTableWidget
from src.gui.widgets.sortable_table_item import SortableTableWidgetItem
from src.utils.helpers import get_asset_path, get_colored_icon


class GiornaliereYearTab(QWidget):
    """Tab per un singolo anno (Giornaliere)."""

    COLUMNS = [
        "DATA",
        "PERSONALE",
        "TCL",
        "DESCRIZIONE\nATTIVITA'",
        "N°\nPREV.",
        "ODC",
        "PDL",
        "INIZIO",
        "FINE",
        "ORE",
    ]
    COL_DATA = 0
    COL_ORE = 9
    COL_DESC = 3
    IDX_NOMEFILE = 10

    def __init__(self, year: int, parent=None):
        super().__init__(parent)
        self.year = year
        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        """Inizializza l'interfaccia utente del tab per l'anno specifico."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 0)
        self.table = ExcelTableWidget()
        self.table.setColumnCount(len(self.COLUMNS))
        self.table.setHorizontalHeaderLabels(self.COLUMNS)

        # --- Ottimizzazione Layout ---
        self.table.setWordWrap(True)  # Abilita testo a capo
        self.table.setTextElideMode(
            Qt.TextElideMode.ElideNone
        )  # Evita i puntini di sospensione

        # --- Configurazione Selezione (Single row, come richiesto) ---
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # Remove hardcoded stylesheet (uses global light.qss)
        self.table.auto_copy_headers = True
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

        # Impostazione larghezze
        self.table.setColumnWidth(0, 95)  # Data
        self.table.setColumnWidth(1, 180)  # Personale
        self.table.setColumnWidth(2, 80)  # TCL
        self.table.setColumnWidth(3, 350)  # Descrizione (abbastanza larga per wrap)
        self.table.setColumnWidth(4, 80)  # N Prev
        self.table.setColumnWidth(5, 110)  # ODC
        self.table.setColumnWidth(6, 80)  # PDL
        self.table.setColumnWidth(7, 70)  # Inizio
        self.table.setColumnWidth(8, 70)  # Fine
        self.table.setColumnWidth(9, 80)  # Ore

        # La descrizione si espande ma permette il wrap
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

    def refresh_data(self):
        """Metodo pubblico per rinfrescare i dati del tab."""
        self._load_data()

    def _load_data(self):
        data = ContabilitaManager.get_giornaliere_by_year(self.year)
        self.table.setSortingEnabled(False)
        self.table.blockSignals(True)
        try:
            self.table.setRowCount(len(data))
            align_right = Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            for row_idx, row_data in enumerate(data):
                for col_idx in range(len(self.COLUMNS)):
                    val = row_data[col_idx]
                    formatted_val = self._format_value(col_idx, val)
                    item = SortableTableWidgetItem(formatted_val)

                    # Allineamento Numeri
                    if col_idx == self.COL_ORE:
                        item.setTextAlignment(align_right)

                    self.table.setItem(row_idx, col_idx, item)

                if len(row_data) > self.IDX_NOMEFILE and self.table.item(row_idx, 0):
                    self.table.item(row_idx, 0).setData(
                        Qt.ItemDataRole.UserRole, row_data[self.IDX_NOMEFILE]
                    )

            # Cruciale per il WordWrap: ridimensiona altezze righe dopo il popolamento
            self.table.resizeRowsToContents()
            self._add_totals_row()
            self._update_totals()
        finally:
            self.table.blockSignals(False)
            self.table.setSortingEnabled(True)

    def _format_value(self, col_idx, val):
        if val is None or str(val).lower() == "nan":
            return ""

        if col_idx == self.COL_DATA:
            return format_date_it(val)
        if col_idx == self.COL_ORE:
            return format_number_smart(val)
        return str(val).strip()

    def _format_number(self, val):
        """Usa il formattatore smart per i totali."""
        return format_number_smart(val)

    def _add_totals_row(self):
        if (
            self.table.rowCount() > 0
            and self.table.item(self.table.rowCount() - 1, 0).text() == "TOTALI"
        ):
            return
        row_idx = self.table.rowCount()
        self.table.insertRow(row_idx)
        item = SortableTableWidgetItem("TOTALI")
        item.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        item.setBackground(Qt.GlobalColor.lightGray)
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row_idx, 0, item)
        for c in range(1, self.table.columnCount()):
            it = SortableTableWidgetItem("")
            it.setBackground(Qt.GlobalColor.lightGray)
            it.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            it.setFlags(it.flags() & ~Qt.ItemFlag.ItemIsEditable)
            if c == self.COL_ORE:
                it.setTextAlignment(
                    Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                )
            self.table.setItem(row_idx, c, it)

    def _update_totals(self):
        total_row_idx = (
            self.table.rowCount() - 1
            if self.table.rowCount() > 0
            and self.table.item(self.table.rowCount() - 1, 0).text() == "TOTALI"
            else -1
        )
        if total_row_idx == -1:
            return
        sum_ore = 0.0
        for r in range(total_row_idx):
            if not self.table.isRowHidden(r):
                item = self.table.item(r, self.COL_ORE)
                if item and item.text():
                    with suppress(Exception):
                        # Pulisce la stringa formattata per fare la somma
                        clean_val = item.text().replace(".", "").replace(",", ".")
                        sum_ore += float(clean_val)
        self.table.item(total_row_idx, self.COL_ORE).setText(
            self._format_number(sum_ore)
        )

    def filter_data(self, text):
        """Filtra i dati dell'anno corrente in base alla ricerca testuale."""
        rows = self.table.rowCount()
        data_rows = (
            rows - 1
            if rows > 0 and self.table.item(rows - 1, 0).text() == "TOTALI"
            else rows
        )
        search_terms = text.lower().split()
        cols = self.table.columnCount()
        for r in range(data_rows):
            if not text:
                self.table.setRowHidden(r, False)
                continue
            row_text = " ".join(
                [
                    self.table.item(r, c).text().lower()
                    for c in range(cols)
                    if self.table.item(r, c)
                ]
            )
            self.table.setRowHidden(
                r, not all(term in row_text for term in search_terms)
            )
        self._update_totals()

    def _show_context_menu(self, pos):
        item = self.table.itemAt(pos)
        if not item or item.text() == "TOTALI":
            return
        filename = self.table.item(item.row(), 0).data(Qt.ItemDataRole.UserRole)
        menu = QMenu(self)
        lyra_action = QAction("Analizza riga con Lyra", self)
        lyra_action.setIcon(get_colored_icon(get_asset_path(Icons.SPARKLES), "#000000"))
        lyra_action.triggered.connect(lambda: self.table._analyze_row_at(pos))
        menu.addAction(lyra_action)
        menu.addSeparator()
        if filename:
            action = QAction(f"Apri {filename}", self)
            action.setIcon(
                get_colored_icon(get_asset_path(Icons.FOLDER_OPEN), "#000000")
            )
            action.triggered.connect(lambda: self._open_giornaliera(filename))
            menu.addAction(action)
        else:
            menu.addAction(QAction("Nessun file associato", self)).setEnabled(False)
        menu.exec(self.table.viewport().mapToGlobal(pos))

    def _open_giornaliera(self, filename):
        config = config_manager.load_config()
        root = os.path.normpath(config.get("giornaliere_path", ""))
        if not root:
            return
        found = None
        year_folder = os.path.join(root, f"Giornaliere {self.year}")
        if Path(year_folder).joinpath(filename).exists():
            found = os.path.join(year_folder, filename)
        if not found:
            for r, _d, files in os.walk(root):
                if filename in files:
                    found = os.path.join(r, filename)
                    break
        if found:
            os.startfile(os.path.normpath(found))
        else:
            QMessageBox.warning(self, "File non trovato", f"Non trovo '{filename}'.")
