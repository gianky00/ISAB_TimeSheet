import json
from datetime import datetime
from typing import Any, Optional

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QColor
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMenu,
    QPushButton,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.core.contabilita_manager import ContabilitaManager
from src.core.excel_importer import ExcelImporter
from src.gui.widgets import ExcelTableWidget
from src.gui.widgets.sortable_table_item import SortableTableWidgetItem
from src.utils.helpers import get_asset_path, get_colored_icon


class AttivitaProgrammateTab(QWidget):
    """Tab per Attività Programmate."""

    COLUMNS = [
        "PS",
        "AREA",
        "PdL",
        "IMP.",
        "DESCRIZIONE\nATTIVITA'",
        "LUN",
        "MAR",
        "MER",
        "GIO",
        "VEN",
        "STATO\nPdL",
        "STATO\nATTIVITA'",
        "DATA\nCONTROLLO",
        "PERSONALE\nIMPIEGATO",
        "PO",
        "AVVISO",
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        """Configura l'interfaccia utente del tab."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 0)

        filter_layout = QHBoxLayout()
        filter_layout.setContentsMargins(5, 0, 5, 5)

        self.chk_ps = QCheckBox("Filtra PS")
        self.chk_ps.stateChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.chk_ps)

        self.chk_po = QCheckBox("Filtra PO")
        self.chk_po.stateChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.chk_po)

        filter_layout.addSpacing(20)
        filter_layout.addWidget(QLabel("Area:"))
        self.combo_area = QComboBox()
        self.combo_area.setMinimumWidth(150)
        self.combo_area.addItem("Tutte")
        self.combo_area.currentTextChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.combo_area)

        filter_layout.addSpacing(15)
        filter_layout.addWidget(QLabel("Stato PdL:"))
        self.combo_stato = QComboBox()
        self.combo_stato.setMinimumWidth(150)
        self.combo_stato.addItem("Tutti")
        self.combo_stato.currentTextChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.combo_stato)

        self.btn_reset = QPushButton("Reset Filtri")
        self.btn_reset.clicked.connect(self._reset_filters)
        filter_layout.addWidget(self.btn_reset)
        filter_layout.addStretch()
        layout.addLayout(filter_layout)

        self.table = ExcelTableWidget()
        self.table.setColumnCount(len(self.COLUMNS))
        self.table.setHorizontalHeaderLabels(self.COLUMNS)
        self.table.setWordWrap(True)
        self.table.setTextElideMode(Qt.TextElideMode.ElideNone)  # No troncamento
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.table.cellDoubleClicked.connect(lambda r, c: self.table.selectRow(r))

        self.table.auto_copy_headers = True
        header = self.table.horizontalHeader()
        # Inizialmente usa Interactive per permettere ridimensionamento automatico
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table.setColumnHidden(0, True)
        self.table.setColumnHidden(14, True)

        # Imposta larghezze minime ragionevoli
        self.table.setColumnWidth(1, 80)  # AREA
        self.table.setColumnWidth(2, 80)  # PdL
        self.table.setColumnWidth(3, 60)  # IMP.
        self.table.setColumnWidth(4, 350)  # DESCRIZIONE ATTIVITA'
        for i in range(5, 10):
            self.table.setColumnWidth(i, 50)  # Giorni settimana
        self.table.setColumnWidth(10, 120)  # STATO PdL
        self.table.setColumnWidth(11, 120)  # STATO ATTIVITA'
        self.table.setColumnWidth(12, 100)  # DATA CONTROLLO
        self.table.setColumnWidth(13, 150)  # PERSONALE IMPIEGATO
        self.table.setColumnWidth(15, 250)  # AVVISO

        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

    def refresh_data(self):
        self._load_data()

    def _load_data(self):
        data = ContabilitaManager.get_attivita_programmate_data()
        self.table.setSortingEnabled(False)
        self.table.blockSignals(True)
        self.table.setRowCount(0)
        try:
            self.table.setRowCount(len(data))
            db_keys = list(ExcelImporter.ATTIVITA_PROGRAMMATE_MAPPING.values())
            for row_idx, row_data in enumerate(data):
                self._populate_table_row(row_idx, row_data, db_keys)
            self.table.resizeRowsToContents()
            self._populate_filters()
            # Adatta le colonne al contenuto
            self._adjust_column_widths()
        finally:
            self.table.blockSignals(False)
            self.table.setSortingEnabled(True)

    def _adjust_column_widths(self):
        """Adatta le larghezze delle colonne al contenuto, mantenendo un minimo leggibile."""
        header = self.table.horizontalHeader()

        # Ridimensiona colonne specifiche al contenuto
        columns_to_resize = [1, 2, 3, 10, 11, 12, 13]  # Escludi quelle con stretch
        for col in columns_to_resize:
            if not self.table.isColumnHidden(col):
                self.table.resizeColumnToContents(col)
                # Aggiungi buffer per leggibilità (10% + 15px)
                current_width = self.table.columnWidth(col)
                self.table.setColumnWidth(col, int(current_width * 1.1) + 15)

        # Imposta Stretch per colonne con testo lungo (dopo aver ridimensionato le altre)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)  # DESCRIZIONE ATTIVITA'
        header.setSectionResizeMode(11, QHeaderView.ResizeMode.Stretch)  # STATO ATTIVITA'
        header.setSectionResizeMode(15, QHeaderView.ResizeMode.Stretch)  # AVVISO

    def _populate_table_row(self, row_idx: int, row_data: tuple, db_keys: list):
        styles_idx = len(self.COLUMNS)
        row_styles = (
            json.loads(row_data[styles_idx]) if len(row_data) > styles_idx and row_data[styles_idx] else {}
        )

        for col_idx in range(len(self.COLUMNS)):
            val = row_data[col_idx]
            text = self._format_cell_text(col_idx, val)
            item = SortableTableWidgetItem(text)
            if col_idx < len(db_keys):
                self._apply_item_style(item, row_styles.get(db_keys[col_idx]))
            self.table.setItem(row_idx, col_idx, item)

    def _format_cell_text(self, col_idx: int, val: Any) -> str:
        s = str(val).strip() if val is not None else ""
        if s.lower() == "nan":
            return ""
        if col_idx == 12 and s:
            try:
                return datetime.strptime(s.split(" ")[0], "%Y-%m-%d").strftime("%d/%m/%Y")
            except Exception:
                pass
        return s

    def _apply_item_style(self, item: QTableWidgetItem, style: Optional[dict]):
        if not style:
            return
        if "fg" in style:
            item.setForeground(QColor(style["fg"]))
        if "bg" in style:
            item.setBackground(QColor(style["bg"]))

    def _populate_filters(self):
        areas, stati = set(), set()
        for r in range(self.table.rowCount()):
            if it := self.table.item(r, 1):
                areas.add(it.text())
            if it := self.table.item(r, 10):
                stati.add(it.text())

        for combo, values, all_text in [
            (self.combo_area, areas, "Tutte"),
            (self.combo_stato, stati, "Tutti"),
        ]:
            curr = combo.currentText()
            combo.blockSignals(True)
            combo.clear()
            combo.addItem(all_text)
            combo.addItems(sorted(values))
            if curr in values:
                combo.setCurrentText(curr)
            combo.blockSignals(False)

    def apply_filters(self):
        f_ps, f_po = self.chk_ps.isChecked(), self.chk_po.isChecked()
        f_area, f_stato = self.combo_area.currentText(), self.combo_stato.currentText()
        for r in range(self.table.rowCount()):
            self.table.setRowHidden(r, self._should_hide_row(r, f_ps, f_po, f_area, f_stato))

    def _should_hide_row(self, row: int, f_ps: bool, f_po: bool, f_area: str, f_stato: str) -> bool:
        """Determina se una riga deve essere nascosta in base ai filtri attivi."""
        if self._is_ps_missing(row, f_ps):
            return True
        if self._is_po_missing(row, f_po):
            return True
        if self._is_area_mismatch(row, f_area):
            return True
        if self._is_stato_mismatch(row, f_stato):
            return True
        return False

    def _is_ps_missing(self, row: int, active: bool) -> bool:
        if not active:
            return False
        it = self.table.item(row, 0)
        return not it or not it.text().strip()

    def _is_po_missing(self, row: int, active: bool) -> bool:
        if not active:
            return False
        it = self.table.item(row, 14)
        return not it or not it.text().strip()

    def _is_area_mismatch(self, row: int, area: str) -> bool:
        if area == "Tutte":
            return False
        it = self.table.item(row, 1)
        return not it or it.text() != area

    def _is_stato_mismatch(self, row: int, stato: str) -> bool:
        if stato == "Tutti":
            return False
        it = self.table.item(row, 10)
        return not it or it.text() != stato

    def _reset_filters(self):
        self.chk_ps.setChecked(False)
        self.chk_po.setChecked(False)
        self.combo_area.setCurrentIndex(0)
        self.combo_stato.setCurrentIndex(0)
        self.apply_filters()

    def filter_data(self, text):
        search_terms = text.lower().split()
        cols = self.table.columnCount()
        self.apply_filters()
        for r in range(self.table.rowCount()):
            if self.table.isRowHidden(r):
                continue
            if text:
                row_text = " ".join(
                    [self.table.item(r, c).text().lower() for c in range(cols) if self.table.item(r, c)]
                )
                if not all(term in row_text for term in search_terms):
                    self.table.setRowHidden(r, True)

    def _show_context_menu(self, pos):
        menu = QMenu(self)
        lyra_action = QAction("Analizza riga con Lyra", self)
        lyra_action.setIcon(get_colored_icon(get_asset_path(Icons.SPARKLES), "#000000"))
        lyra_action.triggered.connect(lambda: self.table._analyze_row_at(pos))
        menu.addAction(lyra_action)
        menu.exec(self.table.viewport().mapToGlobal(pos))
