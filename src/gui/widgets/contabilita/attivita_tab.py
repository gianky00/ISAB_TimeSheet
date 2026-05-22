"""SyncroJob - Contabilità AttivitàProgrammate.

Tab specializzato per la visualizzazione delle attivitàprogrammate settimanali.
Include filtri avanzati per PS, PO, Area e Stato PdL.
"""

from __future__ import annotations

import json
from contextlib import suppress
from datetime import UTC, datetime
from typing import Any, ClassVar

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.core.excel_importer import ExcelImporter
from src.gui.widgets import ExcelTableWidget
from src.gui.widgets.core_widgets import (
    FilterComboBox,
    PrimaryButton,
    SortableTableWidgetItem,
    StandardCheckBox,
)
from src.gui.workers.contabilita_data_worker import ContabilitaDataWorker


class AttivitaProgrammateTab(QWidget):
    """Tab per la visualizzazione e il filtraggio delle AttivitàProgrammate.

    Utilizza una tabella ad alte prestazioni per mostrare lo stato delle PdL e la pianificazione settimanale.

    Inizializza il tab delle attivitàprogrammate.

    Args:
      parent: Widget genitore.

    Attributes:
        COLUMNS: ClassVar[list[str: Segnale o attributo della classe.
    """

    COLUMNS: ClassVar[list[str]] = [
        "PS",
        "AREA",
        "PdL",
        "IMP.",
        "DESCRIZIONE\nATTIVITÀ",
        "LUN",
        "MAR",
        "MER",
        "GIO",
        "VEN",
        "STATO\nPdL",
        "STATO\nATTIVITÀ",
        "DATA\nCONTROLLO",
        "PERSONALE\nIMPIEGATO",
        "PO",
        "AVVISO",
    ]

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.chk_ps: QCheckBox
        self.chk_po: QCheckBox
        self.combo_area: QComboBox
        self.combo_stato: QComboBox
        self.btn_reset: QPushButton
        self.table: ExcelTableWidget
        self.worker: ContabilitaDataWorker | None = None

        self._setup_ui()
        self._load_data()

    def _setup_ui(self) -> None:
        """Configura l'interfaccia utente del tab, inclusi i filtri e la tabella."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 0)

        self._setup_filters(layout)
        self._setup_table(layout)

    def _setup_filters(self, layout: QVBoxLayout) -> None:
        """Configura la sezione dei filtri."""
        filter_layout = QHBoxLayout()
        filter_layout.setContentsMargins(5, 0, 5, 5)

        self.chk_ps = StandardCheckBox("Filtra PS")
        self.chk_ps.stateChanged.connect(lambda _: self.apply_filters())
        filter_layout.addWidget(self.chk_ps)

        self.chk_po = StandardCheckBox("Filtra PO")
        self.chk_po.stateChanged.connect(lambda _: self.apply_filters())
        filter_layout.addWidget(self.chk_po)

        filter_layout.addSpacing(20)
        filter_layout.addWidget(QLabel("Area:"))
        self.combo_area = FilterComboBox()
        self.combo_area.setMinimumWidth(150)
        self.combo_area.addItem("Tutte")
        self.combo_area.currentTextChanged.connect(lambda _: self.apply_filters())
        filter_layout.addWidget(self.combo_area)

        filter_layout.addSpacing(15)
        filter_layout.addWidget(QLabel("Stato PdL:"))
        self.combo_stato = FilterComboBox()
        self.combo_stato.setMinimumWidth(150)
        self.combo_stato.addItem("Tutti")
        self.combo_stato.currentTextChanged.connect(lambda _: self.apply_filters())
        filter_layout.addWidget(self.combo_stato)

        self.btn_reset = PrimaryButton("Reset Filtri")
        self.btn_reset.clicked.connect(self._reset_filters)
        filter_layout.addWidget(self.btn_reset)
        filter_layout.addStretch()
        layout.addLayout(filter_layout)

    def _setup_table(self, layout: QVBoxLayout) -> None:
        """Configura la tabella dei dati."""
        self.table = ExcelTableWidget()
        self.table.setColumnCount(len(self.COLUMNS))
        self.table.setHorizontalHeaderLabels(self.COLUMNS)
        self.table.setWordWrap(True)
        self.table.setTextElideMode(Qt.TextElideMode.ElideNone)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.table.cellDoubleClicked.connect(lambda r, c: self.table.selectRow(r))

        self.table.auto_copy_headers = True
        header = self.table.horizontalHeader()
        if header is None:
            raise RuntimeError("Table horizontal header is None")
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table.setColumnHidden(0, True)
        self.table.setColumnHidden(14, True)

        self._set_column_widths()

        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        v_header = self.table.verticalHeader()
        if v_header is None:
            raise RuntimeError("Table vertical header is None")
        v_header.setVisible(False)
        layout.addWidget(self.table)

    def _set_column_widths(self) -> None:
        """Imposta le larghezze iniziali delle colonne."""
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

    def refresh_data(self) -> None:
        """Ricarica i dati dal database e aggiorna la tabella."""
        self._load_data()

    def _load_data(self) -> None:
        """Esegue il caricamento effettivo dei dati nel modello della tabella (Asincrono)."""
        if self.worker and self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait()

        self.table.setSortingEnabled(False)
        self.table.clearContents()
        self.table.setRowCount(0)
        self.table.setPlaceholderText("Caricamento attività in corso...")

        self.worker = ContabilitaDataWorker("get_attivita_programmate_data")
        self.worker.finished_signal.connect(self._on_data_ready)
        self.worker.error_signal.connect(lambda msg: print(f"Errore Attività: {msg}"))
        self.worker.start()

    def _on_data_ready(self, data: list[tuple[Any, ...]]) -> None:
        """Popola la tabella al termine del caricamento asincrono."""
        self.table.blockSignals(True)
        try:
            self.table.setRowCount(len(data))
            db_keys = list(ExcelImporter.ATTIVITA_PROGRAMMATE_MAPPING.values())
            for row_idx, row_data in enumerate(data):
                self._populate_table_row(row_idx, row_data, db_keys)

            self.table.smart_resize()
            self._populate_filters()
            self._adjust_column_widths()

            self.apply_filters()
            self.table.setPlaceholderText("Nessuna attività programmata trovata.")
        finally:
            self.table.blockSignals(False)
            self.table.setSortingEnabled(True)

    def _adjust_column_widths(self) -> None:
        """Adatta le larghezze delle colonne al contenuto, mantenendo un minimo leggibile."""
        header = self.table.horizontalHeader()
        if header is None:
            raise RuntimeError("Table horizontal header is None - cannot adjust column widths")

        columns_to_resize = [1, 2, 3, 10, 11, 12, 13]
        for col in columns_to_resize:
            if not self.table.isColumnHidden(col):
                self.table.resizeColumnToContents(col)
                current_width = self.table.columnWidth(col)
                self.table.setColumnWidth(col, int(current_width * 1.1) + 15)

        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(11, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(15, QHeaderView.ResizeMode.Stretch)

    def _populate_table_row(self, row_idx: int, row_data: tuple[Any, ...], db_keys: list[str]) -> None:
        """Popola una riga della tabella con i dati e applica gli stili salvati."""
        styles_idx = len(self.COLUMNS)
        row_styles: dict[str, Any] = (
            json.loads(row_data[styles_idx]) if len(row_data) > styles_idx and row_data[styles_idx] else {}
        )

        for col_idx in range(len(self.COLUMNS)):
            val = row_data[col_idx]
            text = self._format_cell_text(col_idx, val)
            item = SortableTableWidgetItem(text)
            if col_idx < len(db_keys):
                self._apply_item_style(item, row_styles.get(db_keys[col_idx]))
            self.table.setItem(row_idx, col_idx, item)

    def _format_cell_text(self, col_idx: int, val: object) -> str:
        """Formatta il testo della cella in base al tipo di dato (es. date)."""
        s = str(val).strip() if val is not None else ""
        if s.lower() == "nan":
            return ""
        if col_idx == 12 and s:
            with suppress(Exception):
                return datetime.strptime(s.split(" ")[0], "%Y-%m-%d").replace(tzinfo=UTC).strftime("%d/%m/%Y")
        return s

    def _apply_item_style(self, item: QTableWidgetItem, style: dict[str, Any] | None) -> None:
        """Applica colori di testo e sfondo all'item in base ai metadati di stile."""
        if not style:
            return
        if "fg" in style:
            item.setForeground(QColor(style["fg"]))
        if "bg" in style:
            item.setBackground(QColor(style["bg"]))

    def _populate_filters(self) -> None:
        """Aggiorna le opzioni dei menu a tendina dei filtri in base ai dati presenti in tabella."""
        areas, stati = set(), set()
        for r in range(self.table.rowCount()):
            if it := self.table.item(r, 1):
                areas.add(it.text())
            if it := self.table.item(r, 10):
                stati.add(it.text())

        for combo, values, all_text in (
            (self.combo_area, areas, "Tutte"),
            (self.combo_stato, stati, "Tutti"),
        ):
            curr: str = combo.current_text() if hasattr(combo, "current_text") else combo.currentText()
            combo.blockSignals(True)
            combo.clear()
            combo.addItem(all_text)
            combo.addItems(sorted(values))
            if curr in values:
                combo.setCurrentText(curr)
            combo.blockSignals(False)

    def apply_filters(self, *args: object) -> None:
        """Applica i filtri correnti (Checkbox e ComboBox) nascondendo le righe non corrispondenti."""
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
        return self._is_stato_mismatch(row, f_stato)

    def _is_ps_missing(self, row: int, active: bool) -> bool:
        """Controlla se manca il flag PS."""
        if not active:
            return False
        it = self.table.item(row, 0)
        return not it or not it.text().strip()

    def _is_po_missing(self, row: int, active: bool) -> bool:
        """Controlla se manca il flag PO."""
        if not active:
            return False
        it = self.table.item(row, 14)
        return not it or not it.text().strip()

    def _is_area_mismatch(self, row: int, area: str) -> bool:
        """Verifica se l'area della riga non corrisponde al filtro."""
        if area == "Tutte":
            return False
        it = self.table.item(row, 1)
        return not it or it.text() != area

    def _is_stato_mismatch(self, row: int, stato: str) -> bool:
        """Verifica se lo stato della riga non corrisponde al filtro."""
        if stato == "Tutti":
            return False
        it = self.table.item(row, 10)
        return not it or it.text() != stato

    def _reset_filters(self) -> None:
        """Ripristina i filtri ai valori predefiniti."""
        self.chk_ps.setChecked(False)
        self.chk_po.setChecked(False)
        self.combo_area.setCurrentIndex(0)
        self.combo_stato.setCurrentIndex(0)
        self.apply_filters()

    def filter_data(self, text: str) -> None:
        """Esegue una ricerca testuale globale su tutte le righe non già nascoste dai filtri.

        Args:
          text: Testo di ricerca.
        """
        search_terms = text.lower().split()
        cols = self.table.columnCount()
        self.apply_filters()
        for r in range(self.table.rowCount()):
            if self.table.isRowHidden(r):
                continue
            if text:
                row_text = " ".join(
                    [cell.text().lower() for c in range(cols) if (cell := self.table.item(r, c)) is not None]
                )
                if not all(term in row_text for term in search_terms):
                    self.table.setRowHidden(r, True)
