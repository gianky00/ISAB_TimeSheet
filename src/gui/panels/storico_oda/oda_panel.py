"""
SyncroJob - Storico OdA Panel
Pannello per la visualizzazione del Database Storico OdA con architettura Master-Detail e raggruppamento (QTreeView).
"""

from datetime import datetime
from typing import List, Tuple

from PyQt6.QtCore import QDate, Qt, QTimer
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

        # Colonne della TreeView (Master)
        # Ordine originale: Data OdA, OdA, Pos, CREATO DA, Descrizione, Valore Netto, Stato
        self.master_headers = [
            "Data OdA",
            "OdA",
            "Pos",
            "CREATO DA",
            "Descrizione",
            "Valore Netto",
            "Stato",
        ]

        # Mapping completo per il Dettaglio
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

        self._raw_full_data = []  # Buffer per i dati completi
        self.worker = None  # Worker per il bot

        # Timer per ricerca ritardata
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.refresh_data)

        self._setup_ui()
        QTimer.singleShot(100, self.refresh_data)

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)

        # 1. Filtri
        self.filters = OdaFilterWidget()
        self.filters.search_changed.connect(lambda: self.search_timer.start(500))
        self.filters.update_clicked.connect(self._on_update_clicked)
        self.filters.import_clicked.connect(self._on_import_clicked)
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
        self.tree.setAnimated(True)
        self.tree.setExpandsOnDoubleClick(False)
        self.tree.setItemDelegate(ChildDescriptionDelegate(self.tree))

        # Selection & Interaction
        self.tree.selectionModel().selectionChanged.connect(self._on_selection_changed)
        self.tree.expanded.connect(self._on_item_expanded)
        self.tree.collapsed.connect(self._on_item_collapsed)
        self.tree.doubleClicked.connect(self._on_tree_double_clicked)

        # Header Styling
        header = self.tree.header()
        header.setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )  # Data OdA
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # OdA
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Pos
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)  # CREATO DA
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)  # Descrizione
        header.setSectionResizeMode(
            5, QHeaderView.ResizeMode.ResizeToContents
        )  # Valore Netto
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)  # Stato

        self.tree.setColumnWidth(0, 100)
        self.tree.setColumnWidth(1, 90)
        self.tree.setColumnWidth(2, 50)
        self.tree.setColumnWidth(6, 80)

        self.splitter.addWidget(self.tree)

        # --- DETAIL VIEW ---
        self.detail_view = OdaDetailView(self.full_headers)
        self.splitter.addWidget(self.detail_view)

        self.splitter.setStretchFactor(0, 3)
        self.splitter.setStretchFactor(1, 1)

        main_layout.addWidget(self.splitter)

    def refresh_data(self):
        """Aggiorna i dati della tabella."""
        self.filters.set_sync_status(
            f"Ultimo Sync: {SyncTracker.get_formatted_status('storico_oda')}"
        )

        search_text = self.filters.search_input.text().strip()
        try:
            full_rows = OdaManager.get_all_oda(search_text if search_text else None)
            self._raw_full_data = full_rows
            self._populate_tree(full_rows)
        except Exception as e:
            print(f"Errore caricamento Storico OdA: {e}")

    def _populate_tree(self, full_rows: List[Tuple]):
        """Popola il modello ad albero raggruppando per ODA + POS."""
        self.model.removeRows(0, self.model.rowCount())

        groups = {}  # (oda, pos) -> ParentItem

        for r in full_rows:
            # Gli indici corrispondono alla query in OdaManager.get_all_oda:
            # 0:org_acq, 1:data_oda, 2:oda, 3:pos_oda, 4:stato, 5:cat_contab, 6:descrizione,
            # 10:valore_netto_pos, 15:nome_destinatario, 28:quantita, 29:unita_mis, 30:prezzo_lordo, 31:testo_breve

            oda = r[2]
            pos = r[3]
            group_key = (oda, pos)

            # Create Parent Group if not exists
            if group_key not in groups:
                val_creato_da = str(r[15]) if r[15] else ""
                val_desc = str(r[6]).strip() if r[6] else ""

                item_creato = QStandardItem(val_creato_da)
                item_desc = QStandardItem(val_desc)
                item_data = QStandardItem(format_date_it(str(r[1])))
                item_oda = QStandardItem(str(oda))
                item_pos = QStandardItem(str(pos))
                item_val = QStandardItem(format_currency_smart(str(r[10])))
                item_stato = QStandardItem(str(r[4]))

                parent_row_items = [
                    item_data,
                    item_oda,
                    item_pos,
                    item_creato,
                    item_desc,
                    item_val,
                    item_stato,
                ]

                for it in parent_row_items:
                    it.setEditable(False)

                # Salviamo i dati completi nel primo item per il dettaglio
                item_data.setData(r, Qt.ItemDataRole.UserRole)

                self.model.appendRow(parent_row_items)
                groups[group_key] = item_data

            parent_item = groups[group_key]

            # Create Child Row (The detailed line)
            raw_testo = str(r[31]).strip() if r[31] else ""
            raw_desc = str(r[6]).strip() if r[6] else ""
            desc = raw_testo if raw_testo and raw_testo.lower() != "nan" else raw_desc

            prezzo = r[30]
            qta = r[28]
            uom = r[29]

            # Col 0: Descrizione (per merge con Col 1 via Delegate)
            c_desc_merged = QStandardItem(str(desc))
            c_desc_merged.setTextAlignment(
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
            )
            c_desc_merged.setData(
                r, Qt.ItemDataRole.UserRole
            )  # Per dettaglio anche sui figli

            # Col 1-4: Empty
            c_empty_1 = QStandardItem("")
            c_empty_2 = QStandardItem("")
            c_empty_3 = QStandardItem("")
            c_empty_4 = QStandardItem("")

            # Col 5: Prezzo Lordo
            c_prezzo = QStandardItem(format_currency_smart(str(prezzo)))

            # Col 6: UOM + Qta
            c_uom_qta = QStandardItem(f"{uom} {qta}")

            child_row_items = [
                c_desc_merged,
                c_empty_1,
                c_empty_2,
                c_empty_3,
                c_empty_4,
                c_prezzo,
                c_uom_qta,
            ]

            for it in child_row_items:
                it.setEditable(False)
                it.setForeground(Qt.GlobalColor.darkBlue)
                if it != c_desc_merged:
                    it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            parent_item.appendRow(child_row_items)

        if len(groups) < 15:
            self.tree.expandAll()

    def _on_selection_changed(self, selected, _deselected):
        indexes = self.tree.selectionModel().selectedRows()
        if not indexes:
            self.detail_view.clear()
            return

        index = indexes[0]
        # I dati sono salvati nell'ItemDataRole.UserRole della riga (col 0 o col 3 dipendentemente dal tipo)
        full_data = index.data(Qt.ItemDataRole.UserRole)

        if full_data:
            self.detail_view.update_details(list(full_data))
        else:
            self.detail_view.clear()

    def _on_item_expanded(self, index):
        self._set_row_bold(index, True)

    def _on_item_collapsed(self, index):
        self._set_row_bold(index, False)

    def _on_tree_double_clicked(self, index):
        source_index = index.sibling(index.row(), 0)
        if self.tree.isExpanded(source_index):
            self.tree.collapse(source_index)
        else:
            self.tree.expand(source_index)

    def _set_row_bold(self, parent_index, bold: bool):
        row = parent_index.row()
        font = QFont()
        font.setBold(bold)
        for col in range(self.model.columnCount()):
            item = self.model.item(row, col)
            if item:
                item.setFont(font)

    def _on_import_clicked(self):
        """Gestisce l'importazione manuale del file Excel Storico OdA."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleziona File Storico OdA",
            "",
            "Excel Files (*.xlsx *.xls);;All Files (*)",
        )
        if not file_path:
            return

        try:
            ToastManager.instance().show("Avvio importazione OdA...", "info")
            success, message, added, _ = OdaManager.import_oda_from_excel(file_path)
            if success:
                ToastManager.instance().show(
                    f"Importazione completata: {added} righe aggiornate.", "success"
                )
                self.refresh_data()
            else:
                QMessageBox.warning(
                    self, "Errore Importazione", f"Impossibile importare:\n{message}"
                )
        except Exception as e:
            QMessageBox.critical(
                self, "Errore Critico", f"Errore durante l'importazione:\n{str(e)}"
            )

    def _on_update_clicked(self):
        """Avvia il bot Dettagli OdA per sincronizzare i dati."""
        try:
            account = config_manager.get_default_account()
            if not account:
                QMessageBox.warning(
                    self, "Attenzione", "Credenziali ISAB non configurate."
                )
                return
            username, password = account.get("username"), account.get("password")

            config = config_manager.load_config()
            fornitore = config.get("last_oda_fornitore", "KK10608 - COEMI S.R.L.")
            dest_path = config.get("path_dettagli_oda", "")

            # Calcola Date (01.01.AnnoCorrente -> Oggi)
            data_da = f"01.01.{QDate.currentDate().year()}"
            data_a = QDate.currentDate().toString("dd.MM.yyyy")

            if not self._show_confirmation_dialog(
                "Aggiornamento OdA",
                f"Avviare scarico OdA per <b>{fornitore}</b>?<br><br>Periodo: {data_da} - {data_a}",
            ):
                return

            self.filters.btn_bot_update.setEnabled(False)
            ToastManager.instance().show("Avvio Bot Dettagli OdA...", "info")

            bot = create_bot(
                "dettagli_oda",
                username=username,
                password=password,
                headless=config.get("browser_headless", False),
                timeout=config.get("browser_timeout", 30),
                download_path=dest_path,
                fornitore=fornitore,
                data_da=data_da,
                data_a=data_a,
            )

            if not bot:
                self.filters.btn_bot_update.setEnabled(True)
                return

            bot_data = {
                "rows": [],
                "fornitore": fornitore,
                "data_da": data_da,
                "data_a": data_a,
            }
            self.worker = BotWorker(bot, bot_data)
            self.worker.finished_signal.connect(self._on_bot_finished)
            self.worker.start()

        except Exception as e:
            self.filters.btn_bot_update.setEnabled(True)
            QMessageBox.critical(self, "Errore", f"Errore durante l'avvio del bot: {e}")

    def _on_bot_finished(self, success: bool):
        self.filters.btn_bot_update.setEnabled(True)
        if success:
            ToastManager.instance().show("Aggiornamento completato!", "success")
            self.refresh_data()
        else:
            QMessageBox.warning(
                self, "Errore", "Il bot ha terminato con errori. Controlla i log."
            )

    def _show_confirmation_dialog(self, title: str, message: str) -> bool:
        dlg = QDialog(self)
        dlg.setWindowTitle(title)
        dlg.setMinimumWidth(350)
        dlg.setWindowFlags(
            dlg.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint
        )
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

            search_text = self.filters.search_input.text().strip()
            rows = OdaManager.get_all_oda(search_text if search_text else None)
            df = pd.DataFrame(rows, columns=self.full_headers)
            df.to_excel(filename, index=False, engine="openpyxl")
            ToastManager.instance().show("Esportazione completata!", "success")
            import os

            os.startfile(filename)
        except Exception as e:
            QMessageBox.critical(self, "Errore Export", f"Impossibile esportare: {e}")
