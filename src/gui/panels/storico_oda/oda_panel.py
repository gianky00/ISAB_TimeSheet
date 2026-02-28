"""
SyncroJob - Storico OdA Panel (Refactored)
Pannello coordinato per la gestione dello Storico OdA.
Utilizza ODAController per la logica di business e ODATreeView per la gerarchia.
Refactored V9.4: Bold on selection and context menu for details.
"""

import os
from contextlib import suppress
from datetime import datetime

import pandas as pd
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QStandardItemModel
from PyQt6.QtWidgets import (
    QFileDialog,
    QMenu,
    QMessageBox,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.core.oda.oda_controller import ODAController
from src.core.oda_manager import OdaManager
from src.core.sync_tracker import SyncTracker
from src.gui.panels.base import BotWorker  # noqa: TC001
from src.gui.widgets import EmptyStateWidget
from src.gui.widgets.toast import ToastManager

from .oda_detail_view import OdaDetailView
from .oda_filter_widget import OdaFilterWidget
from .widgets.oda_tree import ODATreeView


class StoricoOdaPanel(QWidget):
    """Orchestratore dello Storico OdA con architettura Master-Detail modularizzata."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = ODAController()
        self.worker: BotWorker | None = None
        self._last_selected_parent = None

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
            "Quantità",
            "Unità di Mis",
            "Prezzo lordo",
            "Testo breve",
        ]

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(self.master_headers)

        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.refresh_data)

        self._setup_ui()
        QTimer.singleShot(100, self.refresh_data)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 10)
        layout.setSpacing(5)

        self.filters = OdaFilterWidget()
        self.filters.search_changed.connect(lambda: self.search_timer.start(500))
        self.filters.update_clicked.connect(self._on_update_clicked)
        self.filters.import_clicked.connect(self._on_import_clicked)
        self.filters.export_clicked.connect(self._export_to_excel)
        layout.addWidget(self.filters)

        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.tree = ODATreeView(self.model)
        self.tree.configure_headers()
        self.tree.selection_changed_custom.connect(self._on_selection_changed)
        self.tree.context_menu_requested.connect(self._show_context_menu)
        self.splitter.addWidget(self.tree)

        self.detail_view = OdaDetailView(self.full_headers)
        self.detail_view.setVisible(False)
        self.splitter.addWidget(self.detail_view)

        self.empty_state = EmptyStateWidget(
            title="Nessun OdA", message="Prova ad aggiornare il database.", icon_key=Icons.FOLDER
        )
        self.empty_state.setParent(self.tree)
        self.empty_state.hide()

        layout.addWidget(self.splitter)

    def refresh_data(self):
        self.filters.lbl_sync_status.setText(f"Ultimo Sync: {SyncTracker.get_formatted_status('oda')}")
        search_text = self.filters.search_input.text()

        structured_data = self.controller.get_grouped_data(search_text)

        self.model.removeRows(0, self.model.rowCount())
        for oda_data in structured_data:
            root_row = self.controller.create_root_item(oda_data)
            self.model.appendRow(root_row)

            parent_item = root_row[0]
            for pos in oda_data["positions"]:
                parent_item.appendRow(self.controller.create_child_item(pos))

        self.empty_state.setVisible(not structured_data)
        if structured_data:
            self.empty_state.hide()

    def _on_selection_changed(self):
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

        # Grassetto se è un parent (OdA)
        if not item.parent():
            self._last_selected_parent = item
            for col in range(self.model.columnCount()):
                it = self.model.item(item.row(), col)
                if it:
                    font = it.font()
                    font.setBold(True)
                    it.setFont(font)

    def _show_context_menu(self, pos):
        idx = self.tree.indexAt(pos)
        if not idx.isValid():
            return

        menu = QMenu(self)

        # Azione Dettaglio
        detail_act = menu.addAction("🔍 Mostra dettaglio completo")
        if detail_act:
            detail_act.triggered.connect(lambda: self._open_detail_for_index(idx))

        # Azione Espandi/Comprimi
        if self.tree.isExpanded(idx):
            expand_act = menu.addAction("➖ Comprimi")
            if expand_act:
                expand_act.triggered.connect(lambda: self.tree.collapse(idx))
        else:
            expand_act = menu.addAction("➕ Espandi")
            if expand_act:
                expand_act.triggered.connect(lambda: self.tree.expand(idx))

        vp = self.tree.viewport()
        if vp:
            menu.exec(vp.mapToGlobal(pos))

    def _open_detail_for_index(self, index):
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

    def _on_update_clicked(self):
        from src.gui.main_window import MainWindow

        mw = self.window()
        if isinstance(mw, MainWindow):
            mw.workflow_controller.run_carico_ts()

    def _on_import_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleziona File Storico OdA", "", "Excel Files (*.xlsx *.xls)"
        )
        if not file_path:
            return

        try:
            success, message, added, removed = OdaManager.import_oda_from_excel(file_path)
            if success:
                ToastManager.instance().show(
                    f"Importazione completata: +{added} OdA, -{removed} obsoleti", "success"
                )
                self.refresh_data()
            else:
                QMessageBox.warning(self, "Errore Importazione", message)
        except Exception as e:
            QMessageBox.critical(self, "Errore Critico", f"Errore durante l'importazione: {e}")

    def _export_to_excel(self):
        search_text = self.filters.search_input.text()
        raw_data = OdaManager.get_all_oda(search_text)
        if not raw_data:
            return

        df = pd.DataFrame(raw_data, columns=self.full_headers)
        f, _ = QFileDialog.getSaveFileName(
            self,
            "Esporta OdA",
            f"Export_ODA_{datetime.now().strftime('%Y%m%d')}.xlsx",
            "Excel (*.xlsx)",
        )
        if f:
            df.to_excel(f, index=False)
            os.startfile(f)  # noqa: S606
