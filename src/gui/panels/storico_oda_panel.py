"""
SyncroJob - Storico OdA Panel
Pannello per la visualizzazione del Database Storico OdA con architettura Master-Detail e raggruppamento (QTreeView).
"""

from typing import Any, List, Tuple

from PyQt6.QtCore import QDate, Qt, QTimer
from PyQt6.QtGui import QFont, QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QScrollArea,
    QSplitter,
    QStyle,
    QStyledItemDelegate,
    QTreeView,
    QVBoxLayout,
    QWidget,
)

from src.bots import create_bot
from src.core import config_manager
from src.core.constants import Icons
from src.core.database import db_manager
from src.core.oda_manager import OdaManager
from src.core.sync_tracker import SyncTracker
from src.gui.formatters import format_currency_smart, format_date_it
from src.gui.panels.base import BotWorker
from src.gui.widgets.modern_button import ModernButton
from src.gui.widgets.toast import ToastManager
from src.utils.helpers import get_asset_path


class ChildDescriptionDelegate(QStyledItemDelegate):
    """Delegate per gestire lo stile delle righe figlie."""

    def __init__(self, tree_view):
        super().__init__(tree_view)
        self.tree = tree_view

    def paint(self, painter, option, index):
        # Verifica se siamo in una riga figlia (ha un genitore valido)
        if index.parent().isValid():
            col = index.column()

            # --- GESTIONE MERGE RIMOSSA / DISABILITATA PER NUOVE COLONNE ---
            # Con l'aggiunta di "CREATO DA" e "Descrizione" come colonne esplicite,
            # non è più necessario il merge visuale tra Col 0 e Col 1.
            # Lasciamo il comportamento standard.
            # --- GESTIONE MERGE COL 0 e COL 1 (Testo Breve) ---
            if col == 0 or col == 1:
                # Disegna il testo SOLO quando siamo sulla Col 1 (disegnando verso sinistra)
                # Questo evita che il background della Col 1 copra il testo se disegnato sulla Col 0
                if col == 1:
                    # Recupera dati dalla Col 0 (dove sta il testo vero)
                    sibling0 = index.sibling(index.row(), 0)
                    text = sibling0.data()

                    width_col0 = self.tree.columnWidth(0)

                    try:
                        if option.state & QStyle.StateFlag.State_Selected:
                            painter.setPen(option.palette.highlightedText().color())
                        else:
                            painter.setPen(Qt.GlobalColor.darkBlue)

                        # Rettangolo Totale: Inizia a sinistra di Col 1 (inizio Col 0) ed estende per W0 + W1
                        # Option.rect è il rect della Col 1.
                        # Spostiamo a SX di width_col0. Larghezza = W1 + W0.
                        draw_rect = option.rect.adjusted(-width_col0, 0, 0, 0)

                        painter.setClipRect(draw_rect)

                        padded_rect = draw_rect.adjusted(5, 0, 0, 0)

                        painter.drawText(
                            padded_rect,
                            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                            text,
                        )
                    finally:
                        painter.setClipping(False)

                # Se siamo sulla Col 0 o Col 1, non chiamiamo super().paint() per il contenuto standard
                # ma lasciamo gestire il background alla view o lo ridisegniamo se necessario.
                # Qui ritorniamo per evitare doppio disegno del testo.
                return

        super().paint(painter, option, index)


