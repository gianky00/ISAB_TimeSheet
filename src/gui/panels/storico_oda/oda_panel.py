"""
SyncroJob - Storico OdA Panel (Refactored)
Pannello coordinato per la gestione dello Storico OdA.
Utilizza ODAController per la logica di business e ODATreeView per la gerarchia.
Refactored V9.4: Bold on selection and context menu for details.
"""

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
from src.gui.workers.oda_io_worker import OdaIOWorker
from src.utils.helpers import safe_open

from .utils.oda_adapter import ODAAdapter

if TYPE_CHECKING:
    from src.gui.controllers.bot_worker import BotWorker


class StoricoOdaPanel(QWidget):
    """Orchestratore dello Storico OdA con architettura Master-Detail modularizzata."""

    def __init__(self, controller: ODAController, parent: QWidget | None = None) -> None:
        """
        Inizializza il pannello dello storico OdA con iniezione del controller.

        Args:
          controller: Istanza del controller per la logica di business.
          parent: Widget genitore opzionale.
        """
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

        self._setup_toolbar(container_layout)
        self._setup_scroll_area(container_layout)

        layout.addWidget(self.main_container)

    def refresh_data(self) -> None:
        """Aggiorna i dati visualizzati nel tree applicando i filtri correnti."""
        self.filters.lbl_sync_status.setText(f"Ultimo Sync: {SyncTracker.get_formatted_status('oda')}")
        search_text = self.filters.search_input.text()

        structured_data = self.controller.get_grouped_data(search_text)

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
        """
        Mostra il menu contestuale per l'elemento selezionato.

        Args:
          pos: Posizione del clic del mouse.
        """
        idx = self.tree.indexAt(pos)
        if not idx.isValid():
            return

        menu = QMenu(self)

        # Azione Dettaglio
        menu.addAction("[CERCA] Mostra dettaglio completo").triggered.connect(
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
