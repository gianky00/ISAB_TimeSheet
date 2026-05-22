"""
SyncroJob - PDL Database Panel (Refactored)
Pannello coordinato per la gestione del Database PDL SafeWork.
Utilizza PDLController per la logica di business e PDLTableView per la griglia.
"""

import logging
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from PySide6.QtCore import QPoint, Qt, QTimer
from PySide6.QtWidgets import (
    QFileDialog,
    QMenu,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.core.pdl.pdl_controller import PDLController
from src.core.pdl.pdl_dto import PdlRowDTO
from src.core.pdl.pdl_service import PDLService
from src.core.sync_tracker import SyncTracker
from src.gui.components.animated_tab_widget import AnimatedTabWidget
from src.gui.formatters import FastTableModel
from src.gui.widgets import EmptyStateWidget
from src.gui.workers.pdl_data_worker import PDLDataWorker
from src.gui.workers.pdl_io_worker import PdlIOWorker
from src.utils.helpers import safe_open

from .pdl_detail_view import PDLDetailView
from .pdl_filter_widget import PDLFilterWidget
from .programmazione_tab import ProgrammazioneTab
from .widgets.pdl_table import PDLTableView

if TYPE_CHECKING:
    from src.gui.controllers.bot_worker import BotWorker


logger = logging.getLogger(__name__)


class PDLDBPanel(QWidget):
    """Orchestratore del modulo PDL con architettura Master-Detail modularizzata."""

    def __init__(self, controller: PDLController, parent: QWidget | None = None) -> None:
        """
        Inizializza il pannello del database PDL con iniezione del controller.

        Args:
          controller: Istanza del controller per la logica di business.
          parent: Widget genitore opzionale.
        """
        super().__init__(parent)
        self.controller = controller
        self.worker: BotWorker | None = None
        self._raw_full_data: list[PdlRowDTO] = []

        self.master_headers = [
            "Data Creazione",
            "Richiedente",
            "N  PDL",
            "Area",
            "Unità",
            "Stato",
            "Descrizione",
        ]
        self.full_headers = [
            "ID",
            "N  PDL",
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

        self._setup_ui()
        QTimer.singleShot(50, self.refresh_data)
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
        self.filters.area_changed.connect(self._on_area_changed)
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
        """Popola i menu a tendina dei filtri in background (Asincrono)."""
        self.filter_worker = PDLDataWorker("initial_filters")
        self.filter_worker.filters_ready.connect(self._on_filters_ready)
        self.filter_worker.start()

    def _on_filters_ready(self, filter_type: str, results: list[str]) -> None:
        """Callback per il popolamento dei filtri a query completata."""
        if filter_type == "groups":
            self.filters.group_filter.blockSignals(True)
            self.filters.group_filter.clear()
            self.filters.group_filter.addItem("Tutti")
            self.filters.group_filter.addItems(results)
            self.filters.group_filter.blockSignals(False)
            self._update_areas()
        elif filter_type == "areas":
            self.filters.area_filter.blockSignals(True)
            self.filters.area_filter.clear()
            self.filters.area_filter.addItem("Tutte")
            self.filters.area_filter.addItems(results)
            self.filters.area_filter.blockSignals(False)
            self._update_units()
        elif filter_type == "units":
            self.filters.unit_filter.blockSignals(True)
            self.filters.unit_filter.clear()
            self.filters.unit_filter.addItem("Tutte")
            self.filters.unit_filter.addItems(results)
            self.filters.unit_filter.blockSignals(False)

    def refresh_data(self, sort_col: int | None = None) -> None:
        """Ricarica i dati dal database applicando i filtri (Asincrono)."""
        self.filters.lbl_sync_status.setText(f"Ultimo Sync: {SyncTracker.get_formatted_status('pdl')}")
        filters = self.filters.get_filters()

        if hasattr(self, "data_worker") and self.data_worker.isRunning():
            self.data_worker.terminate()
            self.data_worker.wait()

        self.data_worker = PDLDataWorker(
            "fetch_data", controller=self.controller, filters=filters, sort_col=sort_col, sort_order="DESC"
        )
        self.data_worker.data_ready.connect(self._on_pdl_data_ready)
        self.data_worker.start()

    def _on_pdl_data_ready(self, data: list[PdlRowDTO]) -> None:
        """Aggiorna il modello della tabella con i dati caricati in background."""
        self._raw_full_data = data
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
            # _on_site_changed verrà triggherato se connesso, altrimenti chiamiamo noi
            self._on_site_changed()

        if area:
            self.filters.area_filter.setCurrentText(area)
            self._on_area_changed()

        if search is not None:
            self.filters.search_input.setText(search)

        self.refresh_data()

    def _on_site_changed(self) -> None:
        """Gestisce il cambio del filtro Sito e aggiorna le Aree disponibili (Asincrono)."""
        self._update_areas()
        self.refresh_data()

    def _on_area_changed(self) -> None:
        """Gestisce il cambio del filtro Area e aggiorna le Unità disponibili (Asincrono)."""
        self._update_units()
        self.refresh_data()

    def _update_areas(self) -> None:
        """Aggiorna dinamicamente il filtro Area basandosi sul Sito selezionato (Asincrono)."""
        site = self.filters.site_filter.currentText()

        self.area_worker = PDLDataWorker("update_areas", site)
        self.area_worker.filters_ready.connect(self._on_filters_ready)
        self.area_worker.start()

    def _update_units(self) -> None:
        """Aggiorna dinamicamente il filtro Unità (Asincrono)."""
        site = self.filters.site_filter.currentText()
        area = self.filters.area_filter.currentText()

        self.unit_worker = PDLDataWorker("update_units", site, area)
        self.unit_worker.filters_ready.connect(self._on_filters_ready)
        self.unit_worker.start()

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
            pdl_dto = self._raw_full_data[row_idx]
            try:
                interventions = PDLService.get_pdl_interventions(pdl_dto.n_pdl)
            except Exception:
                interventions = []
            self.detail_view.update_details(pdl_dto.to_full_list(), interventions)

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
                pdl_numbers.append(self._raw_full_data[row].n_pdl)

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
        self.filters.area_filter.setCurrentIndex(0)
        self.filters.unit_filter.setCurrentIndex(0)
        self.refresh_data()

    def _on_update_bot_clicked(self) -> None:
        """Avvia il bot di aggiornamento per i PDL navigando alla vista ricerca."""
        main_win: Any = self.window()
        if main_win and hasattr(main_win, "navigation_controller"):
            # Naviga al pannello Ricerca PDL
            main_win.navigation_controller.navigate_to_panel("ricerca_pdl")

            # Tenta di avviare il bot sul pannello ricerca se disponibile
            search_panel = getattr(main_win, "pdl_search_panel", None)
            if search_panel and hasattr(search_panel, "_on_start"):
                QTimer.singleShot(200, search_panel._on_start)

    def _export_to_excel(self) -> None:
        """Esporta i dati filtrati correnti in background."""
        if not self._raw_full_data:
            return

        f, _ = QFileDialog.getSaveFileName(
            self,
            "Esporta PDL",
            f"Export_PDL_{datetime.now(UTC).astimezone().strftime('%Y%m%d')}.xlsx",
            "Excel (*.xlsx)",
        )
        if not f:
            return

        from src.gui.widgets.toast import ToastManager

        ToastManager.instance().show("Esportazione PDL in corso...", "info")

        self.io_worker = PdlIOWorker(f, self._raw_full_data, self.full_headers, parent=self)
        self.io_worker.finished_signal.connect(self._on_export_finished)
        self.io_worker.finished.connect(self.io_worker.deleteLater)
        self.io_worker.start()

    def _on_export_finished(self, success: bool, message: str, file_path: str) -> None:
        """Gestisce il completamento dell'esportazione."""
        from src.gui.widgets.toast import ToastManager

        if success:
            ToastManager.instance().show(message, "success")
            if file_path:
                safe_open(file_path)
        else:
            from PySide6.QtWidgets import QMessageBox

            QMessageBox.warning(self, "Errore Esportazione", message)
