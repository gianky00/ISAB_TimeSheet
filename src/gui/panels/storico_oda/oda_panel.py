"""
SyncroJob - Storico OdA Panel
Pannello per la visualizzazione del Database Storico OdA con architettura Master-Detail e raggruppamento (QTreeView).
"""

from datetime import datetime
from typing import List, Tuple

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMessageBox,
    QSplitter,
    QTreeView,
    QVBoxLayout,
    QWidget,
)

from src.bots import create_bot
from src.core import config_manager
from src.core.oda_manager import OdaManager
from src.core.sync_tracker import SyncTracker
from src.gui.formatters import format_currency_smart, format_date_it
from src.gui.panels.base import BotWorker
from src.gui.widgets.modern_button import ModernButton
from src.gui.widgets.toast import ToastManager

from .oda_delegate import ChildDescriptionDelegate
from .oda_detail_view import OdaDetailView
from .oda_filter_widget import OdaFilterWidget


class StoricoOdaPanel(QWidget):
    """Pannello per lo Storico OdA con vista gerarchica (OdA -> Posizioni)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.full_headers = [
            "OdA",
            "Posizione",
            "Riga",
            "Org. Acq.",
            "Data OdA",
            "Stato",
            "Cat. Contab.",
            "Descrizione",
            "Qta",
            "UoM",
            "Data Consegna",
            "Valore Netto Pos",
            "Valore Residuo",
            "Valore Netto OdA",
            "Divisione",
            "Destinatario",
            "Nome Dest.",
            "Cod. Fornitore",
            "Desc. Fornitore",
            "Emittente Fatt.",
            "Desc. Emittente",
            "Card",
            "Contratto",
            "Pos. Contratto",
            "Gr. Acquisti",
            "Ind. Rilascio",
            "Stato Rilascio",
            "Attività",
            "Quantità",
            "Unità Mis.",
            "Prezzo Lordo",
            "Testo Breve",
            "Aggiornato il",
        ]

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(
            [
                "OdA / Testo Breve",
                "Fornitore / Stato",
                "Data OdA",
                "Netto Pos",
                "Residuo",
            ]
        )

        self._raw_data_map = {}  # Mappa ID -> riga completa per dettaglio

        # Timer per ricerca ritardata
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.refresh_data)

        self._setup_ui()
        QTimer.singleShot(100, self.refresh_data)

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # 1. Filtri
        self.filters = OdaFilterWidget()
        self.filters.search_changed.connect(lambda: self.search_timer.start(500))
        self.filters.update_clicked.connect(self._on_update_clicked)
        self.filters.export_clicked.connect(self._export_to_excel)
        main_layout.addWidget(self.filters)

        # 2. Splitter
        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        # --- TREE VIEW (MASTER) ---
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setAlternatingRowColors(True)
        self.tree.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tree.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tree.setUniformRowHeights(True)
        self.tree.setIndentation(25)
        self.tree.setItemDelegate(ChildDescriptionDelegate(self.tree))

        self.tree.selectionModel().selectionChanged.connect(self._on_selection_changed)

        header = self.tree.header()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        header.setDefaultSectionSize(150)

        self.splitter.addWidget(self.tree)

        # --- DETAIL VIEW ---
        self.detail_view = OdaDetailView(self.full_headers)
        self.splitter.addWidget(self.detail_view)

        self.splitter.setStretchFactor(0, 3)
        self.splitter.setStretchFactor(1, 1)

        main_layout.addWidget(self.splitter)

    def refresh_data(self):
        """Carica i dati dal database e popola il modello gerarchico."""
        self.filters.set_sync_status(
            f"Ultimo Sync: {SyncTracker.get_formatted_status('storico_oda')}"
        )

        search_text = self.filters.search_input.text().strip()
        try:
            rows = OdaManager.get_all_oda(search_text if search_text else None)
            self._populate_tree(rows)
        except Exception as e:
            print(f"Errore refresh OdA: {e}")

    def _populate_tree(self, rows: List[Tuple]):
        """Crea la struttura OdA -> Posizioni."""
        self.model.removeRows(0, self.model.rowCount())
        self._raw_data_map.clear()

        # Raggruppa per OdA
        groups = {}
        for r in rows:
            oda_id = str(r[0])
            if oda_id not in groups:
                groups[oda_id] = []
            groups[oda_id].append(r)

        font_bold = QFont()
        font_bold.setBold(True)

        for oda_id, positions in groups.items():
            # Riga Padre (OdA)
            first_pos = positions[0]
            fornitore = str(first_pos[18])  # Descrizione Fornitore
            data_oda = format_date_it(str(first_pos[4]))
            valore_oda = format_currency_smart(float(first_pos[13] or 0))

            parent = QStandardItem(f"OdA {oda_id}")
            parent.setFont(font_bold)
            parent.setData(oda_id, Qt.ItemDataRole.UserRole)

            item_forn = QStandardItem(fornitore)
            item_date = QStandardItem(data_oda)
            item_val = QStandardItem(valore_oda)
            item_val.setTextAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )
            item_res = QStandardItem("")

            self.model.appendRow([parent, item_forn, item_date, item_val, item_res])

            # Righe Figlie (Posizioni)
            for pos in positions:
                testo_breve = str(pos[31]) or str(pos[7])  # Testo Breve o Descrizione
                stato = str(pos[5])
                val_pos = format_currency_smart(float(pos[11] or 0))
                val_res = format_currency_smart(float(pos[12] or 0))

                # ID univoco per riga: ODA_POS_RIGA
                row_key = f"{pos[0]}_{pos[1]}_{pos[2]}"
                self._raw_data_map[row_key] = pos

                child_oda = QStandardItem(testo_breve)
                child_oda.setData(row_key, Qt.ItemDataRole.UserRole)
                child_oda.setForeground(Qt.GlobalColor.darkBlue)

                child_stato = QStandardItem(stato)
                child_date = QStandardItem("")
                child_val = QStandardItem(val_pos)
                child_val.setTextAlignment(
                    Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                )
                child_res = QStandardItem(val_res)
                child_res.setTextAlignment(
                    Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                )

                parent.appendRow(
                    [child_oda, child_stato, child_date, child_val, child_res]
                )

        # Espandi i primi livelli se pochi risultati
        if len(groups) < 10:
            self.tree.expandAll()

    def _on_selection_changed(self, selected, _deselected):
        indexes = self.tree.selectionModel().selectedRows()
        if not indexes:
            self.detail_view.clear()
            return

        index = indexes[0]
        row_key = index.data(Qt.ItemDataRole.UserRole)

        if row_key and row_key in self._raw_data_map:
            self.detail_view.update_details(list(self._raw_data_map[row_key]))
        else:
            self.detail_view.clear()

    def _on_update_clicked(self):
        """Avvia il bot Dettagli OdA per sincronizzare i dati."""
        try:
            config = config_manager.load_config()

            # Recupero credenziali default (standard ISAB)
            account = config_manager.get_default_account()
            if not account:
                QMessageBox.warning(
                    self,
                    "Attenzione",
                    "Nessun account ISAB configurato in Impostazioni > Account.",
                )
                return

            username = account.get("username", "")
            password = account.get("password", "")

            # Recupero fornitore default
            fornitori = config.get("fornitori", [])
            fornitore = (
                fornitori[0] if fornitori else "KK10608 - COEMI S.R.L."
            )  # Default fallback

            if not username or not password:
                QMessageBox.warning(
                    self, "Attenzione", "Credenziali Portale Fornitori incomplete."
                )
                return

            if not self._show_confirmation_dialog(
                "Aggiornamento OdA",
                f"Avviare la sincronizzazione OdA per il fornitore <b>{fornitore}</b>?",
            ):
                return

            self.filters.btn_bot_update.setEnabled(False)
            ToastManager.instance().show(f"Avvio Sync OdA ({fornitore})...", "info")

            # Calcola range date (01/01/YYYY -> Oggi)
            date_from = f"01.01.{datetime.now().year}"
            date_to = datetime.now().strftime("%d.%m.%Y")

            bot = create_bot(
                "dettagli_oda",
                username=username,
                password=password,
                headless=config.get("browser_headless", True),
                fornitore=fornitore,
                data_da=date_from,
                data_a=date_to,
            )

            if not bot:
                self.filters.btn_bot_update.setEnabled(True)
                return

            # Passiamo una lista vuota per attivare la "lista generale" nel bot
            bot_data = []

            self.worker = BotWorker(bot, bot_data)
            self.worker.finished_signal.connect(self._on_bot_finished)
            self.worker.start()

        except Exception as e:
            self.filters.btn_bot_update.setEnabled(True)
            QMessageBox.critical(self, "Errore", f"Errore avvio bot: {e}")

    def _on_bot_finished(self, success: bool):
        self.filters.btn_bot_update.setEnabled(True)
        if success:
            ToastManager.instance().show("OdA Sincronizzati!", "success")
            self.refresh_data()
        else:
            ToastManager.instance().show("Errore durante il sync OdA", "danger")

    def _show_confirmation_dialog(self, title: str, message: str) -> bool:
        dlg = QDialog(self)
        dlg.setWindowTitle(title)
        dlg.setMinimumWidth(350)
        layout = QVBoxLayout(dlg)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        lbl = QLabel(message)
        lbl.setWordWrap(True)
        lbl.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(lbl)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_cancel = ModernButton("Annulla", variant=ModernButton.Variant.GHOST)
        btn_cancel.clicked.connect(dlg.reject)
        btn_confirm = ModernButton("Avvia", variant=ModernButton.Variant.PRIMARY)
        btn_confirm.clicked.connect(dlg.accept)
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_confirm)
        layout.addLayout(btn_layout)

        return dlg.exec() == 1

    def _export_to_excel(self):
        """Esporta la vista corrente in Excel."""
        try:
            filename, _ = QFileDialog.getSaveFileName(
                self,
                "Esporta Storico OdA",
                f"Storico_OdA_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                "Excel Files (*.xlsx)",
            )
            if not filename:
                return

            import pandas as pd

            # Esportiamo i dati raw correnti filtrati
            search_text = self.filters.search_input.text().strip()
            rows = OdaManager.get_all_oda(search_text if search_text else None)

            df = pd.DataFrame(rows, columns=self.full_headers)
            df.to_excel(filename, index=False, engine="openpyxl")
            ToastManager.instance().show("Esportazione completata!", "success")
            import os

            os.startfile(filename)
        except Exception as e:
            QMessageBox.critical(self, "Errore Export", f"Impossibile esportare: {e}")