class StoricoOdaPanel(QWidget):
    """Pannello per la visualizzazione del Database Storico OdA con Tree View (Grouped)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        # Colonne della TreeView (Master)
        # Nuovo ordine: Data OdA, OdA, Pos, CREATO DA, Descrizione, Valore Netto, Stato
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

        # Use QStandardItemModel for Tree grouping
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(self.master_headers)

        self._raw_full_data = []  # Buffer per i dati completi
        self.worker = None  # Worker per il bot

        # Timer per ricerca ritardata (Debounce)
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.refresh_data)

        self._setup_ui()
        QTimer.singleShot(50, self.refresh_data)

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # 1. Filtri (Top)
        filter_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Cerca ovunque... (OdA, Fornitore, Descrizione, Contratto...)"
        )
        self.search_input.textChanged.connect(lambda: self.search_timer.start(500))
        filter_layout.addWidget(self.search_input)

        # Sync Status
        self.lbl_sync_status = QLabel("")
        self.lbl_sync_status.setStyleSheet(
            "color: #555; font-size: 11px; margin-right: 15px;"
        )
        filter_layout.addWidget(self.lbl_sync_status)

        # Update Button (Bot)
        self.update_btn = ModernButton(
            "Aggiorna",
            variant=ModernButton.Variant.PRIMARY,
            icon=get_asset_path(Icons.REFRESH),
        )
        self.update_btn.clicked.connect(self._on_update_clicked)
        filter_layout.addWidget(self.update_btn)

        import_btn = ModernButton(
            "Importa Excel",
            variant=ModernButton.Variant.GHOST,
            icon=get_asset_path(Icons.UPLOAD),
        )
        import_btn.clicked.connect(self._on_import_clicked)
        filter_layout.addWidget(import_btn)

        main_layout.addLayout(filter_layout)

        # 2. Contenitore Splitter (Tree | Dettaglio)
        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        # --- TREE VIEW (MASTER) ---
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setAlternatingRowColors(True)
        self.tree.setSortingEnabled(False)  # Grouping logic handles sort
        self.tree.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tree.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tree.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tree.setAnimated(True)
        # Disabilita default double click expansion per gestirla manualmente su tutte le colonne
        self.tree.setExpandsOnDoubleClick(False)

        # Selection
        self.tree.selectionModel().selectionChanged.connect(self._on_selection_changed)
        self.tree.expanded.connect(self._on_item_expanded)
        self.tree.collapsed.connect(self._on_item_collapsed)
        self.tree.doubleClicked.connect(self._on_tree_double_clicked)

        # Header Styling - Larghezze colonne in base al contenuto
        header = self.tree.header()
        # Nuovo ordine: 0=Data OdA, 1=OdA, 2=Pos, 3=CREATO DA, 4=Descrizione, 5=Valore Netto, 6=Stato
        header.setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )  # Data OdA
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # OdA
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Pos
        header.setSectionResizeMode(
            3, QHeaderView.ResizeMode.Stretch
        )  # CREATO DA - stretch
        header.setSectionResizeMode(
            4, QHeaderView.ResizeMode.Stretch
        )  # Descrizione - stretch
        header.setSectionResizeMode(
            5, QHeaderView.ResizeMode.ResizeToContents
        )  # Valore Netto
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)  # Stato

        # Larghezze minime per colonne compatte (più spaziatura)
        header.setMinimumSectionSize(50)
        self.tree.setColumnWidth(0, 100)  # Data OdA
        self.tree.setColumnWidth(1, 90)  # OdA
        self.tree.setColumnWidth(2, 50)  # Pos
        self.tree.setColumnWidth(6, 80)  # Stato

        # Custom Delegate Style
        self.tree.setItemDelegate(ChildDescriptionDelegate(self.tree))

        self.splitter.addWidget(self.tree)

        # --- PANNELLO DETTAGLIO (DETAIL) ---
        detail_container = QWidget()
        detail_layout = QVBoxLayout(detail_container)
        detail_layout.setContentsMargins(5, 0, 5, 0)

        detail_title = QLabel("Dettaglio Completo OdA")
        detail_title.setStyleSheet(
            "font-weight: bold; font-size: 14px; color: #2196F3; margin-bottom: 5px;"
        )
        detail_layout.addWidget(detail_title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        self.form_layout = QFormLayout(scroll_content)
        self.form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        self.form_layout.setSpacing(10)

        # Placeholder labels
        self.detail_labels = {}
        for h in self.full_headers:
            val_label = QLabel("-")
            val_label.setWordWrap(True)
            val_label.setTextInteractionFlags(
                Qt.TextInteractionFlag.TextSelectableByMouse
            )
            self.detail_labels[h] = val_label
            self.form_layout.addRow(f"<b>{h}:</b>", val_label)

        scroll.setWidget(scroll_content)
        detail_layout.addWidget(scroll)

        self.splitter.addWidget(detail_container)
        self.splitter.setStretchFactor(0, 3)  # Tabella più larga
        self.splitter.setStretchFactor(1, 1)  # Dettaglio più stretto

        main_layout.addWidget(self.splitter)

    def _on_selection_changed(self, selected, _deselected):
        """Aggiorna il pannello dettaglio quando si seleziona un item."""
        indexes = self.tree.selectionModel().selectedRows()
        if not indexes:
            return

        index = indexes[0]
        item = self.model.itemFromIndex(index)
        if not item or not item.data(Qt.ItemDataRole.UserRole):
            return

        full_data = item.data(Qt.ItemDataRole.UserRole)
        for i, h in enumerate(self.full_headers):
            if i < len(full_data):
                val = self._format_detail_value(h, full_data[i])
                self.detail_labels[h].setText(val)

    def _format_detail_value(self, header: str, value: Any) -> str:
        """Helper per formattare il valore nel pannello dettagli."""
        val = str(value)
        if val.lower() == "nan" or val == "none":
            return ""

        # Apply specific formatting
        if "Data" in header:
            return format_date_it(val)
        elif "Valore" in header or "Prezzo" in header:
            return format_currency_smart(val)

        return val

    def _on_item_expanded(self, index):
        """Imposta il font in grassetto quando il gruppo viene espanso."""
        self._set_row_bold(index, True)

    def _on_item_collapsed(self, index):
        """Rimuove il grassetto quando il gruppo viene collassato."""
        self._set_row_bold(index, False)

    def _on_tree_double_clicked(self, index):
        """Gestisce il doppio click per espandere/collassare la riga (su qualsiasi colonna)."""
        if not index.isValid():
            return

        # QStandardItemModel attaches children ONLY to Column 0 items.
        # Clicking on Col 1, 2... returns an index for an item that technically has NO children.
        # We must redirect the expand/collapse action to the sibling at Column 0.
        source_index = index.sibling(index.row(), 0)

        if self.tree.isExpanded(source_index):
            self.tree.collapse(source_index)
        else:
            self.tree.expand(source_index)

    def _set_row_bold(self, parent_index, bold: bool):
        """Helper per cambiare lo stile di tutte le colonne della riga."""
        row = parent_index.row()
        bold_font = QFont()
        bold_font.setBold(bold)

        for col in range(self.model.columnCount()):
            item = self.model.item(row, col)
            if item:
                item.setFont(bold_font)

    def refresh_data(self):
        """Aggiorna i dati della tabella."""
        self.lbl_sync_status.setText(
            f"Ultimo Sync: {SyncTracker.get_formatted_status('storico_oda')}"
        )
        query, params = self._build_query()

        try:
            full_rows = db_manager.execute_query(
                db_manager.DB_STORICO_ODA, query, tuple(params)
            )
            self._raw_full_data = full_rows
            self._populate_tree(full_rows)
        except Exception as e:
            print(f"Errore caricamento Storico OdA: {e}")

    def _build_query(self) -> Tuple[str, List[Any]]:
        """Costruisce la query SQL."""
        search_text = self.search_input.text().lower().strip()

        # Select columns in the exact order of self.full_headers
        query = """
            SELECT
                org_acq, data_oda, oda, pos_oda, stato, cat_contab, descrizione,
                qta, uom, data_consegna, valore_netto_pos, valore_residuo, valore_netto_oda,
                divisione, destinatario, nome_destinatario, codice_fornitore, descrizione_fornitore,
                emittente_fattura, desc_emittente_fattura, contract_card, contratto,
                posizione_contratto, gruppo_acquisti, indicatore_rilascio, stato_rilascio,
                attivita, num_riga, quantita, unita_mis, prezzo_lordo, testo_breve
            FROM storico_oda
            WHERE 1=1
        """
        params = []

        if search_text:
            # Search in ALL relevant columns
            query += """ AND (
                CAST(oda AS TEXT) LIKE ? OR
                descrizione LIKE ? OR
                descrizione_fornitore LIKE ? OR
                CAST(contratto AS TEXT) LIKE ? OR
                codice_fornitore LIKE ? OR
                CAST(pos_oda AS TEXT) LIKE ? OR
                stato LIKE ? OR
                cat_contab LIKE ? OR
                qta LIKE ? OR
                uom LIKE ? OR
                data_consegna LIKE ? OR
                nome_destinatario LIKE ? OR
                emittente_fattura LIKE ? OR
                desc_emittente_fattura LIKE ? OR
                contract_card LIKE ? OR
                gruppo_acquisti LIKE ? OR
                indicatore_rilascio LIKE ? OR
                stato_rilascio LIKE ? OR
                attivita LIKE ? OR
                CAST(num_riga AS TEXT) LIKE ? OR
                testo_breve LIKE ?
            )"""
            p = f"%{search_text}%"
            # Number of placeholders must match columns above (21)
            params.extend([p] * 21)

        # Order by ODA DESC, POS ASC, NUM_RIGA ASC
        # Usiamo CAST per assicurarci l'ordinamento numerico corretto (10, 20, 100...)
        query += (
            " ORDER BY data_oda DESC, oda DESC, "
            "CAST(pos_oda AS INTEGER) ASC, "
            "CAST(num_riga AS INTEGER) ASC LIMIT 3000"
        )
        return query, params

    def _populate_tree(self, full_rows: List[Tuple]):
        """Popola il modello ad albero raggruppando per ODA + POS."""
        self.model.removeRows(0, self.model.rowCount())

        groups = {}  # (oda, pos) -> ParentItem

        for r in full_rows:
            # Indices based on _build_query / self.full_headers
            # oda=2, data=1, pos=3, valore=10, stato=4
            # num_riga=27, descrizione=6, testo_breve=31, prezzo=30, qta=28, uom=29

            oda = r[2]
            pos = r[3]
            group_key = (oda, pos)

            # Create Parent Group if not exists
            if group_key not in groups:
                # Parent columns: CREATO DA, Descrizione, Data OdA, OdA, Pos, Valore Netto, Stato

                # Extract values for new columns
                # nome_destinatario -> index 15
                # descrizione -> index 6
                val_creato_da = str(r[15]) if r[15] else ""
                val_desc = str(r[6]).strip() if r[6] else ""

                item_creato = QStandardItem(val_creato_da)
                item_desc = QStandardItem(val_desc)
                item_data = QStandardItem(format_date_it(str(r[1])))
                item_oda = QStandardItem(str(oda))
                item_pos = QStandardItem(str(pos))
                item_val = QStandardItem(format_currency_smart(str(r[10])))
                item_stato = QStandardItem(str(r[4]))

                # Parent items (initially not bold until expanded)
                # List order must match self.master_headers:
                # Data OdA, OdA, Pos, CREATO DA, Descrizione, Valore Netto, Stato
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

                # Store full data on the parent too (representative of the position)
                # Store on first column (Data OdA)
                item_data.setData(r, Qt.ItemDataRole.UserRole)

                self.model.appendRow(parent_row_items)
                groups[group_key] = item_data  # Keep reference to first item as parent

            parent_item = groups[group_key]

            # Create Child Row (The detailed line)
            # Nuovo Layout colonne:
            # Col 0 (Data OdA)      -> Empty
            # Col 1 (OdA)           -> Empty
            # Col 2 (Pos)           -> Empty
            # Col 3 (CREATO DA)     -> {Testo Breve/Desc Merged}
            # Col 4 (Descrizione)   -> Empty (merge visivo con Col 3)
            # Col 5 (Valore Netto)  -> {Prezzo Lordo}
            # Col 6 (Stato)         -> {UOM Qta}

            raw_testo = str(r[31]).strip() if r[31] else ""
            raw_desc = str(r[6]).strip() if r[6] else ""
            desc = raw_testo if raw_testo and raw_testo.lower() != "nan" else raw_desc

            prezzo = r[30]
            qta = r[28]
            uom = r[29]

            # Col 0, 1, 2: Empty
            c_empty_0 = QStandardItem("")
            c_empty_1 = QStandardItem("")
            c_empty_2 = QStandardItem("")

            # Col 3: Descrizione (merged)
            c_desc_merged = QStandardItem(str(desc))
            c_desc_merged.setTextAlignment(
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
            )

            # Col 4: Empty (merge visivo)
            c_empty_4 = QStandardItem("")

            # Col 5: Prezzo Lordo
            c_prezzo = QStandardItem(format_currency_smart(str(prezzo)))

            # Col 6: UOM + Qta
            c_uom_qta = QStandardItem(f"{uom} {qta}")

            child_row_items = [
                c_empty_0,
                c_empty_1,
                c_empty_2,
                c_desc_merged,
                c_empty_4,
                c_prezzo,
                c_uom_qta,
            ]

            # Child Read-only e Stile
            for it in child_row_items:
                it.setEditable(False)
                it.setForeground(Qt.GlobalColor.darkBlue)
                if it != c_desc_merged:
                    it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            # Store data on child (col 0)
            c_desc_merged.setData(r, Qt.ItemDataRole.UserRole)

            parent_item.appendRow(child_row_items)

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
            # Mostriamo un feedback immediato
            ToastManager.instance().show("Avvio importazione OdA...", "info")

            # Utilizziamo OdaManager che gestisce DB e Sincronizzazione
            # Nota: OdaManager.import_oda_from_excel restituisce (bool, msg, added, removed)
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
        """Avvia il bot Dettagli OdA per aggiornare i dati."""
        try:
            # 1. Recupera Credenziali
            account = config_manager.get_default_account()
            if not account:
                QMessageBox.warning(
                    self, "Attenzione", "Credenziali SafeWork non configurate."
                )
                return
            username, password = account.get("username"), account.get("password")

            # 2. Recupera Parametri dal Config (salvati dal pannello Dettagli OdA)
            config = config_manager.load_config()
            fornitore = config.get("last_oda_fornitore", "")
            dest_path = config.get("path_dettagli_oda", "")

            if not fornitore:
                QMessageBox.warning(
                    self,
                    "Attenzione",
                    "Fornitore non configurato. Vai nel pannello 'Dettagli OdA' e impostalo.",
                )
                return

            # 3. Calcola Date (01.01.AnnoCorrente -> Oggi)
            current_year = QDate.currentDate().year()
            data_da = f"01.01.{current_year}"
            data_a = QDate.currentDate().toString("dd.MM.yyyy")

            # 4. Conferma
            if not self._show_confirmation_dialog(
                "Aggiornamento OdA",
                f"Avviare scarico OdA per <b>{fornitore}</b>?<br><br>Periodo: {data_da} - {data_a}",
            ):
                return

            self.update_btn.setEnabled(False)
            self.lbl_sync_status.setText("⏳ Bot in esecuzione...")
            ToastManager.instance().show("Avvio Bot Dettagli OdA...", "info")

            # 5. Configura e Avvia Bot
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
                self.update_btn.setEnabled(True)
                self.lbl_sync_status.setText("Errore creazione bot")
                return

            # Input data vuoto per triggerare "Lista Generale" nel bot
            bot_data = {
                "rows": [],
                "fornitore": fornitore,
                "data_da": data_da,
                "data_a": data_a,
            }

            self.worker = BotWorker(bot, bot_data)
            self.worker.log_signal.connect(
                lambda msg: print(f"[BOT] {msg}")
            )  # Opzionale: log su console
            self.worker.finished_signal.connect(self._on_bot_finished)
            self.worker.start()

        except Exception as e:
            import traceback

            traceback.print_exc()
            self.update_btn.setEnabled(True)
            self.lbl_sync_status.setText("❌ Errore")
            QMessageBox.critical(
                self, "Errore Critico", f"Errore durante l'avvio del bot:\n{e}"
            )

    def _show_confirmation_dialog(self, title: str, message: str) -> bool:
        """Mostra una dialog di conferma con stile coerente."""
        try:
            dlg = QDialog(self)
            dlg.setWindowTitle(title)
            dlg.setMinimumWidth(350)

            # Rimuovi il pulsante ? dalla barra del titolo
            dlg.setWindowFlags(
                dlg.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint
            )

            layout = QVBoxLayout(dlg)
            layout.setSpacing(20)
            layout.setContentsMargins(20, 20, 20, 20)

            lbl = QLabel(message)
            lbl.setWordWrap(True)
            lbl.setTextFormat(Qt.TextFormat.RichText)
            lbl.setStyleSheet("font-size: 14px; color: #333;")
            layout.addWidget(lbl)

            btn_layout = QHBoxLayout()
            btn_layout.setSpacing(10)
            btn_layout.addStretch()

            btn_cancel = ModernButton("Annulla", variant=ModernButton.Variant.GHOST)
            btn_cancel.clicked.connect(dlg.reject)

            btn_confirm = ModernButton("Avvia", variant=ModernButton.Variant.PRIMARY)
            btn_confirm.clicked.connect(dlg.accept)

            btn_layout.addWidget(btn_cancel)
            btn_layout.addWidget(btn_confirm)

            layout.addLayout(btn_layout)

            # Usa 1 per Accepted (più sicuro di enum complessi in alcune versioni binding)
            return dlg.exec() == 1
        except Exception as e:
            print(f"Errore Dialog: {e}")
            return False

    def _on_bot_finished(self, success: bool):
        """Callback fine esecuzione bot."""
        self.update_btn.setEnabled(True)
        if success:
            ToastManager.instance().show("Aggiornamento completato!", "success")
            self.refresh_data()
        else:
            self.lbl_sync_status.setText("❌ Errore Bot")
            QMessageBox.warning(
                self, "Errore", "Il bot ha terminato con errori. Controlla i log."
            )
