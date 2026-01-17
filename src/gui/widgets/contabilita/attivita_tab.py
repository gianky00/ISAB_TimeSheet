import json
from datetime import datetime

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

from src.core.contabilita_manager import ContabilitaManager
from src.core.excel_importer import ExcelImporter
from src.gui.widgets import ExcelTableWidget


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
        """Configura l'interfaccia utente del tab, inclusi filtri e tabella."""
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
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self.table.cellDoubleClicked.connect(lambda r, c: self.table.selectRow(r))
        self.table.setStyleSheet(
            """
            QTableWidget {
                background-color: white;
                color: black;
                gridline-color: #e9ecef;
                font-size: 13px;
                border: 1px solid #dee2e6;
                selection-background-color: #0d6efd;
                selection-color: white;
            }
            QTableWidget::item:selected {
                background-color: #0d6efd;
                color: white;
            }
            QHeaderView::section { background-color: #E1F5FE; color: #333333; padding: 10px 5px; border: none; border-right: 1px solid #B3E5FC; border-bottom: 3px solid #81D4FA; font-weight: bold; text-transform: uppercase; font-size: 11px; }
        """
        )
        self.table.auto_copy_headers = True
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table.setColumnHidden(0, True)
        self.table.setColumnHidden(14, True)
        self.table.setColumnWidth(1, 80)
        self.table.setColumnWidth(2, 80)
        self.table.setColumnWidth(3, 60)
        self.table.setColumnWidth(4, 350)
        for i in range(5, 10):
            self.table.setColumnWidth(i, 50)
        self.table.setColumnWidth(10, 120)
        self.table.setColumnWidth(11, 120)
        self.table.setColumnWidth(12, 100)
        self.table.setColumnWidth(13, 150)
        self.table.setColumnWidth(15, 250)
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)

    def refresh_data(self):
        """Ricarica i dati dal database e aggiorna l'interfaccia."""
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
                row_styles = (
                    json.loads(row_data[len(self.COLUMNS)])
                    if len(row_data) > len(self.COLUMNS) and row_data[len(self.COLUMNS)]
                    else {}
                )
                for col_idx in range(len(self.COLUMNS)):
                    val = row_data[col_idx]
                    s = str(val).strip() if val is not None else ""
                    if s.lower() == "nan":
                        s = ""
                    if col_idx == 12 and s:
                        try:
                            s = datetime.strptime(s.split(" ")[0], "%Y-%m-%d").strftime("%d/%m/%Y")
                        except Exception:
                            pass
                    item = QTableWidgetItem(s)
                    if col_idx < len(db_keys):
                        key = db_keys[col_idx]
                        if key in row_styles:
                            style = row_styles[key]
                            if "fg" in style:
                                item.setForeground(QColor(style["fg"]))
                            if "bg" in style:
                                item.setBackground(QColor(style["bg"]))
                    self.table.setItem(row_idx, col_idx, item)
            self.table.resizeRowsToContents()
            self._populate_filters()
        finally:
            self.table.blockSignals(False)
            self.table.setSortingEnabled(True)

    def _populate_filters(self):
        areas, stati = set(), set()
        for r in range(self.table.rowCount()):
            if self.table.item(r, 1):
                areas.add(self.table.item(r, 1).text())
            if self.table.item(r, 10):
                stati.add(self.table.item(r, 10).text())
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
        """Applica la logica di filtraggio combinata alla tabella delle attività."""
        f_ps, f_po = self.chk_ps.isChecked(), self.chk_po.isChecked()
        f_area, f_stato = self.combo_area.currentText(), self.combo_stato.currentText()
        for r in range(self.table.rowCount()):
            hide = False
            if f_ps and (not self.table.item(r, 0) or not self.table.item(r, 0).text().strip()):
                hide = True
            if (
                not hide
                and f_po
                and (not self.table.item(r, 14) or not self.table.item(r, 14).text().strip())
            ):
                hide = True
            if (
                not hide
                and f_area != "Tutte"
                and (not self.table.item(r, 1) or self.table.item(r, 1).text() != f_area)
            ):
                hide = True
            if (
                not hide
                and f_stato != "Tutti"
                and (not self.table.item(r, 10) or self.table.item(r, 10).text() != f_stato)
            ):
                hide = True
            self.table.setRowHidden(r, hide)

    def _reset_filters(self):
        self.chk_ps.setChecked(False)
        self.chk_po.setChecked(False)
        self.combo_area.setCurrentIndex(0)
        self.combo_stato.setCurrentIndex(0)
        self.apply_filters()

    def filter_data(self, text):
        """Esegue una ricerca testuale globale su tutte le colonne visibili."""
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
        lyra_action = QAction("✨ Analizza Riga con Lyra", self)
        lyra_action.triggered.connect(lambda: self.table._analyze_row_at(pos))
        menu.addAction(lyra_action)
        menu.exec(self.table.viewport().mapToGlobal(pos))
