import os
from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QFont
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QMenu,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.core.contabilita_manager import ContabilitaManager
from src.gui.widgets import ExcelTableWidget


class ContabilitaYearTab(QWidget):
    """Tab per un singolo anno (Tabella Dati)."""

    COLUMNS = [
        "DATA\nPREV.",
        "MESE",
        "N°\nPREV.",
        "TOTALE\nPREV.",
        "ATTIVITA'",
        "TCL",
        "ODC",
        "STATO\nATTIVITA'",
        "TIPOLOGIA",
        "ORE\nSP",
        "RESA",
        "ANNOTAZIONI",
    ]

    IDX_INDIRIZZO = 12
    IDX_NOMEFILE = 13
    COL_DATA = 0
    COL_N_PREV = 2
    COL_TOTALE = 3
    COL_ODC = 6
    COL_ORE = 9
    COL_RESA = 10

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

        self.table.setStyleSheet("""
            QTableWidget { background-color: white; color: black; gridline-color: #e9ecef; font-size: 13px; border: 1px solid #dee2e6; selection-background-color: #e7f1ff; selection-color: #0d6efd; }
            QTableWidget::item { color: black; }
            QHeaderView::section { background-color: #E1F5FE; color: #333333; padding: 10px 5px; border: none; border-right: 1px solid #B3E5FC; border-bottom: 3px solid #81D4FA; font-weight: bold; text-transform: uppercase; font-size: 11px; }
        """)

        self.table.auto_copy_headers = True
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

        self.table.setColumnWidth(self.COL_DATA, 100)
        self.table.setColumnWidth(1, 100)
        self.table.setColumnWidth(2, 80)
        self.table.setColumnWidth(self.COL_TOTALE, 120)
        self.table.setColumnWidth(4, 300)
        self.table.setColumnWidth(5, 150)
        self.table.setColumnWidth(6, 120)
        self.table.setColumnWidth(7, 150)
        self.table.setColumnWidth(8, 100)
        self.table.setColumnWidth(self.COL_ORE, 80)
        self.table.setColumnWidth(self.COL_RESA, 80)
        header.setSectionResizeMode(11, QHeaderView.ResizeMode.Stretch)

        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)

        layout.addWidget(self.table)

    def _load_data(self):
        data = ContabilitaManager.get_data_by_year(self.year)
        self.table.setSortingEnabled(False)
        self.table.blockSignals(True)
        try:
            self.table.setRowCount(len(data))
            align_right = Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            right_cols = {self.COL_TOTALE, self.COL_ORE, self.COL_RESA}
            for row_idx, row_data in enumerate(data):
                for col_idx in range(len(self.COLUMNS)):
                    val = row_data[col_idx]
                    formatted = self._format_value(col_idx, val)
                    item = QTableWidgetItem(formatted)
                    if col_idx in right_cols:
                        item.setTextAlignment(align_right)
                    self.table.setItem(row_idx, col_idx, item)
                indirizzo = row_data[self.IDX_INDIRIZZO]
                if self.table.item(row_idx, 0):
                    self.table.item(row_idx, 0).setData(
                        Qt.ItemDataRole.UserRole, indirizzo
                    )
            self.table.resizeRowsToContents()
            self._add_totals_row()
            self._update_totals()
        finally:
            self.table.blockSignals(False)
            self.table.setSortingEnabled(True)

    def _add_totals_row(self):
        if self.table.rowCount() > 0:
            last = self.table.item(self.table.rowCount() - 1, 0)
            if last and last.text() == "TOTALI":
                return
        row_idx = self.table.rowCount()
        self.table.insertRow(row_idx)
        item = QTableWidgetItem("TOTALI")
        item.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        item.setBackground(Qt.GlobalColor.lightGray)
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row_idx, 0, item)
        for c in range(1, self.table.columnCount()):
            it = QTableWidgetItem("")
            it.setBackground(Qt.GlobalColor.lightGray)
            it.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            it.setFlags(it.flags() & ~Qt.ItemFlag.ItemIsEditable)
            if c in [self.COL_TOTALE, self.COL_ORE, self.COL_RESA, self.COL_N_PREV]:
                it.setTextAlignment(
                    Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                )
            self.table.setItem(row_idx, c, it)

    def _update_totals(self):
        total_row_idx = -1
        if self.table.rowCount() > 0:
            last = self.table.item(self.table.rowCount() - 1, 0)
            if last and last.text() == "TOTALI":
                total_row_idx = self.table.rowCount() - 1
        if total_row_idx == -1:
            return

        count_prev, sum_totale, sum_ore = 0, 0.0, 0.0
        for r in range(total_row_idx):
            if not self.table.isRowHidden(r):
                count_prev += 1
                is_excl = False
                r_item = self.table.item(r, self.COL_RESA)
                if r_item and "INS.ORE SP" in r_item.text().upper():
                    is_excl = True
                if not is_excl:
                    t_item = self.table.item(r, self.COL_TOTALE)
                    if t_item:
                        sum_totale += self._parse_currency(t_item.text())
                o_item = self.table.item(r, self.COL_ORE)
                if o_item:
                    sum_ore += self._parse_float(o_item.text())

        self.table.item(total_row_idx, self.COL_N_PREV).setText(str(count_prev))
        self.table.item(total_row_idx, self.COL_TOTALE).setText(
            self._format_currency(sum_totale)
        )
        self.table.item(total_row_idx, self.COL_ORE).setText(
            self._format_number(sum_ore)
        )
        weighted_resa = sum_totale / sum_ore if sum_ore > 0 else 0.0
        self.table.item(total_row_idx, self.COL_RESA).setText(
            self._format_number(weighted_resa)
        )

    def _parse_currency(self, text):
        try:
            return float(
                text.replace("€", "").replace(".", "").replace(",", ".").strip()
            )
        except Exception:
            return 0.0

    def _parse_float(self, text):
        try:
            return float(text.replace(",", "."))
        except Exception:
            return 0.0

    def _format_currency(self, val):
        return f"€ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def _format_number(self, val):
        try:
            v = round(float(val), 2)
            return f"{int(v)}" if v.is_integer() else f"{v:.2f}".replace(".", ",")
        except Exception:
            return str(val)

    def _format_value(self, col_idx, val):
        if not val and val != 0:
            return ""
        s = str(val).strip()
        if not s:
            return ""
        if col_idx == self.COL_DATA:
            for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"):
                try:
                    return datetime.strptime(s.split(" ")[0], fmt).strftime("%d/%m/%Y")
                except Exception:
                    continue
        elif col_idx == self.COL_TOTALE:
            try:
                return self._format_currency(float(s))
            except Exception:
                pass
        elif col_idx in [self.COL_ORE, self.COL_RESA]:
            try:
                return self._format_number(float(s))
            except Exception:
                pass
        elif col_idx == self.COL_ODC:
            return s.replace("-", "/")
        return s

    def filter_data(self, text):
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
        row = item.row()
        file_path = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        menu = QMenu(self)
        lyra_action = QAction("✨ Analizza Riga con Lyra", self)
        lyra_action.triggered.connect(lambda: self.table._analyze_row_at(pos))
        menu.addAction(lyra_action)
        menu.addSeparator()
        action_open = QAction("📂 Apri File", self)
        if file_path:
            action_open.triggered.connect(lambda: os.startfile(file_path))
        else:
            action_open.setEnabled(False)
        menu.addAction(action_open)
        menu.exec(self.table.viewport().mapToGlobal(pos))
