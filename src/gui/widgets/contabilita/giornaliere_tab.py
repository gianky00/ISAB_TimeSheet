import os
from datetime import datetime
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QAction
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHeaderView, QAbstractItemView, QTableWidgetItem, QMenu, QMessageBox
from src.core.contabilita_manager import ContabilitaManager
from src.core import config_manager
from src.gui.widgets import ExcelTableWidget

class GiornaliereYearTab(QWidget):
    """Tab per un singolo anno (Giornaliere)."""

    COLUMNS = ["DATA", "PERSONALE", "TCL", "DESCRIZIONE\nATTIVITA'", "N°\nPREV.", "ODC", "PDL", "INIZIO", "FINE", "ORE"]
    COL_DATA = 0
    COL_ORE = 9
    IDX_NOMEFILE = 10

    def __init__(self, year: int, parent=None):
        super().__init__(parent)
        self.year = year
        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 0)
        self.table = ExcelTableWidget()
        self.table.setColumnCount(len(self.COLUMNS))
        self.table.setHorizontalHeaderLabels(self.COLUMNS)
        self.table.setWordWrap(True)
        self.table.setStyleSheet(
            """
            QTableWidget { background-color: white; color: black; gridline-color: #e9ecef; font-size: 13px; border: 1px solid #dee2e6; selection-background-color: #e7f1ff; selection-color: #0d6efd; }
            QTableWidget::item { color: black; }
            QHeaderView::section { background-color: #E1F5FE; color: #333333; padding: 10px 5px; border: none; border-right: 1px solid #B3E5FC; border-bottom: 3px solid #81D4FA; font-weight: bold; text-transform: uppercase; font-size: 11px; }
        """)
        self.table.auto_copy_headers = True
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table.setColumnWidth(0, 100); self.table.setColumnWidth(1, 200); self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 300); self.table.setColumnWidth(4, 80); self.table.setColumnWidth(5, 120)
        self.table.setColumnWidth(6, 80); self.table.setColumnWidth(7, 80); self.table.setColumnWidth(8, 80)
        self.table.setColumnWidth(9, 80)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

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
                    item = QTableWidgetItem(self._format_value(col_idx, val))
                    if col_idx == self.COL_ORE: item.setTextAlignment(align_right)
                    self.table.setItem(row_idx, col_idx, item)
                if len(row_data) > self.IDX_NOMEFILE and self.table.item(row_idx, 0):
                    self.table.item(row_idx, 0).setData(Qt.ItemDataRole.UserRole, row_data[self.IDX_NOMEFILE])
            self.table.resizeRowsToContents()
            self._add_totals_row()
            self._update_totals()
        finally:
            self.table.blockSignals(False)
            self.table.setSortingEnabled(True)

    def _add_totals_row(self):
        if self.table.rowCount() > 0 and self.table.item(self.table.rowCount()-1, 0).text() == "TOTALI": return
        row_idx = self.table.rowCount()
        self.table.insertRow(row_idx)
        item = QTableWidgetItem("TOTALI")
        item.setFont(QFont("Arial", 10, QFont.Weight.Bold)); item.setBackground(Qt.GlobalColor.lightGray)
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row_idx, 0, item)
        for c in range(1, self.table.columnCount()):
            it = QTableWidgetItem("")
            it.setBackground(Qt.GlobalColor.lightGray); it.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            it.setFlags(it.flags() & ~Qt.ItemFlag.ItemIsEditable)
            if c == self.COL_ORE: it.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row_idx, c, it)

    def _update_totals(self):
        total_row_idx = self.table.rowCount() - 1 if self.table.rowCount() > 0 and self.table.item(self.table.rowCount()-1, 0).text() == "TOTALI" else -1
        if total_row_idx == -1: return
        sum_ore = 0.0
        for r in range(total_row_idx):
            if not self.table.isRowHidden(r):
                item = self.table.item(r, self.COL_ORE)
                if item and item.text(): sum_ore += float(item.text().replace(",", "."))
        self.table.item(total_row_idx, self.COL_ORE).setText(self._format_number(sum_ore))

    def _format_number(self, val):
        try:
            v = round(float(val), 2)
            s_v = f"{v:g}".replace(".", ",")
            return s_v
        except: return str(val)

    def _format_value(self, col_idx, val):
        if not val: return ""
        s = str(val).strip()
        if s.lower() == "nan": return ""
        if col_idx == self.COL_DATA:
            for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"):
                try: return datetime.strptime(s.split(" ")[0], fmt).strftime("%d/%m/%Y")
                except: continue
        if col_idx == self.COL_ORE: return self._format_number(val)
        return s

    def filter_data(self, text):
        rows = self.table.rowCount()
        data_rows = rows - 1 if rows > 0 and self.table.item(rows-1, 0).text() == "TOTALI" else rows
        search_terms = text.lower().split()
        cols = self.table.columnCount()
        for r in range(data_rows):
            if not text:
                self.table.setRowHidden(r, False)
                continue
            row_text = " ".join([self.table.item(r, c).text().lower() for c in range(cols) if self.table.item(r, c)])
            self.table.setRowHidden(r, not all(term in row_text for term in search_terms))
        self._update_totals()

    def _show_context_menu(self, pos):
        item = self.table.itemAt(pos)
        if not item or item.text() == "TOTALI": return
        filename = self.table.item(item.row(), 0).data(Qt.ItemDataRole.UserRole)
        menu = QMenu(self)
        lyra_action = QAction("✨ Analizza Riga con Lyra", self)
        lyra_action.triggered.connect(lambda: self.table._analyze_row_at(pos))
        menu.addAction(lyra_action)
        menu.addSeparator()
        if filename:
            action = QAction(f"📂 Apri {filename}", self)
            action.triggered.connect(lambda: self._open_giornaliera(filename))
            menu.addAction(action)
        else:
            menu.addAction(QAction("Nessun file associato", self)).setEnabled(False)
        menu.exec(self.table.viewport().mapToGlobal(pos))

    def _open_giornaliera(self, filename):
        config = config_manager.load_config()
        root = os.path.normpath(config.get("giornaliere_path", ""))
        if not root: return
        found = None
        year_folder = os.path.join(root, f"Giornaliere {self.year}")
        if os.path.exists(os.path.join(year_folder, filename)): found = os.path.join(year_folder, filename)
        if not found:
            for r, d, files in os.walk(root):
                if filename in files: found = os.path.join(r, filename); break
        if found: os.startfile(os.path.normpath(found))
        else: QMessageBox.warning(self, "File non trovato", f"Non trovo '{filename}'.")
