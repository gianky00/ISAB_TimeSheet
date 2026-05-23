"""SyncroJob - Storico OdA Panel (Refactored).

Pannello coordinato per la gestione dello Storico OdA.
Utilizza ODAController per la logica di business e ODATreeView per la gerarchia.
Refactored V9.4: Bold on selection and context menu for details.
"""

import logging
from contextlib import suppress
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from PySide6.QtCore import QPoint, Qt, QTimer
from PySide6.QtGui import QShowEvent, QStandardItemModel
from PySide6.QtWidgets import (
    QFileDialog,
    QMenu,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from src.core.oda.oda_controller import ODAController
from src.core.sync_tracker import SyncTracker
from src.gui.widgets.toast import ToastManager
from src.gui.workers.oda_data_worker import ODADataWorker
from src.gui.workers.oda_io_worker import OdaIOWorker
from src.utils.helpers import safe_open

from .oda_filter_widget import OdaFilterWidget
from .oda_legend import OdaLegendWidget
from .utils.oda_adapter import ODAAdapter
from .widgets.oda_tree import ODATreeView

if TYPE_CHECKING:
    from src.gui.controllers.bot_worker import BotWorker

logger = logging.getLogger(__name__)


class StoricoOdaPanel(QWidget):
    """Orchestratore dello Storico OdA con architettura Master-Detail modularizzata.

    Inizializza il pannello dello storico OdA con iniezione del controller.

    Args:
      controller: Istanza del controller per la logica di business.
      parent: Widget genitore opzionale.
    """

    def __init__(self, controller: ODAController, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.controller = controller
        self.worker: BotWorker | None = None
        from PySide6.QtGui import QStandardItem

        self._last_selected_parent: QStandardItem | None = None

        self.master_headers = [
            "Data OdA",
            "OdA",
            "Pos",
            "CREATO DA",
            "Descrizione",
            "Valore Netto",
            "Stato",
            "Ind. Rilascio",
        ]
        self.full_headers = [
            "Org. Acq.",
            "Data OdA",
            "OdA",
            "Pos OdA",
            "Stato",
            "Cat. Contab.",
            "Descrizione",
            "Qta",
            "UOM",
            "Data Consegna",
            "Valore Netto Pos. ODA",
            "Valore Residuo ODA",
            "Valore Netto ODA",
            "Divisione",
            "Destinatario",
            "Nome Destinatario",
            "Codice Fornitore",
            "Descrizione Fornitore",
            "Emittente Fattura",
            "Descrizione Emittente Fattura",
            "Contract Card",
            "Contratto",
            "Posizione Contratto",
            "Gruppo Acquisti",
            "Indicatore Rilascio",
            "Stato Rilascio",
            "Attività",
            "Num riga",
            "Quantit ",
            "Unità di Mis",
            "Prezzo lordo",
            "Testo breve",
        ]

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(self.master_headers)
        self._data_worker: ODADataWorker | None = None

        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.refresh_data)

        self._first_refresh_done = False
        self._setup_ui()
        # Il refresh iniziale viene differito a showEvent per non bloccare lo startup

    def showEvent(self, event: QShowEvent) -> None:
        """Esegue il primo refresh solo quando il pannello diventa visibile."""
        super().showEvent(event)
        if not self._first_refresh_done:
            self._first_refresh_done = True
            QTimer.singleShot(50, self.refresh_data)

    def _setup_ui(self) -> None:
        """Inizializza l'interfaccia utente del pannello con stile Modern Card."""
        from src.gui.styles.ui_effects import UIEffectsManager
        from src.gui.styles.widget_styles import CARD_SHADOW_BLUR, CARD_SHADOW_COLOR, CARD_STYLE

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Container principale
        self.main_container = QWidget()
        self.main_container.setStyleSheet(CARD_STYLE)
        UIEffectsManager.apply_shadow(self.main_container, blur=CARD_SHADOW_BLUR, color=CARD_SHADOW_COLOR)
        UIEffectsManager.animate_fade(self.main_container, duration=400)

        container_layout = QVBoxLayout(self.main_container)
        container_layout.setContentsMargins(15, 15, 15, 15)
        container_layout.setSpacing(5)

        self.filters = OdaFilterWidget()
        self.filters.search_changed.connect(lambda: self.search_timer.start(300))
        self.filters.update_clicked.connect(self._on_update_clicked)
        self.filters.import_clicked.connect(self._on_import_clicked)
        self.filters.export_clicked.connect(self._export_to_excel)

        self._setup_toolbar(container_layout)
        self._setup_scroll_area(container_layout)

        layout.addWidget(self.main_container)

    def refresh_data(self) -> None:
        """Ricarica i dati degli ordini di acquisto applicando i filtri (Asincrono)."""
        self.filters.lbl_sync_status.setText(f"Ultimo Sync: {SyncTracker.get_formatted_status('oda')}")
        search_text = self.filters.search_input.text()

        if self._data_worker and self._data_worker.isRunning():
            self._data_worker.terminate()
            self._data_worker.wait()

        self._data_worker = ODADataWorker(self.controller, search_text)
        self._data_worker.finished_signal.connect(self._on_oda_data_ready)
        self._data_worker.error_signal.connect(lambda msg: logger.error(f"ODA Error: {msg}"))
        self._data_worker.start()

    def _on_oda_data_ready(self, structured_data: list[dict[str, Any]]) -> None:
        """Popola il modello gerarchico con i dati caricati dal worker."""
        self.model.removeRows(0, self.model.rowCount())

        for oda_data in structured_data:
            root_row = ODAAdapter.create_root_row(oda_data)
            self.model.appendRow(root_row)

            parent_item = root_row[0]
            for pos in oda_data["positions"]:
                parent_item.appendRow(ODAAdapter.create_child_row(pos))

        self.empty_state.setVisible(not structured_data)
        if structured_data:
            self.empty_state.hide()

    def _setup_toolbar(self, parent_layout: QVBoxLayout) -> None:
        """Configura la barra dei filtri e la legenda."""
        parent_layout.addWidget(self.filters)
        parent_layout.addWidget(OdaLegendWidget())

    def _setup_scroll_area(self, parent_layout: QVBoxLayout) -> None:
        """Configura l'area di visualizzazione del tree."""
        from PySide6.QtWidgets import QScrollArea, QSplitter

        from src.gui.styles.widget_styles import SCROLL_AREA_BORDERED
        from src.gui.widgets.empty_state import EmptyStateWidget

        from .oda_detail_view import OdaDetailView

        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        # Tree View
        self.tree = ODATreeView(self.model)
        self.tree.selection_changed_custom.connect(self._on_selection_changed)
        self.tree.context_menu_requested.connect(self._show_context_menu)
        self.tree.configure_headers()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.tree)
        scroll.setStyleSheet(SCROLL_AREA_BORDERED)

        self.splitter.addWidget(scroll)

        # Dettaglio
        self.detail_view = OdaDetailView(headers=self.full_headers)
        self.detail_view.setVisible(False)
        self.splitter.addWidget(self.detail_view)
        self.splitter.setStretchFactor(0, 1)

        parent_layout.addWidget(self.splitter)

        # Empty state
        self.empty_state = EmptyStateWidget("Nessun ordine trovato.")
        parent_layout.addWidget(self.empty_state)

    def _on_selection_changed(self) -> None:
        """Gestisce il cambiamento di selezione per evidenziare il record padre."""
        sel_model = self.tree.selectionModel()
        if not sel_model:
            return
        idx = sel_model.selectedRows()

        # Reset bold precedente
        if self._last_selected_parent:
            with suppress(Exception):
                for col in range(self.model.columnCount()):
                    it = self.model.item(self._last_selected_parent.row(), col)
                    if it:
                        font = it.font()
                        font.setBold(False)
                        it.setFont(font)
            self._last_selected_parent = None

        if not idx:
            return

        item = self.model.itemFromIndex(idx[0])
        if not item:
            return

        # Grassetto se  un parent (OdA)
        if not item.parent():
            self._last_selected_parent = item
            for col in range(self.model.columnCount()):
                it = self.model.item(item.row(), col)
                if it:
                    font = it.font()
                    font.setBold(True)
                    it.setFont(font)

    def _show_context_menu(self, pos: QPoint) -> None:
        """Mostra il menu contestuale per l'elemento selezionato.

        Args:
          pos: Posizione del clic del mouse.
        """
        idx = self.tree.indexAt(pos)
        if not idx.isValid():
            return

        menu = QMenu(self)

        # Azione Dettaglio
        menu.addAction("Mostra dettaglio completo").triggered.connect(
            lambda: self._open_detail_for_index(idx)
        )

        # Azione Espandi/Comprimi
        if self.tree.isExpanded(idx):
            menu.addAction("  Comprimi").triggered.connect(lambda: self.tree.collapse(idx))
        else:
            menu.addAction("  Espandi").triggered.connect(lambda: self.tree.expand(idx))

        vp = self.tree.viewport()
        if vp:
            menu.exec(vp.mapToGlobal(pos))

    def _open_detail_for_index(self, index: Any) -> None:
        """Recupera i dati e apre il pannello laterale."""
        item = self.model.itemFromIndex(index)
        if not item:
            return

        # Recuperiamo i dati completi dal UserRole della colonna 0
        parent = item.parent()
        row_item = self.model.item(item.row(), 0) if not parent else parent.child(item.row(), 0)

        if row_item:
            raw_data = row_item.data(Qt.ItemDataRole.UserRole)
            if raw_data:
                self.detail_view.update_details(raw_data)
                self.detail_view.setVisible(True)
                self.splitter.setSizes([int(self.width() * 0.7), int(self.width() * 0.3)])

    def _on_update_clicked(self) -> None:
        """Esegue il workflow di aggiornamento del database tramite Dettagli OdA."""
        from src.gui.main_window.main import MainWindow

        mw = self.window()
        if isinstance(mw, MainWindow):
            mw.workflow_controller.run_dettagli_oda_update()

    def _on_import_clicked(self) -> None:
        """Gestisce l'importazione manuale asincrona di un file Excel OdA."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleziona File Storico OdA", "", "Excel Files (*.xlsx *.xls)"
        )
        if not file_path:
            return

        ToastManager.instance().show("Importazione OdA in corso...", "info")
        self.io_worker = OdaIOWorker("import", file_path, parent=self)
        self.io_worker.finished_signal.connect(self._on_io_finished)
        self.io_worker.finished.connect(self.io_worker.deleteLater)
        self.io_worker.start()

    def _export_to_excel(self) -> None:
        """Esporta i dati filtrati correnti in background."""
        f, _ = QFileDialog.getSaveFileName(
            self,
            "Esporta OdA",
            f"Export_ODA_{datetime.now(UTC).astimezone().strftime('%Y%m%d')}.xlsx",
            "Excel (*.xlsx)",
        )
        if not f:
            return

        ToastManager.instance().show("Esportazione in corso...", "info")
        search_text = self.filters.search_input.text()
        self.io_worker = OdaIOWorker(
            "export", f, {"search_text": search_text, "headers": self.full_headers}, parent=self
        )
        self.io_worker.finished_signal.connect(self._on_io_finished)
        self.io_worker.finished.connect(self.io_worker.deleteLater)
        self.io_worker.start()

    def _on_io_finished(self, success: bool, message: str, stats: dict[str, Any]) -> None:
        """Gestisce il completamento delle operazioni di I/O."""
        if success:
            if "added" in stats:
                ToastManager.instance().show(
                    f"Importazione completata: +{stats['added']} OdA, -{stats['removed']} obsoleti", "success"
                )
                self.refresh_data()
            else:
                ToastManager.instance().show(message, "success")
                if "path" in stats:
                    safe_open(stats["path"])
        else:
            QMessageBox.warning(self, "Operazione Fallita", message)
