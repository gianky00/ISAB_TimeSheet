"""
SyncroJob - PDL Database Panel (Refactored)
Pannello coordinato per la gestione del Database PDL SafeWork.
Utilizza PDLController per la logica di business e PDLTableView per la griglia.
"""

import logging
import os
from datetime import datetime
from typing import Any

from PyQt6.QtCore import QPoint, Qt, QTimer
from PyQt6.QtWidgets import (
    QFileDialog,
    QMenu,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.core.database import pdl_queries
from src.core.pdl.pdl_controller import PDLController
from src.core.sync_tracker import SyncTracker
from src.gui.components.animated_tab_widget import AnimatedTabWidget
from src.gui.formatters import FastTableModel
from src.gui.panels.base import BotWorker  # noqa: TC001
from src.gui.widgets import EmptyStateWidget
from src.gui.workers.data_loader_worker import DataLoaderWorker

from .pdl_detail_view import PDLDetailView
from .pdl_filter_widget import PDLFilterWidget
from .programmazione_tab import ProgrammazioneTab
from .widgets.pdl_table import PDLTableView

logger = logging.getLogger(__name__)


class PDLDBPanel(QWidget):
    """Orchestratore del modulo PDL con architettura Master-Detail modularizzata."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Inizializza il pannello del database PDL.

        Args:
            parent: Widget genitore opzionale.
        """
        super().__init__(parent)
        self.controller = PDLController()
        self.worker: BotWorker | None = None
        self._raw_full_data: list[tuple[Any, ...]] = []

        self.master_headers = [
            "Data Creazione",
            "Richiedente",
            "N° PDL",
            "Area",
            "Unità",
            "Stato",
            "Descrizione",
        ]
        self.full_headers = [
            "ID",
            "N° PDL",
            "Data Creazione",
            "Area",
            "Unità",
            "Ditta",
            "Descrizione",
            "Tipologia",
            "Stato",
            "Apparecchiatura",
            "Richiedente",
            "Data Richiesta",
            "Emittente",
            "Data Emissione",
            "Aprente",
            "Data Apertura",
            "Priorità",
            "Contratto",
            "Ordine",
            "Sito",
            "Importato il",
        ]

        self.model = FastTableModel([], self.master_headers)
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.refresh_data)

        self.data_worker: DataLoaderWorker | None = None

        self._setup_ui()
        # Caricamento asincrono immediato: non blocca lo splash screen!
        QTimer.singleShot(10, self.refresh_data)
        QTimer.singleShot(100, self._populate_initial_filters)

    def _setup_ui(self) -> None:
        """Configura l'interfaccia grafica e i componenti principali."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.tabs = AnimatedTabWidget()

        # --- TAB 1: DATABASE ---
        self.db_tab = QWidget()
        db_lay = QVBoxLayout(self.db_tab)
        db_lay.setContentsMargins(10, 10, 10, 10)
        db_lay.setSpacing(5)

        self.filters = PDLFilterWidget()
        self.filters.filter_changed.connect(self.refresh_data)
        self.filters.site_changed.connect(self._on_site_changed)
        self.filters.area_changed.connect(self.refresh_data)
        self.filters.update_clicked.connect(self._on_update_bot_clicked)
        self.filters.reset_clicked.connect(self._reset_filters)
        self.filters.export_clicked.connect(self._export_to_excel)
        self.filters.search_input.textChanged.connect(lambda: self.search_timer.start(500))
        db_lay.addWidget(self.filters)

        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.table = PDLTableView(self.model)
        self.table.header_clicked.connect(self._on_header_clicked)
        self.table.row_double_clicked.connect(self._toggle_detail_view)
        self.table.selection_changed_custom.connect(self._on_selection_changed)
        self.table.context_menu_requested.connect(self._show_context_menu)
        self.splitter.addWidget(self.table)

        self.detail_view = PDLDetailView(self.full_headers)
        self.detail_view.setVisible(False)
        self.splitter.addWidget(self.detail_view)

        self.empty_state = EmptyStateWidget(
            title="Nessun PDL",
            message="Sincronizza il database per visualizzare i permessi.",
            icon_key=Icons.FILE_TEXT,
        )
        self.empty_state.setParent(self.table)
        self.empty_state.hide()

        self.splitter.setStretchFactor(0, 3)
        self.splitter.setStretchFactor(1, 1)
        db_lay.addWidget(self.splitter)

        # --- TAB 2: PROGRAMMAZIONE ---
        self.prog_tab = ProgrammazioneTab()
        self.tabs.addTab(self.db_tab, "Database PDL")
        self.tabs.addTab(self.prog_tab, "Programmazione")
        layout.addWidget(self.tabs)

    def _populate_initial_filters(self) -> None:
        """Popola i menu a tendina dei filtri con i dati unici presenti nel DB."""
        # Logica di popolamento spostata parzialmente nel controller in futuro
        try:
            from src.core.database import db_manager

            q = "SELECT DISTINCT SUBSTR(n_pdl, INSTR(n_pdl, '/') + 1) as grp FROM pdl WHERE n_pdl LIKE '%/%' ORDER BY grp"
            rows = db_manager.execute_query(db_manager.DB_PDL, q)
            self.filters.group_filter.blockSignals(True)
            self.filters.group_filter.clear()
            self.filters.group_filter.addItem("Tutti")
            for r in rows:
                if r[0]:
                    self.filters.group_filter.addItem(str(r[0]))
            self.filters.group_filter.blockSignals(False)
            self._update_areas()
        except Exception:
            logger.warning("Impossibile caricare i filtri PDL.")

    def refresh_data(self, sort_col: int | None = None) -> None:
        """
        Innesca il caricamento asincrono dei dati dal database.
        """
        if self.data_worker and self.data_worker.isRunning():
            self.data_worker.terminate()
            self.data_worker.wait()

        self.filters.lbl_sync_status.setText(f"Ultimo Sync: {SyncTracker.get_formatted_status('pdl')}")
        filters = self.filters.get_filters()
        sort_order = "DESC"

        # Crea il worker per caricare i dati in background
        self.data_worker = DataLoaderWorker(self.controller.get_pdl_data, filters, sort_col, sort_order)
        self.data_worker.finished.connect(self._on_data_loaded)
        self.data_worker.start()

    def _on_data_loaded(self, raw_data: Any) -> None:
        """Callback eseguita al termine del caricamento asincrono."""
        self._raw_full_data = raw_data or []

        self.empty_state.setVisible(not self._raw_full_data)
        if self._raw_full_data:
            self.empty_state.hide()

        master_rows = self.controller.process_master_rows(self._raw_full_data)
        self.model.update_data(master_rows)
        self.table.optimize_columns(len(self.master_headers))

    def set_filters(
        self, site: str | None = None, area: str | None = None, search: str | None = None
    ) -> None:
        """
        Imposta i filtri del pannello programmaticamente.

        Args:
            site: Nome del sito da selezionare.
            area: Nome dell'area da selezionare.
            search: Testo di ricerca.
        """
        if site:
            self.filters.site_filter.setCurrentText(site)
            self._update_areas()

        if area:
            self.filters.area_filter.setCurrentText(area)

        if search is not None:
            self.filters.search_input.setText(search)

        self.refresh_data()

    def _on_site_changed(self) -> None:
        """Gestisce il cambio del filtro Sito e aggiorna le Aree disponibili."""
        self._update_areas()
        self.refresh_data()

    def _update_areas(self) -> None:
        """Aggiorna dinamicamente il filtro Area basandosi sul Sito selezionato."""
        # Delega query leggera a helper futuro
        site = self.filters.site_filter.currentText()
        q = "SELECT DISTINCT area FROM pdl WHERE 1=1"
        p = []
        if site != "Tutti i siti":
            q += " AND sito = ?"
            p.append(site)
        q += " ORDER BY area"
        from src.core.database import db_manager

        rows = db_manager.execute_query(db_manager.DB_PDL, q, tuple(p))
        self.filters.area_filter.blockSignals(True)
        self.filters.area_filter.clear()
        self.filters.area_filter.addItem("Tutte")
        for r in rows:
            if r[0]:
                self.filters.area_filter.addItem(str(r[0]))
        self.filters.area_filter.blockSignals(False)

    def _on_selection_changed(self) -> None:
        """Aggiorna la vista di dettaglio quando viene selezionata una riga."""
        sel_model = self.table.selectionModel()
        if not sel_model:
            return
        idx = sel_model.selectedRows()
        if not idx:
            self.detail_view.clear()
            return

        row_idx = idx[0].row()
        if row_idx < len(self._raw_full_data):
            full_data = self._raw_full_data[row_idx]
            try:
                interventions = pdl_queries.PDLQueries.get_pdl_interventions(str(full_data[1]))
            except Exception:
                interventions = []
            self.detail_view.update_details(full_data, interventions)

    def _toggle_detail_view(self) -> None:
        """Mostra o nasconde il pannello laterale di dettaglio."""
        self.detail_view.setVisible(not self.detail_view.isVisible())
        if self.detail_view.isVisible():
            self.splitter.setSizes([int(self.width() * 0.7), int(self.width() * 0.3)])

    def _show_context_menu(self, pos: QPoint) -> None:
        """Mostra il menu contestuale nella posizione specificata."""
        menu = QMenu(self)
        menu.addAction("Mostra/Nascondi dettaglio", self._toggle_detail_view)

        sel_model = self.table.selectionModel()
        if sel_model and sel_model.hasSelection():
            menu.addSeparator()
            menu.addAction("Stampa PDL Selezionati", self._on_print_selected)

        vp = self.table.viewport()
        if vp:
            menu.exec(vp.mapToGlobal(pos))

    def _on_print_selected(self) -> None:
        """Estrae i numeri PDL dalle righe selezionate e invia il comando di stampa alla MainWindow."""
        sel_model = self.table.selectionModel()
        if not sel_model:
            return

        indexes = sel_model.selectedRows()
        if not indexes:
            return

        pdl_numbers = []
        for idx in indexes:
            row = idx.row()
            if row < len(self._raw_full_data):
                # La colonna 1 è "N° PDL" nei full_headers
                pdl_numbers.append(str(self._raw_full_data[row][1]))

        if pdl_numbers:
            main_win = self.window()
            if main_win and hasattr(main_win, "trigger_pdl_print"):
                main_win.trigger_pdl_print(pdl_numbers)

    def _on_header_clicked(self, idx: int) -> None:
        """Esegue l'ordinamento dei dati al clic sull'header della colonna."""
        self.refresh_data(sort_col=idx)

    def _reset_filters(self) -> None:
        """Ripristina tutti i filtri allo stato predefinito."""
        self.filters.search_input.clear()
        self.filters.group_filter.setCurrentIndex(0)
        self.filters.site_filter.setCurrentIndex(0)
        self.refresh_data()

    def _on_update_bot_clicked(self) -> None:
        """Avvia il bot di aggiornamento per i PDL (implementazione delegata)."""
        # Logica bot delegata a BotController futuro, per ora rimane qui ma ripulita

    def _export_to_excel(self) -> None:
        """Esporta l'intero set di dati filtrato in formato Excel."""
        import pandas as pd
        if not self._raw_full_data:
            return
        df = pd.DataFrame(self._raw_full_data, columns=self.full_headers)
        f, _ = QFileDialog.getSaveFileName(
            self, "Esporta PDL", f"Export_PDL_{datetime.now().strftime('%Y%m%d')}.xlsx", "Excel (*.xlsx)"
        )
        if f:
            df.to_excel(f, index=False)
            os.startfile(f)  # noqa: S606
