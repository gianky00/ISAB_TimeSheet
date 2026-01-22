"""
SyncroJob - Storico OdA Panel
Pannello per la visualizzazione del Database Storico OdA con architettura Master-Detail e raggruppamento (QTreeView).
"""

from typing import Any, List, Tuple

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QFormLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSplitter,
    QStyle,
    QStyledItemDelegate,
    QTreeView,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QMessageBox,
)

from src.core.constants import Icons
from src.core.database import db_manager
from src.core.oda_manager import OdaManager
from src.gui.formatters import format_currency_smart, format_date_it
from src.gui.widgets.toast import ToastManager
from src.utils.helpers import get_asset_path, get_colored_icon


class ChildDescriptionDelegate(QStyledItemDelegate):
    """Delegate per gestire lo stile delle righe figlie."""

    def __init__(self, tree_view):
        super().__init__(tree_view)
        self.tree = tree_view

    def paint(self, painter, option, index):
        # Verifica se siamo in una riga figlia (ha un genitore valido)
        if index.parent().isValid():
            col = index.column()
            
            # --- GESTIONE MERGE COL 0 e COL 1 (Testo Breve) ---
            if col == 0 or col == 1:
                # Disegna il testo SOLO quando siamo sulla Col 1 (disegnando verso sinistra)
                # Questo evita che il background della Col 1 copra il testo se disegnato sulla Col 0
                if col == 1:
                    # Recupera dati dalla Col 0 (dove sta il testo vero)
                    sibling0 = index.sibling(index.row(), 0)
                    text = sibling0.data()
                    
                    width_col0 = self.tree.columnWidth(0)
                    width_col1 = self.tree.columnWidth(1)

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
        # Sequence: Data OdA, OdA, Pos, Valore Netto, Stato
        self.master_headers = [
            "Data OdA",
            "OdA",
            "Pos",
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

        refresh_btn = QPushButton("Aggiorna")
        refresh_btn.setIcon(get_colored_icon(get_asset_path(Icons.REFRESH), "#000000"))
        refresh_btn.clicked.connect(self.refresh_data)
        filter_layout.addWidget(refresh_btn)

        import_btn = QPushButton("Importa Excel")
        import_btn.setIcon(get_colored_icon(get_asset_path(Icons.UPLOAD), "#000000"))
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

        # Header Styling
        header = self.tree.header()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

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
                # Parent columns: Data OdA, OdA, Pos, Valore Netto, Stato
                item_data = QStandardItem(format_date_it(str(r[1])))
                item_oda = QStandardItem(str(oda))
                item_pos = QStandardItem(str(pos))
                item_val = QStandardItem(format_currency_smart(str(r[10])))
                item_stato = QStandardItem(str(r[4]))

                # Parent items (initially not bold until expanded)
                for it in [item_data, item_oda, item_pos, item_val, item_stato]:
                    it.setEditable(False)

                # Store full data on the parent too (representative of the position)
                # Store on first column (Data OdA)
                item_data.setData(r, Qt.ItemDataRole.UserRole)

                self.model.appendRow(
                    [item_data, item_oda, item_pos, item_val, item_stato]
                )
                groups[group_key] = item_data

            parent_item = groups[group_key]

            # Create Child Row (The detailed line)
            # Alignment for children (NEW LAYOUT):
            # Col 0 (Data OdA) + Col 1 (OdA) -> {Testo Breve} or {Descrizione} (Merged via Delegate)
            # Col 2 (Pos)          -> {Unità di Mis} {Quantità}
            # Col 3 (Valore Netto) -> {Quantità}
            # Col 4 (Stato)        -> {Prezzo Lordo}

            num_riga = r[27]
            raw_testo = str(r[31]).strip() if r[31] else ""
            raw_desc = str(r[6]).strip() if r[6] else ""
            desc = raw_testo if raw_testo and raw_testo.lower() != "nan" else raw_desc
            
            prezzo = r[30]
            qta = r[28]
            uom = r[29]

            # Create Child Row (The detailed line)
            # Alignment for children (UPDATED LAYOUT 2):
            # Col 0 (Data OdA) + Col 1 (OdA) -> {Testo Breve} (Merged via Delegate on Col 1)
            # Col 2 (Pos)          -> {Unità di Mis} {Quantità}
            # Col 3 (Valore Netto) -> {Prezzo Lordo}
            # Col 4 (Stato)        -> Empty

            num_riga = r[27]
            raw_testo = str(r[31]).strip() if r[31] else ""
            raw_desc = str(r[6]).strip() if r[6] else ""
            desc = raw_testo if raw_testo and raw_testo.lower() != "nan" else raw_desc
            
            prezzo = r[30]
            qta = r[28]
            uom = r[29]

            # Col 0: Descrizione (Disegnata dal Delegate sulla Col 1)
            c_desc_merged = QStandardItem(str(desc))
            
            # Col 1: Empty (Usata dal delegate per disegnare esteso)
            c_empty = QStandardItem("")
            
            # Col 2: UOM + Qta
            c_uom_qta = QStandardItem(f"{uom} {qta}")
            
            # Col 3: Prezzo Lordo (Spostato qui)
            c_prezzo = QStandardItem(format_currency_smart(str(prezzo)))
            
            # Col 4: Empty (Svuotato)
            c_stato_empty = QStandardItem("")

            # Child Read-only e Stile
            for it in [c_desc_merged, c_empty, c_uom_qta, c_prezzo, c_stato_empty]:
                it.setEditable(False)
                it.setForeground(Qt.GlobalColor.darkBlue) 
                it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # La descrizione merged la lasciamo allineata a sinistra
            c_desc_merged.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

            # Store data on child (col 0)
            c_desc_merged.setData(r, Qt.ItemDataRole.UserRole)

            parent_item.appendRow([c_desc_merged, c_empty, c_uom_qta, c_prezzo, c_stato_empty])

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
                QMessageBox.warning(self, "Errore Importazione", f"Impossibile importare:\n{message}")
                
        except Exception as e:
            QMessageBox.critical(self, "Errore Critico", f"Errore durante l'importazione:\n{str(e)}")
