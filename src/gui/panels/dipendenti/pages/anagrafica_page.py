# mypy: disable-error-code="no-untyped-def, no-untyped-call, arg-type, attr-defined, misc, no-redef"
"""
SyncroJob - Anagrafica Page (Refactored)
Pagina coordinata per la gestione anagrafica dipendenti.
"""

import logging
from typing import TYPE_CHECKING, Any

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)

from src.core.dipendenti.anagrafica_controller import AnagraficaController
from src.core.dipendenti.data_helpers import format_db_date
from src.core.sync_tracker import SyncTracker
from src.gui.formatters import FastTableModel
from src.gui.panels.dipendenti.utils.report_generator import ReportGenerator
from src.gui.widgets.toast import ToastManager

from ..widgets.anagrafica_header import AnagraficaHeaderWidget
from ..widgets.employee_detail_view import EmployeeDetailView
from ..widgets.employee_table import EmployeeTableView

if TYPE_CHECKING:
    from src.gui.controllers.bot_worker import BotWorker

logger = logging.getLogger(__name__)


class AnagraficaPage(QWidget):
    """Pagina per la visualizzazione e gestione anagrafica dipendenti - Versione Modularizzata."""

    def __init__(self, controller: AnagraficaController, parent: QWidget | None = None) -> None:
        """
        Inizializza la pagina anagrafica con iniezione del controller.

        Args:
          controller: Istanza del controller per la logica di business.
          parent: Widget genitore opzionale.
        """
        super().__init__(parent)
        self.controller = controller
        self.worker: BotWorker | None = None
        self.current_filter = None

        self.headers = [
            "SCAD.\nISAB",
            "ID\nRISORSA",
            "Cognome",
            "Nome",
            "CODICE FISCALE",
            "ID\nBADGE",
            "DATA\nASSUNZIONE",
        ]
        self.model = FastTableModel([], self.headers)

        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.refresh_data)

        self._setup_ui()
        QTimer.singleShot(50, self.refresh_data)

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        # 1. Header (Ricerca, Azioni, Card)
        self.header = AnagraficaHeaderWidget()
        self.header.search_changed.connect(lambda _: self.search_timer.start(500))
        self.header.import_requested.connect(self._on_import_clicked)
        self.header.report_requested.connect(self._generate_email_report)
        self.header.update_requested.connect(self._on_update_bot_clicked)
        self.header.filter_changed.connect(self._on_card_filter)
        layout.addWidget(self.header)

        # 2. Area Contenuti
        content_layout = QHBoxLayout()
        content_layout.setSpacing(10)

        self.table = EmployeeTableView(self.model)
        self.table.configure_columns([80, 100, 200, 150, 180, 100, 145])
        self.table.employee_selected.connect(self._on_selection_changed)
        self.table.monitoring_toggled.connect(self._on_monitoring_toggled)
        content_layout.addWidget(self.table)

        self.detail_view = EmployeeDetailView()
        content_layout.addWidget(self.detail_view)
        content_layout.addStretch()

        layout.addLayout(content_layout)

    def refresh_data(self) -> None:
        """Sincronizza i dati tra DB, Controller e UI."""
        self.header.set_sync_status(f"Ultimo Sync: {SyncTracker.get_formatted_status('timbrature')}")

        # 1. Caricamento dati grezzi
        full_rows = AnagraficaController.get_employees(self.header.search_input.text())

        # 2. Processing (Calcolo scadenze e filtri)
        dtos, counts = AnagraficaController.process_rows(full_rows, self.current_filter)

        # 3. Map DTOs to UI structure
        master_rows = [d.to_table_row() for d in dtos]
        metadata = [d.get_metadata() for d in dtos]

        # 4. Aggiornamento UI
        self.model.update_data(master_rows, metadata)
        self.model.set_column_formatter(0, self._inactivation_formatter)
        self.header.update_counts(counts)
        self.header.update_card_styles(self.current_filter)

    def _inactivation_formatter(self, value: Any) -> str:
        if value is None or value == "":
            return ""
        try:
            days = max(0, int(value))
            return f"\u25cf {days}"
        except Exception:
            return str(value)

    def _on_card_filter(self, filter_type: str | None) -> None:
        if self.current_filter == filter_type:
            self.current_filter = None
        else:
            self.current_filter = filter_type
        self.refresh_data()

    def _on_monitoring_toggled(self, id_risorsa: str, enable: bool) -> None:
        if AnagraficaController.toggle_monitoring(id_risorsa, enable):
            status = "riattivato" if enable else "escluso"
            ToastManager.instance().show(f"Monitoraggio {status}", "success")
            self.refresh_data()

    def _on_selection_changed(self, row_idx: int) -> None:
        row_data = self.model._data[row_idx]

        # Indici di colonna nel database/modello dati esteso
        COL_ID_RISORSA = 1
        COL_NOME = 3
        COL_COD_FISCALE = 4
        COL_BADGE = 5
        COL_DATA_ASSUNZIONE = 6
        COL_DATA_NASCITA = 7
        COL_DATA_IMPORT = 8
        COL_COGNOME = 9

        mapping = {
            "ID Risorsa": COL_ID_RISORSA,
            "Cognome": COL_COGNOME,
            "Nome": COL_NOME,
            "Data Nascita": COL_DATA_NASCITA,
            "Codice Fiscale": COL_COD_FISCALE,
            "Badge": COL_BADGE,
            "Data Assunzione": COL_DATA_ASSUNZIONE,
            "Importato il": COL_DATA_IMPORT,
        }

        details = {}
        for h, idx in mapping.items():
            val = str(row_data[idx]) if row_data[idx] is not None else ""
            if val.lower() in ("nan", "none"):
                val = ""
            if h == "Importato il":
                val = format_db_date(val)
            details[h] = val

        access_info = AnagraficaController.get_last_isab_access(
            str(row_data[COL_COGNOME]), str(row_data[COL_NOME])
        )
        self.detail_view.update_data(details, access_info)

    def _on_import_clicked(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleziona Anagrafica", "", "CSV Files (*.csv);;All Files (*)"
        )
        if not file_path:
            return
        # ... logica importazione delegata al controller ...

    def _generate_email_report(self) -> None:
        """Richiama la generazione del report email."""
        ReportGenerator.generate_email_report(self)

    def _on_update_bot_clicked(self) -> None:
        # ... logica bot delegata a BotController ...
        pass
