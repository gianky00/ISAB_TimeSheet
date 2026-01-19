"""
SyncroJob - Storico OdA Panel
Pannello per la visualizzazione del Database Storico OdA con architettura Master-Detail e raggruppamento (QTreeView).
"""

from typing import Any, List, Tuple

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QStandardItem, QStandardItemModel, QFont
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
    QTreeView,
    QVBoxLayout,
    QWidget,
    QStyledItemDelegate,
    QStyle
)

from src.core.constants import Icons
from src.core.database import db_manager
from src.gui.formatters import format_currency_smart, format_date_it
from src.utils.helpers import get_asset_path, get_colored_icon


class ChildDescriptionDelegate(QStyledItemDelegate):
    """Delegate per estendere il testo della descrizione (Col 1) sulla colonna successiva per i figli."""

    def __init__(self, tree_view):
        super().__init__(tree_view)
        self.tree = tree_view

    def paint(self, painter, option, index):
        # Verifica se siamo in una riga figlia
        if index.parent().isValid():
            col = index.column()
            # Gestione Colonna 1 (Descrizione) e Colonna 2 (Pos, che è vuota per i figli)
            if col == 1 or col == 2:
                # Recupera i dati dalla colonna 1 (dove c'è il testo)
                # Se siamo alla col 2, dobbiamo prendere i dati dalla col 1 (sibling)
                if col == 1:
                    text = index.data()
                else:
                    # Col 2: Prendi testo dalla col 1
                    sibling = index.sibling(index.row(), 1)
                    text = sibling.data()

                # Calcola larghezze
                width_col1 = self.tree.columnWidth(1)
                width_col2 = self.tree.columnWidth(2)
                
                painter.save()

                # Gestione Selezione (Background)
                # Il background viene disegnato dalla view di solito, ma per sicurezza ridisegniamo
                # se vogliamo stile custom o se l'estensione crea artefatti.
                # Qui ci limitiamo a gestire il testo.
                
                if option.state & QStyle.StateFlag.State_Selected:
                    painter.setPen(option.palette.highlightedText().color())
                else:
                    painter.setPen(option.palette.text().color())

                # Calcolo Rettangolo di Disegno "Totale" (spanning col 1 + 2)
                # L'obiettivo è disegnare il testo in un rettangolo che copre entrambe le colonne,
                # ma traslato correttamente in base alla colonna corrente.
                
                if col == 1:
                    # Siamo in Col 1: Rettangolo è (rect.x, rect.y, w1 + w2, h)
                    draw_rect = option.rect.adjusted(0, 0, width_col2, 0)
                else:
                    # Siamo in Col 2: Rettangolo deve "iniziare" dalla Col 1 visivamente
                    # rect.x è l'inizio della Col 2.
                    # Vogliamo disegnare allo stesso offset assoluto di Col 1.
                    # draw_rect deve essere spostato a sinistra di width_col1 ed esteso a destra
                    draw_rect = option.rect.adjusted(-width_col1, 0, 0, 0)
                    # La larghezza del draw_rect diventa width_col2 + width_col1?
                    # No, rect.adjusted modifica le coordinate.
                    # option.rect (Col2) ha width = w2.
                    # Adjusted(-w1, 0, 0, 0) -> x = x - w1, width = w2 + w1.
                    # Questo è corretto. Il testo verrà disegnato a partire dall'inizio di Col 1.
                
                # Disegno
                # Impostiamo il clipping al rect della cella corrente per evitare sbavature su altre colonne
                # (anche se il drawText clippa, è meglio essere espliciti se usiamo rect più grandi)
                painter.setClipRect(option.rect)
                
                # Align Left per iniziare sempre da sinistra (inizio Col 1)
                painter.drawText(draw_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, text)
                
                painter.restore()
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
        main_layout.addLayout(filter_layout)

        # 2. Contenitore Splitter (Tree | Dettaglio)
        self.splitter = QSplitter(Qt.Orientation.Horizontal)

                # --- TREE VIEW (MASTER) ---
                self.tree = QTreeView()
                self.tree.setModel(self.model)
                self.tree.setAlternatingRowColors(True)
                self.tree.setSortingEnabled(False) # Grouping logic handles sort
                self.tree.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
                self.tree.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
                self.tree.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
                self.tree.setAnimated(True)
                # Disabilita default double click expansion per gestirla manualmente su tutte le colonne
                self.tree.setExpandsOnDoubleClick(False)
                
                # Selection
                self.tree.selectionModel().selectionChanged.connect(self._on_selection_changed)        self.tree.expanded.connect(self._on_item_expanded)
        self.tree.collapsed.connect(self._on_item_collapsed)
        self.tree.doubleClicked.connect(self._on_tree_double_clicked)

        # Header Styling
        header = self.tree.header()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # Custom Delegate per visualizzazione estesa descrizione
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
        if not item:
            return

        # Retrieve full data stored in UserRole
        full_data = item.data(Qt.ItemDataRole.UserRole)

        if full_data:
            for i, h in enumerate(self.full_headers):
                if i < len(full_data):
                    val = str(full_data[i])
                    if val.lower() == "nan" or val == "None":
                        val = ""

                    # Apply specific formatting for detail view
                    if "Data" in h:
                        val = format_date_it(val)
                    elif "Valore" in h or "Prezzo" in h:
                        val = format_currency_smart(val)

                    self.detail_labels[h].setText(val)
        else:
            # If parent item selected (without specific row data, or aggregate), clear details or show summary?
            # Usually parent has the first row data as representative or aggregate.
            # Let's see how populate_tree attaches data.
            pass

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
        
        # Forza toggle espansione su qualsiasi colonna
        # Nota: QTreeView di default espande solo sulla colonna con l'indicatore (spesso 0).
        # Qui lo forziamo ovunque.
        if self.tree.isExpanded(index):
            self.tree.collapse(index)
        else:
            self.tree.expand(index)

    def _set_row_bold(self, parent_index, bold: bool):
        """Helper per cambiare lo stile di tutte le colonne della riga."""
        model = self.tree.model()
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
            query += """ AND (
                CAST(oda AS TEXT) LIKE ? OR
                descrizione LIKE ? OR
                descrizione_fornitore LIKE ? OR
                CAST(contratto AS TEXT) LIKE ? OR
                codice_fornitore LIKE ?
            )"""
            p = f"%{search_text}%"
            params.extend([p, p, p, p, p])

        # Order by ODA, POS, NUM_RIGA so grouping is easy
        query += " ORDER BY oda DESC, pos_oda ASC, CAST(num_riga AS INTEGER) ASC LIMIT 3000"
        return query, params

    def _populate_tree(self, full_rows: List[Tuple]):
        """Popola il modello ad albero raggruppando per ODA + POS."""
        self.model.removeRows(0, self.model.rowCount())

        groups = {} # (oda, pos) -> ParentItem

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

                self.model.appendRow([item_data, item_oda, item_pos, item_val, item_stato])
                groups[group_key] = item_data

            parent_item = groups[group_key]

            # Create Child Row (The detailed line)
            # Child layout mapping to columns:
            # Col 0 (Data) -> "Riga: {num_riga}"
            # Col 1 (OdA) -> {Testo Breve} or {Descrizione}
            # Col 2 (Pos) -> ""
            # Col 3 (Valore) -> {Prezzo Lordo}
            # Col 4 (Stato) -> {Quantita} {UOM}

            num_riga = r[27]
            
            # Robust Text Extraction
            raw_testo = str(r[31]).strip() if r[31] else ""
            raw_desc = str(r[6]).strip() if r[6] else ""
            
            # Use Testo Breve if valid (not "nan", not empty), else Descrizione
            if raw_testo and raw_testo.lower() != "nan":
                desc = raw_testo
            else:
                desc = raw_desc

            prezzo = r[30]
            qta = r[28]
            uom = r[29]

            c_riga = QStandardItem(f"Riga: {num_riga}")
            c_desc = QStandardItem(str(desc))
            c_empty = QStandardItem("")
            c_prezzo = QStandardItem(format_currency_smart(str(prezzo)))
            c_qta = QStandardItem(f"{qta} {uom}" if qta else "")

            # Child Read-only
            for it in [c_riga, c_desc, c_empty, c_prezzo, c_qta]:
                it.setEditable(False)
                # Visual distinction
                it.setForeground(Qt.GlobalColor.darkGray)

            # Store data on child
            c_riga.setData(r, Qt.ItemDataRole.UserRole)

            parent_item.appendRow([c_riga, c_desc, c_empty, c_prezzo, c_qta])
