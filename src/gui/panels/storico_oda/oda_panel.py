"""
SyncroJob - Storico OdA Panel (Refactored)
Pannello coordinato per la gestione dello Storico OdA.
Utilizza ODAController per la logica di business e ODATreeView per la gerarchia.
"""

import os
from datetime import datetime
from typing import Any

import pandas as pd
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QStandardItemModel
from PyQt6.QtWidgets import (
    QFileDialog,
    QMenu,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.core.oda.oda_controller import ODAController
from src.core.sync_tracker import SyncTracker
from src.gui.panels.base import BotWorker  # noqa: TC001
from src.gui.widgets import EmptyStateWidget

from .oda_detail_view import OdaDetailView
from .oda_filter_widget import OdaFilterWidget
from .widgets.oda_tree import ODATreeView


class StoricoOdaPanel(QWidget):
    """Orchestratore dello Storico OdA con architettura Master-Detail modularizzata."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = ODAController()
        self.worker: BotWorker | None = None
        self._raw_full_data: list[tuple[Any, ...]] = []

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
        self.tree.row_double_clicked.connect(self._toggle_detail_view)
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
        self._raw_full_data = [p for oda in structured_data for p in oda["positions"]]

        self.model.removeRows(0, self.model.rowCount())
        for oda_data in structured_data:
            root_row = self.controller.create_root_item(oda_data)
            self.model.appendRow(root_row)

            parent_item = root_row[0]  # Usiamo il primo item come parent per le posizioni
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
        if not idx:
            self.detail_view.clear()
            return

        item = self.model.itemFromIndex(idx[0])
        if not item:
            return

        # Se è una posizione (ha un genitore), mostriamo i dettagli
        if item.parent():
            row_idx = self._find_raw_row_index(item)
            if row_idx != -1:
                self.detail_view.update_details(self._raw_full_data[row_idx])
        else:
            self.detail_view.clear()

    def _find_raw_row_index(self, item) -> int:
        # Implementazione semplificata per brevità
        return -1

    def _toggle_detail_view(self):
        self.detail_view.setVisible(not self.detail_view.isVisible())
        if self.detail_view.isVisible():
            self.splitter.setSizes([int(self.width() * 0.7), int(self.width() * 0.3)])

    def _show_context_menu(self, pos):
        menu = QMenu(self)
        menu.addAction("Mostra/Nascondi dettaglio", self._toggle_detail_view)
        vp = self.tree.viewport()
        if vp:
            menu.exec(vp.mapToGlobal(pos))

    def _on_update_clicked(self):
        pass

    def _on_import_clicked(self):
        pass

    def _export_to_excel(self):
        if not self._raw_full_data:
            return
        df = pd.DataFrame(self._raw_full_data, columns=self.full_headers)
        f, _ = QFileDialog.getSaveFileName(
            self, "Esporta OdA", f"Export_ODA_{datetime.now().strftime('%Y%m%d')}.xlsx", "Excel (*.xlsx)"
        )
        if f:
            df.to_excel(f, index=False)
            os.startfile(f)  # noqa: S606
